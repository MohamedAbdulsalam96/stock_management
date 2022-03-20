import frappe
import json

@frappe.whitelist()
def get_valuation_rate(records):
    if isinstance(records, str):
        records = json.loads(records)
    if records:
        total_qty = 0
        total_amount = 0

        for record in records:
            total_qty += record['actual_qty']
            total_amount += record['amount']
        
        valuation_rate = total_amount / total_qty
        return valuation_rate

def get_records(item, warehouse):
    records = frappe.db.get_list('Stock Ledger Entry', filters={'item_code': item, 'warehouse': warehouse}, fields=['*'])
    return records