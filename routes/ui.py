"""
UI routes blueprint for FlashMap application.
"""

from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/")
def index():
    """Renders the main FlashMap CRUD web interface."""
    return render_template("index.html")
