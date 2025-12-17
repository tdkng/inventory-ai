import streamlit as st
import math

st.header("Inventory Risk Overview")

gold = st.session_state["gold_inventory"]

st.dataframe(
    gold,
    use_container_width=True
)

high_risk = gold[gold["risk_level"] == "HIGH"]

st.subheader("High Risk Items")
st.dataframe(high_risk)

for idx, (_, row) in enumerate(high_risk.iterrows()):
    st.markdown(f"**Part Number:** {row['part_number']}")
    st.markdown(f"- Available Quantity: {row['available_qty']}")
    st.markdown(f"- Average Daily Usage: {row['avg_daily_usage']}")
    st.markdown(f"- Lead Time (days): {row['lead_time_days']}")
    st.markdown(f"- Days of Supply: {row['days_of_supply']}")
    st.markdown(f"- Risk Level: {row['risk_level']}")
    st.markdown("---")

    # check if explanation is already cached
    explanation = row.get("risk_explanation", "")

    if explanation and not (isinstance(explanation, float) and math.isnan(explanation)):
        # use cached explanation
        st.markdown(f"**AI Explanation:** {explanation}")
    else:
        st.markdown(f"**AI Explanation:** Not yet generated.")
    
    st.markdown("----")