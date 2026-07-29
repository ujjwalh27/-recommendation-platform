# Production Monitoring & Continuous Learning Platform (PMCLP) Runbook

## 1. Executive Summary & System Overview

The **Production Monitoring & Continuous Learning Platform (PMCLP)** provides operational observability, quality assurance, human review workflows, failure analysis indexing, automated regression gating, and recommendation readiness tracking for the Daiv Video Intelligence Platform.

```
User Upload  --->  Semantic Intelligence Engine
                         │
                         ├────────► Recommendation Engine
                         ├────────► Production Prediction Logger
                         ├────────► Prediction Audit Trail
                         ├────────► Human Review Queue
                         ├────────► Failure Repository
                         └────────► Operational Dashboards
```

---

## 2. Component Architecture & Modules

### Module 1 – Production Prediction Logger
- **File**: `backend/monitoring/prediction_logger.py`
- **Storage**: `production_monitoring/prediction_logs.json`
- **Schema**: Enforced by `prediction_log_schema.json`

### Module 2 – Prediction Audit Trail
- **File**: `backend/monitoring/audit_trail.py`
- **Storage**: `production_monitoring/audit_trails/{prediction_id}.json`
- **Schema**: Enforced by `audit_schema.json`

### Module 3 – Human Review Queue
- **File**: `backend/review/review_queue.py`
- **Routing Rules**: Triggered when confidence $< 0.75$, unknown ritual/deity/temple detected, low OCR/whisper confidence, or modality disagreement.

### Module 4 – Failure Repository
- **File**: `backend/failures/failure_repository.py`
- **Storage**: `failure_repository.json`
- **Categories**: Visual Ambiguity, Audio Failure, OCR Failure, Unknown Ritual, Occlusion, Low Lighting, Camera Motion, Rule Conflict, Taxonomy Gap.

### Module 5 – Operational Dashboards
- **File**: `backend/dashboards/dashboard_provider.py` & React UI `PMCLPDashboard.jsx`

### Module 6 – Unknown Knowledge Detection
- **File**: `backend/monitoring/unknown_detector.py`
- **Storage**: `production_monitoring/taxonomy_proposals.json`

### Module 7 – Regression Testing Framework
- **File**: `backend/regression/regression_runner.py` & CLI `scripts/regression_runner.py`
- **Gating**: Blocks deployment if Overall Accuracy $< 88.0\%$ or F1 $< 0.85$.

### Module 8 – Monthly Quality Report Generator
- **File**: `backend/reports/monthly_report.py` & CLI `scripts/monthly_report_generator.py`

### Module 9 – Semantic Version Management
- Tracks independent component versions (`model_version`, `taxonomy_version`, `rule_engine_version`, `benchmark_version`, `challenge_version`, `production_version`).

### Module 10 – Downstream Recommendation Readiness
- Tracks metadata completeness score, missing deity/ritual breakdown, semantic processing latency, and recommendation feed eligibility percentage.

---

## 3. Operational Runbook Procedures

### Procedure A: Reviewing Low-Confidence Predictions
1. Navigate to **Monitoring (PMCLP)** -> **Human Review Queue**.
2. Inspect predicted class, confidence score, and routing reason.
3. Click **Accept** if prediction is correct, or **Correct** to specify actual ritual class and failure root cause.

### Procedure B: Approving New Taxonomy Proposals
1. Navigate to **Monitoring (PMCLP)** -> **Unknown Taxonomy**.
2. Review detected unknown entity, occurrence count, and sample video IDs.
3. Click **Approve & Merge** to safely incorporate into `dbb_taxonomy.json`.

### Procedure C: Executing Automated Regression Testing
```bash
python scripts/regression_runner.py
```
- Verify that `deployment_gate_status` outputs `PASSED - DEPLOYMENT APPROVED`.

### Procedure D: Generating Monthly Quality Reports
```bash
python scripts/monthly_report_generator.py
```
- Report output saved to `production_monitoring/monthly_report_July_2026.md`.
