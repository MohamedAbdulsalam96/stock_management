# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import today, now
from frappe import _

class Item(WebsiteGenerator):

	def validate(self):
		if self.maintain_stock == 1 and self.opening_stock == 0:
			frappe.throw(_("Opening Stock is required for stock item."))
		if self.maintain_stock == 1 and self.valuation_rate == 0:
			frappe.throw(_("Valuation Rate is required for stock item."))

		if not self.item_name:
			self.item_name = self.item_code

	def create_stock_entry(self):
		stock = frappe.new_doc('Stock Entry')
		stock.title = "Material Receipt"
		stock.posting_date = today()
		stock.posting_time = now()
		stock.stock_entry_type = "Material Receipt"
		stock.append('items', {
			'item_code': self.item_code,
			'target_warehouse': self.default_warehouse,
			'quantity': self.opening_stock,
			'rate': self.valuation_rate,
			'amount': self.opening_stock * self.valuation_rate
			})
		stock.docstatus = 1
		stock.insert()

	def after_insert(self):
		if self.maintain_stock == 1:
			self.create_stock_entry()
