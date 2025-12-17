import sys
sys.path.append('/Users/timothynguyen/Documents/projects/inventory-ai/models/')

from schemas import InventoryPosition, PurchaseOrder
from typing import Dict, Any
import datetime
import requests

class ERPClient:
    def __init__(self, base_url, api_key, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout


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
    
    
    def fetch_purchase_orders(self) -> list[PurchaseOrder]:
        raw = self._get("/purchase-orders")
        return [
            PurchaseOrder(
                po_number=po["poNumber"],
                part_number=po["partNumber"],
                order_qty=po["orderQty"],
                order_date=po["orderDate"],
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
        ts = datetime.utcnow().isoformat()
        path = f"data/bronze/{name}_{ts}.json"
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)

