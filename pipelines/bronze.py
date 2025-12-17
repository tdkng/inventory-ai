from services.erp_client import ERPClient

def ingest_inventory(erp_client: ERPClient) -> dict:
    raw_inventory = erp_client.fetch_inventory()
    erp_client._store_bronze(
        payload={"items": [item.dict() for item in raw_inventory]},
        name="inventory"
    )
    return {"items": [item.dict() for item in raw_inventory]}


def ingest_purchase_orders(erp_client: ERPClient) -> dict:
    raw_purchase_orders = erp_client.fetch_purchase_orders()
    erp_client._store_bronze(
        payload={"purchaseOrders": [po.dict() for po in raw_purchase_orders]},
        name="purchase_orders"
    )
    return {"purchaseOrders": [po.dict() for po in raw_purchase_orders]}

