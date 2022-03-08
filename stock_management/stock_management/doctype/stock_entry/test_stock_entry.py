# Copyright (c) 2022, Rahib Hassan and Contributors
# See license.txt

import frappe
import unittest

def create_stock_entry():
	se = frappe.get_doc({
		'doctype': 'Stock Entry',
		'stock_entry_type': 'Material Receipt',
		'items': [{
			'target_warehouse': 'Stores',
			'item_code': 'PROD - 001',
			'quantity': 100
		}]
	}).submit()
	return se

class TestStockEntry(unittest.TestCase):
	def setUp(self):
		print("Setting up stocks entry")

	def tearDown(self):
		frappe.db.rollback()
		frappe.set_user("Administrator")
	
	def test_ledger_posting(self):
		doc = create_stock_entry()
		sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name}, 'name')