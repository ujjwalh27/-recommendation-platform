import React, { useState, useEffect } from "react";

const BASE_URL = "http://localhost:8000";

function ContentIntelligence() {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [progressLogs, setProgressLogs] = useState([]);
    const [currentStage, setCurrentStage] = useState("");
    const [analysisResult, setAnalysisResult] = useState(null);
    const [history, setHistory] = useState([]);
    const [activeDetailTab, setActiveDetailTab] = useState("reasoning");

    const renderGroundingBadge = (field) => {
        if (!analysisResult || !analysisResult.provenance_report) return null;
        const pData = analysisResult.provenance_report[field];
        if (!pData) return null;
        const status = pData.hallucination_classification;
        
        let color = "#10b981"; // supported (green)
        let bg = "rgba(16, 185, 129, 0.1)";
        let text = "Grounded";
        
        if (status === "Unsupported") {
            color = "#ef4444"; // unsupported (red)
            bg = "rgba(239, 68, 68, 0.1)";
            text = "Unsupported";
        } else if (status === "Partially Supported") {
            color = "#f59e0b"; // partially supported (yellow)
            bg = "rgba(245, 158, 11, 0.1)";
            text = "Inferred";
        }
        
        return (
            <span style={{
                fontSize: "8px",
                padding: "2px 6px",
                borderRadius: "4px",
                fontWeight: "800",
                background: bg,
                color: color,
                marginLeft: "8px",
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                border: `1px solid ${color}44`,
                display: "inline-block",
                verticalAlign: "middle"
            }} title={`${text} - Reason: ${pData.reason} (Derived from: ${pData.derived_from?.join(', ') || 'N/A'})`}>
                {text}
            </span>
        );
    };

    // Fetch previously analyzed videos
    const fetchHistory = async () => {
        try {
            const res = await fetch(`${BASE_URL}/content-intelligence/videos`);
            const data = await res.json();
            // Sort by timestamp descending if available
            setHistory(data.reverse());
        } catch (err) {
            console.error("Failed to load analyzed history:", err);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setAnalysisResult(null);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setUploading(true);
        setAnalysisResult(null);
        setCurrentStage("Uploading file to server...");
        setProgressLogs(["[Upload] Uploading raw mp4 file..."]);

        const formData = new FormData();
        formData.append("file", file);

        // Simple mock logger progression during pipeline running
        const mockLogTimer = setInterval(() => {
            setProgressLogs(prev => {
                if (prev.length === 1) {
                    setCurrentStage("Extracting audio WAV track...");
                    return [...prev, "[Audio] Running ffmpeg extraction..."];
                } else if (prev.length === 2) {
                    setCurrentStage("Transcribing speech...");
                    return [...prev, "[Whisper] Analyzing audio spectrum...", "[Whisper] Decoding phonemes..."];
                } else if (prev.length === 4) {
                    setCurrentStage("OCR text reading...");
                    return [...prev, "[EasyOCR] Scanning frames at key intervals..."];
                } else if (prev.length === 5) {
                    setCurrentStage("YOLO object detection...");
                    return [...prev, "[YOLOv11] Classifying frame bounding boxes..."];
                } else if (prev.length === 6) {
                    setCurrentStage("Action and Scene recognition...");
                    return [...prev, "[CLIP] Analyzing zero-shot scene environment...", "[VideoMAE] Parsing kinetic motions..."];
                } else if (prev.length === 8) {
                    setCurrentStage("Ollama Metadata Fusion...");
                    return [...prev, "[MiniCPM-V 4.5] Synthesizing vision tags, summaries, and title..."];
                } else if (prev.length === 9) {
                    setCurrentStage("Evaluating visual grounding...");
                    return [...prev, "[Pipeline] Evaluating visual tags against grounding models..."];
                } else if (prev.length === 10) {
                    setCurrentStage("Filtering hallucinations...");
                    return [...prev, "[Pipeline] Flagging out unsupported metadata hallucinations..."];
                } else if (prev.length === 11) {
                    setCurrentStage("Building embedding text...");
                    return [...prev, "[Pipeline] Building validated embedding text..."];
                } else if (prev.length === 12) {
                    setCurrentStage("Generating vector embedding...");
                    return [...prev, "[Pipeline] Generating vector embedding on MiniLM..."];
                } else if (prev.length === 13) {
                    setCurrentStage("Finalizing indexing report...");
                    return [...prev, "[Pipeline] Finalizing database record indexing..."];
                }
                return prev;
            });
        }, 3200);

        try {
            const res = await fetch(`${BASE_URL}/content-intelligence/analyze`, {
                method: "POST",
                body: formData
            });

            clearInterval(mockLogTimer);

            if (!res.ok) {
                throw new Error("Pipeline execution failed.");
            }

            const result = await res.json();
            setAnalysisResult(result);
            setCurrentStage("Analysis Complete!");
            setProgressLogs(prev => [...prev, "[Pipeline] Completed. Catalog & Recommendation Feed Synchronized!"]);
            fetchHistory();
            window.dispatchEvent(new CustomEvent("catalog_updated"));
        } catch (err) {
            clearInterval(mockLogTimer);
            setCurrentStage("Error running pipeline");
            setProgressLogs(prev => [...prev, `[Error] ${err.message}`]);
        } finally {
            setUploading(false);
        }
    };

    const selectHistoryItem = (item) => {
        setAnalysisResult(item);
    };

    return (
        <div className="dashboard-container" style={{ overflowY: "auto", paddingBottom: "40px" }}>
            <div className="feed-column" style={{ maxWidth: "100%", width: "100%", flex: "none" }}>
                <div className="feed-header-row">
                    <div className="feed-title">
                        <h1>Content Intelligence Center</h1>
                        <p>Zero-Metadata Local Multimodal Analysis & Dynamic Recommender Seeding</p>
                    </div>
                </div>

                {/* Main Action Grid */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1.5fr", gap: "24px", marginTop: "20px" }}>
                    
                    {/* Left Column: Upload / Progress / History */}
                    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
                        
                        {/* Upload Card */}
                        <div className="dashboard-widget-card" style={{ padding: "20px" }}>
                            <h3 style={{ display: "flex", alignItems: "center", margin: "0 0 16px 0", color: "#38bdf8" }}>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ width: "18px", height: "18px", marginRight: "8px" }}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
                                Upload Video File
                            </h3>
                            <form onSubmit={handleUpload} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                                <div style={{
                                    border: "2px dashed rgba(56, 189, 248, 0.3)",
                                    borderRadius: "12px",
                                    padding: "30px 16px",
                                    textAlign: "center",
                                    background: "rgba(0,0,0,0.2)",
                                    cursor: "pointer",
                                    transition: "all 0.2s"
                                }}
                                onClick={() => document.getElementById("video-file-input").click()}
                                >
                                    <input 
                                        type="file" 
                                        id="video-file-input" 
                                        accept="video/mp4" 
                                        onChange={handleFileChange} 
                                        style={{ display: "none" }}
                                    />
                                    <div style={{ fontSize: "32px", marginBottom: "8px" }}>🎬</div>
                                    <span style={{ fontSize: "13px", color: file ? "#fff" : "#94a3b8", fontWeight: "700" }}>
                                        {file ? file.name : "Drag & Drop MP4 or Click to Browse"}
                                    </span>
                                    {file && <div style={{ fontSize: "11px", color: "#38bdf8", marginTop: "4px" }}>{(file.size / (1024*1024)).toFixed(2)} MB</div>}
                                </div>

                                <button 
                                    type="submit" 
                                    disabled={!file || uploading} 
                                    className="reels-nav-btn" 
                                    style={{
                                        position: "static", 
                                        width: "100%", 
                                        height: "42px", 
                                        background: (!file || uploading) ? "rgba(255,255,255,0.05)" : "var(--accent)",
                                        color: (!file || uploading) ? "#475569" : "#000",
                                        fontWeight: "800",
                                        borderRadius: "10px",
                                        cursor: (!file || uploading) ? "not-allowed" : "pointer"
                                    }}
                                >
                                    {uploading ? "Analyzing Pipeline..." : "Launch Analysis Pipeline"}
                                </button>
                            </form>
                        </div>

                        {/* Logs widget */}
                        {(uploading || progressLogs.length > 0) && (
                            <div className="dashboard-widget-card" style={{ padding: "20px", display: "flex", flexDirection: "column", height: "260px" }}>
                                <h3 style={{ display: "flex", alignItems: "center", margin: "0 0 10px 0", fontSize: "14px", color: "var(--accent)" }}>
                                    <span className="ping-dot" style={{ display: uploading ? "inline-block" : "none", width: "8px", height: "8px", borderRadius: "50%", background: "#10b981", marginRight: "8px", animation: "ping-fade 1.5s infinite" }}></span>
                                    Pipeline Activity Console
                                </h3>
                                <div style={{ fontSize: "12px", color: "#38bdf8", marginBottom: "8px", fontWeight: "700" }}>{currentStage}</div>
                                <div style={{
                                    flex: 1, 
                                    background: "rgba(0,0,0,0.3)", 
                                    borderRadius: "8px", 
                                    padding: "10px", 
                                    overflowY: "auto", 
                                    fontFamily: "monospace",
                                    fontSize: "11px",
                                    color: "#e2e8f0"
                                }}>
                                    {progressLogs.map((log, i) => (
                                        <div key={i} style={{ marginBottom: "4px" }}>
                                            <span style={{ color: "#a855f7" }}>[Pipeline]</span> {log}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* History widget */}
                        <div className="dashboard-widget-card" style={{ padding: "20px", flex: 1 }}>
                            <h3 style={{ display: "flex", alignItems: "center", margin: "0 0 12px 0", color: "#94a3b8" }}>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ width: "16px", height: "16px", marginRight: "8px" }}><path d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>
                                Catalog Seeding History
                            </h3>
                            <div style={{ display: "flex", flexDirection: "column", gap: "8px", overflowY: "auto", maxHeight: "300px" }}>
                                {history.length === 0 ? (
                                    <div style={{ color: "#475569", fontStyle: "italic", fontSize: "12px" }}>No clips uploaded yet.</div>
                                ) : (
                                    history.map((item, idx) => (
                                        <div 
                                            key={idx} 
                                            onClick={() => selectHistoryItem(item)}
                                            style={{
                                                display: "flex",
                                                alignItems: "center",
                                                gap: "10px",
                                                padding: "8px 12px",
                                                background: analysisResult?.video_id === item.video_id ? "rgba(56, 189, 248, 0.12)" : "rgba(255,255,255,0.02)",
                                                border: analysisResult?.video_id === item.video_id ? "1px solid var(--accent)" : "1px solid rgba(255,255,255,0.05)",
                                                borderRadius: "8px",
                                                cursor: "pointer",
                                                transition: "all 0.15s"
                                            }}
                                        >
                                            <div style={{ width: "32px", height: "32px", background: "#1e1b4b", borderRadius: "6px", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--accent)" }}>
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                                    <polygon points="23 7 16 12 23 17 23 7"/>
                                                    <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                                                </svg>
                                            </div>
                                            <div style={{ flex: 1, minWidth: 0 }}>
                                                <div style={{ color: "#fff", fontSize: "12px", fontWeight: "700", textOverflow: "ellipsis", overflow: "hidden", whiteSpace: "nowrap" }}>
                                                    {item.title || f`Clip ${item.video_id}`}
                                                </div>
                                                <div style={{ color: "#64748b", fontSize: "10px" }}>ID: {item.video_id} • Score: {(item.confidence*100).toFixed(0)}%</div>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>

                    </div>

                    {/* Right Column: Active Video Analysis Telemetry */}
                    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
                        {analysisResult ? (
                            <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
                                
                                {/* Video Preview & Fused Info Widget */}
                                <div className="dashboard-widget-card" style={{ padding: "20px" }}>
                                    <h3 style={{ display: "flex", alignItems: "center", margin: "0 0 16px 0", color: "var(--accent)" }}>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ width: "18px", height: "18px", marginRight: "8px" }}><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
                                        Multimodal Fused Metadata Report
                                    </h3>
                                    
                                    <div style={{ display: "flex", gap: "20px", alignItems: "flex-start" }}>
                                        {/* HTML5 video preview player & confidence meters */}
                                        <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "200px", flexShrink: 0 }}>
                                            <video 
                                                src={`${BASE_URL}/videos/${analysisResult.video_id}.mp4`}
                                                controls 
                                                style={{
                                                    width: "100%", 
                                                    borderRadius: "10px", 
                                                    border: "1px solid rgba(255,255,255,0.08)",
                                                    background: "#000"
                                                }}
                                            />
                                            {/* Confidence Scores Grid */}
                                            <div style={{ background: "rgba(0,0,0,0.2)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                <div style={{ fontSize: "10px", color: "var(--accent)", fontWeight: "800", textTransform: "uppercase", marginBottom: "8px" }}>Model Confidence</div>
                                                <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                                                    {Object.entries(
                                                        typeof analysisResult.confidence === "object" ? analysisResult.confidence : {
                                                            speech: analysisResult.confidence || 0.8,
                                                            ocr: 0.7,
                                                            objects: 0.8,
                                                            scenes: 0.9,
                                                            actions: 0.75,
                                                            audio_events: 0.8
                                                        }
                                                    ).map(([model, val]) => (
                                                        <div key={model} style={{ fontSize: "9px" }}>
                                                            <div style={{ display: "flex", justifyContent: "space-between", color: "#cbd5e1", marginBottom: "2px" }}>
                                                                <span style={{ textTransform: "capitalize" }}>{model}</span>
                                                                <span>{((val || 0) * 100).toFixed(0)}%</span>
                                                            </div>
                                                            <div style={{ width: "100%", height: "3px", background: "rgba(255,255,255,0.1)", borderRadius: "2px", overflow: "hidden" }}>
                                                                <div style={{ width: `${(val || 0) * 100}%`, height: "100%", background: "var(--accent)" }}></div>
                                                            </div>
                                                        </div>
                                                    ))}
                                                    <div style={{ fontSize: "10px", borderTop: "1px solid rgba(255,255,255,0.1)", paddingTop: "6px", marginTop: "4px", display: "flex", justifyContent: "space-between", color: "#fff", fontWeight: "700" }}>
                                                        <span>Overall</span>
                                                        <span>{((analysisResult.overall_confidence || analysisResult.confidence || 0.85) * (typeof analysisResult.confidence === "object" ? 100 : 100)).toFixed(0)}%</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "8px" }}>
                                            <div style={{ fontSize: "10px", color: "var(--accent)", fontWeight: "800", textTransform: "uppercase" }}>
                                                AI Generated Title {renderGroundingBadge("title")}
                                            </div>
                                            <div style={{ fontSize: "17px", fontWeight: "800", color: "#fff", letterSpacing: "-0.5px" }}>{analysisResult.title}</div>
                                            
                                            <div style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "800", textTransform: "uppercase", marginTop: "4px" }}>
                                                AI Generated Summary {renderGroundingBadge("summary")}
                                            </div>
                                            <div style={{ fontSize: "12.5px", color: "#cbd5e1", lineHeight: "1.4" }}>{analysisResult.summary}</div>
                                            
                                            {/* CMREE Canonical Semantic Intelligence Box */}
                                             <div style={{
                                                 background: "linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%)",
                                                 padding: "12px",
                                                 borderRadius: "8px",
                                                 border: "1px solid rgba(56, 189, 248, 0.25)",
                                                 margin: "8px 0"
                                             }}>
                                                 <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                                                     <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "10px", color: "var(--accent)", fontWeight: "900", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                                                         <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                                             <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                                                         </svg>
                                                         CMREE Canonical Semantic Intelligence
                                                     </div>
                                                     <span style={{ fontSize: "9px", padding: "2px 6px", background: "rgba(16, 185, 129, 0.2)", color: "#34d399", borderRadius: "4px", fontWeight: "800" }}>
                                                         Rule Confidence: {((analysisResult.cmree_confidence || analysisResult.canonical_metadata?.confidence || 0.95) * 100).toFixed(0)}%
                                                     </span>
                                                 </div>
                                                 <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "8px" }}>
                                                     <div>
                                                         <div style={{ fontSize: "8.5px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Primary Ritual</div>
                                                         <div style={{ fontSize: "12px", color: "#fff", fontWeight: "800" }}>{analysisResult.primary_ritual || analysisResult.canonical_metadata?.primary_ritual || "Devotional Worship"}</div>
                                                     </div>
                                                     <div>
                                                         <div style={{ fontSize: "8.5px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Ritual Family</div>
                                                         <div style={{ fontSize: "12px", color: "#38bdf8", fontWeight: "800" }}>{analysisResult.ritual_family || analysisResult.canonical_metadata?.ritual_family || "Pooja"}</div>
                                                     </div>
                                                     <div>
                                                         <div style={{ fontSize: "8.5px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Primary Deity</div>
                                                         <div style={{ fontSize: "12px", color: "#c084fc", fontWeight: "800" }}>
                                                            {analysisResult.primary_deity || analysisResult.canonical_metadata?.primary_deity || "Unassigned / General"}
                                                        </div>
                                                     </div>
                                                 </div>
                                                 {(analysisResult.temple || analysisResult.canonical_metadata?.temple) && (
                                                     <div style={{ marginTop: "6px", fontSize: "10.5px", color: "#cbd5e1" }}>
                                                         <strong>Temple:</strong> {analysisResult.temple || analysisResult.canonical_metadata?.temple} • <strong>Offerings:</strong> {(analysisResult.offerings || analysisResult.canonical_metadata?.offerings || []).join(", ") || "Flowers"}
                                                     </div>
                                                 )}
                                             </div>

                                             {/* CEEE Multimodal Signal Fusion & Context Card */}
                                             {(analysisResult.perceptual_metadata || analysisResult.emotional_metadata) && (
                                                 <div style={{
                                                     background: "linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(56, 189, 248, 0.08) 100%)",
                                                     padding: "12px",
                                                     borderRadius: "8px",
                                                     border: "1px solid rgba(16, 185, 129, 0.25)",
                                                     margin: "8px 0"
                                                 }}>
                                                     <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                                                         <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "10px", color: "#34d399", fontWeight: "900", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                                                             <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                                                 <circle cx="12" cy="12" r="10"/>
                                                                 <path d="M12 8v8M8 12h8"/>
                                                             </svg>
                                                             CEEE Multimodal Signal Fusion & Context Intelligence (Layer 2 & 3)
                                                         </div>
                                                         <span style={{ fontSize: "9px", padding: "2px 6px", background: "rgba(56, 189, 248, 0.2)", color: "#38bdf8", borderRadius: "4px", fontWeight: "800" }}>
                                                             7 Models Fused
                                                         </span>
                                                     </div>
                                                     <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: "6px" }}>
                                                         <div style={{ background: "rgba(0,0,0,0.2)", padding: "6px 8px", borderRadius: "6px" }}>
                                                             <div style={{ fontSize: "8px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Environment</div>
                                                             <div style={{ fontSize: "11px", color: "#34d399", fontWeight: "800" }}>{analysisResult.perceptual_metadata?.environment?.value || "Sacred Space"}</div>
                                                         </div>
                                                         <div style={{ background: "rgba(0,0,0,0.2)", padding: "6px 8px", borderRadius: "6px" }}>
                                                             <div style={{ fontSize: "8px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Lighting</div>
                                                             <div style={{ fontSize: "11px", color: "#fbbf24", fontWeight: "800" }}>{analysisResult.perceptual_metadata?.lighting?.value || "Warm"}</div>
                                                         </div>
                                                         <div style={{ background: "rgba(0,0,0,0.2)", padding: "6px 8px", borderRadius: "6px" }}>
                                                             <div style={{ fontSize: "8px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Energy Level</div>
                                                             <div style={{ fontSize: "11px", color: "#f472b6", fontWeight: "800" }}>{analysisResult.emotional_metadata?.energy_level?.value || "Moderate"}</div>
                                                         </div>
                                                         <div style={{ background: "rgba(0,0,0,0.2)", padding: "6px 8px", borderRadius: "6px" }}>
                                                             <div style={{ fontSize: "8px", color: "#94a3b8", textTransform: "uppercase", fontWeight: "800" }}>Emotional Tone</div>
                                                             <div style={{ fontSize: "11px", color: "#38bdf8", fontWeight: "800" }}>{analysisResult.emotional_metadata?.emotional_tone?.value || "Reverent"}</div>
                                                         </div>
                                                     </div>
                                                 </div>
                                             )}

                                             {/* Legacy Category Grid */}
                                             <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px 16px", margin: "6px 0", background: "rgba(255,255,255,0.02)", padding: "10px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.04)" }}>
                                                <div>
                                                    <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800" }}>
                                                        Category {renderGroundingBadge("category")}
                                                    </div>
                                                    <div style={{ fontSize: "12px", color: "#fff", fontWeight: "700" }}>{analysisResult.category || "Entertainment"}</div>
                                                </div>
                                                <div>
                                                    <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800" }}>
                                                        Subcategory {renderGroundingBadge("subcategory")}
                                                    </div>
                                                    <div style={{ fontSize: "12px", color: "#fff", fontWeight: "700" }}>{analysisResult.subcategory || "General Video"}</div>
                                                </div>
                                                <div>
                                                    <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800" }}>
                                                        Mood {renderGroundingBadge("mood")}
                                                    </div>
                                                    <div style={{ fontSize: "12px", color: "#fff", fontWeight: "700" }}>{analysisResult.mood || "Normal"}</div>
                                                </div>
                                                <div>
                                                    <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800" }}>
                                                        Language & Type {renderGroundingBadge("language")}
                                                    </div>
                                                    <div style={{ fontSize: "12px", color: "#fff", fontWeight: "700" }}>{analysisResult.language || "English"} • {analysisResult.content_type || "Video Clip"}</div>
                                                </div>
                                            </div>

                                            <div>
                                                <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800", marginBottom: "4px" }}>
                                                    Tags {renderGroundingBadge("tags")}
                                                </div>
                                                <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                                                    {analysisResult.tags?.map((t, idx) => (
                                                        <span key={idx} style={{
                                                            fontSize: "9px",
                                                            padding: "3px 6px",
                                                            background: "rgba(56, 189, 248, 0.1)",
                                                            color: "var(--accent)",
                                                            borderRadius: "10px",
                                                            fontWeight: "800"
                                                        }}>
                                                            #{t}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>

                                            {/* Entities pills */}
                                            {analysisResult.entities && analysisResult.entities.length > 0 && (
                                                <div style={{ marginTop: "4px" }}>
                                                    <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800", marginBottom: "4px" }}>
                                                        Identified Named Entities {renderGroundingBadge("entities")}
                                                    </div>
                                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                                                        {analysisResult.entities.map((ent, idx) => (
                                                            <span key={idx} style={{
                                                                fontSize: "9px",
                                                                padding: "3px 6px",
                                                                background: "rgba(168, 85, 247, 0.1)",
                                                                color: "#c084fc",
                                                                borderRadius: "10px",
                                                                fontWeight: "800"
                                                            }}>
                                                                👤 {typeof ent === "object" ? ent.name || JSON.stringify(ent) : ent}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}

                                            {/* Final Embedding Text Block */}
                                            <div style={{ marginTop: "6px" }}>
                                                <div style={{ fontSize: "9px", color: "#64748b", textTransform: "uppercase", fontWeight: "800", marginBottom: "4px" }}>
                                                    Final Embedding Text (MiniLM Input) {renderGroundingBadge("embedding_text")}
                                                </div>
                                                <div style={{ fontSize: "11px", color: "#94a3b8", background: "rgba(0,0,0,0.15)", padding: "8px", borderRadius: "6px", border: "1px solid rgba(255,255,255,0.05)", lineHeight: "1.4", fontStyle: "italic" }}>
                                                    "{analysisResult.embedding_text || `${analysisResult.title} - ${analysisResult.summary}`}"
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Intermediate Modality Extractions Widget */}
                                <div className="dashboard-widget-card" style={{ padding: "20px", display: "flex", flexDirection: "column", minHeight: "300px" }}>
                                    <h3 style={{ margin: "0 0 14px 0" }}>Intermediate Modality Extractions</h3>
                                    
                                    {/* Tabs */}
                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "4px", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "8px", marginBottom: "14px" }}>
                                        {["reasoning", "perceptual_metadata", "emotional_metadata", "evidence_graph", "transcript", "ocr", "objects", "scenes", "actions", "audio_events", "embedding"].map(tab => (
                                            <button
                                                key={tab}
                                                onClick={() => setActiveDetailTab(tab)}
                                                style={{
                                                    padding: "6px 12px",
                                                    borderRadius: "6px",
                                                    fontSize: "12px",
                                                    fontWeight: "700",
                                                    border: "none",
                                                    cursor: "pointer",
                                                    background: activeDetailTab === tab ? "rgba(255,255,255,0.06)" : "transparent",
                                                    color: activeDetailTab === tab ? "var(--accent)" : "#64748b"
                                                }}
                                            >
                                                {tab.replace("_", " ").toUpperCase()}
                                            </button>
                                        ))}
                                    </div>

                                    {/* Tab Viewport */}
                                    <div style={{ flex: 1, overflowY: "auto", fontSize: "13px" }}>
                                         {activeDetailTab === "perceptual_metadata" && (
                                             <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                                                 <div style={{ color: "#34d399", fontWeight: "700", fontSize: "14px" }}>Layer 2 — Objective Perceptual Metadata</div>
                                                 <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                                                     {Object.entries(analysisResult.perceptual_metadata || {}).map(([key, data]) => (
                                                         <div key={key} style={{ background: "rgba(255,255,255,0.02)", padding: "10px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                             <div style={{ fontSize: "10px", color: "#34d399", textTransform: "uppercase", fontWeight: "800" }}>{key.replace("_", " ")}</div>
                                                             <div style={{ fontSize: "13px", color: "#fff", fontWeight: "700" }}>{typeof data === "object" ? data.value : String(data)}</div>
                                                             {typeof data === "object" && data.reason && (
                                                                 <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>{data.reason}</div>
                                                             )}
                                                         </div>
                                                     ))}
                                                 </div>
                                             </div>
                                         )}

                                         {activeDetailTab === "emotional_metadata" && (
                                             <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                                                 <div style={{ color: "#f472b6", fontWeight: "700", fontSize: "14px" }}>Layer 3 — Experiential & Emotional Metadata</div>
                                                 <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                                                     {Object.entries(analysisResult.emotional_metadata || {}).map(([key, data]) => (
                                                         <div key={key} style={{ background: "rgba(255,255,255,0.02)", padding: "10px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                             <div style={{ fontSize: "10px", color: "#f472b6", textTransform: "uppercase", fontWeight: "800" }}>{key.replace("_", " ")}</div>
                                                             <div style={{ fontSize: "13px", color: "#fff", fontWeight: "700" }}>{typeof data === "object" ? data.value : String(data)}</div>
                                                             {typeof data === "object" && data.reason && (
                                                                 <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>{data.reason}</div>
                                                             )}
                                                         </div>
                                                     ))}
                                                 </div>
                                             </div>
                                         )}

                                         {activeDetailTab === "reasoning" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                                                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2.5">
                                                        <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
                                                        <path d="M12 6v6l4 2"/>
                                                    </svg>
                                                    <div style={{ color: "#38bdf8", fontWeight: "700", fontSize: "14px" }}>Engine Reasoning & Semantic Understanding:</div>
                                                </div>
                                                <div style={{ background: "rgba(56, 189, 248, 0.05)", border: "1px solid rgba(56, 189, 248, 0.15)", padding: "14px", borderRadius: "10px", lineHeight: "1.6", color: "#e2e8f0" }}>
                                                    {analysisResult.reasoning || "No reasoning logs compiled yet."}
                                                </div>

                                                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", marginTop: "8px" }}>
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>Primary Topic</div>
                                                        <div style={{ fontSize: "13px", color: "#fff", fontWeight: "700" }}>{analysisResult.primary_topic || "Not determined"}</div>
                                                    </div>
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>Target Audience Intent</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.target_audience && analysisResult.target_audience.length > 0 ? (
                                                                analysisResult.target_audience.map((aud, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#f472b6", background: "rgba(244, 114, 182, 0.1)", padding: "2px 6px", borderRadius: "6px", fontWeight: "600" }}>{aud}</span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>General</span>
                                                            )}
                                                        </div>
                                                    </div>
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>Secondary Topics</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.secondary_topics && analysisResult.secondary_topics.length > 0 ? (
                                                                analysisResult.secondary_topics.map((t, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#c084fc", background: "rgba(192, 132, 252, 0.1)", padding: "2px 6px", borderRadius: "6px", fontWeight: "600" }}>🏷️ {t}</span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>None</span>
                                                            )}
                                                        </div>
                                                    </div>
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>Physical Activities</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.activities && analysisResult.activities.length > 0 ? (
                                                                analysisResult.activities.map((a, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#fb7185", background: "rgba(251, 113, 133, 0.1)", padding: "2px 6px", borderRadius: "6px", fontWeight: "600" }}>🏃 {a}</span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>None</span>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                        {activeDetailTab === "evidence_graph" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                                                <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
                                                    <span style={{ fontSize: "20px" }}>🕸</span>
                                                    <div style={{ color: "#10b981", fontWeight: "700", fontSize: "14px" }}>Normalized Structured Evidence Graph:</div>
                                                </div>
                                                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                                                    {/* Speech Modality */}
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#a855f7", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>🗣 Speech Transcription</div>
                                                        <div style={{ fontSize: "12px", color: "#cbd5e1", lineHeight: "1.4", fontStyle: "italic" }}>
                                                            {analysisResult.evidence_graph?.speech && analysisResult.evidence_graph.speech.length > 0 ? (
                                                                `"${analysisResult.evidence_graph.speech.map(item => typeof item === 'object' ? item.value || JSON.stringify(item) : item).join(', ')}"`
                                                            ) : (
                                                                "No dialogue observed."
                                                            )}
                                                        </div>
                                                    </div>

                                                    {/* OCR Modality */}
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#10b981", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>📺 On-Screen Text (OCR)</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.evidence_graph?.ocr && analysisResult.evidence_graph.ocr.length > 0 ? (
                                                                analysisResult.evidence_graph.ocr.map((item, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#10b981", background: "rgba(16, 185, 129, 0.1)", padding: "2px 6px", borderRadius: "4px" }}>
                                                                        {typeof item === 'object' ? item.value || JSON.stringify(item) : String(item)}
                                                                    </span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>No screen text.</span>
                                                            )}
                                                        </div>
                                                    </div>

                                                    {/* Vision Modality */}
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#60a5fa", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>👁 Objects & Scenes (YOLO/CLIP)</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.evidence_graph?.vision && analysisResult.evidence_graph.vision.length > 0 ? (
                                                                analysisResult.evidence_graph.vision.map((item, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#60a5fa", background: "rgba(96, 165, 250, 0.1)", padding: "2px 6px", borderRadius: "4px" }}>
                                                                        {typeof item === 'object' ? item.value || JSON.stringify(item) : String(item)}
                                                                    </span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>No visual cues.</span>
                                                            )}
                                                        </div>
                                                    </div>

                                                    {/* Actions Modality */}
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                                                        <div style={{ fontSize: "10px", color: "#fb7185", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>🏃 Kinetic Actions (VideoMAE)</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.evidence_graph?.actions && analysisResult.evidence_graph.actions.length > 0 ? (
                                                                analysisResult.evidence_graph.actions.map((item, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#fb7185", background: "rgba(251, 113, 133, 0.1)", padding: "2px 6px", borderRadius: "4px" }}>
                                                                        {typeof item === 'object' ? item.value || JSON.stringify(item) : String(item)}
                                                                    </span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>No motion cues.</span>
                                                            )}
                                                        </div>
                                                    </div>

                                                    {/* Audio Modality */}
                                                    <div style={{ background: "rgba(255,255,255,0.02)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)", gridColumn: "span 2" }}>
                                                        <div style={{ fontSize: "10px", color: "#facc15", fontWeight: "800", textTransform: "uppercase", marginBottom: "6px" }}>🔊 Audio Events (AST)</div>
                                                        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                                                            {analysisResult.evidence_graph?.audio && analysisResult.evidence_graph.audio.length > 0 ? (
                                                                analysisResult.evidence_graph.audio.map((item, i) => (
                                                                    <span key={i} style={{ fontSize: "11px", color: "#facc15", background: "rgba(250, 204, 21, 0.1)", padding: "2px 6px", borderRadius: "4px" }}>
                                                                        {typeof item === 'object' ? item.value || JSON.stringify(item) : String(item)}
                                                                    </span>
                                                                ))
                                                            ) : (
                                                                <span style={{ fontSize: "11px", color: "#475569", fontStyle: "italic" }}>Ambient environment.</span>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                        {activeDetailTab === "transcript" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                                                <div style={{ color: "#a855f7", fontWeight: "700" }}>Speech Transcribed Output:</div>
                                                <div style={{ background: "rgba(0,0,0,0.2)", padding: "12px", borderRadius: "8px", fontStyle: "italic", lineHeight: "1.5" }}>
                                                    {analysisResult.transcript || "No dialogue detected in audio track."}
                                                </div>
                                            </div>
                                        )}

                                        {activeDetailTab === "ocr" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                                                <div style={{ color: "#10b981", fontWeight: "700" }}>Extracted Screen Text Timestamps:</div>
                                                {!Array.isArray(analysisResult.ocr) || analysisResult.ocr.length === 0 ? (
                                                    <div style={{ color: "#475569", fontStyle: "italic" }}>No characters detected on screen.</div>
                                                ) : (
                                                    analysisResult.ocr.map((o, idx) => (
                                                        <div key={idx} style={{ display: "flex", gap: "12px", background: "rgba(0,0,0,0.15)", padding: "8px 12px", borderRadius: "6px" }}>
                                                            <span style={{ color: "var(--accent)", fontWeight: "700", width: "40px" }}>{typeof o === 'object' ? o.timestamp || '0' : '0'}s</span>
                                                            <span style={{ color: "#cbd5e1" }}>{typeof o === 'object' ? o.text || JSON.stringify(o) : String(o)}</span>
                                                        </div>
                                                    ))
                                                )}
                                            </div>
                                        )}

                                        {activeDetailTab === "objects" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                                                <div style={{ color: "#60a5fa", fontWeight: "700" }}>YOLOv11 Objects Detections:</div>
                                                {analysisResult.objects?.length === 0 ? (
                                                    <div style={{ color: "#475569", fontStyle: "italic" }}>No distinct objects detected.</div>
                                                ) : (
                                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                                                        {analysisResult.objects?.map((obj, idx) => (
                                                            <span key={idx} style={{
                                                                fontSize: "12px",
                                                                padding: "6px 12px",
                                                                background: "rgba(96, 165, 250, 0.12)",
                                                                color: "#60a5fa",
                                                                borderRadius: "8px",
                                                                fontWeight: "700"
                                                            }}>
                                                                📦 {obj.toUpperCase()}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        )}

                                        {activeDetailTab === "scenes" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                                                <div style={{ color: "#34d399", fontWeight: "700" }}>CLIP Classified Environments:</div>
                                                {analysisResult.scenes?.length === 0 ? (
                                                    <div style={{ color: "#475569", fontStyle: "italic" }}>No scene matching computed.</div>
                                                ) : (
                                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                                                        {analysisResult.scenes?.map((sc, idx) => (
                                                            <span key={idx} style={{
                                                                fontSize: "12px",
                                                                padding: "6px 12px",
                                                                background: "rgba(52, 211, 153, 0.12)",
                                                                color: "#34d399",
                                                                borderRadius: "8px",
                                                                fontWeight: "700"
                                                            }}>
                                                                🏞 {sc.toUpperCase()}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        )}

                                        {activeDetailTab === "actions" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                                                <div style={{ color: "#fb7185", fontWeight: "700" }}>VideoMAE Kinetics Activities:</div>
                                                {analysisResult.actions?.length === 0 ? (
                                                    <div style={{ color: "#475569", fontStyle: "italic" }}>No clear activities detected.</div>
                                                ) : (
                                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                                                        {analysisResult.actions?.map((act, idx) => (
                                                            <span key={idx} style={{
                                                                fontSize: "12px",
                                                                padding: "6px 12px",
                                                                background: "rgba(251, 113, 133, 0.12)",
                                                                color: "#fb7185",
                                                                borderRadius: "8px",
                                                                fontWeight: "700"
                                                            }}>
                                                                🏃 {act.toUpperCase()}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        )}

                                        {activeDetailTab === "audio_events" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                                                <div style={{ color: "#facc15", fontWeight: "700" }}>AST Audio Events:</div>
                                                {analysisResult.audio_events?.length === 0 ? (
                                                    <div style={{ color: "#475569", fontStyle: "italic" }}>Ambient silence.</div>
                                                ) : (
                                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                                                        {analysisResult.audio_events?.map((ev, idx) => (
                                                            <span key={idx} style={{
                                                                fontSize: "12px",
                                                                padding: "6px 12px",
                                                                background: "rgba(250, 204, 21, 0.12)",
                                                                color: "#facc15",
                                                                borderRadius: "8px",
                                                                fontWeight: "700"
                                                            }}>
                                                                🔊 {ev.toUpperCase()}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        )}

                                        {activeDetailTab === "embedding" && (
                                            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                                                <div style={{ color: "var(--accent)", fontWeight: "700" }}>MiniLM Embedding Vector:</div>
                                                <div style={{
                                                    background: "rgba(0,0,0,0.3)", 
                                                    padding: "12px", 
                                                    borderRadius: "8px", 
                                                    fontFamily: "monospace",
                                                    fontSize: "11px",
                                                    maxHeight: "150px",
                                                    overflowY: "auto",
                                                    color: "#94a3b8",
                                                    lineHeight: "1.5",
                                                    wordBreak: "break-all"
                                                }}>
                                                    [ {analysisResult.embedding?.slice(0, 15).join(", ")} ... (384 dimensions normalized) ]
                                                </div>
                                                <div style={{ fontSize: "11px", color: "#475569" }}>
                                                    Provenance: Compiled on {analysisResult.provenance?.timestamp} ({analysisResult.provenance?.platform_os}) using {analysisResult.provenance?.processing_time_sec}s compute.
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>

                            </div>
                        ) : (
                            <div className="dashboard-widget-card" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px", height: "400px", color: "#475569" }}>
                                <div style={{ fontSize: "48px", marginBottom: "16px" }}>📊</div>
                                <div style={{ fontWeight: "700", color: "#64748b" }}>Telemetry Dashboard Offline</div>
                                <div style={{ fontSize: "12px", textAlign: "center", marginTop: "6px" }}>Upload a video file or choose a previously analyzed clip from the catalog sidebar to display intelligence telemetry.</div>
                            </div>
                        )}
                    </div>

                </div>
            </div>
        </div>
    );
}

export default ContentIntelligence;
