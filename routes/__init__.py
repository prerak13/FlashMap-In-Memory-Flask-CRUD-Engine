"""
Routes package initialization for FlashMap application.
"""

from routes.ui import ui_bp
from routes.api import api_bp

__all__ = ["ui_bp", "api_bp"]
