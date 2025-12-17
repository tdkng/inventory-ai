import pandas as pd
from datetime import datetime

def compute_inventory_risk(silver_inventory, silver_usage, silver_purchase_orders, silver_parts) -> pd.DataFrame:
    # merge inventory with parts to get lead_time_days
    df = silver_inventory.merge(
        silver_parts[["part_number", "lead_time_days"]],
        on="part_number",
        how="left"
    )

    # merge inventory with parts to get lead_time_days
    df = silver_inventory.merge(
        silver_parts[["part_number", "lead_time_days"]],
        on="part_number",
        how="left"
    )

    # compute avg daily usage
    usage_rate = (
        silver_usage
        .groupby("part_number")["quantity_used"]
        .mean()
        .reset_index(name="avg_daily_usage")
    )

    # merge inventory + usage
    df = df.merge(
        usage_rate,
        on="part_number",
        how="left"
    )

    # handle parts with no usage history
    df["avg_daily_usage"] = df["avg_daily_usage"].fillna(0)

    # compute incoming supply within lead time
    today = pd.Timestamp(datetime.now())

    open_pos = silver_purchase_orders[
        silver_purchase_orders["status"] == "OPEN"
    ].copy()

    open_pos["expected_receipt_date"] = pd.to_datetime(
        open_pos["expected_receipt_date"]
    )

    incoming = (
        open_pos[open_pos["expected_receipt_date"] <= today + pd.to_timedelta(df["lead_time_days"], unit="D").max()]
        .groupby("part_number")["order_qty"]
        .sum()
        .reset_index(name="incoming_qty")
    )

    df = df.merge(incoming, on="part_number", how="left")
    df["incoming_qty"] = df["incoming_qty"].fillna(0)

    # days of supply
    df["days_of_supply"] = df.apply(
        lambda r: float("inf")
        if r["avg_daily_usage"] == 0
        else r["available_qty"] / r["avg_daily_usage"],
        axis=1
    )

    # risk logic
    df["risk_flag"] = df["days_of_supply"] < df["lead_time_days"]

    df["risk_level"] = pd.cut(
        df["days_of_supply"],
        bins=[-1, 7, 30, float("inf")],
        labels=["HIGH", "MEDIUM", "LOW"]
    )

    return df[
        [
            "part_number",
            "available_qty",
            "avg_daily_usage",
            "incoming_qty",
            "days_of_supply",
            "lead_time_days",
            "risk_level",
            "risk_flag"
        ]
    ]


def generate_purchasing_recommendations(silver_inventory, silver_usage, silver_parts, buffer_days=10):
    # merge inventory with parts to get lead_time_days
    df = silver_inventory.merge(
        silver_parts[["part_number", "lead_time_days"]],
        on="part_number",
        how="left"
    )

    # avg daily usage
    usage_rate = (
        silver_usage
        .groupby("part_number")["quantity_used"]
        .mean()
        .reset_index(name="avg_daily_usage")
    )

    df = df.merge(
        usage_rate,
        on="part_number",
        how="left"
    )

    df["avg_daily_usage"] = df["avg_daily_usage"].fillna(0)

    # target stock level
    df["target_days"] = df["lead_time_days"] + buffer_days
    df["target_qty"] = df["target_days"] * df["avg_daily_usage"]

    # recommended order quantity
    df["recommended_order_qty"] = (
        df["target_qty"] - df["available_qty"]
    ).clip(lower=0)

    # flag items needing reorder
    df["reorder_flag"] = df["recommended_order_qty"] > 0

    return df[df["reorder_flag"]][
        [
            "part_number",
            "available_qty",
            "avg_daily_usage",
            "lead_time_days",
            "recommended_order_qty"
        ]
    ].sort_values("recommended_order_qty", ascending=False)
