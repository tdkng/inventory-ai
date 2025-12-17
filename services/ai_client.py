from openai import OpenAI

class AIInsightService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def explain_inventory_risk(self, row: dict) -> str:
        context = {
            "part_number": row["part_number"],
            "available_qty": row["available_qty"],
            "avg_daily_usage": row["avg_daily_usage"],
            "lead_time_days": row["lead_time_days"],
            "days_of_supply": row["days_of_supply"],
            "risk_level": row["risk_level"]
        }

        SYSTEM_PROMPT = """
        You are an operations assistant.
        Explain inventory risk clearly and concisely.
        Do not invent numbers.
        Base reasoning only on provided data.
        """

        USER_PROMPT = f"""
        Explain why this part is classified as {context['risk_level']} risk.

        Data:
        {context}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT}
                ]
            )
            explanation = response.choices[0].message.content
            return explanation
        except Exception as e:
            print(f"Error type and message: {type(e).__name__} – {e}")
            return "AI explanation unavailable. Please refer to inventory metrics."

