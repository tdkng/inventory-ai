from services.erp_client import ERPClient
from pipelines.bronze import ingest_inventory, ingest_purchase_orders
from pipelines.silver import inventory_to_silver, usage_to_silver
from pipelines.gold import compute_inventory_risk

def run_pipeline():
    erp = ERPClient("http://localhost:8000/", "test-key")
    
    raw_inventory = ingest_inventory(erp)
    raw_purchase_orders = ingest_purchase_orders(erp)

    silver_inventory = inventory_to_silver(raw_inventory)
    silver_usage = usage_to_silver(raw_purchase_orders)

    gold_inventory = compute_inventory_risk(
        silver_inventory, silver_usage
    )

    return gold_inventory

if __name__ == "__main__":
    gold = run_pipeline()
    print(gold)

