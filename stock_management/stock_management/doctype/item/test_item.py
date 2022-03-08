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
			stock_entry = frappe.get_doc('Stock Entry', d)
			stock_entry_items = stock_entry.items
			for m in stock_entry_items:
				if m.item_code == item.item_code:
					return
				
				frappe.throw("Stock entry not created")