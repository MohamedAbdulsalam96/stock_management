import frappe

@frappe.whitelist()
def get_valuation_rate(item_code, source_warehouse):
    records = frappe.db.get_list('Stock Ledger Entry', 
        filters={'item_code': item_code, 'warehouse': source_warehouse},
        fields=['incoming_rate', 'actual_qty', 'warehouse', 'item_code', 'amount'])
    if records:
        return calculate_valuation_rate(records)

def calculate_valuation_rate(records):
    
    total_qty = 0
    total_amount = 0
    for record in records:
        total_qty += record.actual_qty
        total_amount += record.amount

    valuation_rate = total_amount / total_qty
    print(valuation_rate)
    return valuation_rate
