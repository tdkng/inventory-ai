import pandas as pd
from services.inventory_logic import InventoryDecisionEngine

def build_inventory_risk_gold(
    engine: InventoryDecisionEngine,
    silver_inventory,
    silver_usage,
    silver_purchase_orders,
    silver_parts
) -> pd.DataFrame:
    df = engine.compute_inventory_risk(
        silver_inventory, silver_usage, silver_purchase_orders, silver_parts
    )
    df["as_of"] = pd.Timestamp.utcnow()
    df["risk_explanation"] = ""
    return df

def build_purchasing_recommendations_gold(
    engine: InventoryDecisionEngine,
    silver_inventory,
    silver_usage,
    silver_parts
) -> pd.DataFrame:
    df = engine.generate_purchasing_recommendations(
        silver_inventory, silver_usage, silver_parts
    )
    df["as_of"] = pd.Timestamp.utcnow()
    return df

