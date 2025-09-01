"""
Market Basket Analysis Suite - Utilities Package
================================================

This package contains utility modules for the Market Basket Analysis application:
- styles.py: CSS styling and theme management
- data_processor.py: Data processing and transformation utilities
- export_manager.py: Export functionality for multiple file formats

Author: Market Basket Analysis Suite
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Market Basket Analysis Suite"

# Import main utility classes for easy access
try:
    from .data_processor import DataProcessor
    from .export_manager import ExportManager
    
    __all__ = ['DataProcessor', 'ExportManager']
    
except ImportError as e:
    # Handle import errors gracefully
    print(f"Warning: Could not import all utility modules: {e}")
    __all__ = []
