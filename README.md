# inventory-ai
ai-assisted inventory risk &amp; reorder decision dashboard

features:
- consistent inventory snapshots
- ai recommendations for risk factors and purchase orders
- deterministic and auditable business logic

architecture:
erp api --extract--> bronze --validate--> silver --bus-logic--> gold --> open ai insight --> streamlit ui

how to use:
- mock_erp_server.py currently is being used to mock a real API and plays the role of providing data to the inventory system via available GET methods
- enter virtual environment (venv)
- run mock_erp_server.py and start up streamlit ui with app.py
- wait for data to load in, then select part which you want OpenAI to analyze in risk factor

entering virtual environment
```bash
source .venv/bin/activate
```

running mock_erp_server.py
```bash
python mock_erp_server.py
```

running streamlit (app.py)
```bash
streamlit run app.py
```
