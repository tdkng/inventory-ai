import sys
sys.path.append('/Users/timothynguyen/Documents/projects/inventory-ai/models/')

from schemas import InventoryPosition, UsageRecord, PurchaseOrder, Part
from typing import Dict, Any
from datetime import datetime
import json
import requests

class ERPClient:
    def __init__(self, base_url, api_key, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def fetch_parts(self) -> list[Part]:
        raw = self._get("/parts")
        return [
            Part(
                part_number=part["partNumber"],
                description=part.get("description"),
                unit_price=part["unitPrice"],
                unit_of_measure=part["unitOfMeasure"],
                lead_time_days=part.get("leadTimeDays")
            )
            for part in raw.get("parts", [])
        ]


    def fetch_inventory(self) -> list[InventoryPosition]:
        raw = self._get("/inventory")
        return [
            InventoryPosition(
                part_number=item["partNumber"],
                warehouse=item["warehouse"],
                on_hand_qty=item["onHandQty"],
                allocated_qty=item["allocatedQty"],
                available_qty=item["availableQty"],
                last_updated=item["lastUpdated"]
            )
            for item in raw["items"]
        ]

    def fetch_usage(self) -> list[UsageRecord]:
        raw = self._get("/usage-records")
        return [
            UsageRecord(
                part_number=usage["partNumber"],
                quantity_used=usage["quantityUsed"],
                usage_date=usage["usageDate"]
            )
            for usage in raw.get("usageRecords", [])
        ]

    
    def fetch_purchase_orders(self) -> list[PurchaseOrder]:
        raw = self._get("/purchase-orders")
        return [
            PurchaseOrder(
                po_number=po["poNumber"],
                part_number=po["partNumber"],
                order_qty=po["orderQty"],
                status=po["status"],
                expected_receipt_date=po["expectedReceiptDate"],
                customer=po["customer"]
            )
            for po in raw.get("purchaseOrders", [])
        ]
    

    def _get(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            raise RuntimeError(f"ERP request failed: {e}")

        if response.status_code != 200:
            raise RuntimeError(
                f"ERP returned {response.status_code}: {response.text}"
            )

        try:
            return response.json()
        except ValueError:
            raise RuntimeError("ERP returned invalid JSON")
        

    def _store_bronze(self, payload: dict, name: str):
        ts = datetime.now().isoformat()
        path = f"data/bronze/{name}_{ts}.json"
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)

