const API = "http://127.0.0.1:5000";


// =========================
// PRODUCT VARIANT
// =========================

function saveVariant() {

    let variant = {
        ProductID: Number(document.getElementById("productID").value),
        SizeID: Number(document.getElementById("sizeID").value),
        ColorID: Number(document.getElementById("colorID").value),
        SKUCode: document.getElementById("skuCode").value,
        Barcode: document.getElementById("barcode").value,
        SellingPrice: Number(document.getElementById("sellingPrice").value)
    };

    fetch(API + "/api/product-variants", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(variant)
    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.status === "success") {
            loadVariants();
        }

    })

    .catch(error => {
        console.log(error);
        alert("Cannot connect to backend");
    });
}


function loadVariants() {

    fetch(API + "/api/product-variants")

    .then(response => response.json())

    .then(variants => {

        let table = document.getElementById("variantTable");

        table.innerHTML = "";

        variants.forEach(variant => {

            table.innerHTML += `
                <tr>
                    <td>${variant.VariantID}</td>
                    <td>${variant.ProductID}</td>
                    <td>${variant.SizeID}</td>
                    <td>${variant.ColorID}</td>
                    <td>${variant.SKUCode}</td>
                    <td>${variant.Barcode || ""}</td>
                    <td>${variant.SellingPrice}</td>
                </tr>
            `;

        });

    })

    .catch(error => {
        console.log(error);
        alert("Cannot load variants");
    });
}



// =========================
// STOCK
// =========================

function saveStock() {

    let stock = {

        VariantID: Number(
            document.getElementById("variantID").value
        ),

        WarehouseID: Number(
            document.getElementById("warehouseID").value
        ),

        QtyAvailable: Number(
            document.getElementById("qtyAvailable").value
        )

    };


    fetch(API + "/api/stock", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(stock)

    })

    .then(response => response.json())

    .then(data => {

        console.log(data);

        alert(data.message);

        if (data.status === "success") {
            loadStock();
        }

    })

    .catch(error => {

        console.log(error);

        alert("Cannot connect to backend");

    });
}



function loadStock() {

    fetch(API + "/api/stock")

    .then(response => response.json())

    .then(stockList => {

        let table = document.getElementById("stockTable");

        table.innerHTML = "";

        stockList.forEach(stock => {

            table.innerHTML += `
                <tr>
                    <td>${stock.StockID}</td>
                    <td>${stock.VariantID}</td>
                    <td>${stock.WarehouseID}</td>
                    <td>${stock.QtyAvailable}</td>
                    <td>${stock.LastUpdatedOn}</td>
                </tr>
            `;

        });

    })

    .catch(error => {

        console.log(error);

        alert("Cannot load stock");

    });
}
// SALES ORDER

function saveSalesOrder() {

    let order = {
        OrderNo: document.getElementById("orderNo").value,
        OrderDate: document.getElementById("orderDate").value,
        CustomerID: Number(document.getElementById("orderCustomerID").value),
        WarehouseID: Number(document.getElementById("orderWarehouseID").value),
        OrderStatus: document.getElementById("orderStatus").value,
        Remarks: document.getElementById("orderRemarks").value,
        CreatedBy: document.getElementById("createdBy").value
    };

    fetch(API + "/api/sales-orders", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(order)
    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.status === "success") {
            loadSalesOrders();
        }

    })

    .catch(error => {
        console.log(error);
        alert("Cannot connect to backend");
    });
}


function loadSalesOrders() {

    fetch(API + "/api/sales-orders")

    .then(response => response.json())

    .then(orders => {

        let table = document.getElementById("salesOrderTable");

        table.innerHTML = "";

        orders.forEach(order => {

            table.innerHTML += `
                <tr>
                    <td>${order.SalesOrderID}</td>
                    <td>${order.OrderNo}</td>
                    <td>${order.OrderDate}</td>
                    <td>${order.CustomerID}</td>
                    <td>${order.WarehouseID}</td>
                    <td>${order.OrderStatus}</td>
                    <td>${order.Remarks || ""}</td>
                </tr>
            `;

        });

    })

    .catch(error => {
        console.log(error);
        alert("Cannot load sales orders");
    });
}
// INVOICE

function saveInvoice() {

    let invoice = {
        InvoiceNo: document.getElementById("invoiceNo").value,
        InvoiceDate: document.getElementById("invoiceDate").value,
        SalesOrderID: Number(document.getElementById("invoiceSalesOrderID").value),
        CustomerID: Number(document.getElementById("invoiceCustomerID").value),
        WarehouseID: Number(document.getElementById("invoiceWarehouseID").value),
        PlaceOfSupply: document.getElementById("placeOfSupply").value,
        InvoiceType: document.getElementById("invoiceType").value,
        SubTotal: Number(document.getElementById("subTotal").value),
        TotalDiscount: Number(document.getElementById("totalDiscount").value),
        TotalCGST: Number(document.getElementById("totalCGST").value),
        TotalSGST: Number(document.getElementById("totalSGST").value),
        TotalIGST: Number(document.getElementById("totalIGST").value),
        RoundOff: Number(document.getElementById("roundOff").value),
        GrandTotal: Number(document.getElementById("grandTotal").value),
        InvoiceStatus: "Pending",
        CreatedBy: "Admin"
    };

    fetch(API + "/api/invoices", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(invoice)
    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.status === "success") {
            loadInvoices();
        }

    })

    .catch(error => {
        console.log(error);
        alert("Cannot connect to backend");
    });
}


function loadInvoices() {

    fetch(API + "/api/invoices")

    .then(response => response.json())

    .then(invoices => {

        let table = document.getElementById("invoiceTable");

        table.innerHTML = "";

        invoices.forEach(invoice => {

            table.innerHTML += `
                <tr>
                    <td>${invoice.InvoiceID}</td>
                    <td>${invoice.InvoiceNo}</td>
                    <td>${invoice.InvoiceDate}</td>
                    <td>${invoice.SalesOrderID}</td>
                    <td>${invoice.CustomerID}</td>
                    <td>${invoice.SubTotal}</td>
                    <td>${invoice.GrandTotal}</td>
                    <td>${invoice.InvoiceStatus}</td>
                </tr>
            `;

        });

    })

    .catch(error => {
        console.log(error);
        alert("Cannot load invoices");
    });
}
// PAYMENT

function savePayment() {

    let payment = {
        InvoiceID: Number(document.getElementById("paymentInvoiceID").value),
        PaymentDate: document.getElementById("paymentDate").value,
        Amount: Number(document.getElementById("paymentAmount").value),
        PaymentMode: document.getElementById("paymentMode").value,
        ReferenceNo: document.getElementById("referenceNo").value,
        Remarks: document.getElementById("paymentRemarks").value
    };

    fetch(API + "/api/payments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payment)
    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.status === "success") {
            loadPayments();
        }

    })

    .catch(error => {
        console.log(error);
        alert("Cannot connect to backend");
    });
}


function loadPayments() {

    fetch(API + "/api/payments")

    .then(response => response.json())

    .then(payments => {

        let table = document.getElementById("paymentTable");

        table.innerHTML = "";

        payments.forEach(payment => {

            table.innerHTML += `
                <tr>
                    <td>${payment.PaymentID}</td>
                    <td>${payment.InvoiceID}</td>
                    <td>${payment.PaymentDate}</td>
                    <td>${payment.Amount}</td>
                    <td>${payment.PaymentMode}</td>
                    <td>${payment.ReferenceNo || ""}</td>
                    <td>${payment.Remarks || ""}</td>
                </tr>
            `;

        });

    })

    .catch(error => {
        console.log(error);
        alert("Cannot load payments");
    });
}
// DASHBOARD

function loadDashboard() {

    fetch(API + "/api/dashboard")

    .then(response => response.json())

    .then(data => {

        document.getElementById("dashboardProducts").innerText = data.products;
        document.getElementById("dashboardCustomers").innerText = data.customers;
        document.getElementById("dashboardOrders").innerText = data.orders;
        document.getElementById("dashboardInvoices").innerText = data.invoices;
        document.getElementById("dashboardPayments").innerText = data.payments;

    })

    .catch(error => {
        console.log(error);
        alert("Cannot load dashboard");
    });
}
// =============================
// NAVIGATION
// =============================

function showSection(section, button) {

    // Remove active from all tabs
    document.querySelectorAll(".tab").forEach(tab => {
        tab.classList.remove("active");
    });

    // Add active to clicked tab
    button.classList.add("active");

    // Scroll to selected section
    const sectionMap = {
        dashboard: "dashboard",
        customer: "customer",
        product: "product",
        variant: "variant",
        stock: "stock",
        order: "order",
        invoice: "invoice",
        payment: "payment"
    };

    const target = document.getElementById(sectionMap[section]);

    if (target) {
        target.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}
// ================= CUSTOMER =================

function saveCustomer() {

    let customer = {
        CustomerCode: document.getElementById("customerCode").value,
        CustomerName: document.getElementById("customerName").value,
        CustomerType: document.getElementById("customerType").value,
        Phone: document.getElementById("customerPhone").value,
        Email: document.getElementById("customerEmail").value,
        GSTIN: document.getElementById("customerGSTIN").value,
        City: document.getElementById("customerCity").value
    };

    fetch(API + "/api/customers", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(customer)
    })
    .then(response => response.json())
    .then(data => {

        alert(data.message);

        if (data.status === "success") {
            loadCustomers();
        }

    })
    .catch(error => {

        console.log(error);
        alert("Cannot connect to backend");

    });
}


function loadCustomers() {

    fetch(API + "/api/customers")

    .then(response => response.json())

    .then(customers => {

        let table = document.getElementById("customerTable");

        table.innerHTML = "";

        customers.forEach(customer => {

            table.innerHTML += `
                <tr>

                    <td>${customer.CustomerID}</td>

                    <td>${customer.CustomerCode}</td>

                    <td>${customer.CustomerName}</td>

                    <td>${customer.CustomerType}</td>

                    <td>${customer.Phone || ""}</td>

                    <td>${customer.Email || ""}</td>

                    <td>${customer.City || ""}</td>

                </tr>
            `;

        });

    })

    .catch(error => {

        console.log(error);
        alert("Cannot load customers");

    });
}



// ================= PRODUCT =================

function saveProduct() {

    let product = {

        ProductCode: document.getElementById("productCode").value,

        ProductName: document.getElementById("productName").value,

        CategoryID: Number(
            document.getElementById("categoryID").value
        ),

        BrandID: Number(
            document.getElementById("brandID").value
        ),

        HSNCode: document.getElementById("hsnCode").value,

        UOMID: Number(
            document.getElementById("uomID").value
        ),

        TaxID: Number(
            document.getElementById("taxID").value
        ),

        Fabric: document.getElementById("fabric").value,

        Season: document.getElementById("season").value,

        Gender: document.getElementById("gender").value,

        MRP: Number(
            document.getElementById("mrp").value
        )

    };


    fetch(API + "/api/products", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(product)

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.status === "success") {
            loadProducts();
        }

    })

    .catch(error => {

        console.log(error);
        alert("Cannot connect to backend");

    });
}



function loadProducts() {

    fetch(API + "/api/products")

    .then(response => response.json())

    .then(products => {

        let table = document.getElementById("productTable");

        table.innerHTML = "";


        products.forEach(product => {

            table.innerHTML += `

                <tr>

                    <td>${product.ProductID}</td>

                    <td>${product.ProductCode}</td>

                    <td>${product.ProductName}</td>

                    <td>${product.CategoryID}</td>

                    <td>${product.BrandID}</td>

                    <td>${product.HSNCode || ""}</td>

                    <td>${product.UOMID}</td>

                    <td>${product.TaxID}</td>

                    <td>${product.Fabric || ""}</td>

                    <td>${product.Season || ""}</td>

                    <td>${product.Gender || ""}</td>

                    <td>${product.MRP}</td>

                </tr>

            `;

        });

    })

    .catch(error => {

        console.log(error);
        alert("Cannot load products");

    });
}



// ================= DASHBOARD =================

function loadDashboard() {

    Promise.all([

        fetch(API + "/api/products")
            .then(response => response.json()),

        fetch(API + "/api/customers")
            .then(response => response.json()),

        fetch(API + "/api/sales-orders")
            .then(response => response.json()),

        fetch(API + "/api/invoices")
            .then(response => response.json()),

        fetch(API + "/api/payments")
            .then(response => response.json())

    ])

    .then(data => {

        document.getElementById("dashboardProducts").textContent =
            data[0].length;

        document.getElementById("dashboardCustomers").textContent =
            data[1].length;

        document.getElementById("dashboardOrders").textContent =
            data[2].length;

        document.getElementById("dashboardInvoices").textContent =
            data[3].length;

        document.getElementById("dashboardPayments").textContent =
            data[4].length;

    })

    .catch(error => {

        console.log(error);

        alert("Cannot load dashboard");

    });
}



// ================= NAVIGATION =================

function showSection(section, button) {

    document.querySelectorAll(".tab").forEach(tab => {

        tab.classList.remove("active");

    });


    button.classList.add("active");


    const sectionMap = {

        dashboard: "dashboard",

        customer: "customer",

        product: "product",

        variant: "variant",

        stock: "stock",

        order: "order",

        invoice: "invoice",

        payment: "payment"

    };


    const target =
        document.getElementById(sectionMap[section]);


    if (target) {

        target.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }


    // Automatically load data

    if (section === "dashboard") {
        loadDashboard();
    }

    if (section === "customer") {
        loadCustomers();
    }

    if (section === "product") {
        loadProducts();
    }

    if (section === "variant") {
        loadVariants();
    }

    if (section === "stock") {
        loadStock();
    }

    if (section === "order") {
        loadSalesOrders();
    }

    if (section === "invoice") {
        loadInvoices();
    }

    if (section === "payment") {
        loadPayments();
    }

}