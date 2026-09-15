"""
SOC Triage Engine Package

This package contains the core logic for AI-powered security alert triage,
including rule-based, machine learning, and LLM-based classification methods.
"""

__version__ = "1.0.0"
__author__ = "Neha Purohit"

from .ai_triage_engine import TriageEngine
from .metrics_calculator import calculate_accuracy

__all__ = ['TriageEngine', 'calculate_accuracy']
