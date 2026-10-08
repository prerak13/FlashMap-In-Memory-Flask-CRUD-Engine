"""
FlashMap: Flask CRUD Application with In-Memory Hashmap Storage.
"""

from flask import Flask, render_template, request, jsonify
from store import db
from routes import ui_bp, api_bp

app = Flask(__name__)

# --- Register Blueprints ---
app.register_blueprint(ui_bp)
app.register_blueprint(api_bp)



# --- Error Handlers ---

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Not Found", "message": "The requested endpoint does not exist."}), 404
    return render_template("index.html"), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal Server Error", "message": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)

