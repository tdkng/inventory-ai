import streamlit as st

from services.erp_client import ERPClient
from services.inventory_logic import InventoryDecisionEngine
from pipelines.bronze import ingest_inventory, ingest_usage, ingest_purchase_orders, ingest_parts
from pipelines.silver import inventory_to_silver, usage_to_silver, purchase_orders_to_silver, parts_to_silver
from pipelines.gold import build_inventory_risk_gold, build_purchasing_recommendations_gold

@st.cache_data
def run_pipeline():
    erp = ERPClient("http://localhost:8000/", "test-key")
    
    raw_inventory = ingest_inventory(erp)
    raw_usage = ingest_usage(erp)
    raw_purchase_orders = ingest_purchase_orders(erp)
    raw_parts = ingest_parts(erp)

    silver_inventory = inventory_to_silver(raw_inventory)
    silver_usage = usage_to_silver(raw_usage)
    silver_purchase_orders = purchase_orders_to_silver(raw_purchase_orders)
    silver_parts = parts_to_silver(raw_parts)

    gold_inventory = build_inventory_risk_gold(
        InventoryDecisionEngine(),
        silver_inventory,
        silver_usage,
        silver_purchase_orders,
        silver_parts
    )

    gold_purchasing = build_purchasing_recommendations_gold(
        InventoryDecisionEngine(),
        silver_inventory,
        silver_usage,
        silver_parts
    )

    # print(gold_inventory)
    # print(gold_purchasing)

    return {
        "inventory": gold_inventory,
        "purchasing": gold_purchasing,
    }


if __name__ == "__main__":
    st.set_page_config(page_title="Inventory AI", layout="wide")

    st.title("Inventory Decision Support")
    gold = run_pipeline()
    st.success("Data loaded")

    st.session_state["gold_inventory"] = gold["inventory"]
    st.session_state["gold_purchasing"] = gold["purchasing"]

