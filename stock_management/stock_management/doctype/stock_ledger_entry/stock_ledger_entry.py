# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from stock_management.stock_management.doctype.stock_entry.calculate_valuation_rate import get_valuation_rate

class StockLedgerEntry(Document):
	def validate(self):
		if self.entry_type == 'Source':
			records = frappe.db.get_list('Stock Ledger Entry', 
        		filters={'item_code': self.item_code, 'warehouse': self.warehouse},
        		fields=['incoming_rate', 'actual_qty', 'warehouse', 'item_code', 'amount'])
			rate = get_valuation_rate(records)
			rate = -(rate)
			self.incoming_rate = rate
			self.amount = -(self.incoming_rate * self.actual_qty)
			return
		
		self.amount = self.incoming_rate * self.actual_qty
