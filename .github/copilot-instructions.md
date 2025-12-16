# AI Coding Agent Instructions for inventory-ai

## Project Overview

**inventory-ai** is an AI-assisted inventory risk & reorder decision dashboard. It's a data pipeline + Streamlit UI system that extracts ERP data, validates & transforms it through a medallion architecture (bronze/silver/gold), applies business logic, and provides AI recommendations (not commands).

### Architecture: Bronze → Silver → Gold → UI

- **Bronze Layer** (`data/bronze/`): Raw JSON exports from ERP API
- **Silver Layer** (`data/silver/`): Validated, cleaned tables (schema-driven)
- **Gold Layer** (`data/gold/`): Business metrics & signals (inventory health, reorder signals, risk scoring)
- **UI** (`pages/`, `app.py`): Streamlit app with tabs for inventory, purchasing, and AI insights

### Critical Design Principle

AI provides **recommendations only, never commands**. The system remains deterministic and auditable—business logic is transparent and business decisions are human-validated.

---

## Key Components & Service Boundaries

### Services (`services/`)

1. **`erp_client.py`** - ERP System Interface

   - Handles all external ERP API communication
   - Methods: `get_order()`, `create_order()`, `update_inventory()`, `get_part_details()`
   - Returns raw data (bronze layer candidate)
   - **Pattern**: Encapsulates API details; all ERP changes flow through here

2. **`ai_client.py`** - AI Integration (OpenAI, currently empty)

   - Responsible for OpenAI API calls and prompt engineering
   - Should follow the "recommendations only" philosophy
   - Output goes to `ai_insights.py` page

3. **`inventory_logic.py`** - Business Logic (currently empty)
   - This is where bronze→silver→gold transformations happen
   - Validation rules, metrics calculation, reorder signal logic
   - Should be deterministic and testable independently

### Models (`models/schemas.py`)

Uses **Pydantic** exclusively for all data contracts:

- `Part` - master data (part_number, description, unit_price, unit_of_measure, lead_time_days)
- `InventoryPosition` - warehouse-level inventory state
- `UsageRecord` - consumption history for demand signals
- `PurchaseOrder` - order metadata for lead time analysis

**Pattern**: Every data transformation validates against a schema. No unvalidated data moves between layers.

### UI Pages (`pages/`)

- `inventory.py` - Inventory snapshots, on-hand/allocated/available quantities
- `purchasing.py` - Purchase order management & reorder recommendations
- `ai_insights.py` - LLM-powered narrative insights (no direct commands)

**Pattern**: Pages are thin UI layers. Logic stays in `services/inventory_logic.py`.

---

## Critical Data Flow Patterns

### Extraction → Validation → Business Logic

```
ERPClient.get_order() → bronze/raw.json →
Pydantic validation (schemas.py) → silver/clean_tables/ →
inventory_logic.py (metrics, signals) → gold/metrics.json →
pages (UI rendering) or ai_client (insight generation)
```

**When adding data flows:**

1. Define the Pydantic schema in `models/schemas.py` **first**
2. Extract via `ERPClient` method
3. Validate with `.parse_obj()` or `.validate()` in `inventory_logic.py`
4. Store validated data in silver/gold layers
5. Expose via page or AI endpoint

### No Direct ERP Mutations Without Logic

Any `create_order()` or `update_inventory()` call must:

- Come from validated reorder recommendations (not raw AI suggestions)
- Be logged (utils/logging.py)
- Be trackable in audit trail (gold layer)

---

## Developer Workflows

### Branch Strategy

- **main**: Production-ready code
- **feature/\***: Feature branches for development (e.g., `feature/data-ingestion-layer`)
- Merge via PR; all changes flow through git history (auditable requirement)

### Adding a New Data Endpoint

1. **Add Pydantic schema** in `models/schemas.py` (describes the data contract)
2. **Add ERPClient method** in `services/erp_client.py` (extraction)
3. **Add processing logic** in `services/inventory_logic.py` (validation + transformation)
4. **Add UI display** in appropriate `pages/*.py`
5. **Add cache** in `utils/cache.py` if needed (for performance)

### Testing Data Layers

- Bronze layer: Test `ERPClient` methods return valid JSON
- Silver layer: Test Pydantic validation catches malformed data
- Gold layer: Test `inventory_logic.py` produces correct metrics
- No formal test framework in place yet; add pytest when tests are formalized

---

## Project-Specific Conventions

### Configuration

- `config.py`: Centralized config (API keys, thresholds, timeouts)
- Currently empty; populate with environment-aware settings for bronze/silver/gold paths

### Logging & Caching

- `utils/logging.py`: Should audit all ERP mutations and AI recommendations
- `utils/cache.py`: Cache bronze→silver transformations to avoid re-processing; invalidate on new data
- **Pattern**: Bronze data is immutable; cache aggressively. Silver/gold can be regenerated.

### Naming Conventions

- Snake case: `part_number`, `on_hand_qty`, `available_qty` (matches database/ERP style)
- Table/file names match schema names: `InventoryPosition` → `inventory_positions.json` in silver/
- API methods follow CRUD: `get_*`, `create_*`, `update_*`

### Gold Layer Signals

The gold layer computes **domain-specific signals**, not generic analytics:

- Reorder signals (when to buy)
- Stockout risk (lead time vs. usage rate)
- Overstock risk (holding cost vs. turnover)
- Safety stock recommendations (variability-based)

These feed AI insights, not direct commands.

---

## Common Pitfalls to Avoid

1. **Unvalidated Data**: Never skip Pydantic validation—schema mismatch silently breaks downstream logic
2. **Skipping Bronze**: Don't fetch directly to silver; store raw exports first (audit trail requirement)
3. **AI Command Confusion**: AI output is a _recommendation field_ in gold layer, not an executable action
4. **Schema Versioning**: When modifying schemas, consider backward compatibility (bronze data is immutable)
5. **Cache Staleness**: Always tag cached data with fetch timestamp; invalidate on new bronze imports

---

## External Dependencies & Integration Points

- **Streamlit**: UI framework (see `pages/` structure)
- **Pydantic**: Data validation (all schemas in `models/schemas.py`)
- **OpenAI API**: AI recommendations (via `ai_client.py`, not yet implemented)
- **ERP System**: External API (SAP, NetSuite, etc.—mocked in `ERPClient` currently)
- **File Storage**: Bronze/silver/gold stored as JSON files locally (`data/` directory)

---

## Getting Started as an AI Agent

1. **Understand the flow**: Read README.md, then trace a data import in `services/erp_client.py` → `services/inventory_logic.py` → `pages/inventory.py`
2. **Check schemas first**: Any new data? Define Pydantic model in `models/schemas.py` before writing extraction code
3. **Reference branch**: Working on `feature/data-ingestion-layer`; merge to main when ready
4. **Test locally**: Run `streamlit run app.py` to validate UI changes; mock ERP data for testing
5. **Audit trail**: All mutations must be logged and trackable in git history
