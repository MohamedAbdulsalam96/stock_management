# Copyright (c) 2022, Rahib Hassan and Contributors
# See license.txt

import frappe
import unittest

def create_item(item_code):
	if frappe.db.exists('Item', item_code):
		return frappe.get_doc('Item', item_code)

	item = frappe.get_doc({
		'doctype': 'Item',
		'item_code': item_code,
		'item_name': item_code,
		'maintain_stock': 1,
		'default_warehouse': 'All Warehouse',
		'opening_stock': 100,
		'valuation_rate': 200
	}).insert()

	return item

class TestItem(unittest.TestCase):
	def setUp(self):
		pass
	
	def tearDown(self):
		frappe.db.rollback()

	def test_stock_entry_creation(self):
		item = create_item("Iron")
		stock_entries = frappe.db.get_list('Stock Entry', {'stock_entry_type': 'Material Receipt'})
		
		for d in stock_entries:
			child_entry = frappe.db.get_list('Stock Entry Item', {'parent': d.name}, ['item_code'])
			if child_entry[0].item_code == 'Iron':
				return

		frappe.throw("Stock Entry not created")