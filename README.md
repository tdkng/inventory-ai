# inventory-ai
ai-assisted inventory risk &amp; reorder decision dashboard

goals:
- consistent inventory snapshots
- ai for recommendations only, not commands
- deterministic and auditable business logic

architecture:
erp api --extract--> bronze --validate--> silver --bus-logic--> gold --> open ai insight --> streamlit ui
