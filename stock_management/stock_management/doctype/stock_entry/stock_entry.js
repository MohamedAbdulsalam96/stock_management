// Copyright (c) 2022, Rahib Hassan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry Item", "item_code", function(frm, cdt, cdn)
{
    console.log("Hello")
    var row = locals[cdt][cdn]
    frappe.call
    ({
        "method": "stock_management.stock_management.doctype.stock_entry.calculate_valuation_rate.get_valuation_rate",
        "args": 
        {
            "item_code": row.item_code, 
            "source_warehouse": row.source_warehouse
        },
        callback: function(r){
            console.log(r.message)
            frappe.model.set_value(cdt, cdn, "rate", r.message);
        }
    });
});