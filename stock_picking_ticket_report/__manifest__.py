# Part of Softhealer Technologies.
{
    "name": "Stock Picking Receipt Report - Backend",
    "website": "https://www.odoo.com",
    "category": "Invoice",
    "summary": "This module useful to generate receipt from backend.",
    "author": "Tecnativa",
    "authors": ["cristdrcr", "Erick Delgado"],
    "version": "14.0.0.0.1",
    "depends": ["base", "stock", "product"],
    "application": True,
    "data": [
        "data/report_paperformat.xml",
        "reports/pos_stock_picking_report.xml",
    ],
    "images": [
        "static/description/background.png",
    ],
    "auto_install": False,
    "installable": True,
    "price": 30,
    "currency": "EUR",
    "license": "LGPL-3",
}
