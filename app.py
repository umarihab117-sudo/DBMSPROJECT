from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from waitress import serve
import os

app = Flask(__name__)

# Allow frontend to access this API
CORS(app)

# ==================================================
# DATABASE SETTINGS
# ==================================================

DB_NAME = os.environ.get("DB_NAME", "GarmentSalesDB")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))

# For local computer = true
# For online database = false
CREATE_DATABASE = os.environ.get("CREATE_DATABASE", "true").lower() == "true"


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

def fast_initialize():

    conn = None
    cursor = None

    try:

        # --------------------------------------------------
        # CREATE DATABASE IF REQUIRED
        # --------------------------------------------------

        if CREATE_DATABASE:

            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                port=MYSQL_PORT
            )

            cursor = conn.cursor()

            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
            )

            cursor.close()
            conn.close()

            conn = None
            cursor = None

        # --------------------------------------------------
        # CONNECT TO DATABASE
        # --------------------------------------------------

        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DB_NAME,
            port=MYSQL_PORT
        )

        cursor = conn.cursor()

        # ==================================================
        # CATEGORY
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                CategoryID INT AUTO_INCREMENT PRIMARY KEY,
                CategoryName VARCHAR(100) NOT NULL UNIQUE,
                IsActive TINYINT(1) NOT NULL DEFAULT 1
            )
        """)

        # ==================================================
        # BRAND
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Brand (
                BrandID INT AUTO_INCREMENT PRIMARY KEY,
                BrandName VARCHAR(100) NOT NULL UNIQUE,
                IsActive TINYINT(1) NOT NULL DEFAULT 1
            )
        """)

        # ==================================================
        # COLOR
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Color (
                ColorID INT AUTO_INCREMENT PRIMARY KEY,
                ColorName VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        # ==================================================
        # SIZE
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Size (
                SizeID INT AUTO_INCREMENT PRIMARY KEY,
                SizeName VARCHAR(20) NOT NULL UNIQUE,
                SizeOrder INT NULL
            )
        """)

        # ==================================================
        # UOM
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UOM (
                UOMID INT AUTO_INCREMENT PRIMARY KEY,
                UOMName VARCHAR(20) NOT NULL UNIQUE
            )
        """)

        # ==================================================
        # TAX MASTER
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TaxMaster (
                TaxID INT AUTO_INCREMENT PRIMARY KEY,
                TaxName VARCHAR(50) NOT NULL,
                CGSTPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                SGSTPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                IGSTPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                IsActive TINYINT(1) NOT NULL DEFAULT 1
            )
        """)

        # ==================================================
        # WAREHOUSE
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Warehouse (
                WarehouseID INT AUTO_INCREMENT PRIMARY KEY,
                WarehouseName VARCHAR(100) NOT NULL,
                Location VARCHAR(200) NULL
            )
        """)

        # ==================================================
        # PRODUCT
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Product (
                ProductID INT AUTO_INCREMENT PRIMARY KEY,
                ProductCode VARCHAR(30) NOT NULL UNIQUE,
                ProductName VARCHAR(200) NOT NULL,
                CategoryID INT NOT NULL,
                BrandID INT NULL,
                HSNCode VARCHAR(15) NULL,
                UOMID INT NOT NULL,
                TaxID INT NOT NULL,
                Fabric VARCHAR(100) NULL,
                Season VARCHAR(30) NULL,
                Gender VARCHAR(15) NULL,
                MRP DECIMAL(12,2) NOT NULL DEFAULT 0,
                IsActive TINYINT(1) NOT NULL DEFAULT 1,
                CreatedOn DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (CategoryID)
                    REFERENCES Category(CategoryID),

                FOREIGN KEY (BrandID)
                    REFERENCES Brand(BrandID),

                FOREIGN KEY (UOMID)
                    REFERENCES UOM(UOMID),

                FOREIGN KEY (TaxID)
                    REFERENCES TaxMaster(TaxID)
            )
        """)

        # ==================================================
        # PRODUCT VARIANT
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProductVariant (
                VariantID INT AUTO_INCREMENT PRIMARY KEY,
                ProductID INT NOT NULL,
                SizeID INT NOT NULL,
                ColorID INT NOT NULL,
                SKUCode VARCHAR(50) NOT NULL UNIQUE,
                Barcode VARCHAR(50) NULL UNIQUE,
                SellingPrice DECIMAL(12,2) NOT NULL,
                IsActive TINYINT(1) NOT NULL DEFAULT 1,

                FOREIGN KEY (ProductID)
                    REFERENCES Product(ProductID),

                FOREIGN KEY (SizeID)
                    REFERENCES Size(SizeID),

                FOREIGN KEY (ColorID)
                    REFERENCES Color(ColorID),

                CONSTRAINT UQ_ProductVariant
                    UNIQUE (ProductID, SizeID, ColorID)
            )
        """)

        # ==================================================
        # STOCK
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Stock (
                StockID INT AUTO_INCREMENT PRIMARY KEY,
                VariantID INT NOT NULL,
                WarehouseID INT NOT NULL,
                QtyAvailable INT NOT NULL DEFAULT 0,
                LastUpdatedOn DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,

                FOREIGN KEY (VariantID)
                    REFERENCES ProductVariant(VariantID),

                FOREIGN KEY (WarehouseID)
                    REFERENCES Warehouse(WarehouseID),

                CONSTRAINT UQ_Stock
                    UNIQUE (VariantID, WarehouseID)
            )
        """)

        # ==================================================
        # CUSTOMER
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Customer (
                CustomerID INT AUTO_INCREMENT PRIMARY KEY,
                CustomerCode VARCHAR(30) NOT NULL UNIQUE,
                CustomerName VARCHAR(150) NOT NULL,
                CustomerType VARCHAR(20) NOT NULL DEFAULT 'Retail',
                Phone VARCHAR(20) NULL,
                Email VARCHAR(100) NULL,
                GSTIN VARCHAR(20) NULL,
                BillingAddress VARCHAR(300) NULL,
                ShippingAddress VARCHAR(300) NULL,
                City VARCHAR(50) NULL,
                State VARCHAR(50) NULL,
                Pincode VARCHAR(10) NULL,
                CreditLimit DECIMAL(12,2) NOT NULL DEFAULT 0,
                IsActive TINYINT(1) NOT NULL DEFAULT 1,
                CreatedOn DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ==================================================
        # SALES ORDER
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SalesOrder (
                SalesOrderID INT AUTO_INCREMENT PRIMARY KEY,
                OrderNo VARCHAR(30) NOT NULL UNIQUE,
                OrderDate DATE NOT NULL,
                CustomerID INT NOT NULL,
                WarehouseID INT NULL,
                OrderStatus VARCHAR(20) NOT NULL DEFAULT 'Pending',
                Remarks VARCHAR(300) NULL,
                CreatedBy VARCHAR(50) NULL,
                CreatedOn DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (CustomerID)
                    REFERENCES Customer(CustomerID),

                FOREIGN KEY (WarehouseID)
                    REFERENCES Warehouse(WarehouseID)
            )
        """)

        # ==================================================
        # SALES ORDER DETAIL
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SalesOrderDetail (
                SalesOrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
                SalesOrderID INT NOT NULL,
                VariantID INT NOT NULL,
                Qty INT NOT NULL,
                Rate DECIMAL(12,2) NOT NULL,
                DiscountPercent DECIMAL(5,2) NOT NULL DEFAULT 0,

                DiscountAmount DECIMAL(12,2)
                    GENERATED ALWAYS AS
                    (ROUND(Qty * Rate * DiscountPercent / 100, 2))
                    STORED,

                TaxableAmount DECIMAL(12,2)
                    GENERATED ALWAYS AS
                    (ROUND(
                        (Qty * Rate) -
                        (Qty * Rate * DiscountPercent / 100),
                        2
                    ))
                    STORED,

                FOREIGN KEY (SalesOrderID)
                    REFERENCES SalesOrder(SalesOrderID),

                FOREIGN KEY (VariantID)
                    REFERENCES ProductVariant(VariantID)
            )
        """)

        # ==================================================
        # INVOICE
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Invoice (
                InvoiceID INT AUTO_INCREMENT PRIMARY KEY,
                InvoiceNo VARCHAR(30) NOT NULL UNIQUE,
                InvoiceDate DATE NOT NULL,
                SalesOrderID INT NULL,
                CustomerID INT NOT NULL,
                WarehouseID INT NULL,
                PlaceOfSupply VARCHAR(50) NULL,
                InvoiceType VARCHAR(10) NOT NULL DEFAULT 'B2C',

                SubTotal DECIMAL(14,2) NOT NULL DEFAULT 0,
                TotalDiscount DECIMAL(14,2) NOT NULL DEFAULT 0,
                TotalCGST DECIMAL(14,2) NOT NULL DEFAULT 0,
                TotalSGST DECIMAL(14,2) NOT NULL DEFAULT 0,
                TotalIGST DECIMAL(14,2) NOT NULL DEFAULT 0,
                RoundOff DECIMAL(6,2) NOT NULL DEFAULT 0,
                GrandTotal DECIMAL(14,2) NOT NULL DEFAULT 0,

                InvoiceStatus VARCHAR(20) NOT NULL DEFAULT 'Unpaid',
                CreatedBy VARCHAR(50) NULL,
                CreatedOn DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (SalesOrderID)
                    REFERENCES SalesOrder(SalesOrderID),

                FOREIGN KEY (CustomerID)
                    REFERENCES Customer(CustomerID),

                FOREIGN KEY (WarehouseID)
                    REFERENCES Warehouse(WarehouseID)
            )
        """)

        # ==================================================
        # INVOICE DETAIL
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS InvoiceDetail (
                InvoiceDetailID INT AUTO_INCREMENT PRIMARY KEY,
                InvoiceID INT NOT NULL,
                VariantID INT NOT NULL,
                HSNCode VARCHAR(15) NULL,
                Qty INT NOT NULL,
                Rate DECIMAL(12,2) NOT NULL,
                DiscountPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                DiscountAmount DECIMAL(12,2) NOT NULL DEFAULT 0,
                TaxableAmount DECIMAL(12,2) NOT NULL DEFAULT 0,

                CGSTPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                CGSTAmount DECIMAL(12,2) NOT NULL DEFAULT 0,

                SGSTPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                SGSTAmount DECIMAL(12,2) NOT NULL DEFAULT 0,

                IGSTPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
                IGSTAmount DECIMAL(12,2) NOT NULL DEFAULT 0,

                LineTotal DECIMAL(12,2) NOT NULL DEFAULT 0,

                FOREIGN KEY (InvoiceID)
                    REFERENCES Invoice(InvoiceID),

                FOREIGN KEY (VariantID)
                    REFERENCES ProductVariant(VariantID)
            )
        """)

        # ==================================================
        # PAYMENT
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payment (
                PaymentID INT AUTO_INCREMENT PRIMARY KEY,
                InvoiceID INT NOT NULL,
                PaymentDate DATE NOT NULL,
                PaymentMode VARCHAR(20) NOT NULL,
                Amount DECIMAL(12,2) NOT NULL,
                ReferenceNo VARCHAR(50) NULL,
                Remarks VARCHAR(200) NULL,
                CreatedOn DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (InvoiceID)
                    REFERENCES Invoice(InvoiceID)
            )
        """)

        # ==================================================
        # DEFAULT DATA
        # ==================================================

        cursor.execute("""
            INSERT IGNORE INTO UOM (UOMID, UOMName)
            VALUES
            (1, 'PCS'),
            (2, 'SET'),
            (3, 'PAIR')
        """)

        cursor.execute("""
            INSERT IGNORE INTO Category (CategoryID, CategoryName)
            VALUES
            (1, 'Shirts'),
            (2, 'T-Shirts'),
            (3, 'Trousers'),
            (4, 'Kidswear'),
            (5, 'Sarees')
        """)

        cursor.execute("""
            INSERT IGNORE INTO Color (ColorID, ColorName)
            VALUES
            (1, 'Red'),
            (2, 'Blue'),
            (3, 'Black'),
            (4, 'White'),
            (5, 'Green')
        """)

        cursor.execute("""
            INSERT IGNORE INTO Size (SizeID, SizeName, SizeOrder)
            VALUES
            (1, 'S', 1),
            (2, 'M', 2),
            (3, 'L', 3),
            (4, 'XL', 4),
            (5, 'XXL', 5)
        """)

        cursor.execute("""
            INSERT IGNORE INTO TaxMaster
            (TaxID, TaxName, CGSTPercent, SGSTPercent, IGSTPercent)
            VALUES
            (1, 'GST 5%', 2.5, 2.5, 5.0),
            (2, 'GST 12%', 6.0, 6.0, 12.0),
            (3, 'GST 18%', 9.0, 9.0, 18.0)
        """)

        conn.commit()

        print("MySQL Database and Tables ready.")

    except mysql.connector.Error as err:

        print("Database error:", err)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_db():

    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME,
        port=MYSQL_PORT
    )


# ==================================================
# INITIALIZE DATABASE
# ==================================================

fast_initialize()


# ==================================================
# HOME / HEALTH CHECK
# ==================================================

@app.route('/')
def home():

    return jsonify({
        "status": "success",
        "message": "Garment Sales Management API is running"
    })


@app.route('/health')
def health():

    return jsonify({
        "status": "ok"
    })


# ==================================================
# CUSTOMER API - ADD
# ==================================================

@app.route('/api/customers', methods=['POST'])
def add_customer():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    if 'CustomerCode' not in data or 'CustomerName' not in data:

        return jsonify({
            "status": "error",
            "message": "Customer Code and Name are required"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO Customer
            (
                CustomerCode,
                CustomerName,
                CustomerType,
                Phone,
                Email,
                GSTIN,
                City
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('CustomerCode'),
            data.get('CustomerName'),
            data.get('CustomerType', 'Retail'),
            data.get('Phone'),
            data.get('Email'),
            data.get('GSTIN'),
            data.get('City')
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Customer saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# CUSTOMER API - GET
# ==================================================

@app.route('/api/customers', methods=['GET'])
def get_customers():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                CustomerID,
                CustomerCode,
                CustomerName,
                CustomerType,
                Phone,
                Email,
                City
            FROM Customer
            ORDER BY CreatedOn DESC
        """)

        customers = cursor.fetchall()

        return jsonify(customers), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# PRODUCT API - ADD
# ==================================================

@app.route('/api/products', methods=['POST'])
def add_product():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    if 'ProductCode' not in data or 'ProductName' not in data:

        return jsonify({
            "status": "error",
            "message": "Product Code and Product Name are required"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO Product
            (
                ProductCode,
                ProductName,
                CategoryID,
                BrandID,
                HSNCode,
                UOMID,
                TaxID,
                Fabric,
                Season,
                Gender,
                MRP
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('ProductCode'),
            data.get('ProductName'),
            data.get('CategoryID'),
            data.get('BrandID'),
            data.get('HSNCode'),
            data.get('UOMID'),
            data.get('TaxID'),
            data.get('Fabric'),
            data.get('Season'),
            data.get('Gender'),
            data.get('MRP', 0)
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Product saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# PRODUCT API - GET
# ==================================================

@app.route('/api/products', methods=['GET'])
def get_products():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                ProductID,
                ProductCode,
                ProductName,
                CategoryID,
                BrandID,
                HSNCode,
                UOMID,
                TaxID,
                Fabric,
                Season,
                Gender,
                MRP
            FROM Product
            ORDER BY CreatedOn DESC
        """)

        products = cursor.fetchall()

        return jsonify(products), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# PRODUCT VARIANT API
# ==================================================

@app.route('/api/product-variants', methods=['POST'])
def add_product_variant():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO ProductVariant
            (
                ProductID,
                SizeID,
                ColorID,
                SKUCode,
                Barcode,
                SellingPrice
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('ProductID'),
            data.get('SizeID'),
            data.get('ColorID'),
            data.get('SKUCode'),
            data.get('Barcode'),
            data.get('SellingPrice')
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Product Variant saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


@app.route('/api/product-variants', methods=['GET'])
def get_product_variants():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                VariantID,
                ProductID,
                SizeID,
                ColorID,
                SKUCode,
                Barcode,
                SellingPrice,
                IsActive
            FROM ProductVariant
            ORDER BY VariantID DESC
        """)

        variants = cursor.fetchall()

        return jsonify(variants), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# STOCK API
# ==================================================

@app.route('/api/stock', methods=['POST'])
def add_stock():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO Stock
            (
                VariantID,
                WarehouseID,
                QtyAvailable
            )
            VALUES (%s, %s, %s)
        """

        values = (
            data.get('VariantID'),
            data.get('WarehouseID'),
            data.get('QtyAvailable')
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Stock saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


@app.route('/api/stock', methods=['GET'])
def get_stock():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                StockID,
                VariantID,
                WarehouseID,
                QtyAvailable,
                LastUpdatedOn
            FROM Stock
            ORDER BY StockID DESC
        """)

        stock = cursor.fetchall()

        return jsonify(stock), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# SALES ORDER API
# ==================================================

@app.route('/api/sales-orders', methods=['POST'])
def add_sales_order():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO SalesOrder
            (
                OrderNo,
                OrderDate,
                CustomerID,
                WarehouseID,
                OrderStatus,
                Remarks,
                CreatedBy
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('OrderNo'),
            data.get('OrderDate'),
            data.get('CustomerID'),
            data.get('WarehouseID'),
            data.get('OrderStatus', 'Pending'),
            data.get('Remarks'),
            data.get('CreatedBy')
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Sales Order saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


@app.route('/api/sales-orders', methods=['GET'])
def get_sales_orders():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                SalesOrderID,
                OrderNo,
                OrderDate,
                CustomerID,
                WarehouseID,
                OrderStatus,
                Remarks,
                CreatedBy
            FROM SalesOrder
            ORDER BY SalesOrderID DESC
        """)

        orders = cursor.fetchall()

        return jsonify(orders), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# SALES ORDER DETAIL API
# ==================================================

@app.route('/api/sales-order-details', methods=['POST'])
def add_sales_order_detail():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO SalesOrderDetail
            (
                SalesOrderID,
                VariantID,
                Qty,
                Rate,
                DiscountPercent
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            data.get('SalesOrderID'),
            data.get('VariantID'),
            data.get('Qty'),
            data.get('Rate'),
            data.get('DiscountPercent', 0)
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Sales Order Detail saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


@app.route('/api/sales-order-details', methods=['GET'])
def get_sales_order_details():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                SalesOrderDetailID,
                SalesOrderID,
                VariantID,
                Qty,
                Rate,
                DiscountPercent,
                DiscountAmount,
                TaxableAmount
            FROM SalesOrderDetail
            ORDER BY SalesOrderDetailID DESC
        """)

        details = cursor.fetchall()

        return jsonify(details), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# INVOICE API
# ==================================================

@app.route('/api/invoices', methods=['POST'])
def add_invoice():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO Invoice
            (
                InvoiceNo,
                InvoiceDate,
                SalesOrderID,
                CustomerID,
                WarehouseID,
                PlaceOfSupply,
                InvoiceType,
                SubTotal,
                TotalDiscount,
                TotalCGST,
                TotalSGST,
                TotalIGST,
                RoundOff,
                GrandTotal,
                InvoiceStatus,
                CreatedBy
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            data.get('InvoiceNo'),
            data.get('InvoiceDate'),
            data.get('SalesOrderID'),
            data.get('CustomerID'),
            data.get('WarehouseID'),
            data.get('PlaceOfSupply'),
            data.get('InvoiceType'),
            data.get('SubTotal'),
            data.get('TotalDiscount', 0),
            data.get('TotalCGST', 0),
            data.get('TotalSGST', 0),
            data.get('TotalIGST', 0),
            data.get('RoundOff', 0),
            data.get('GrandTotal'),
            data.get('InvoiceStatus', 'Pending'),
            data.get('CreatedBy')
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Invoice saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


@app.route('/api/invoices', methods=['GET'])
def get_invoices():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                InvoiceID,
                InvoiceNo,
                InvoiceDate,
                SalesOrderID,
                CustomerID,
                WarehouseID,
                PlaceOfSupply,
                InvoiceType,
                SubTotal,
                TotalDiscount,
                TotalCGST,
                TotalSGST,
                TotalIGST,
                RoundOff,
                GrandTotal,
                InvoiceStatus,
                CreatedBy
            FROM Invoice
            ORDER BY InvoiceID DESC
        """)

        invoices = cursor.fetchall()

        return jsonify(invoices), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# PAYMENT API
# ==================================================

@app.route('/api/payments', methods=['POST'])
def add_payment():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO Payment
            (
                InvoiceID,
                PaymentDate,
                Amount,
                PaymentMode,
                ReferenceNo,
                Remarks
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('InvoiceID'),
            data.get('PaymentDate'),
            data.get('Amount'),
            data.get('PaymentMode'),
            data.get('ReferenceNo'),
            data.get('Remarks')
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Payment saved successfully!"
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


@app.route('/api/payments', methods=['GET'])
def get_payments():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                PaymentID,
                InvoiceID,
                PaymentDate,
                Amount,
                PaymentMode,
                ReferenceNo,
                Remarks
            FROM Payment
            ORDER BY PaymentID DESC
        """)

        payments = cursor.fetchall()

        return jsonify(payments), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# DASHBOARD
# ==================================================

@app.route('/api/dashboard', methods=['GET'])
def dashboard():

    conn = None
    cursor = None

    try:

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM Product")
        products = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM Customer")
        customers = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM SalesOrder")
        orders = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM Invoice")
        invoices = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM Payment")
        payments = cursor.fetchone()["total"]

        return jsonify({
            "products": products,
            "customers": customers,
            "orders": orders,
            "invoices": invoices,
            "payments": payments
        }), 200

    except mysql.connector.Error as err:

        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == '__main__':

    print("Server running on http://127.0.0.1:5000")

    serve(
        app,
        host='127.0.0.1',
        port=5000
    )
