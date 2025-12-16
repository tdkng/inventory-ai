# inventory-ai
ai-assisted inventory risk &amp; reorder decision dashboard

goals:
- consistent inventory snapshots
- ai for recommendations only, not commands
- deterministic and auditable business logic

architecture:
erp api --extract--> bronze (raw JSON) --validate--> silver (clean tables) --bus-logic--> gold (metrics + signals) --> streamlit ui --> open ai insight
