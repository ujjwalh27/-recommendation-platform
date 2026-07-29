import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.reports.monthly_report import MonthlyReportGeneratorEngine

def main():
    print("==========================================================================")
    print("      PMCLP MONTHLY QUALITY REPORT GENERATOR CLI")
    print("==========================================================================")

    engine = MonthlyReportGeneratorEngine()
    report = engine.generate_monthly_report("July 2026")

    print(f"Report Generated for: {report['month']}")
    print(f"Total Videos Processed: {report['total_videos_processed']}")
    print(f"Overall Accuracy Percent: {report['overall_accuracy_percent']}%")
    print(f"Recommendation Eligibility Rate: {report['recommendation_eligibility_percent']}%")
    print(f"\nMarkdown Report Saved to production_monitoring/monthly_report_July_2026.md")

if __name__ == "__main__":
    main()
