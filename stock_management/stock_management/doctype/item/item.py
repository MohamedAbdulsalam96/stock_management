# Copyright (c) 2022, Rahib Hassan and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import today, now
from frappe import _

class Item(WebsiteGenerator):

	def validate(self):
		if not self.item_name:
			self.item_name = self.item_code

	def create_stock_entry(self):
		stock = frappe.new_doc('Stock Entry')
		stock.title = 'Material Receipt'
		stock.posting_date = today()
		stock.posting_time = now()
		stock.stock_entry_type = 'Material Receipt'
		stock.append('items', {
			'item_code': self.item_code,
			'target_warehouse': self.default_warehouse,
			'quantity': self.opening_stock,
			'rate': self.valuation_rate,
			'amount': self.opening_stock * self.valuation_rate
			})
		stock.insert()
		stock.submit()

	def after_insert(self):
		if self.opening_stock:
			self.create_stock_entry()
