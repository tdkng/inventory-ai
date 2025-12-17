import streamlit as st

st.header("Purchasing Recommendations")

gold = st.session_state["gold_purchasing"]

st.dataframe(
    gold.sort_values("recommended_order_qty", ascending=False),
    use_container_width=True
)

st.subheader("Recommended Orders")

for _, row in gold.sort_values("recommended_order_qty", ascending=False).iterrows():
    st.markdown(f"**Part Number:** {row['part_number']}")
    st.markdown(f"- Available Quantity: {row['available_qty']}")
    st.markdown(f"- Average Daily Usage: {row['avg_daily_usage']}")
    st.markdown(f"- Lead Time (days): {row['lead_time_days']}")
    st.markdown(f"- Recommended Order Quantity: {row['recommended_order_qty']}")
    st.markdown("----")