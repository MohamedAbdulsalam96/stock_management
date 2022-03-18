// Copyright (c) 2022, Rahib Hassan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry Item", "item_code", function(frm, cdt, cdn)
{
    // console.log("Hello eMan")
    var row = locals[cdt][cdn]
    if (row.source_warehouse)
    {
        var sle_entries = frappe.db.get_list('Stock Ledger Entry', {
            fields: ['actual_qty', 'amount'],
            filters: {
                item_code: row.item_code,
                warehouse: row.source_warehouse
            }
        }).then(e => {console.log(e)
            frappe.call({
                method: "stock_management.stock_management.doctype.stock_entry.calculate_valuation_rate.get_valuation_rate",
                args: {
                    records: e
                },
                callback: function(r){
                    // console.log(r.message)
                    frappe.model.set_value(cdt, cdn, "rate", r.message);
                }
            })
        });
    }
});