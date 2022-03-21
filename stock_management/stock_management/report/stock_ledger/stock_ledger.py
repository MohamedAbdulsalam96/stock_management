# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	
	rows = get_data(filters)
	columns = get_columns()

	return columns, rows

def get_columns():
	return [
		{
			'fieldname': 'posting_date',
			'label': _('Posting Date')
		},
		{
			'fieldname': 'posting_time',
			'label': _('Posting Time')
		},
		{
			'fieldname': 'item_code',
			'label': _('Item'),
			'fieldtype': 'Link',
			'options': 'Item',
			'width': 110
		},
		{
			'fieldname': 'warehouse',
			'label': _('Warehouse'),
			'fieldtype': 'Link',
			'options': 'Warehouse',
		},
		{
			'fieldname': 'qty',
			'label': _('Quantity'),
			'width': 110
		},
		{
			'fieldname': 'updated_qty',
			'label': _('Quantity after transaction'),
			'fieldtype': 'Float',
			'width': 110
		},
		{
			'fieldname': 'rate',
			'label': _('Rate'),
			'width': 110
		},
		{
			'fieldname': 'valuation_rate',
			'label': _('Valuation Rate'),
			'width': 120
		},
		{
			'fieldname': 'stock_value',
			'label': _('Stock Value'),
			'fieldtype': 'Currency',
			'width': 110
		},
		{
			'fieldname': 'stock_value_difference',
			'label': _('Stock Value Difference'),
			'fieldtype': 'Currency',
			'width': 110
		},
		{
			'fieldname': 'voucher_type',
			'label': _('Voucher Type'),
			'fieldtype': 'Link',
			'options': 'Doctype'
		},
		{
			'fieldname': 'voucher_no',
			'label': _('Voucher No.'),
			'fieldtype': 'Link',
			'options': 'Stock Ledger Entry',
			'width': 160
		},
	]
	
def get_data(filters):
	
	conditions = get_conditions(filters)
	
	results = frappe.db.sql("""
		SELECT
			item_code, warehouse, actual_qty, incoming_rate, amount, voucher_type, voucher_no, posting_date, posting_time
		FROM
			`tabStock Ledger Entry` as sle
		WHERE
			sle.docstatus = 1 %s
		"""%(conditions), filters, as_dict=True)

	rows = ex_execute(results)

	return rows

def get_conditions(filters):
	conditions = ""
	if filters.get("item_code"):
		conditions += "and sle.item_code = %s" % frappe.db.escape(filters.get("item_code"), percent=False)
		
	if filters.get("warehouse"):
		conditions += "and sle.warehouse = %s" % frappe.db.escape(filters.get("warehouse"), percent=False)
	
	return conditions

def ex_execute(results):
	data = []
	print("\n\nResults and data")
	print(results, data)
    # adding the first record unconditionally
	first = results[0]
	append_data(data, first, first['actual_qty'], first['incoming_rate'], first['amount'])
	print("\n\ndata after appending\n")
	print(data)
	for result in results[1:]:
		check_value(result, data)
	return data

def check_value(result, data):
	updated_qty = result['actual_qty']
	valuation_rate = result['incoming_rate']
	stock_value_difference = result['amount']

	for d in reversed(data):
		if result['item_code'] == d['item_code'] and result['warehouse'] == d['warehouse']:
			updated_qty, valuation_rate, stock_value_difference = update_value(result, d, updated_qty, valuation_rate, stock_value_difference)
			break
	append_data(data, result, updated_qty, valuation_rate, stock_value_difference)

def update_value(result, d, updated_qty, valuation_rate, stock_value_difference):
	updated_qty += d['updated_qty']
	valuation_rate = calculate_valuation_rate(result, d)
	stock_value_difference += d['stock_value_difference']

	return updated_qty, valuation_rate, stock_value_difference

def calculate_valuation_rate(result, d):
	total_sum = d['stock_value'] + result['amount']
	total_quantity =  d['qty'] + result['actual_qty']
	print(total_sum, total_quantity)
	rate = total_sum / total_quantity
	rate = round(rate, 2)
	return rate

def append_data(data, result, updated_qty, valuation_rate, stock_value_difference):
	data.append({'item_code': result['item_code'], 'warehouse': result['warehouse'], 
		'qty': result['actual_qty'], 'updated_qty': updated_qty, 'rate': result['incoming_rate'],
		'valuation_rate': valuation_rate, 'stock_value': result['amount'], 
		'stock_value_difference': stock_value_difference, 'posting_date': result['posting_date'],
		'voucher_type': result['voucher_type'], 'voucher_no': result['voucher_no']})
	