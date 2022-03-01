// Copyright (c) 2022, Rahib Hassan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Balance"] = {
	"filters": [
		{
			'fieldname': 'warehouse',
			'fieldtype': 'Link',
			'label': ('Warehouse'),
			'options': 'Warehouse'
		},
		{
			'fieldname': 'from',
			'fieldtype': 'Date',
			'label': ('From Date'),
			'default': dateutil.year_start()
		},
		{
			'fieldname': 'to',
			'fieldtype': 'Date',
			'label': ('To Date'),
			'default': dateutil.year_end()
		},
		{
			'fieldname': 'item_code',
			'fieldtype': 'Link',
			'label': ('Item'),
			'options': 'Item'
		},
	]
};
