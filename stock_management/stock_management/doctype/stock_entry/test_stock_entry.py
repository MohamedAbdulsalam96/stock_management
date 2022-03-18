# Copyright (c) 2022, Rahib Hassan and Contributors
# See license.txt

import frappe
import unittest
from stock_management.stock_management.doctype.item.test_item import create_item

def create_stock_entry(item, entry_type, rate, quantity, source_warehouse=None, target_warehouse=None):
	se = frappe.get_doc({
		'doctype': 'Stock Entry',
		'stock_entry_type': entry_type,
		'items': [{
			'target_warehouse': target_warehouse,
			'source_warehouse': source_warehouse,
			'item_code': item,
			'quantity': quantity,
			'rate': rate
		}]
	}).submit()
	return se

class TestStockEntry(unittest.TestCase):
	def tearDown(self):
		frappe.db.rollback()
	
	def test_receipt_posting(self):
		item = frappe.get_last_doc('Item')
		doc = create_stock_entry(item.item_code, 'Material Receipt', 100, 25, target_warehouse='Stores')
		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')

		self.assertTrue(sle)

	def test_issue_posting(self):
		item = frappe.get_last_doc('Item')
		doc = create_stock_entry(item.item_code, 'Material Issue', 200, 12, source_warehouse='Stores')
		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')

		self.assertTrue(sle)

	
	def test_transfer_posting(self):
		item = frappe.get_last_doc('Item')
		doc = create_stock_entry(item.item_code, 'Stock Transfer', 50, 80, source_warehouse='Stores', target_warehouse='Finished Goods')
		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')

		self.assertTrue(sle)
	
	def test_calculate_moving_average(self):
		total_amount = 0
		total_quantity = 0
		item = create_item("CCVVXX", warehouse = 'Stores')
		create_stock_entry(item.item_code, 'Material Receipt', 100, 100, target_warehouse = 'Stores')
		create_stock_entry(item.item_code, 'Material Receipt', 50, 100, target_warehouse = 'Stores')
		entries = frappe.db.get_list('Stock Ledger Entry', filters={'item_code': item.item_code}, fields=['actual_qty', 'amount'])
	
		for entry in entries:
			total_amount += entry.amount
			total_quantity += entry.actual_qty
	
		moving_rate = total_amount / total_quantity

		self.assertEqual(moving_rate, 75)