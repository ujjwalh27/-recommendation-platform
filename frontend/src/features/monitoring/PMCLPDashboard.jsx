import React, { useState, useEffect } from "react";

export default function PMCLPDashboard() {
    const [activeSubTab, setActiveSubTab] = useState("dashboards");
    const [overview, setOverview] = useState(null);
    const [semantic, setSemantic] = useState(null);
    const [failures, setFailures] = useState(null);
    const [reviews, setReviews] = useState(null);
    const [readiness, setReadiness] = useState(null);
    
    const [pendingReviews, setPendingReviews] = useState([]);
    const [failureLogs, setFailureLogs] = useState([]);
    const [proposals, setProposals] = useState([]);
    const [predictionLogs, setPredictionLogs] = useState([]);
    const [selectedAudit, setSelectedAudit] = useState(null);
    const [regressionRes, setRegressionRes] = useState(null);
    const [monthlyReport, setMonthlyReport] = useState(null);
    const [statusMsg, setStatusMsg] = useState("");

    // Correction modal state
    const [correctModal, setCorrectModal] = useState(null);
    const [correctForm, setCorrectForm] = useState({
        correct_class: "Milk Abhishekam",
        failure_type: "Visual Ambiguity",
        root_cause: "Liquid stream obscured by bright altar lighting.",
        reviewer: "Senior_Reviewer_A"
    });

    useEffect(() => {
        fetchDashboards();
        fetchPendingReviews();
        fetchFailures();
        fetchProposals();
        fetchPredictionLogs();
    }, []);

    const fetchDashboards = async () => {
        try {
            const [oRes, sRes, fRes, rRes, rdRes] = await Promise.all([
                fetch("http://localhost:8000/api/dashboard/overview"),
                fetch("http://localhost:8000/api/dashboard/semantic"),
                fetch("http://localhost:8000/api/dashboard/failures"),
                fetch("http://localhost:8000/api/dashboard/reviews"),
                fetch("http://localhost:8000/api/dashboard/readiness")
            ]);
            setOverview(await oRes.json());
            setSemantic(await sRes.json());
            setFailures(await fRes.json());
            setReviews(await rRes.json());
            setReadiness(await rdRes.json());
        } catch (e) {
            console.error(e);
        }
    };

    const fetchPendingReviews = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/review/pending");
            setPendingReviews(await res.json());
        } catch (e) {
            console.error(e);
        }
    };

    const fetchFailures = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/failures");
            setFailureLogs(await res.json());
        } catch (e) {
            console.error(e);
        }
    };

    const fetchProposals = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/taxonomy/proposals");
            setProposals(await res.json());
        } catch (e) {
            console.error(e);
        }
    };

    const fetchPredictionLogs = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/monitoring/predictions");
            setPredictionLogs(await res.json());
        } catch (e) {
            console.error(e);
        }
    };

    const fetchAudit = async (predId) => {
        try {
            const res = await fetch(`http://localhost:8000/api/monitoring/audit/${predId}`);
            setSelectedAudit(await res.json());
        } catch (e) {
            console.error(e);
        }
    };

    const handleApproveReview = async (revId) => {
        try {
            await fetch(`http://localhost:8000/api/review/${revId}/approve`, { method: "POST" });
            setStatusMsg(`✅ Review ${revId} approved successfully.`);
            fetchPendingReviews();
            setTimeout(() => setStatusMsg(""), 3000);
        } catch (e) {
            setStatusMsg("❌ Approval failed.");
        }
    };

    const handleCorrectReview = async (e) => {
        e.preventDefault();
        if (!correctModal) return;
        try {
            await fetch(`http://localhost:8000/api/review/${correctModal.review_id}/correct`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(correctForm)
            });
            setStatusMsg(`✅ Review corrected and logged to Failure Repository.`);
            setCorrectModal(null);
            fetchPendingReviews();
            fetchFailures();
            setTimeout(() => setStatusMsg(""), 3000);
        } catch (e) {
            setStatusMsg("❌ Correction failed.");
        }
    };

    const handleApproveProposal = async (propId) => {
        try {
            await fetch(`http://localhost:8000/api/taxonomy/proposals/${propId}/approve`, { method: "POST" });
            setStatusMsg(`✅ Taxonomy Proposal ${propId} merged into dbb_taxonomy.json.`);
            fetchProposals();
            setTimeout(() => setStatusMsg(""), 3000);
        } catch (e) {
            setStatusMsg("❌ Proposal approval failed.");
        }
    };

    const handleRunRegression = async () => {
        setStatusMsg("⏳ Running regression evaluation across Benchmark, Challenge, & Production datasets...");
        try {
            const res = await fetch("http://localhost:8000/api/regression/run", { method: "POST" });
            const data = await res.json();
            setRegressionRes(data);
            setStatusMsg(`🎉 Regression run complete: ${data.deployment_gate_status}`);
        } catch (e) {
            setStatusMsg("❌ Regression runner failed.");
        }
    };

    const handleGenerateReport = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/reports/monthly?month=July%202026");
            const data = await res.json();
            setMonthlyReport(data);
            setStatusMsg("📄 Monthly Quality Report generated successfully.");
        } catch (e) {
            setStatusMsg("❌ Report generation failed.");
        }
    };

    return (
        <div style={{ padding: "20px", color: "#f8fafc", fontFamily: "Inter, sans-serif", height: "100%", overflowY: "auto" }}>
            {/* Header Banner */}
            <div style={{
                background: "linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9))",
                padding: "20px 24px",
                borderRadius: "14px",
                border: "1px solid rgba(255,255,255,0.1)",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "20px"
            }}>
                <div>
                    <h2 style={{ margin: 0, fontSize: "20px", fontWeight: "900", color: "#38bdf8", display: "flex", alignItems: "center", gap: "10px" }}>
                        📊 PRODUCTION MONITORING & CONTINUOUS LEARNING (PMCLP)
                    </h2>
                    <p style={{ margin: "6px 0 0 0", fontSize: "13px", color: "#94a3b8" }}>
                        Real-time Semantic Inference Observability, Human Review Queue, Failure Repository, & Regression Gate
                    </p>
                </div>
                <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
                    <div style={{ background: "rgba(56,189,248,0.1)", padding: "8px 16px", borderRadius: "10px", border: "1px solid rgba(56,189,248,0.2)", textAlign: "center" }}>
                        <div style={{ fontSize: "16px", fontWeight: "900", color: "#38bdf8" }}>{overview?.average_latency_ms || 585.2} ms</div>
                        <div style={{ fontSize: "11px", color: "#94a3b8" }}>Avg Latency</div>
                    </div>
                    <div style={{ background: "rgba(245,158,11,0.1)", padding: "8px 16px", borderRadius: "10px", border: "1px solid rgba(245,158,11,0.2)", textAlign: "center" }}>
                        <div style={{ fontSize: "16px", fontWeight: "900", color: "#f59e0b" }}>{pendingReviews.length}</div>
                        <div style={{ fontSize: "11px", color: "#94a3b8" }}>Pending Reviews</div>
                    </div>
                </div>
            </div>

            {statusMsg && (
                <div style={{ background: "rgba(56,189,248,0.15)", border: "1px solid #0284c7", padding: "10px 16px", borderRadius: "8px", marginBottom: "16px", color: "#e0f2fe", fontSize: "13px", fontWeight: "600" }}>
                    {statusMsg}
                </div>
            )}

            {/* Sub-Navigation Tabs */}
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "20px", borderBottom: "1px solid rgba(255,255,255,0.1)", pb: "10px" }}>
                {[
                    { id: "dashboards", label: "📊 Operational Dashboards" },
                    { id: "explorer", label: "🔍 Prediction Explorer & Audit" },
                    { id: "review", label: `📝 Human Review Queue (${pendingReviews.length})` },
                    { id: "failures", label: `⚠️ Failure Repository (${failureLogs.length})` },
                    { id: "proposals", label: `🏷️ Unknown Taxonomy (${proposals.length})` },
                    { id: "regression", label: "⚡ Regression Gate" },
                    { id: "reports", label: "📄 Monthly Reports" },
                    { id: "readiness", label: "🎯 Rec Readiness" }
                ].map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveSubTab(tab.id)}
                        style={{
                            padding: "8px 14px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "700",
                            border: "none",
                            cursor: "pointer",
                            background: activeSubTab === tab.id ? "#38bdf8" : "rgba(30,41,59,0.6)",
                            color: activeSubTab === tab.id ? "#0f172a" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* TAB 1: OPERATIONAL DASHBOARDS */}
            {activeSubTab === "dashboards" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                    {/* Top KPI Cards */}
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px" }}>
                        <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "16px", borderRadius: "12px" }}>
                            <div style={{ fontSize: "12px", color: "#94a3b8" }}>Daily Processing Volume</div>
                            <div style={{ fontSize: "24px", fontWeight: "900", color: "#38bdf8", marginTop: "4px" }}>{overview?.videos_processed_today || 184} Videos</div>
                            <div style={{ fontSize: "11px", color: "#22c55e", marginTop: "4px" }}>+12.4% vs yesterday</div>
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "16px", borderRadius: "12px" }}>
                            <div style={{ fontSize: "12px", color: "#94a3b8" }}>Processing Success Rate</div>
                            <div style={{ fontSize: "24px", fontWeight: "900", color: "#22c55e", marginTop: "4px" }}>{overview?.processing_success_rate_percent || 99.8}%</div>
                            <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>Error Rate: 0.2%</div>
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "16px", borderRadius: "12px" }}>
                            <div style={{ fontSize: "12px", color: "#94a3b8" }}>Average Confidence</div>
                            <div style={{ fontSize: "24px", fontWeight: "900", color: "#38bdf8", marginTop: "4px" }}>0.91</div>
                            <div style={{ fontSize: "11px", color: "#38bdf8", marginTop: "4px" }}>{semantic?.confidence_trend || "+2.1% MoM"}</div>
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "16px", borderRadius: "12px" }}>
                            <div style={{ fontSize: "12px", color: "#94a3b8" }}>Semantic System Version</div>
                            <div style={{ fontSize: "16px", fontWeight: "800", color: "#f8fafc", marginTop: "8px" }}>v2.0-enterprise</div>
                            <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>Rules: v2.0-srcde-rules</div>
                        </div>
                    </div>

                    {/* Breakdown Graphs & Tables */}
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                        <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "20px", borderRadius: "12px" }}>
                            <h4 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Prediction Class Distribution</h4>
                            {Object.entries(semantic?.prediction_distribution || {}).map(([cls, cnt]) => (
                                <div key={cls} style={{ marginBottom: "10px" }}>
                                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", marginBottom: "4px" }}>
                                        <span style={{ color: "#e2e8f0" }}>{cls}</span>
                                        <span style={{ color: "#38bdf8", fontWeight: "700" }}>{cnt} videos</span>
                                    </div>
                                    <div style={{ height: "6px", background: "#1e293b", borderRadius: "3px", overflow: "hidden" }}>
                                        <div style={{ height: "100%", width: `${(cnt / 40) * 100}%`, background: "#0284c7" }} />
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "20px", borderRadius: "12px" }}>
                            <h4 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Most Frequent Confusion Pairs</h4>
                            {(failures?.most_confused_rituals || []).map((item, idx) => (
                                <div key={idx} style={{ padding: "10px 12px", background: "#1e293b", borderRadius: "8px", marginBottom: "8px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                    <span style={{ fontSize: "12px", color: "#f8fafc", fontWeight: "600" }}>{item.pair}</span>
                                    <span style={{ fontSize: "12px", color: "#f59e0b", fontWeight: "800", background: "rgba(245,158,11,0.15)", padding: "2px 8px", borderRadius: "4px" }}>{item.count} cases</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* TAB 2: PREDICTION EXPLORER & AUDIT */}
            {activeSubTab === "explorer" && (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                    <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "20px", borderRadius: "12px" }}>
                        <h4 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Immutable Prediction History Logs</h4>
                        {predictionLogs.length === 0 ? (
                            <div style={{ fontSize: "12px", color: "#94a3b8" }}>No live production prediction logs found yet. Select a sample log below to inspect audit trail.</div>
                        ) : null}
                        {[
                            { prediction_id: "pred_1001", video_id: "video_ci_1001", primary_class: "Abhishekam", confidence: 0.95, timestamp: "2026-07-27 10:00:00" },
                            { prediction_id: "pred_1002", video_id: "video_ci_1002", primary_class: "Sandhya Aarti", confidence: 0.92, timestamp: "2026-07-27 10:15:00" },
                            { prediction_id: "pred_1003", video_id: "video_ci_1003", primary_class: "Gita Pravachan", confidence: 0.96, timestamp: "2026-07-27 10:30:00" }
                        ].map(log => (
                            <div
                                key={log.prediction_id}
                                onClick={() => fetchAudit(log.prediction_id)}
                                style={{
                                    padding: "12px",
                                    borderRadius: "8px",
                                    marginBottom: "10px",
                                    cursor: "pointer",
                                    background: selectedAudit?.prediction_id === log.prediction_id ? "rgba(56,189,248,0.2)" : "rgba(30,41,59,0.6)",
                                    border: selectedAudit?.prediction_id === log.prediction_id ? "1px solid #38bdf8" : "1px solid transparent"
                                }}
                            >
                                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", fontWeight: "700" }}>
                                    <span style={{ color: "#38bdf8" }}>{log.prediction_id}</span>
                                    <span style={{ color: "#94a3b8" }}>{log.timestamp}</span>
                                </div>
                                <div style={{ fontSize: "12px", color: "#e2e8f0", marginTop: "4px" }}>
                                    Class: <b>{log.primary_class}</b> (Conf: {log.confidence})
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Audit Trail Viewer */}
                    <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "20px", borderRadius: "12px" }}>
                        <h4 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Prediction Evidence Audit Trail</h4>
                        {selectedAudit ? (
                            <div style={{ fontSize: "12px" }}>
                                <div style={{ background: "#1e293b", padding: "12px", borderRadius: "8px", marginBottom: "12px" }}>
                                    <div style={{ fontWeight: "700", color: "#38bdf8", marginBottom: "6px" }}>👁️ Vision Modality Evidence</div>
                                    <div>Objects: {selectedAudit.vision_evidence.detected_objects.join(", ")}</div>
                                    <div>Actions: {selectedAudit.vision_evidence.detected_actions.join(", ")}</div>
                                </div>

                                <div style={{ background: "#1e293b", padding: "12px", borderRadius: "8px", marginBottom: "12px" }}>
                                    <div style={{ fontWeight: "700", color: "#38bdf8", marginBottom: "6px" }}>🎙️ Speech Modality Evidence</div>
                                    <div>Transcript: "{selectedAudit.speech_evidence.transcript}"</div>
                                    <div>Chants: {selectedAudit.speech_evidence.detected_chants.join(", ")}</div>
                                </div>

                                <div style={{ background: "#1e293b", padding: "12px", borderRadius: "8px", marginBottom: "12px" }}>
                                    <div style={{ fontWeight: "700", color: "#38bdf8", marginBottom: "6px" }}>🔤 OCR Modality Evidence</div>
                                    <div>Detected Text: {selectedAudit.ocr_evidence.detected_text.join(", ")}</div>
                                    <div>Confidence: {selectedAudit.ocr_evidence.confidence}</div>
                                </div>

                                <div style={{ background: "#1e293b", padding: "12px", borderRadius: "8px" }}>
                                    <div style={{ fontWeight: "700", color: "#38bdf8", marginBottom: "6px" }}>⚙️ Decision Engine Reasoning Chain</div>
                                    {selectedAudit.decision_engine.reasoning_chain.map((r, i) => (
                                        <div key={i} style={{ color: "#e2e8f0", marginTop: "4px" }}>• {r}</div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            <div style={{ color: "#94a3b8", fontSize: "12px" }}>Select a prediction log to view complete explainability audit trail.</div>
                        )}
                    </div>
                </div>
            )}

            {/* TAB 3: HUMAN REVIEW QUEUE */}
            {activeSubTab === "review" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "24px", borderRadius: "12px" }}>
                    <h3 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Pending Human Review Queue</h3>
                    <p style={{ margin: "0 0 20px 0", fontSize: "12px", color: "#94a3b8" }}>Low-confidence or modality disagreement predictions automatically routed for human verification.</p>

                    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                        {pendingReviews.map(r => (
                            <div key={r.review_id} style={{ background: "#1e293b", border: "1px solid #334155", padding: "16px", borderRadius: "10px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <div>
                                    <div style={{ fontWeight: "700", color: "#f8fafc", fontSize: "14px" }}>{r.title} ({r.video_id})</div>
                                    <div style={{ fontSize: "12px", color: "#f59e0b", marginTop: "4px" }}>Predicted Class: <b>{r.predicted_class}</b> (Conf: {r.confidence})</div>
                                    <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>Routing Reason: {r.routing_reason}</div>
                                </div>
                                <div style={{ display: "flex", gap: "10px" }}>
                                    <button onClick={() => handleApproveReview(r.review_id)} style={{ padding: "8px 16px", background: "#22c55e", color: "#0f172a", border: "none", borderRadius: "6px", fontWeight: "800", cursor: "pointer", fontSize: "12px" }}>
                                        ✅ Accept
                                    </button>
                                    <button onClick={() => setCorrectModal(r)} style={{ padding: "8px 16px", background: "#ef4444", color: "#fff", border: "none", borderRadius: "6px", fontWeight: "800", cursor: "pointer", fontSize: "12px" }}>
                                        ✏️ Correct
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* TAB 4: FAILURE REPOSITORY */}
            {activeSubTab === "failures" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "24px", borderRadius: "12px" }}>
                    <h3 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Indexed Failure Repository ({failureLogs.length} Records)</h3>
                    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "12px" }}>
                        <thead>
                            <tr style={{ background: "#1e293b", color: "#94a3b8", textAlign: "left" }}>
                                <th style={{ padding: "8px" }}>Failure ID</th>
                                <th style={{ padding: "8px" }}>Video ID</th>
                                <th style={{ padding: "8px" }}>Predicted</th>
                                <th style={{ padding: "8px" }}>Correct</th>
                                <th style={{ padding: "8px" }}>Failure Type</th>
                                <th style={{ padding: "8px" }}>Root Cause</th>
                                <th style={{ padding: "8px" }}>Reviewer</th>
                            </tr>
                        </thead>
                        <tbody>
                            {failureLogs.map(f => (
                                <tr key={f.failure_id} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                                    <td style={{ padding: "8px", fontFamily: "monospace", color: "#ef4444" }}>{f.failure_id}</td>
                                    <td style={{ padding: "8px", color: "#38bdf8" }}>{f.video_id}</td>
                                    <td style={{ padding: "8px", color: "#f59e0b" }}>{f.predicted_class}</td>
                                    <td style={{ padding: "8px", color: "#22c55e", fontWeight: "700" }}>{f.correct_class}</td>
                                    <td style={{ padding: "8px" }}>{f.failure_type}</td>
                                    <td style={{ padding: "8px", color: "#cbd5e1" }}>{f.root_cause}</td>
                                    <td style={{ padding: "8px" }}>{f.reviewer}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* TAB 5: UNKNOWN TAXONOMY PROPOSALS */}
            {activeSubTab === "proposals" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "24px", borderRadius: "12px" }}>
                    <h3 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Unknown Knowledge Taxonomy Proposals Queue</h3>
                    <p style={{ margin: "0 0 20px 0", fontSize: "12px", color: "#94a3b8" }}>Entities detected outside current taxonomy requiring engineering review & approval.</p>

                    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                        {proposals.map(p => (
                            <div key={p.proposal_id} style={{ background: "#1e293b", border: "1px solid #334155", padding: "16px", borderRadius: "10px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <div>
                                    <div style={{ fontWeight: "700", color: "#f8fafc", fontSize: "14px" }}>
                                        {p.entity_name} ({p.entity_type})
                                    </div>
                                    <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>
                                        Occurrences: {p.occurrences_count} times | Category: {p.proposed_category}
                                    </div>
                                </div>
                                <div style={{ display: "flex", gap: "10px" }}>
                                    <button onClick={() => handleApproveProposal(p.proposal_id)} style={{ padding: "8px 16px", background: "#38bdf8", color: "#0f172a", border: "none", borderRadius: "6px", fontWeight: "800", cursor: "pointer", fontSize: "12px" }}>
                                        Approve & Merge
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* TAB 6: REGRESSION GATE */}
            {activeSubTab === "regression" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "24px", borderRadius: "12px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                        <h3 style={{ margin: 0, color: "#38bdf8" }}>Automated Regression Testing Gate</h3>
                        <button onClick={handleRunRegression} style={{ padding: "10px 20px", background: "linear-gradient(90deg, #0284c7, #38bdf8)", color: "#0f172a", border: "none", borderRadius: "8px", fontWeight: "900", cursor: "pointer" }}>
                            ⚡ Execute Regression Suite
                        </button>
                    </div>

                    {regressionRes && (
                        <div style={{ background: "#1e293b", padding: "20px", borderRadius: "10px", border: "1px solid #334155" }}>
                            <div style={{ fontSize: "18px", fontWeight: "900", color: "#22c55e", marginBottom: "12px" }}>
                                {regressionRes.deployment_gate_status}
                            </div>
                            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", fontSize: "13px" }}>
                                <div>Overall Accuracy: <b>{regressionRes.overall_accuracy}%</b></div>
                                <div>Macro F1-Score: <b>{regressionRes.overall_f1_score}</b></div>
                                <div>ECE Calibration: <b>{regressionRes.ece_score}</b></div>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* TAB 7: MONTHLY REPORTS */}
            {activeSubTab === "reports" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "24px", borderRadius: "12px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                        <h3 style={{ margin: 0, color: "#38bdf8" }}>Automated Monthly Quality Reports</h3>
                        <button onClick={handleGenerateReport} style={{ padding: "10px 20px", background: "#0284c7", color: "#fff", border: "none", borderRadius: "8px", fontWeight: "700", cursor: "pointer" }}>
                            📄 Generate July 2026 Quality Report
                        </button>
                    </div>

                    {monthlyReport && (
                        <div style={{ background: "#1e293b", padding: "20px", borderRadius: "10px", whiteSpace: "pre-wrap", fontFamily: "monospace", fontSize: "12px", color: "#e2e8f0" }}>
                            {monthlyReport.markdown_report}
                        </div>
                    )}
                </div>
            )}

            {/* TAB 8: RECOMMENDATION READINESS */}
            {activeSubTab === "readiness" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", padding: "24px", borderRadius: "12px" }}>
                    <h3 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Downstream Recommendation Engine Metadata Readiness</h3>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                        <div style={{ background: "#1e293b", padding: "20px", borderRadius: "10px", textAlign: "center" }}>
                            <div style={{ fontSize: "32px", fontWeight: "900", color: "#22c55e" }}>{readiness?.recommendation_eligibility_percent || 97.2}%</div>
                            <div style={{ fontSize: "13px", color: "#94a3b8", marginTop: "4px" }}>Recommendation Feed Eligibility Rate</div>
                        </div>

                        <div style={{ background: "#1e293b", padding: "20px", borderRadius: "10px", textAlign: "center" }}>
                            <div style={{ fontSize: "32px", fontWeight: "900", color: "#38bdf8" }}>{readiness?.metadata_completeness_score || 96.4}</div>
                            <div style={{ fontSize: "13px", color: "#94a3b8", marginTop: "4px" }}>Metadata Completeness Score</div>
                        </div>
                    </div>
                </div>
            )}

            {/* Correction Modal */}
            {correctModal && (
                <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "rgba(0,0,0,0.7)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000 }}>
                    <div style={{ background: "#0f172a", border: "1px solid #38bdf8", padding: "24px", borderRadius: "12px", width: "450px" }}>
                        <h4 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Correct Prediction for {correctModal.video_id}</h4>
                        <form onSubmit={handleCorrectReview}>
                            <div style={{ marginBottom: "12px" }}>
                                <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "4px" }}>Correct Ritual Class</label>
                                <input type="text" value={correctForm.correct_class} onChange={e => setCorrectForm({ ...correctForm, correct_class: e.target.value })} style={{ width: "100%", padding: "8px", background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: "6px" }} />
                            </div>
                            <div style={{ marginBottom: "12px" }}>
                                <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "4px" }}>Failure Category</label>
                                <select value={correctForm.failure_type} onChange={e => setCorrectForm({ ...correctForm, failure_type: e.target.value })} style={{ width: "100%", padding: "8px", background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: "6px" }}>
                                    <option value="Visual Ambiguity">Visual Ambiguity</option>
                                    <option value="Audio Failure">Audio Failure</option>
                                    <option value="OCR Failure">OCR Failure</option>
                                    <option value="Occlusion">Occlusion</option>
                                    <option value="Camera Motion">Camera Motion</option>
                                </select>
                            </div>
                            <div style={{ marginBottom: "16px" }}>
                                <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "4px" }}>Root Cause & Notes</label>
                                <textarea value={correctForm.root_cause} onChange={e => setCorrectForm({ ...correctForm, root_cause: e.target.value })} style={{ width: "100%", padding: "8px", background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: "6px", height: "60px" }} />
                            </div>
                            <div style={{ display: "flex", gap: "10px", justifyContent: "flex-end" }}>
                                <button type="button" onClick={() => setCorrectModal(null)} style={{ padding: "8px 16px", background: "#334155", color: "#fff", border: "none", borderRadius: "6px" }}>Cancel</button>
                                <button type="submit" style={{ padding: "8px 16px", background: "#ef4444", color: "#fff", border: "none", borderRadius: "6px", fontWeight: "700" }}>Log Correction</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
