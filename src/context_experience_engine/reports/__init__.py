"""
Validation Reports Subsystem for MSFACR
Computes signal coverage, metadata completeness, and explainability metrics.
"""

from .validator import MSFACRValidator

__all__ = ["MSFACRValidator"]
