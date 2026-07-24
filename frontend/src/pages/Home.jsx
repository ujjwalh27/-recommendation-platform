import React, { useState } from "react";
import VideoFeed from "../features/feed/VideoFeed";
import ContentIntelligence from "../features/intelligence/ContentIntelligence";
import KnowledgeGraphXAI from "../features/intelligence/KnowledgeGraphXAI";
import ObservabilityMetrics from "../features/intelligence/ObservabilityMetrics";

function Home() {
    const [activeTab, setActiveTab] = useState("intel");

    return (
        <div style={{ display: "flex", flexDirection: "column", height: "100vh", backgroundColor: "var(--bg)", overflow: "hidden" }}>
            {/* Global Premium Navigation Header */}
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "12px 24px",
                borderBottom: "1px solid rgba(255,255,255,0.08)",
                background: "rgba(10,15,26,0.85)",
                backdropFilter: "blur(12px)",
                zIndex: 100
            }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2.5" style={{ width: "22px", height: "22px" }}>
                        <polygon points="12 2 2 7 12 12 22 7 12 2" />
                        <polyline points="2 17 12 22 22 17" />
                        <polyline points="2 12 12 17 22 12" />
                    </svg>
                    <span style={{ fontWeight: "900", fontSize: "15px", color: "#fff", letterSpacing: "-0.5px" }}>DAIV VIDEO INTELLIGENCE ENGINE</span>
                </div>
                
                <div style={{ display: "flex", gap: "8px" }}>
                    <button 
                        onClick={() => setActiveTab("intel")} 
                        style={{
                            padding: "6px 14px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "intel" ? "var(--accent)" : "transparent",
                            color: activeTab === "intel" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        🧠 Content Intelligence
                    </button>

                    <button 
                        onClick={() => setActiveTab("kg_xai")} 
                        style={{
                            padding: "6px 14px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "kg_xai" ? "var(--accent)" : "transparent",
                            color: activeTab === "kg_xai" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        🕸 Knowledge Graph & XAI
                    </button>

                    <button 
                        onClick={() => setActiveTab("observability")} 
                        style={{
                            padding: "6px 14px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "observability" ? "var(--accent)" : "transparent",
                            color: activeTab === "observability" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        📊 Observability & Metrics
                    </button>

                    <button 
                        onClick={() => setActiveTab("feed")} 
                        style={{
                            padding: "6px 14px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "feed" ? "var(--accent)" : "transparent",
                            color: activeTab === "feed" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        🎥 Recommendation Feed
                    </button>
                </div>
            </div>
            
            {/* Screen Content Window */}
            <div style={{ flex: 1, overflow: "hidden" }}>
                {activeTab === "intel" && <ContentIntelligence />}
                {activeTab === "kg_xai" && <KnowledgeGraphXAI />}
                {activeTab === "observability" && <ObservabilityMetrics />}
                {activeTab === "feed" && <VideoFeed />}
            </div>
        </div>
    );
}

export default Home;