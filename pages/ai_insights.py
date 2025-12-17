from dotenv import load_dotenv
import streamlit as st
import os

from services.ai_client import AIInsightService

st.header("AI Explanation")

gold = st.session_state["gold_inventory"]
part = st.selectbox("Select part", gold["part_number"])

row = gold[gold["part_number"] == part].iloc[0].to_dict()

if st.button("Explain Risk"):
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        ai_service = AIInsightService(api_key=OPENAI_API_KEY)

        explanation = ai_service.explain_inventory_risk(row)

        st.write(explanation)
        st.markdown(f"**Part Number:** {row['part_number']}")
        st.markdown(f"- Available Quantity: {row['available_qty']}")
        st.markdown(f"- Average Daily Usage: {row['avg_daily_usage']}")
        st.markdown(f"- Lead Time (days): {row['lead_time_days']}")
        st.markdown(f"- Days of Supply: {row['days_of_supply']}")
        st.markdown(f"- Risk Level: {row['risk_level']}")
        st.markdown("----")
        
        # save explanation to session state to cache it
        part_idx = gold[gold["part_number"] == part].index[0]
        st.session_state["gold_inventory"].loc[part_idx, "risk_explanation"] = explanation
        st.success("✓ Explanation saved to cache")
    else:
        st.warning("OPENAI_API_KEY not set. Set the environment variable to enable AI insights:")
        st.code("export OPENAI_API_KEY='sk-...'", language="bash")

