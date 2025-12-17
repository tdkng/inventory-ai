import pandas as pd

def parts_to_silver(raw_parts: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_parts["parts"])
    return df

def inventory_to_silver(raw_inventory: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_inventory["items"])
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    return df


def usage_to_silver(raw_usage: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_usage["usageRecords"])
    df["usage_date"] = pd.to_datetime(df["usage_date"])
    return df


def purchase_orders_to_silver(raw_purchase_orders: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_purchase_orders["purchaseOrders"])
    df["expected_receipt_date"] = pd.to_datetime(df["expected_receipt_date"])
    return df

