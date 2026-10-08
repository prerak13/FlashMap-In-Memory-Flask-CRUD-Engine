"""
In-Memory Hashmap Data Repository for Flask CRUD Application.
Uses Python dictionary (hashmap) as the storage backend with thread-safe locking.
"""

from datetime import datetime
import uuid
import threading
from typing import Dict, List, Optional, Any


class HashMapStore:
    """
    Thread-safe Hashmap Data Store for managing items in memory.
    """

    def __init__(self):
        # The primary hashmap storing items keyed by unique string IDs
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.seed_sample_data()

    def seed_sample_data(self):
        """Populates the store with initial demonstration items."""
        with self._lock:
            self._store.clear()
            samples = [
                {
                    "title": "Design System Architecture",
                    "description": "Draft component guidelines and glassmorphism styling variables.",
                    "category": "Design",
                    "priority": "High",
                    "status": "In Progress"
                },
                {
                    "title": "Implement Flask Hashmap Storage",
                    "description": "Create thread-safe CRUD data access layer using Python dictionary.",
                    "category": "Backend",
                    "priority": "Urgent",
                    "status": "Completed"
                },
                {
                    "title": "API Documentation & cURL Examples",
                    "description": "Write clean README.md detailing REST endpoints, request payloads, and setup instructions.",
                    "category": "Documentation",
                    "priority": "Medium",
                    "status": "In Progress"
                },
                {
                    "title": "Unit Testing & QA Verification",
                    "description": "Verify all REST API endpoints (GET, POST, PUT, DELETE) pass unittest assertions.",
                    "category": "QA",
                    "priority": "High",
                    "status": "Pending"
                },
                {
                    "title": "Optimize Responsive UI Layout",
                    "description": "Ensure mobile touch targets and grid system adapt smoothly on narrow viewports.",
                    "category": "Frontend",
                    "priority": "Low",
                    "status": "Pending"
                }
            ]

            now = datetime.utcnow().isoformat() + "Z"
            for idx, item in enumerate(samples, start=1):
                item_id = f"item-{idx:03d}"
                self._store[item_id] = {
                    "id": item_id,
                    "title": item["title"],
                    "description": item["description"],
                    "category": item["category"],
                    "priority": item["priority"],
                    "status": item["status"],
                    "created_at": now,
                    "updated_at": now
                }

    def get_all(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves all items from hashmap with optional filtering and search."""
        with self._lock:
            items = list(self._store.values())

        # Filter by search string
        if search:
            query = search.strip().lower()
            items = [
                i for i in items
                if query in i["title"].lower() or query in i["description"].lower() or query in i["category"].lower()
            ]

        # Filter by status
        if status and status != "All":
            items = [i for i in items if i["status"].lower() == status.lower()]

        # Filter by priority
        if priority and priority != "All":
            items = [i for i in items if i["priority"].lower() == priority.lower()]

        # Filter by category
        if category and category != "All":
            items = [i for i in items if i["category"].lower() == category.lower()]

        # Sort by updated_at descending
        items.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return items

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single item by its ID (O(1) Hashmap Lookup)."""
        with self._lock:
            return self._store.get(item_id)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new item and adds it to the hashmap store."""
        with self._lock:
            new_id = f"item-{uuid.uuid4().hex[:8]}"
            now = datetime.utcnow().isoformat() + "Z"

            item = {
                "id": new_id,
                "title": data.get("title", "").strip(),
                "description": data.get("description", "").strip(),
                "category": data.get("category", "General").strip(),
                "priority": data.get("priority", "Medium").strip(),
                "status": data.get("status", "Pending").strip(),
                "created_at": now,
                "updated_at": now
            }

            # O(1) Insertion into hashmap
            self._store[new_id] = item
            return item

    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates an existing item in the hashmap store."""
        with self._lock:
            if item_id not in self._store:
                return None

            existing = self._store[item_id]
            now = datetime.utcnow().isoformat() + "Z"

            existing["title"] = data.get("title", existing["title"]).strip()
            existing["description"] = data.get("description", existing["description"]).strip()
            existing["category"] = data.get("category", existing["category"]).strip()
            existing["priority"] = data.get("priority", existing["priority"]).strip()
            existing["status"] = data.get("status", existing["status"]).strip()
            existing["updated_at"] = now

            return existing

    def patch_status(self, item_id: str, status: str) -> Optional[Dict[str, Any]]:
        """Updates only the status of an existing item."""
        with self._lock:
            if item_id not in self._store:
                return None

            existing = self._store[item_id]
            existing["status"] = status.strip()
            existing["updated_at"] = datetime.utcnow().isoformat() + "Z"
            return existing

    def delete(self, item_id: str) -> bool:
        """Deletes an item from the hashmap store by ID (O(1) Deletion)."""
        with self._lock:
            if item_id in self._store:
                del self._store[item_id]
                return True
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Calculates store analytics."""
        with self._lock:
            items = list(self._store.values())

        total = len(items)
        completed = sum(1 for i in items if i["status"].lower() == "completed")
        in_progress = sum(1 for i in items if i["status"].lower() == "in progress")
        pending = sum(1 for i in items if i["status"].lower() == "pending")

        priority_breakdown = {
            "Urgent": sum(1 for i in items if i["priority"].lower() == "urgent"),
            "High": sum(1 for i in items if i["priority"].lower() == "high"),
            "Medium": sum(1 for i in items if i["priority"].lower() == "medium"),
            "Low": sum(1 for i in items if i["priority"].lower() == "low")
        }

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "priority_breakdown": priority_breakdown
        }


# Global in-memory hashmap store instance
db = HashMapStore()

