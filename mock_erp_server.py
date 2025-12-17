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