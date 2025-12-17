from flask import Flask, jsonify, request
from datetime import datetime
from functools import wraps

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Mock ERP Server is running."

@app.route("/inventory", methods=["GET"])
def inventory():
    return jsonify({
        "items": [
            {
                "partNumber": "PART-001",
                "warehouse": "WH-A",
                "onHandQty": 100,
                "allocatedQty": 20,
                "availableQty": 80,
                "lastUpdated": datetime.now().isoformat()
            },
            {
                "partNumber": "PART-002",
                "warehouse": "WH-B",
                "onHandQty": 50,
                "allocatedQty": 10,
                "availableQty": 40,
                "lastUpdated": datetime.now().isoformat()
            }
        ]
    })

@app.route("/usage-records", methods=["GET"])
def usage_records():
    return jsonify({
        "usageRecords": [
            {
                "partNumber": "PART-001",
                "quantityUsed": 15,
                "usageDate": "2025-12-14"
            },
            {
                "partNumber": "PART-001",
                "quantityUsed": 20,
                "usageDate": "2025-12-15"
            },
            {
                "partNumber": "PART-002",
                "quantityUsed": 8,
                "usageDate": "2025-12-14"
            },
            {
                "partNumber": "PART-002",
                "quantityUsed": 12,
                "usageDate": "2025-12-15"
            },
            {
                "partNumber": "PART-001",
                "quantityUsed": 10,
                "usageDate": "2025-12-16"
            }
        ]
    })

@app.route("/purchase-orders", methods=["GET"])
def purchase_orders():
    return jsonify({
        "purchaseOrders": [
            {
                "poNumber": "PO-001",
                "partNumber": "PART-001",
                "orderQty": 50,
                "orderDate": "2025-12-15",
                "customer": "ACME Corp"
            },
            {
                "poNumber": "PO-002",
                "partNumber": "PART-002",
                "orderQty": 25,
                "orderDate": "2025-12-16",
                "customer": "TechCorp Inc"
            }
        ]
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)