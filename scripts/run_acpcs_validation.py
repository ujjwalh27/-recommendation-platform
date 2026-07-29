"""
ACPCS Validation Suite Launcher
Runs automated test suite across all 6 ACPCS validation scenarios.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from content_catalog.validation.runner import ACPCSValidationRunner

if __name__ == "__main__":
    runner = ACPCSValidationRunner()
    results = runner.run_all_tests()
    if not results["overall_passed"]:
        sys.exit(1)
