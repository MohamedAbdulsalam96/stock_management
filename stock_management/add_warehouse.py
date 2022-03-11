import frappe

def create_default_warehouse():
    create_warehouse('All Warehouse', is_group=1)
    create_warehouse('Stores', parent_warehouse='All Warehouse')
    create_warehouse('Finished Goods', parent_warehouse='All Warehouse')
    create_warehouse('Work In Progress', parent_warehouse='All Warehouse')

def create_warehouse(warehouse_name, is_group=0, parent_warehouse=None):
    warehouse = frappe.get_doc({
        'doctype': 'Warehouse',
        'warehouse_name': warehouse_name,
        'is_group': is_group,
        'parent_warehouse': parent_warehouse
    })
    warehouse.insert()