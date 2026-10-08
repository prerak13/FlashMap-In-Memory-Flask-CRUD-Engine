"""
REST API Blueprint for FlashMap application.
"""

from flask import Blueprint, jsonify, request
from store import db

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/items", methods=["GET"])
def get_items():
    """Retrieve all items with optional filters."""
    search = request.args.get("search")
    status = request.args.get("status")
    priority = request.args.get("priority")
    category = request.args.get("category")

    items = db.get_all(search=search, status=status, priority=priority, category=category)
    return jsonify({
        "success": True,
        "count": len(items),
        "data": items
    }), 200


@api_bp.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    """Retrieve a single item by Hashmap Key ID."""
    item = db.get_by_id(item_id)
    if not item:
        return jsonify({
            "success": False,
            "error": "Item not found",
            "message": f"No item exists with ID '{item_id}'"
        }), 404

    return jsonify({
        "success": True,
        "data": item
    }), 200


@api_bp.route("/items", methods=["POST"])
def create_item():
    """Create a new item in the hashmap."""
    data = request.get_json() or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Field 'title' is required and cannot be empty."
        }), 400

    item = db.create(data)
    return jsonify({
        "success": True,
        "message": "Item created successfully",
        "data": item
    }), 201


@api_bp.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    """Update an existing item in the hashmap."""
    data = request.get_json() or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Field 'title' is required and cannot be empty."
        }), 400

    updated = db.update(item_id, data)
    if not updated:
        return jsonify({
            "success": False,
            "error": "Item not found",
            "message": f"No item exists with ID '{item_id}'"
        }), 404

    return jsonify({
        "success": True,
        "message": "Item updated successfully",
        "data": updated
    }), 200


@api_bp.route("/items/<item_id>/status", methods=["PATCH"])
def patch_item_status(item_id):
    """Quick update of item status."""
    data = request.get_json() or {}
    status = data.get("status", "").strip()

    if not status:
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Field 'status' is required."
        }), 400

    updated = db.patch_status(item_id, status)
    if not updated:
        return jsonify({
            "success": False,
            "error": "Item not found",
            "message": f"No item exists with ID '{item_id}'"
        }), 404

    return jsonify({
        "success": True,
        "message": "Item status updated",
        "data": updated
    }), 200


@api_bp.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item from the hashmap by ID."""
    deleted = db.delete(item_id)
    if not deleted:
        return jsonify({
            "success": False,
            "error": "Item not found",
            "message": f"No item exists with ID '{item_id}'"
        }), 404

    return jsonify({
        "success": True,
        "message": f"Item '{item_id}' deleted successfully"
    }), 200


@api_bp.route("/stats", methods=["GET"])
def get_stats():
    """Retrieve hashmap metrics and statistics."""
    stats = db.get_stats()
    return jsonify({
        "success": True,
        "data": stats
    }), 200


@api_bp.route("/reset", methods=["POST"])
def reset_sample_data():
    """Reset hashmap to initial sample state."""
    db.seed_sample_data()
    return jsonify({
        "success": True,
        "message": "Store reset to sample data successfully"
    }), 200
