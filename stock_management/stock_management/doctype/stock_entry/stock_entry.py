# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, now

class StockEntry(Document):

	def warehouse_validation(self, entry_type, item):

		if entry_type == "Stock Transfer":
			if not item.source_warehouse or not item.target_warehouse:
				frappe.throw(_("Source and Target Warehouse is Mandatory"))

		if entry_type == "Material Issue":
			if not item.source_warehouse:
				frappe.throw(_(f"Source Warehouse mandatory for {entry_type}"))
			item.target_warehouse = None

		if entry_type == "Material Receipt":
			if not item.target_warehouse:
				frappe.throw(_(f"Target Warehouse mandatory for {entry_type}"))
			item.target_warehouse = None

	def last_doc_values(self, item, warehouse):

		try:
			last_doc = frappe.get_last_doc('Stock Ledger Entry', 
				filters={'item_code': item.item_code, 'warehouse': warehouse})
		except:
			last_quantity = 0
			last_value = 0
		else:
			last_quantity = last_doc.qty_after_transaction
			last_value = last_doc.stock_value
		
		
		return last_quantity + item.quantity
			# stock_value = last_doc.stock_value + valuation_rate()
			# return quantity, stock_value

	def create_stock_ledger(self, item, warehouse, warehouse_type):

		stock_ledger = frappe.new_doc('Stock Ledger Entry')
		stock_ledger.item_code = item.item_code
		stock_ledger.warehouse = warehouse
		stock_ledger.posting_date = today()
		stock_ledger.posting_time = now()
		stock_ledger.voucher_type = "Stock Entry"
		stock_ledger.voucher_no = self.name
		
		if warehouse_type == "Source":
			stock_ledger.incoming_rate = -(item.rate)
		elif warehouse_type == "Target":
			stock_ledger.actual_qty = item.quantity

		stock_ledger.incoming_rate = item.rate
		stock_ledger.amount = stock_ledger.incoming_rate * stock_ledger.actual_qty
		stock_ledger.insert()
		stock_ledger.submit()

		# qty, value = self.last_doc_values(item, warehouse)

	def submit(self):

		for item in self.items:

			if item.source_warehouse and item.target_warehouse:
				self.create_stock_ledger(item, warehouse = item.source_warehouse, warehouse_type = "Source")
				self.create_stock_ledger(item, warehouse = item.target_warehouse, warehouse_type = "Target")

			elif item.source_warehouse:
				self.create_stock_ledger(item, warehouse = item.source_warehouse, warehouse_type = "Source")

			elif item.target_warehouse:
				self.create_stock_ledger(item, warehouse = item.source_warehouse, warehouse_type = "Target")
				
	def validate(self):

		for item in self.items:
			self.warehouse_validation(self.stock_entry_type, item)
