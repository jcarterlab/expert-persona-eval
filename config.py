"""
Configuration settings module.

This module loads values from environment variables where 
available with sensible defaults provided for local execution.
"""

from dotenv import load_dotenv
import os

load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
BASIC_MODEL = os.getenv('BASIC_MODEL', 'gemini-2.5-flash-lite')
RANDOM_SEED = int(os.getenv('RANDOM_SEED', 2026))
DS_SAMPLE_NO = int(os.getenv('DS_SAMPLE_NO', 10))
LLM_RETRY_ATTEMPTS = int(os.getenv('LLM_RETRY_ATTEMPTS', 4))
LLM_WAIT_TIME = int(os.getenv('LLM_WAIT_TIME', 15))