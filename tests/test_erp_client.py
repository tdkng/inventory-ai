import pytest
from unittest.mock import Mock, patch
from datetime import datetime

import sys
sys.path.append('/Users/timothynguyen/Documents/projects/inventory-ai/services/')
sys.path.append('/Users/timothynguyen/Documents/projects/inventory-ai/models/')

from erp_client import ERPClient
from schemas import InventoryPosition, PurchaseOrder
import requests


@pytest.fixture
def erp_client():
    """Create an ERPClient instance for testing."""
    return ERPClient("https://api.example.com", "test-api-key")


class TestFetchInventory:
    """Tests for fetch_inventory() method."""

    def test_fetch_inventory_returns_list_of_inventory_positions(self, erp_client):
        """Test that fetch_inventory parses JSON and returns InventoryPosition objects."""
        mock_response = {
            "items": [
                {
                    "partNumber": "PART-001",
                    "warehouse": "WH-A",
                    "onHandQty": 100,
                    "allocatedQty": 20,
                    "availableQty": 80,
                    "lastUpdated": "2025-12-16T10:00:00"
                },
                {
                    "partNumber": "PART-002",
                    "warehouse": "WH-B",
                    "onHandQty": 50,
                    "allocatedQty": 10,
                    "availableQty": 40,
                    "lastUpdated": "2025-12-16T10:00:00"
                }
            ]
        }
        
        with patch.object(erp_client, '_get', return_value=mock_response):
            result = erp_client.fetch_inventory()
        
        assert len(result) == 2
        assert all(isinstance(inv, InventoryPosition) for inv in result)
        assert result[0].part_number == "PART-001"
        assert result[0].on_hand_qty == 100
        assert result[0].available_qty == 80
        assert result[1].part_number == "PART-002"

    def test_fetch_inventory_empty_response(self, erp_client):
        """Test that fetch_inventory handles empty inventory list."""
        mock_response = {"items": []}
        
        with patch.object(erp_client, '_get', return_value=mock_response):
            result = erp_client.fetch_inventory()
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_fetch_inventory_calls_get_with_correct_path(self, erp_client):
        """Test that fetch_inventory calls _get with the correct endpoint."""
        mock_response = {"items": []}
        
        with patch.object(erp_client, '_get', return_value=mock_response) as mock_get:
            erp_client.fetch_inventory()
        
        mock_get.assert_called_once_with("/inventory")


class TestFetchPurchaseOrders:
    """Tests for fetch_purchase_orders() method."""

    def test_fetch_purchase_orders_returns_list_of_purchase_orders(self, erp_client):
        """Test that fetch_purchase_orders parses JSON and returns PurchaseOrder objects."""
        mock_response = {
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
        }
        
        with patch.object(erp_client, '_get', return_value=mock_response):
            result = erp_client.fetch_purchase_orders()
        
        assert len(result) == 2
        assert all(isinstance(po, PurchaseOrder) for po in result)
        assert result[0].po_number == "PO-001"
        assert result[0].part_number == "PART-001"
        assert result[0].order_qty == 50
        assert result[1].customer == "TechCorp Inc"

    def test_fetch_purchase_orders_empty_response(self, erp_client):
        """Test that fetch_purchase_orders handles missing or empty purchaseOrders."""
        mock_response = {}
        
        with patch.object(erp_client, '_get', return_value=mock_response):
            result = erp_client.fetch_purchase_orders()
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_fetch_purchase_orders_calls_get_with_correct_path(self, erp_client):
        """Test that fetch_purchase_orders calls _get with the correct endpoint."""
        mock_response = {"purchaseOrders": []}
        
        with patch.object(erp_client, '_get', return_value=mock_response) as mock_get:
            erp_client.fetch_purchase_orders()
        
        mock_get.assert_called_once_with("/purchase-orders")


class TestGetMethod:
    """Tests for the _get() helper method."""

    def test_get_makes_request_with_correct_headers(self, erp_client):
        """Test that _get sends Authorization header with Bearer token."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_get.return_value = mock_response
            
            result = erp_client._get("/test-endpoint")
        
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == "https://api.example.com/test-endpoint"
        headers = call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer test-api-key"
        assert headers["Accept"] == "application/json"

    def test_get_returns_json_response(self, erp_client):
        """Test that _get returns parsed JSON from response."""
        expected_data = {"key": "value", "items": [1, 2, 3]}
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = erp_client._get("/test")
        
        assert result == expected_data

    def test_get_raises_on_non_200_status(self, erp_client):
        """Test that _get raises RuntimeError on non-200 HTTP status."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            mock_get.return_value = mock_response
            
            with pytest.raises(RuntimeError, match="ERP returned 404"):
                erp_client._get("/nonexistent")

    def test_get_raises_on_invalid_json(self, erp_client):
        """Test that _get raises RuntimeError when response is not valid JSON."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response
            
            with pytest.raises(RuntimeError, match="invalid JSON"):
                erp_client._get("/test")

    def test_get_raises_on_request_exception(self, erp_client):
        """Test that _get raises RuntimeError on network errors."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException("Connection timeout")
            
            with pytest.raises(RuntimeError, match="ERP request failed"):
                erp_client._get("/test")

    def test_get_strips_trailing_slash_from_base_url(self):
        """Test that base_url trailing slash is removed during init."""
        client_with_slash = ERPClient("https://api.example.com/", "key")
        client_without_slash = ERPClient("https://api.example.com", "key")
        
        assert client_with_slash.base_url == "https://api.example.com"
        assert client_without_slash.base_url == "https://api.example.com"
