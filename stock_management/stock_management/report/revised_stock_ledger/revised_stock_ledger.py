# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from stock_management.stock_management.doctype.stock_entry.calculate_valuation_rate import get_records, get_valuation_rate

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
			'width': 120
		},
		{
			'fieldname': 'actual_qty',
			'label': _('Quantity'),
			'width': 110
		},
		{
			'fieldname': 'updated_qty',
			'label': _('Quantity after transaction'),
			'fieldtype': 'Float',
			'width': 130
		},
		{
			'fieldname': 'incoming_rate',
			'label': _('Rate'),
			'width': 110
		},
		{
			'fieldname': 'valuation_rate',
			'label': _('Valuation Rate'),
			'width': 120
		},
		{
			'fieldname': 'amount',
			'label': _('Stock Value'),
			'fieldtype': 'Currency',
			'width': 110
		},
		{
			'fieldname': 'stock_value_after_transaction',
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
	all_filters = [['docstatus', '=', 1]]
	orm_filters = get_conditions(filters, all_filters)
	
	records = frappe.db.get_list('Stock Ledger Entry', filters=orm_filters, order_by='posting_time asc',
		fields=['item_code', 'warehouse', 'posting_date', 'posting_time', 'actual_qty', 'incoming_rate', 'amount', 'voucher_type', 'voucher_no'])
	
	data = process_data(records)

	return data

def get_conditions(filters, all_filters):
	conditions = ""
	if filters.get("item_code"):
		all_filters.append(['item_code', '=', filters.get('item_code')])
		
	if filters.get("warehouse"):
		all_filters.append(['warehouse', '=', filters.get('warehouse')])
	
	return all_filters

def process_data(records):
	rows = []
	processed_data = {}
	for record in records:
		combination = (record['item_code'], record['warehouse'])
		
		if combination in processed_data:
			comb_values = processed_data[combination]
			
			# sle_entries = get_records(combination[0], combination[1], add_filters = "{'posting_time': comb_values[-1]['posting_time'] < record['posting_time']}")
			sle_entries = frappe.db.get_list('Stock Ledger Entry', filters={'posting_time':['<=', record['posting_time']], 'item_code': combination[0], 'warehouse': combination[1]}, fields=['*'])
			valuation_rate = get_valuation_rate(sle_entries)

			record['valuation_rate'] = round(valuation_rate, 2)
			record['stock_value'] = comb_values[-1]['amount']
			record['stock_value_after_transaction'] = comb_values[-1]['stock_value_after_transaction'] + record['amount']
			record['updated_qty'] = comb_values[-1]['updated_qty'] + record['actual_qty']
				
			processed_data[combination].append(record)
			rows.append(record)
		else:
			processed_data[combination] = [record]
			processed_data[combination][-1].update({'stock_value_after_transaction': record['amount'], 'updated_qty': record['actual_qty'], 'valuation_rate': record['incoming_rate']})
			rows.append(record)

	return rows