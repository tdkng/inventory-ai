import pandas as pd

def parts_to_silver(raw_parts: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_parts["parts"])
    # convert camelCase column names to snake_case
    df = df.rename(columns={
        "partNumber": "part_number",
        "unitPrice": "unit_price",
        "unitOfMeasure": "unit_of_measure",
        "leadTimeDays": "lead_time_days"
    }, errors='ignore')
    
    # ensure lead_time_days exists; if not, add with default value
    if "lead_time_days" not in df.columns:
        df["lead_time_days"] = 14
    
    return df

def inventory_to_silver(raw_inventory: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_inventory["items"])
    # convert camelCase column names to snake_case
    df = df.rename(columns={
        "partNumber": "part_number",
        "onHandQty": "on_hand_qty",
        "allocatedQty": "allocated_qty",
        "availableQty": "available_qty",
        "lastUpdated": "last_updated"
    }, errors='ignore')
    
    # ensure required columns exist
    if "last_updated" not in df.columns and "lastUpdated" in df.columns:
        df["last_updated"] = df["lastUpdated"]
    
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    return df


def usage_to_silver(raw_usage: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_usage["usageRecords"])
    # convert camelCase column names to snake_case
    df = df.rename(columns={
        "partNumber": "part_number",
        "quantityUsed": "quantity_used",
        "usageDate": "usage_date"
    }, errors='ignore')
    
    # ensure required columns exist
    if "usage_date" not in df.columns and "usageDate" in df.columns:
        df["usage_date"] = df["usageDate"]
    
    df["usage_date"] = pd.to_datetime(df["usage_date"])
    return df


def purchase_orders_to_silver(raw_purchase_orders: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw_purchase_orders["purchaseOrders"])
    # convert camelCase column names to snake_case
    df = df.rename(columns={
        "poNumber": "po_number",
        "partNumber": "part_number",
        "orderQty": "order_qty",
        "expectedReceiptDate": "expected_receipt_date"
    }, errors='ignore')
    
    # ensure required columns exist
    if "expected_receipt_date" not in df.columns and "expectedReceiptDate" in df.columns:
        df["expected_receipt_date"] = df["expectedReceiptDate"]
    
    df["expected_receipt_date"] = pd.to_datetime(df["expected_receipt_date"])
    return df

