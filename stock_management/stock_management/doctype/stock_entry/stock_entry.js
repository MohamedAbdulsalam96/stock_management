// Copyright (c) 2022, Rahib Hassan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry Item", "rate", function(frm, cdt, cdn)
{
    var row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "amount", row.quantity * row.rate);
});

frappe.ui.form.on("Stock Entry Item", "quantity", function(frm, cdt, cdn)
{
    var row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "amount", row.quantity * row.rate);
});

frappe.ui.form.on("Stock Entry Item", "item_code", function(frm, cdt, cdn)
{
    var row = locals[cdt][cdn];
    function calculate_valuation_rate()
    {
        frappe.db.get_list('Stock Ledger Entry', 
        {
            fields:['incoming_rate', 'actual_qty'], filters:{item_code: row.item_code}
        }).then(
            records => {
            let rate = 0;
            let qty = 0;
            let total_qty = 0;
            let total_amount = 0;
            function calculate_sum(){
                for(var i = 0; i < records.length; i++){
                    rate = records[i]['incoming_rate'];
                    qty = records[i]['actual_qty']
                    total_qty += qty
                    total_amount += rate * qty; 
                }
                let valuation_rate = total_amount / total_qty
                console.log(valuation_rate)
                frappe.model.set_value(cdt, cdn, "rate", valuation_rate);
            };
            calculate_sum()
        })
    }
    calculate_valuation_rate();
});
