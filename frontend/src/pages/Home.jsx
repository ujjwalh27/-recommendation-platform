import React, { useState } from "react";
import ContentIntelligence from "../features/intelligence/ContentIntelligence";
import VideoFeed from "../features/feed/VideoFeed";
import PMCLPDashboard from "../features/monitoring/PMCLPDashboard";
import BenchmarkBuilder from "../features/intelligence/BenchmarkBuilder";

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
                background: "rgba(10,15,26,0.92)",
                backdropFilter: "blur(12px)",
                zIndex: 100
            }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div style={{
                        width: "28px",
                        height: "28px",
                        borderRadius: "8px",
                        background: "linear-gradient(135deg, var(--accent) 0%, #0284c7 100%)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "#000"
                    }}>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                        </svg>
                    </div>
                    <div>
                        <span style={{ fontWeight: "900", fontSize: "15px", color: "#fff", letterSpacing: "-0.5px" }}>
                            DAIV PLATFORM
                        </span>
                        <span style={{ fontSize: "10px", color: "var(--accent)", marginLeft: "8px", padding: "2px 6px", background: "rgba(56, 189, 248, 0.12)", borderRadius: "4px", fontWeight: "800" }}>
                            CMREE SEMANTIC LIVE
                        </span>
                    </div>
                </div>
                
                <div style={{ display: "flex", gap: "8px" }}>
                    <button 
                        onClick={() => setActiveTab("intel")} 
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "6px",
                            padding: "8px 16px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "intel" ? "var(--accent)" : "rgba(255,255,255,0.04)",
                            color: activeTab === "intel" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                            <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
                            <path d="M12 6v6l4 2"/>
                        </svg>
                        Multimodal Intelligence & CMREE
                    </button>

                    <button 
                        onClick={() => setActiveTab("feed")} 
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "6px",
                            padding: "8px 16px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "feed" ? "var(--accent)" : "rgba(255,255,255,0.04)",
                            color: activeTab === "feed" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                            <polygon points="23 7 16 12 23 17 23 7"/>
                            <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                        </svg>
                        Real-Time Recommendation Feed
                    </button>

                    <button 
                        onClick={() => setActiveTab("pmclp")} 
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "6px",
                            padding: "8px 16px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "pmclp" ? "var(--accent)" : "rgba(255,255,255,0.04)",
                            color: activeTab === "pmclp" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                            <line x1="18" y1="20" x2="18" y2="10"/>
                            <line x1="12" y1="20" x2="12" y2="4"/>
                            <line x1="6" y1="20" x2="6" y2="14"/>
                        </svg>
                        Production Monitoring (PMCLP)
                    </button>

                    <button 
                        onClick={() => setActiveTab("dbb")} 
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "6px",
                            padding: "8px 16px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "800",
                            border: "none",
                            cursor: "pointer",
                            background: activeTab === "dbb" ? "var(--accent)" : "rgba(255,255,255,0.04)",
                            color: activeTab === "dbb" ? "#000" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                            <circle cx="12" cy="12" r="10"/>
                            <circle cx="12" cy="12" r="6"/>
                            <circle cx="12" cy="12" r="2"/>
                        </svg>
                        Benchmark Builder (DBB)
                    </button>
                </div>
            </div>
            
            {/* Screen Content Window */}
            <div style={{ flex: 1, overflow: "hidden" }}>
                {activeTab === "intel" && <ContentIntelligence />}
                {activeTab === "feed" && <VideoFeed />}
                {activeTab === "pmclp" && <PMCLPDashboard />}
                {activeTab === "dbb" && <BenchmarkBuilder />}
            </div>
        </div>
    );
}

export default Home;