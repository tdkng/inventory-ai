from services.erp_client import ERPClient

def ingest_inventory(erp_client: ERPClient) -> dict:
    raw_inventory = erp_client.fetch_inventory()
    erp_client._store_bronze(
        payload={"items": [item.dict() for item in raw_inventory]},
        name="inventory"
    )
    return {"items": [item.dict() for item in raw_inventory]}

def ingest_usage(erp_client: ERPClient) -> dict:
    raw_usage = erp_client.fetch_usage()
    erp_client._store_bronze(
        payload={"usageRecords": [usage.dict() for usage in raw_usage]},
        name="usage"
    )
    return {"usageRecords": [usage.dict() for usage in raw_usage]}


def ingest_purchase_orders(erp_client: ERPClient) -> dict:
    raw_purchase_orders = erp_client.fetch_purchase_orders()
    erp_client._store_bronze(
        payload={"purchaseOrders": [po.dict() for po in raw_purchase_orders]},
        name="purchase_orders"
    )
    return {"purchaseOrders": [po.dict() for po in raw_purchase_orders]}


def ingest_parts(erp_client: ERPClient) -> dict:
    raw_parts = erp_client.fetch_parts()
    erp_client._store_bronze(
        payload={"parts": [part.dict() for part in raw_parts]},
        name="parts"
    )
    return {"parts": [part.dict() for part in raw_parts]}

