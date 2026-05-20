"""
Entry point script for running the FastAPI application.
Usage: python run.py
"""
import sys

from app.main import main

if __name__ == "__main__":
    sys.exit(main())
