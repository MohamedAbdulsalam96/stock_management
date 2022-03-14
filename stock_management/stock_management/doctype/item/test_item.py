# Copyright (c) 2022, Rahib Hassan and Contributors
# See license.txt

import frappe
import unittest

def create_item(item_code, warehouse, opening_stock=None, valuation_rate=None):
	if frappe.db.exists('Item', item_code):
		return frappe.get_doc('Item', item_code)

	item = frappe.get_doc({
		'doctype': 'Item',
		'item_code': item_code,
		'item_name': item_code,
		'maintain_stock': 1,
		'default_warehouse': warehouse,
		'opening_stock': opening_stock,
		'valuation_rate': valuation_rate
	}).insert()

	return item

class TestItem(unittest.TestCase):	
	def tearDown(self):
		frappe.db.rollback()

	def test_stock_entry_creation(self):
		item = create_item("Iron", warehouse='Stores', opening_stock=100, valuation_rate=200)
		stock_entry = frappe.get_last_doc('Stock Entry Item', filters={'item_code': item.item_code})
		
		self.assertEqual(stock_entry.item_code, item.item_code)