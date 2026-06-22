"""
Configuration settings module.

This module loads values from environment variables where 
available with sensible defaults provided for local execution.
"""

from dotenv import load_dotenv
import os

load_dotenv()

# --------------------------------------------------
# API keys
# --------------------------------------------------

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')



LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()