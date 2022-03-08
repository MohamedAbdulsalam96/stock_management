results = [{'item_code': 'Steel', 'warehouse': 'All Warehouse', 'actual_qty': 15.0, 'incoming_rate': 50.0, 'amount': 750.0},
	{'item_code': 'Steel', 'warehouse': 'All Warehouse', 'actual_qty': 20.0, 'incoming_rate': 60.0, 'amount': 1200.0},
	{'item_code': 'Steel', 'warehouse': 'All Warehouse', 'actual_qty': 10.0, 'incoming_rate': 50.0, 'amount': 500.0},
	{'item_code': 'Steel', 'warehouse': 'Finished Goods', 'actual_qty': 10.0, 'incoming_rate': 12.0, 'amount': 120.0}, 
	{'item_code': 'Steel', 'warehouse': 'Finished Goods', 'actual_qty': 5.0, 'incoming_rate': 15.0, 'amount': 75.0},
	{'item_code': 'Steel', 'warehouse': 'Finished Goods', 'actual_qty': -12.0, 'incoming_rate': -13.0, 'amount': -156.0}, 
	{'item_code': 'Steel', 'warehouse': 'Finished Goods', 'actual_qty': -5.0, 'incoming_rate': -13.0, 'amount': -65.0},
	{'item_code': 'Iron', 'warehouse': 'All Warehouse', 'actual_qty': 200.0, 'incoming_rate': 50.0, 'amount': 10000.0}, 
	{'item_code': 'Iron', 'warehouse': 'All Warehouse', 'actual_qty': 100.0, 'incoming_rate': 75.0, 'amount': 7500.0}, 
	{'item_code': 'Iron', 'warehouse': 'Finished Goods', 'actual_qty': 40.0, 'incoming_rate': 90.0, 'amount': 3600.0}, 
	{'item_code': 'Iron', 'warehouse': 'Finished Goods', 'actual_qty': -5.0, 'incoming_rate': -90.0, 'amount': -450.0}
    ]

data = []

def execute():
    # adding the first record unconditionally
    first = results[0]
    append_data(first, first['actual_qty'], first['incoming_rate'], first['amount'])
    
    for result in results[1:]:
        check_value(result, data)
    print(data)

def check_value(result, data):
    updated_qty = result['actual_qty']
    valuation_rate = result['incoming_rate']
    stock_value_difference = result['amount']

    for d in data:
        if result['item_code'] == d['item_code'] and result['warehouse'] == d['warehouse']:
            updated_qty, valuation_rate, stock_value_difference = update_value(result, d, updated_qty, valuation_rate, stock_value_difference)
    
    append_data(result, updated_qty, valuation_rate, stock_value_difference)

def update_value(result, d, updated_qty, valuation_rate, stock_value_difference):
    updated_qty += d['updated_qty']
    valuation_rate = calculate_valuation_rate(result, d)
    stock_value_difference += d['stock_value_difference']

    return updated_qty, valuation_rate, stock_value_difference

def calculate_valuation_rate(result, d):
    rate = (d['stock_value'] + result['amount']) / d['qty'] + result['actual_qty']
    return rate

def append_data(result, updated_qty, valuation_rate, stock_value_difference):
    data.append({'item_code': result['item_code'], 'warehouse': result['warehouse'], 
		'qty': result['actual_qty'], 'updated_qty': updated_qty, 'rate': result['incoming_rate'],
		'valuation_rate': valuation_rate, 'stock_value': result['amount'], 
		'stock_value_difference': stock_value_difference})
