# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, now

class StockEntry(Document):

	# def __init__(self, *args, **kwargs):
	# 	entry_type = self.stock_entry_type

	def warehouse_validation(self, entry_type, item):
		if entry_type == "Stock Transfer":
			if not item.source_warehouse and not item.target_warehouse:
				frappe.throw(_("Source and Target Warehouse is Mandatory"))
		if entry_type == "Material Issue":
			if not item.source_warehouse:
				frappe.throw(_(f"Source Warehouse mandatory for {entry_type}"))
			item.target_warehouse = None
		elif entry_type == "Material Receipt":
			if not item.target_warehouse:
				frappe.throw(_(f"Target Warehouse mandatory for {entry_type}"))
			item.target_warehouse = None

	def valuation_rate():
		pass

	def calculate_current_quantity(self, item, warehouse):
		last_doc = frappe.get_last_doc('Stock Ledger Entry', filters={'item_code': item.item_code, 'warehouse': warehouse})
		if last_doc:
			quantity = last_doc.qty_after_transaction + item.quantity
			# stock_value = last_doc.stock_value + valuation_rate()

	def create_stock_ledger(self, item, warehouse):
		stock_ledger = frappe.new_doc('Stock Ledger Entry')
		stock_ledger.item_code = item.item_code
		stock_ledger.warehouse = item.target_warehouse
		stock_ledger.posting_date = today()
		stock_ledger.posting_time = now()
		stock_ledger.voucher_type = "Stock Entry"
		stock_ledger.voucher_no = self.name
		stock_ledger.actual_qty = item.quantity
		# stock_ledger.qty_after_transaction = self.calculate_current_quantity(item, warehouse)
		stock_ledger.qty_after_transaction = item.quantity
		stock_ledger.incoming_rate = item.rate
		# stock_ledger.stock_value = calculate_stock_value(item)
		stock_ledger.insert()
		stock_ledger.submit()

	def submit(self):
		for item in self.items:
			self.create_stock_ledger(item, warehouse = item.target_warehouse)
			if item.source_warehouse:
				self.create_stock_ledger(item, warehouse = item.source_warehouse)
	
	def validate(self):
		for item in self.items:
			self.warehouse_validation(self.stock_entry_type, item)
