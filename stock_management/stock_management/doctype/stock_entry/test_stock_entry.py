# Copyright (c) 2022, Rahib Hassan and Contributors
# See license.txt

import frappe
import unittest
from stock_management.stock_management.doctype.item.test_item import create_item
from stock_management.stock_management.report.stock_balance.stock_balance import get_stock_balance

def get_stock_difference(item, entry_type, stock, warehouse):
	initial_stock_balance = get_stock_balance(item.item_code, warehouse)

	if entry_type == 'Material Receipt':
		doc = create_stock_entry(item.item_code, 'Material Receipt', 100, stock, target_warehouse = warehouse)
	elif entry_type == 'Material Issue':
		doc = create_stock_entry(item.item_code, 'Material Issue', 200, stock, source_warehouse = warehouse)
	
	stock_after_entry = get_stock_balance(item.item_code, warehouse)
	stock_difference = stock_after_entry - initial_stock_balance

	return stock_difference, doc


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
		warehouse = 'Stores'
		stock = 25
		difference, doc = get_stock_difference(item, 'Material Receipt', stock, warehouse)
		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')

		self.assertEqual(stock, difference)
		self.assertTrue(sle)

	def test_issue_posting(self):
		item = frappe.get_last_doc('Item')
		warehouse = 'Finished Goods'
		stock = 12
		difference, doc = get_stock_difference(item, 'Material Issue', stock, warehouse)
		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')

		self.assertEqual(stock, -(difference))
		self.assertTrue(sle)
	
	def test_transfer_posting(self):
		item = frappe.get_last_doc('Item')
		source_warehouse = 'Finished Goods'
		target_warehouse = 'Stores'
		stock = 5
		initial_stock_balance_source = get_stock_balance(item.item_code, source_warehouse)
		initial_stock_balance_target = get_stock_balance(item.item_code, target_warehouse)

		doc = create_stock_entry(item.item_code, 'Stock Transfer', 50, stock, source_warehouse = source_warehouse, target_warehouse = target_warehouse)

		stock_after_entry_source = get_stock_balance(item.item_code, source_warehouse)
		stock_after_entry_target = get_stock_balance(item.item_code, target_warehouse)

		source_difference = initial_stock_balance_source - stock_after_entry_source
		target_difference = stock_after_entry_target - initial_stock_balance_target

		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')

		self.assertEqual(stock, source_difference)
		self.assertEqual(stock, target_difference)

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