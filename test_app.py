"""
Unit Tests for Flask CRUD Application with In-Memory Hashmap Storage.
"""

import json
import unittest
from app import app, db


class FlaskCRUDTestCase(unittest.TestCase):
    """Test suite for CRUD REST endpoints using in-memory hashmap."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.seed_sample_data()

    def test_get_all_items(self):
        """Test retrieving all items from hashmap."""
        res = self.app.get('/api/items')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 5)

    def test_get_single_item(self):
        """Test getting a specific item by hashmap ID."""
        res = self.app.get('/api/items/item-001')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], 'item-001')

    def test_get_nonexistent_item(self):
        """Test fetching an ID that does not exist in hashmap."""
        res = self.app.get('/api/items/invalid-id-999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_item(self):
        """Test inserting a new item into hashmap."""
        payload = {
            "title": "Build Hashmap Dashboard",
            "description": "Create responsive web UI with glassmorphism",
            "category": "Frontend",
            "priority": "High",
            "status": "Pending"
        }
        res = self.app.post('/api/items', data=json.dumps(payload), content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn("item-", data['data']['id'])
        self.assertEqual(data['data']['title'], payload['title'])

    def test_create_item_validation_failure(self):
        """Test creating an item with missing required title."""
        payload = {"description": "Missing title field"}
        res = self.app.post('/api/items', data=json.dumps(payload), content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_update_item(self):
        """Test updating existing item in hashmap."""
        payload = {
            "title": "Design System Architecture (Updated)",
            "description": "Updated glassmorphism style rules",
            "category": "Design",
            "priority": "Urgent",
            "status": "Completed"
        }
        res = self.app.put('/api/items/item-001', data=json.dumps(payload), content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['title'], payload['title'])

    def test_patch_item_status(self):
        """Test patching item status."""
        payload = {"status": "Completed"}
        res = self.app.patch('/api/items/item-001/status', data=json.dumps(payload), content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['data']['status'], "Completed")

    def test_delete_item(self):
        """Test deleting an item from hashmap."""
        res = self.app.delete('/api/items/item-001')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify O(1) key is deleted
        verify_res = self.app.get('/api/items/item-001')
        self.assertEqual(verify_res.status_code, 404)

    def test_search_and_filter(self):
        """Test search query and filter parameters."""
        res = self.app.get('/api/items?search=Architecture')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(all('Architecture' in item['title'] or 'Architecture' in item['description'] for item in data['data']))

    def test_stats_endpoint(self):
        """Test metrics calculation endpoint."""
        res = self.app.get('/api/stats')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('total', data['data'])
        self.assertIn('completed', data['data'])


if __name__ == '__main__':
    unittest.main()
