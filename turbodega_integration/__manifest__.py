{
    "name": "TURBODEGA - REST API CLIENT -TEST",
    "version": "13.0.1.1.0",
    "author": "Tecnativa",
    "authors": ["Erick Delgado"],
    "category": "Tools",
    "support": "odoo.com",
    "summary": """
    Extends the REST API TURBODEGA
    agregar un botón que obtenga el resourceid

    """,
    "license": "LGPL-3",
    "demo": [],
    "depends": [
        "base",
        "sale_management",
        "contacts",
        "stock",
        "account",
        "product_manufacturer",
        "product_brand",
        "base_address_extended",
        "l10n_latam_base",
        "l10n_latam_invoice_document",
        "l10n_pe",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml",
        "views/res_company_view.xml",
        "views/partner_view.xml",
        "views/data.xml",
        "views/logs_request_view.xml",
    ],
    "installable": True,
}
