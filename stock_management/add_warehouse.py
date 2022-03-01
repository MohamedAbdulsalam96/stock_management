import frappe

def create_default_warehouse():
    create_warehouse('All Warehouse')
    create_warehouse('Stores')
    create_warehouse('Finished Goods')
    create_warehouse('Work In Progress')

def create_warehouse(warehouse_name):
    warehouse = frappe.get_doc({
        'doctype': 'Warehouse',
        'warehouse_name': warehouse_name,
        'is_group': 1,
    })

    if warehouse_name != 'All Warehouse':
            warehouse.parent_warehouse = 'All Warehouse'
    warehouse.insert()