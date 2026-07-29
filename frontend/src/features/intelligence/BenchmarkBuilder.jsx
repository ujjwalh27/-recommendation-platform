import React, { useState, useEffect } from "react";

export default function BenchmarkBuilder() {
    const [subTab, setSubTab] = useState("annotate");
    const [taxonomy, setTaxonomy] = useState(null);
    const [annotations, setAnnotations] = useState([]);
    const [candidates, setCandidates] = useState([]);
    const [searchQuery, setSearchQuery] = useState("Sai Baba Milk Abhishekam");
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [evalResults, setEvalResults] = useState(null);
    const [evaluating, setEvaluating] = useState(false);
    const [statusMsg, setStatusMsg] = useState("");

    // Form state for annotation studio
    const [formState, setFormState] = useState({
        video_id: "",
        title: "",
        content_type: "Ritual",
        primary_class: "Abhishekam",
        sub_class: "Milk Abhishekam",
        primary_deity: "Shirdi Sai Baba",
        temple: "Shirdi Sai Mandir",
        festival: "Guru Purnima",
        language: "Hindi",
        secondary_activities: ["Pouring Milk", "Offering Flowers"]
    });

    useEffect(() => {
        fetchTaxonomy();
        fetchAnnotations();
        fetchCandidates(searchQuery);
    }, []);

    const fetchTaxonomy = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/dbb/taxonomy");
            const data = await res.json();
            setTaxonomy(data);
        } catch (e) {
            console.error(e);
        }
    };

    const fetchAnnotations = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/dbb/annotations");
            const data = await res.json();
            const list = Array.isArray(data) ? data : (data?.annotations || []);
            setAnnotations(list);
            if (list.length > 0 && !selectedVideo) {
                selectVideoForEdit(list[0]);
            }
        } catch (e) {
            console.error("Failed to fetch annotations:", e);
            setAnnotations([]);
        }
    };

    const fetchCandidates = async (q) => {
        try {
            const res = await fetch(`http://localhost:8000/api/dbb/candidates?query=${encodeURIComponent(q)}`);
            const data = await res.json();
            const list = Array.isArray(data) ? data : (data?.candidates || []);
            setCandidates(list);
        } catch (e) {
            console.error("Failed to fetch candidates:", e);
            setCandidates([]);
        }
    };

    const selectVideoForEdit = (v) => {
        setSelectedVideo(v);
        setFormState({
            video_id: v.video_id || `dbb_vid_${Date.now()}`,
            title: v.title || "Devotional Worship Stream",
            content_type: v.content_type || "Ritual",
            primary_class: v.primary_class || "Abhishekam",
            sub_class: v.sub_class || "Milk Abhishekam",
            primary_deity: v.primary_deity || "Shirdi Sai Baba",
            temple: v.temple || "Shirdi Sai Mandir",
            festival: v.festival || "Guru Purnima",
            language: v.language || "Hindi",
            secondary_activities: v.secondary_activities || ["Pouring Milk", "Offering Flowers"]
        });
    };

    const handleSaveAnnotation = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://localhost:8000/api/dbb/annotate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formState)
            });
            const data = await res.json();
            setStatusMsg(`✅ Annotation saved for ${formState.video_id}!`);
            fetchAnnotations();
            setTimeout(() => setStatusMsg(""), 4000);
        } catch (err) {
            setStatusMsg(`❌ Failed to save annotation: ${err}`);
        }
    };

    const handleRunBenchmark = async () => {
        setEvaluating(true);
        setStatusMsg("⏳ Running classifier evaluation against ground-truth dataset...");
        try {
            const res = await fetch("http://localhost:8000/api/dbb/run-benchmark", { method: "POST" });
            const data = await res.json();
            setEvalResults(data);
            setStatusMsg(`🎉 Benchmark completed! Overall Accuracy: ${data.overall_accuracy_percent}%`);
        } catch (e) {
            setStatusMsg("❌ Benchmark execution failed.");
        } finally {
            setEvaluating(false);
        }
    };

    const exportCSV = () => {
        window.open("http://localhost:8000/api/dbb/export?format=csv", "_blank");
    };

    const exportJSON = () => {
        const jsonStr = JSON.stringify(annotations, null, 2);
        const blob = new Blob([jsonStr], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "dbb_benchmark_dataset.json";
        a.click();
    };

    const toggleActivity = (act) => {
        const cur = formState.secondary_activities || [];
        if (cur.includes(act)) {
            setFormState({ ...formState, secondary_activities: cur.filter(x => x !== act) });
        } else {
            setFormState({ ...formState, secondary_activities: [...cur, act] });
        }
    };

    return (
        <div style={{ padding: "20px", color: "#f8fafc", fontFamily: "Inter, sans-serif", height: "100%", overflowY: "auto" }}>
            {/* Header Banner */}
            <div style={{
                background: "linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95))",
                padding: "20px 24px",
                borderRadius: "14px",
                border: "1px solid rgba(255,255,255,0.1)",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "20px",
                boxShadow: "0 10px 25px -5px rgba(0,0,0,0.5)"
            }}>
                <div>
                    <h2 style={{ margin: 0, fontSize: "20px", fontWeight: "900", color: "#38bdf8", display: "flex", alignItems: "center", gap: "10px" }}>
                        🎯 DAIV BENCHMARK BUILDER (DBB)
                    </h2>
                    <p style={{ margin: "6px 0 0 0", fontSize: "13px", color: "#94a3b8" }}>
                        Internal Dataset Management & Ground-Truth Annotation Studio for Video Intelligence Platform
                    </p>
                </div>
                <div style={{ display: "flex", gap: "16px", alignItems: "center" }}>
                    <div style={{ background: "rgba(56,189,248,0.1)", padding: "8px 16px", borderRadius: "10px", border: "1px solid rgba(56,189,248,0.2)", textAlign: "center" }}>
                        <div style={{ fontSize: "18px", fontWeight: "900", color: "#38bdf8" }}>{annotations.length}</div>
                        <div style={{ fontSize: "11px", color: "#94a3b8" }}>Annotated Videos</div>
                    </div>
                    <button onClick={exportJSON} style={{ padding: "8px 14px", borderRadius: "8px", background: "#334155", color: "#fff", border: "none", fontWeight: "700", cursor: "pointer", fontSize: "12px" }}>
                        📥 Export JSON
                    </button>
                    <button onClick={exportCSV} style={{ padding: "8px 14px", borderRadius: "8px", background: "#0284c7", color: "#fff", border: "none", fontWeight: "700", cursor: "pointer", fontSize: "12px" }}>
                        📊 Export CSV
                    </button>
                </div>
            </div>

            {statusMsg && (
                <div style={{ background: "rgba(56,189,248,0.15)", border: "1px solid #0284c7", padding: "10px 16px", borderRadius: "8px", marginBottom: "16px", color: "#e0f2fe", fontSize: "13px", fontWeight: "600" }}>
                    {statusMsg}
                </div>
            )}

            {/* Sub Tabs */}
            <div style={{ display: "flex", gap: "10px", marginBottom: "20px", borderBottom: "1px solid rgba(255,255,255,0.1)", pb: "10px" }}>
                {[
                    { id: "annotate", label: "📝 Annotation Studio" },
                    { id: "search", label: "🔍 Candidate Discovery" },
                    { id: "inventory", label: "📦 Benchmark Inventory" },
                    { id: "eval", label: "📊 Benchmark Evaluator" },
                    { id: "taxonomy", label: "⚙️ Taxonomy Manager" }
                ].map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setSubTab(tab.id)}
                        style={{
                            padding: "8px 16px",
                            borderRadius: "8px",
                            fontSize: "13px",
                            fontWeight: "700",
                            border: "none",
                            cursor: "pointer",
                            background: subTab === tab.id ? "#38bdf8" : "rgba(30,41,59,0.6)",
                            color: subTab === tab.id ? "#0f172a" : "#94a3b8",
                            transition: "all 0.2s"
                        }}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* TAB 1: ANNOTATION STUDIO */}
            {subTab === "annotate" && (
                <div style={{ display: "grid", gridTemplateColumns: "320px 1fr", gap: "20px" }}>
                    {/* Video Selector Sidebar */}
                    <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "16px", maxHeight: "650px", overflowY: "auto" }}>
                        <h4 style={{ margin: "0 0 12px 0", fontSize: "14px", color: "#f1f5f9" }}>Select Video to Annotate</h4>
                        {annotations.map(v => (
                            <div
                                key={v.video_id}
                                onClick={() => selectVideoForEdit(v)}
                                style={{
                                    padding: "10px 12px",
                                    borderRadius: "8px",
                                    marginBottom: "8px",
                                    cursor: "pointer",
                                    background: formState.video_id === v.video_id ? "rgba(56,189,248,0.2)" : "rgba(30,41,59,0.5)",
                                    border: formState.video_id === v.video_id ? "1px solid #38bdf8" : "1px solid transparent",
                                    transition: "all 0.15s"
                                }}
                            >
                                <div style={{ fontSize: "12px", fontWeight: "700", color: "#f8fafc" }}>{v.title || v.video_id}</div>
                                <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>
                                    {v.primary_class} • {v.sub_class}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Annotation Form */}
                    <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "24px" }}>
                        <form onSubmit={handleSaveAnnotation}>
                            <h3 style={{ margin: "0 0 16px 0", fontSize: "16px", color: "#38bdf8" }}>
                                Annotate Video: {formState.video_id}
                            </h3>

                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Video Title / Description</label>
                                    <input
                                        type="text"
                                        value={formState.title}
                                        onChange={e => setFormState({ ...formState, title: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    />
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Content Type (Stage 1)</label>
                                    <select
                                        value={formState.content_type}
                                        onChange={e => setFormState({ ...formState, content_type: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.content_types || ["Ritual", "Music", "Discourse", "Temple", "Festival"]).map(c => (
                                            <option key={c} value={c}>{c}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Primary Class (Stage 2)</label>
                                    <select
                                        value={formState.primary_class}
                                        onChange={e => setFormState({ ...formState, primary_class: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.rituals || ["Abhishekam", "Aarti", "Pooja", "Archana", "Bhajan", "Pravachan"]).map(r => (
                                            <option key={r} value={r}>{r}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Subtype (Stage 3)</label>
                                    <select
                                        value={formState.sub_class}
                                        onChange={e => setFormState({ ...formState, sub_class: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.subtypes[formState.primary_class] || taxonomy?.subtypes["Abhishekam"] || ["Milk Abhishekam"]).map(s => (
                                            <option key={s} value={s}>{s}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Primary Deity</label>
                                    <select
                                        value={formState.primary_deity}
                                        onChange={e => setFormState({ ...formState, primary_deity: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.deities || ["Shirdi Sai Baba"]).map(d => (
                                            <option key={d} value={d}>{d}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Temple / Setting</label>
                                    <select
                                        value={formState.temple}
                                        onChange={e => setFormState({ ...formState, temple: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.temples || ["Shirdi Sai Mandir"]).map(t => (
                                            <option key={t} value={t}>{t}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Festival / Occasion</label>
                                    <select
                                        value={formState.festival}
                                        onChange={e => setFormState({ ...formState, festival: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.festivals || ["Guru Purnima"]).map(f => (
                                            <option key={f} value={f}>{f}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "6px" }}>Language</label>
                                    <select
                                        value={formState.language}
                                        onChange={e => setFormState({ ...formState, language: e.target.value })}
                                        style={{ width: "100%", padding: "8px 12px", borderRadius: "6px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                                    >
                                        {(taxonomy?.languages || ["Hindi"]).map(l => (
                                            <option key={l} value={l}>{l}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            {/* Secondary Activities Checkboxes */}
                            <div style={{ marginTop: "20px" }}>
                                <label style={{ fontSize: "12px", color: "#94a3b8", display: "block", marginBottom: "8px" }}>Secondary Activities & Ritual Actions</label>
                                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: "10px" }}>
                                    {(taxonomy?.secondary_activities || ["Pouring Milk", "Offering Flowers"]).map(act => {
                                        const checked = (formState.secondary_activities || []).includes(act);
                                        return (
                                            <label key={act} style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "12px", color: "#e2e8f0", cursor: "pointer", background: checked ? "rgba(56,189,248,0.15)" : "#1e293b", padding: "6px 10px", borderRadius: "6px", border: checked ? "1px solid #38bdf8" : "1px solid #334155" }}>
                                                <input
                                                    type="checkbox"
                                                    checked={checked}
                                                    onChange={() => toggleActivity(act)}
                                                />
                                                {act}
                                            </label>
                                        );
                                    })}
                                </div>
                            </div>

                            <button type="submit" style={{ marginTop: "24px", padding: "10px 24px", background: "#38bdf8", color: "#0f172a", border: "none", borderRadius: "8px", fontWeight: "900", fontSize: "14px", cursor: "pointer" }}>
                                💾 Save Annotation to Benchmark Dataset
                            </button>
                        </form>
                    </div>
                </div>
            )}

            {/* TAB 2: CANDIDATE DISCOVERY */}
            {subTab === "search" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "20px" }}>
                    <h3 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Devotional Search Query & Candidate Discovery</h3>
                    <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={e => setSearchQuery(e.target.value)}
                            placeholder="Enter devotional search query..."
                            style={{ flex: 1, padding: "10px 14px", borderRadius: "8px", background: "#1e293b", border: "1px solid #334155", color: "#fff" }}
                        />
                        <button onClick={() => fetchCandidates(searchQuery)} style={{ padding: "10px 20px", background: "#0284c7", color: "#fff", border: "none", borderRadius: "8px", fontWeight: "700", cursor: "pointer" }}>
                            🔍 Search Candidates
                        </button>
                    </div>

                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "20px" }}>
                        {(taxonomy?.predefined_search_queries || []).map(q => (
                            <button
                                key={q}
                                onClick={() => { setSearchQuery(q); fetchCandidates(q); }}
                                style={{ padding: "6px 12px", borderRadius: "20px", background: "rgba(56,189,248,0.1)", border: "1px solid rgba(56,189,248,0.2)", color: "#38bdf8", fontSize: "12px", cursor: "pointer" }}
                            >
                                {q}
                            </button>
                        ))}
                    </div>

                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "16px" }}>
                        {(candidates || []).map(c => (
                            <div key={c.video_id} style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "10px", padding: "16px" }}>
                                <div style={{ fontWeight: "700", color: "#f8fafc", fontSize: "14px" }}>{c.title}</div>
                                <div style={{ fontSize: "12px", color: "#94a3b8", margin: "6px 0" }}>Source: {c.source} | Duration: {c.duration}</div>
                                <div style={{ fontSize: "11px", color: "#38bdf8" }}>Suggested: {c.suggested_primary_class} ({c.suggested_sub_class})</div>
                                <button
                                    onClick={() => {
                                        selectVideoForEdit({
                                            video_id: c.video_id,
                                            title: c.title,
                                            content_type: c.suggested_content_type,
                                            primary_class: c.suggested_primary_class,
                                            sub_class: c.suggested_sub_class,
                                            primary_deity: c.suggested_deity,
                                            temple: "Shirdi Sai Mandir",
                                            festival: "Daily Devotional",
                                            language: "Hindi",
                                            secondary_activities: ["Pouring Milk", "Offering Flowers"]
                                        });
                                        setSubTab("annotate");
                                    }}
                                    style={{ marginTop: "12px", width: "100%", padding: "6px", background: "#334155", color: "#fff", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "700", cursor: "pointer" }}
                                >
                                    ✏️ Annotate in Studio
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* TAB 3: INVENTORY */}
            {subTab === "inventory" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "20px" }}>
                    <h3 style={{ margin: "0 0 16px 0", color: "#38bdf8" }}>Annotated Ground-Truth Benchmark Inventory ({(annotations || []).length} Records)</h3>
                    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
                        <thead>
                            <tr style={{ background: "#1e293b", color: "#94a3b8", textAlign: "left" }}>
                                <th style={{ padding: "10px" }}>Video ID</th>
                                <th style={{ padding: "10px" }}>Title</th>
                                <th style={{ padding: "10px" }}>Content Type</th>
                                <th style={{ padding: "10px" }}>Primary Class</th>
                                <th style={{ padding: "10px" }}>Sub Class</th>
                                <th style={{ padding: "10px" }}>Deity</th>
                                <th style={{ padding: "10px" }}>Temple</th>
                                <th style={{ padding: "10px" }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(annotations || []).map(a => (
                                <tr key={a.video_id} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                                    <td style={{ padding: "10px", fontFamily: "monospace", color: "#38bdf8" }}>{a.video_id}</td>
                                    <td style={{ padding: "10px", color: "#f8fafc" }}>{a.title}</td>
                                    <td style={{ padding: "10px" }}>{a.content_type}</td>
                                    <td style={{ padding: "10px", fontWeight: "700" }}>{a.primary_class}</td>
                                    <td style={{ padding: "10px" }}>{a.sub_class}</td>
                                    <td style={{ padding: "10px" }}>{a.primary_deity}</td>
                                    <td style={{ padding: "10px" }}>{a.temple}</td>
                                    <td style={{ padding: "10px" }}>
                                        <button onClick={() => { selectVideoForEdit(a); setSubTab("annotate"); }} style={{ padding: "4px 8px", background: "#0284c7", color: "#fff", border: "none", borderRadius: "4px", fontSize: "11px", cursor: "pointer" }}>
                                            Edit
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* TAB 4: BENCHMARK EVALUATOR */}
            {subTab === "eval" && (
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "24px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                        <div>
                            <h3 style={{ margin: 0, color: "#38bdf8" }}>DBB Classifier Benchmark Evaluator</h3>
                            <p style={{ margin: "4px 0 0 0", fontSize: "12px", color: "#94a3b8" }}>Compare classifier predictions against ground-truth annotations and measure accuracy, F1, & failure modes.</p>
                        </div>
                        <button
                            onClick={handleRunBenchmark}
                            disabled={evaluating}
                            style={{ padding: "10px 24px", background: "linear-gradient(90deg, #0284c7, #38bdf8)", color: "#0f172a", border: "none", borderRadius: "8px", fontWeight: "900", fontSize: "14px", cursor: "pointer" }}
                        >
                            {evaluating ? "⏳ Evaluating..." : "⚡ Run Live Benchmark"}
                        </button>
                    </div>

                    {evalResults && (
                        <div>
                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "16px", marginBottom: "24px" }}>
                                <div style={{ background: "#1e293b", padding: "16px", borderRadius: "10px", textAlign: "center" }}>
                                    <div style={{ fontSize: "28px", fontWeight: "900", color: "#38bdf8" }}>{evalResults.overall_accuracy_percent}%</div>
                                    <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>Overall Accuracy</div>
                                </div>

                                <div style={{ background: "#1e293b", padding: "16px", borderRadius: "10px", textAlign: "center" }}>
                                    <div style={{ fontSize: "28px", fontWeight: "900", color: "#38bdf8" }}>{evalResults.macro_f1_score}</div>
                                    <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>Macro F1-Score</div>
                                </div>

                                <div style={{ background: "#1e293b", padding: "16px", borderRadius: "10px", textAlign: "center" }}>
                                    <div style={{ fontSize: "28px", fontWeight: "900", color: "#38bdf8" }}>{evalResults.total_annotated_videos}</div>
                                    <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>Evaluated Benchmark Videos</div>
                                </div>
                            </div>

                            <h4 style={{ color: "#f1f5f9", marginBottom: "12px" }}>Per-Class Metrics</h4>
                            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px", marginBottom: "24px" }}>
                                <thead>
                                    <tr style={{ background: "#1e293b", color: "#94a3b8", textAlign: "left" }}>
                                        <th style={{ padding: "8px" }}>Primary Class</th>
                                        <th style={{ padding: "8px" }}>Precision</th>
                                        <th style={{ padding: "8px" }}>Recall</th>
                                        <th style={{ padding: "8px" }}>F1-Score</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(evalResults.per_class_metrics).map(([cls, m]) => (
                                        <tr key={cls} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                                            <td style={{ padding: "8px", fontWeight: "700", color: "#f8fafc" }}>{cls}</td>
                                            <td style={{ padding: "8px" }}>{(m.precision * 100).toFixed(1)}%</td>
                                            <td style={{ padding: "8px" }}>{(m.recall * 100).toFixed(1)}%</td>
                                            <td style={{ padding: "8px", fontWeight: "700", color: "#38bdf8" }}>{m.f1_score.toFixed(4)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
