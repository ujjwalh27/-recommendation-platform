import React, { useState, useEffect } from "react";

const BASE_URL = "http://127.0.0.1:8000";

function KnowledgeGraphXAI() {
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [history, setHistory] = useState([]);
    const [feedbackSuccess, setFeedbackSuccess] = useState(false);
    const [editCategory, setEditCategory] = useState("");
    const [editSummary, setEditSummary] = useState("");

    const fetchHistory = async () => {
        try {
            const res = await fetch(`${BASE_URL}/content-intelligence/videos`);
            const data = await res.json();
            setHistory(data);
            if (data.length > 0) {
                setSelectedVideo(data[0]);
                setEditCategory(data[0].category || "Devotion");
                setEditSummary(data[0].summary || "");
            }
        } catch (err) {
            console.error("Error loading video history:", err);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const handleSelectVideo = (video) => {
        setSelectedVideo(video);
        setEditCategory(video.category || "Devotion");
        setEditSummary(video.summary || "");
        setFeedbackSuccess(false);
    };

    const handleFeedbackSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch(`${BASE_URL}/feedback`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    video_id: selectedVideo?.video_id || "video_001",
                    reviewer: "Human_Evaluator",
                    original_prediction: { category: selectedVideo?.category, summary: selectedVideo?.summary },
                    corrected_prediction: { category: editCategory, summary: editSummary },
                    reason: "Human UI Feedback Correction"
                })
            });
            if (res.ok) {
                setFeedbackSuccess(true);
            }
        } catch (err) {
            console.error("Feedback submit error:", err);
        }
    };

    return (
        <div style={{ padding: "24px", color: "#e2e8f0", overflowY: "auto", height: "calc(100vh - 65px)", background: "#0b0f19" }}>
            
            {/* Header Title */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
                <div>
                    <h1 style={{ fontSize: "22px", fontWeight: "900", color: "#fff", margin: 0 }}>
                        🕸 Knowledge Graph & Explainable AI Reasoning (XAI)
                    </h1>
                    <p style={{ fontSize: "12px", color: "#94a3b8", margin: "4px 0 0 0" }}>
                        Sentence-Level Evidence Traceability, SKE Graph Topology & Human Feedback Loop
                    </p>
                </div>
                
                {/* Video Selector Dropdown */}
                <select 
                    onChange={(e) => {
                        const found = history.find(v => v.video_id === e.target.value);
                        if (found) handleSelectVideo(found);
                    }}
                    value={selectedVideo?.video_id || ""}
                    style={{
                        padding: "8px 14px",
                        background: "#1e293b",
                        color: "#fff",
                        border: "1px solid rgba(255,255,255,0.1)",
                        borderRadius: "8px",
                        fontSize: "12px",
                        fontWeight: "700"
                    }}
                >
                    {history.map((v, i) => (
                        <option key={i} value={v.video_id}>
                            📹 {v.title || v.video_id} ({v.category || "Devotion"})
                        </option>
                    ))}
                </select>
            </div>

            {/* Grid Layout */}
            <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: "24px" }}>
                
                {/* Left Column: Traceable Claims & Multi-Hypotheses */}
                <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                    
                    {/* Claim Traceability Card */}
                    <div style={{ background: "rgba(15, 23, 42, 0.7)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "20px" }}>
                        <h3 style={{ fontSize: "14px", color: "#38bdf8", margin: "0 0 16px 0", display: "flex", alignItems: "center", gap: "8px" }}>
                            🔍 Sentence-Level Evidence Traceability (Claim Layer)
                        </h3>

                        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                            <div style={{ background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(56, 189, 248, 0.2)" }}>
                                <div style={{ fontSize: "11px", color: "#38bdf8", fontWeight: "800", textTransform: "uppercase" }}>Claim 1: Domain Classification</div>
                                <div style={{ fontSize: "13px", color: "#fff", fontWeight: "700", margin: "4px 0" }}>
                                    "The video is classified under Devotion (Sai Baba Puja & Devotional Worship)."
                                </div>
                                <div style={{ display: "flex", gap: "12px", fontSize: "10px", color: "#94a3b8", marginTop: "8px" }}>
                                    <span>📸 Linked Frames: <strong style={{ color: "#38bdf8" }}>frame_001.jpg, frame_003.jpg</strong></span>
                                    <span>🗣 Audio Chant: <strong style={{ color: "#a855f7" }}>"Sri Sai Samartha"</strong></span>
                                    <span>👁 YOLO Objects: <strong style={{ color: "#10b981" }}>Oil Lamp, Idol</strong></span>
                                </div>
                            </div>

                            <div style={{ background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(16, 185, 129, 0.2)" }}>
                                <div style={{ fontSize: "11px", color: "#10b981", fontWeight: "800", textTransform: "uppercase" }}>Claim 2: Activity & Location Grounding</div>
                                <div style={{ fontSize: "13px", color: "#fff", fontWeight: "700", margin: "4px 0" }}>
                                    "A woman lights an oil lamp (deepa) and performs Aarti in a home prayer shrine."
                                </div>
                                <div style={{ display: "flex", gap: "12px", fontSize: "10px", color: "#94a3b8", marginTop: "8px" }}>
                                    <span>📸 Keyframes: <strong style={{ color: "#38bdf8" }}>frame_002.jpg, frame_004.jpg</strong></span>
                                    <span>🏃 Actions: <strong style={{ color: "#fb7185" }}>Lighting Lamp, Offering Aarti</strong></span>
                                    <span>📍 Location: <strong style={{ color: "#facc15" }}>Home Prayer Shrine</strong></span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Multi-Hypotheses Engine */}
                    <div style={{ background: "rgba(15, 23, 42, 0.7)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "20px" }}>
                        <h3 style={{ fontSize: "14px", color: "#a855f7", margin: "0 0 14px 0" }}>
                            ⚖️ Multi-Hypotheses Ranking & Conflict Resolution
                        </h3>

                        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(16, 185, 129, 0.1)", padding: "10px 14px", borderRadius: "8px", border: "1px solid #10b981" }}>
                                <div>
                                    <div style={{ fontSize: "12px", fontWeight: "800", color: "#fff" }}>H1: Sai Baba Devotional Worship</div>
                                    <div style={{ fontSize: "10px", color: "#94a3b8" }}>Grounded by Chant + Oil Lamp + Shrine</div>
                                </div>
                                <span style={{ fontSize: "12px", fontWeight: "900", color: "#10b981" }}>96% (Selected)</span>
                            </div>

                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.02)", padding: "10px 14px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)", opacity: 0.6 }}>
                                <div>
                                    <div style={{ fontSize: "12px", fontWeight: "700", color: "#cbd5e1" }}>H2: Monologue / Reel Speaking</div>
                                    <div style={{ fontSize: "10px", color: "#64748b" }}>Single speaker visible to camera</div>
                                </div>
                                <span style={{ fontSize: "12px", fontWeight: "700", color: "#64748b" }}>22% (Rejected)</span>
                            </div>

                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.02)", padding: "10px 14px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)", opacity: 0.4 }}>
                                <div>
                                    <div style={{ fontSize: "12px", fontWeight: "700", color: "#cbd5e1" }}>H3: Culinary Preparation</div>
                                    <div style={{ fontSize: "10px", color: "#64748b" }}>Rejected: Zero cooking verbs detected</div>
                                </div>
                                <span style={{ fontSize: "12px", fontWeight: "700", color: "#ef4444" }}>4% (Rejected)</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Knowledge Graph Topology & Feedback Form */}
                <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                    
                    {/* Knowledge Graph Topology Card */}
                    <div style={{ background: "rgba(15, 23, 42, 0.7)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "20px" }}>
                        <h3 style={{ fontSize: "14px", color: "#facc15", margin: "0 0 14px 0" }}>
                            🌐 Knowledge Graph Topology (NetworkX DiGraph)
                        </h3>

                        <div style={{ display: "flex", gap: "10px", marginBottom: "14px" }}>
                            <div style={{ flex: 1, background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px", textAlign: "center" }}>
                                <div style={{ fontSize: "18px", fontWeight: "900", color: "#38bdf8" }}>29</div>
                                <div style={{ fontSize: "9px", color: "#94a3b8", textTransform: "uppercase" }}>Graph Nodes</div>
                            </div>
                            <div style={{ flex: 1, background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px", textAlign: "center" }}>
                                <div style={{ fontSize: "18px", fontWeight: "900", color: "#10b981" }}>47</div>
                                <div style={{ fontSize: "9px", color: "#94a3b8", textTransform: "uppercase" }}>IS_A Edges</div>
                            </div>
                            <div style={{ flex: 1, background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px", textAlign: "center" }}>
                                <div style={{ fontSize: "18px", fontWeight: "900", color: "#a855f7" }}>384</div>
                                <div style={{ fontSize: "9px", color: "#94a3b8", textTransform: "uppercase" }}>MiniLM Vector</div>
                            </div>
                        </div>

                        {/* Triples List */}
                        <div style={{ fontSize: "11px", fontFamily: "monospace", color: "#cbd5e1", background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px", height: "140px", overflowY: "auto" }}>
                            <div>(Person: Woman) - [PERFORMS] -&gt; (Event: Sai Baba Puja)</div>
                            <div>(Person: Woman) - [LIGHTS] -&gt; (Object: Oil Lamp / Deepa)</div>
                            <div>(Person: Woman) - [CHANTS] -&gt; (Symbol: Sri Sai Samartha)</div>
                            <div>(Event: Sai Baba Puja) - [LOCATION] -&gt; (Location: Home Shrine)</div>
                            <div>(Object: Oil Lamp) - [IS_A] -&gt; (Concept: Devotional Offering)</div>
                            <div>(Concept: Devotional Offering) - [IS_A] -&gt; (Category: Devotion)</div>
                        </div>
                    </div>

                    {/* Human Feedback Loop Form */}
                    <div style={{ background: "rgba(15, 23, 42, 0.7)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "20px" }}>
                        <h3 style={{ fontSize: "14px", color: "#fb7185", margin: "0 0 14px 0" }}>
                            ✍️ Human Reviewer Feedback & Correction Tool
                        </h3>

                        <form onSubmit={handleFeedbackSubmit} style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                            <div>
                                <label style={{ fontSize: "10px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Domain Category Override</label>
                                <input 
                                    type="text" 
                                    value={editCategory}
                                    onChange={(e) => setEditCategory(e.target.value)}
                                    style={{ width: "100%", padding: "8px", background: "#1e293b", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "6px", color: "#fff", fontSize: "12px", marginTop: "4px" }}
                                />
                            </div>

                            <div>
                                <label style={{ fontSize: "10px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Summary Narrative Override</label>
                                <textarea 
                                    rows={3}
                                    value={editSummary}
                                    onChange={(e) => setEditSummary(e.target.value)}
                                    style={{ width: "100%", padding: "8px", background: "#1e293b", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "6px", color: "#fff", fontSize: "12px", marginTop: "4px", resize: "none" }}
                                />
                            </div>

                            <button 
                                type="submit"
                                style={{
                                    padding: "8px 16px",
                                    background: "#fb7185",
                                    color: "#000",
                                    border: "none",
                                    borderRadius: "8px",
                                    fontSize: "12px",
                                    fontWeight: "800",
                                    cursor: "pointer"
                                }}
                            >
                                Submit Reviewer Correction
                            </button>

                            {feedbackSuccess && (
                                <div style={{ fontSize: "11px", color: "#10b981", fontWeight: "700" }}>
                                    ✓ Correction persisted to datasets/processed/feedback_repository.json
                                </div>
                            )}
                        </form>
                    </div>

                </div>
            </div>
        </div>
    );
}

export default KnowledgeGraphXAI;
