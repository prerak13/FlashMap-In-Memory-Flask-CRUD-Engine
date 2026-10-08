# ⚡ FlashMap: In-Memory Flask CRUD Engine

A lightweight, modern, and production-structured **Flask CRUD Web Application and REST API**. Instead of a traditional database, this application utilizes a thread-safe Python dictionary (**Hashmap**) in memory for rapid data operations with $O(1)$ lookups, insertions, updates, and deletions.

---

## 🌟 Key Features

- 🧠 **In-Memory Hashmap Storage**: Data is encapsulated inside `HashMapStore` (`store.py`) backed by Python's `dict` data structure and protected by `threading.Lock` for thread safety.
- 🧱 **Modular Flask Blueprints**: Clean separation of concerns with dedicated blueprints for Web UI routes (`routes/ui.py`) and REST API endpoints (`routes/api.py`).
- ⚡ **RESTful API**: Complete set of CRUD endpoints supporting JSON request/response payloads, query search, and multi-criteria filtering.
- 🎨 **Modern Glassmorphism UI**: Beautiful dark-theme dashboard built with responsive HTML5, CSS custom properties, micro-animations, stat counter cards, and toast notifications.
- 🔍 **Search & Multi-Criteria Filtering**: Instant search across titles/descriptions with filtering by Status (*Pending*, *In Progress*, *Completed*), Priority (*Urgent*, *High*, *Medium*, *Low*), and Category.
- 🛡️ **Centralized Error Handling**: Context-aware 404 and 500 error handlers that return structured JSON for API routes and fallback HTML for browser requests.
- 🧪 **Automated Test Suite**: 100% test coverage using Python's built-in `unittest` framework testing all REST routes and error boundary conditions.

---

## 📁 Project Structure

```text
FlashMap/
├── app.py              # Main Flask application initialization & error handlers
├── store.py            # In-memory Hashmap data repository & thread-safe lock
├── test_app.py         # Automated unit test suite (10/10 passing)
├── pyrightconfig.json  # Pyright / Pylance Python language server config
├── requirements.txt    # Python package dependencies
├── README.md           # Project documentation & API reference
├── routes/             # 📁 Flask Blueprints Package
│   ├── __init__.py     # Package exports for ui_bp & api_bp
│   ├── ui.py           # Web UI Blueprint (Renders index.html)
│   └── api.py          # REST API Blueprint (url_prefix="/api")
├── templates/
│   └── index.html      # Glassmorphism Web UI template
└── static/
    ├── css/
    │   └── style.css   # Dark theme CSS styling & design system
    └── js/
        └── app.js      # Async fetch logic & interactive UI state
```

---

## 🧩 Architecture & Blueprint Overview

### 1. **Modular Routing (`routes/`)**
The application uses Flask **Blueprints** to decouple the web user interface from API business logic:
* **`routes/ui.py` (`ui_bp`)**: Serves the main frontend Web UI on `/`.
* **`routes/api.py` (`api_bp`)**: Scoped with `url_prefix="/api"`, serving all REST API endpoints (`/api/items`, `/api/stats`, `/api/reset`).

### 2. **Application Factory (`app.py`)**
`app.py` acts as the orchestrator:
* Registers `ui_bp` and `api_bp`.
* Defines global error handlers (`404` and `500`).
* Starts the development server when executed directly via `if __name__ == "__main__":`.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.8+** installed on your system.

### 2. Setup Virtual Environment
```bash
# Navigate to project directory
cd /path/to/Flask

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
*Access the Web UI in your browser at:* **`http://localhost:5050`**

---

## 🧪 Running Unit Tests

Run the test suite using `unittest`:
```bash
python -m unittest test_app.py
```

---

## 📡 REST API Documentation

### API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/items` | Retrieve all items (supports `search`, `status`, `priority`, `category` query filters) |
| `GET` | `/api/items/<id>` | Fetch a single item by Hashmap Key ID |
| `POST` | `/api/items` | Create a new item |
| `PUT` | `/api/items/<id>` | Update an existing item |
| `PATCH` | `/api/items/<id>/status` | Quick update item status |
| `DELETE` | `/api/items/<id>` | Delete an item from Hashmap |
| `GET` | `/api/stats` | Get metrics summary (total items, status breakdown) |
| `POST` | `/api/reset` | Seed/Reset hashmap store with default sample data |

---

## 💻 cURL Examples

#### 1. Fetch All Items (With Search & Filters)
```bash
curl -X GET "http://localhost:5050/api/items?search=Flask&status=Completed"
```

#### 2. Create a New Item
```bash
curl -X POST "http://localhost:5050/api/items" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Optimize Redis Caching Layer",
           "description": "Benchmarking memory usage and latency.",
           "category": "Backend",
           "priority": "High",
           "status": "Pending"
         }'
```

#### 3. Fetch Single Item by ID
```bash
curl -X GET "http://localhost:5050/api/items/item-001"
```

#### 4. Update an Item
```bash
curl -X PUT "http://localhost:5050/api/items/item-001" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Design System Architecture (v2)",
           "description": "Updated glassmorphism guidelines.",
           "category": "Design",
           "priority": "Urgent",
           "status": "In Progress"
         }'
```

#### 5. Patch Item Status
```bash
curl -X PATCH "http://localhost:5050/api/items/item-001/status" \
     -H "Content-Type: application/json" \
     -d '{"status": "Completed"}'
```

#### 6. Delete an Item
```bash
curl -X DELETE "http://localhost:5050/api/items/item-001"
```

#### 7. Retrieve Store Statistics
```bash
curl -X GET "http://localhost:5050/api/stats"
```

---

## ⚙️ How the Hashmap DB Works

The in-memory storage layer in `store.py` uses a Python dictionary (`dict`), providing standard hash map operations:

- **Insertion (`POST`)**: $O(1)$ time complexity by key assignment `self._store[id] = item`.
- **Lookup (`GET /<id>`)**: $O(1)$ direct hashmap key access `self._store.get(id)`.
- **Deletion (`DELETE /<id>`)**: $O(1)$ key removal via `del self._store[id]`.
- **Thread Safety**: Uses `threading.Lock()` context managers (`with self._lock:`) to prevent race conditions during concurrent HTTP requests.

---

## 📜 License
This project is open-source and free to use.
