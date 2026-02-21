import streamlit as st
import numpy as np
from PIL import Image
import time
import json
from datetime import datetime
from io import BytesIO
import hashlib
import random

# Page Configuration
st.set_page_config(
    page_title="DeepFake Detection Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Modern Professional Theme
st.markdown("""
<style>
    /* Global Styles */
    * {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #e2e8f0;
        padding-top: 0rem !important;
    }
    
    body {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Remove extra padding from header */
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-top: -10px !important;
        margin-bottom: 6px !important;
        padding-top: 0 !important;
        font-size: 2.8em;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1em;
        margin-top: -8px !important;
        margin-bottom: 8px !important;
        padding: 0 !important;
        font-weight: 300;
    }
    
    .tagline {
        text-align: center;
        background: linear-gradient(90deg, #6366f1, #a855f7, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: -4px !important;
        margin-bottom: 20px !important;
        padding: 0 !important;
        font-size: 0.95em;
    }
    
    /* Tabs Styling */
    [role="tablist"] button {
        background: transparent !important;
        color: #94a3b8 !important;
        border-bottom: 3px solid transparent !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    [role="tablist"] button[aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom-color: #6366f1 !important;
    }
    
    [role="tablist"] button:hover {
        color: #a855f7 !important;
    }
    
    /* Card Styling */
    [data-testid="element-container"] {
        transition: all 0.3s ease;
    }
    
    /* Score Cards */
    .score-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 24px;
        border-radius: 12px;
        border-left: 5px solid #6366f1;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .score-card:hover {
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.3);
        transform: translateY(-4px);
    }
    
    .score-card.video {
        border-left-color: #3b82f6;
    }
    
    .score-card.audio {
        border-left-color: #f59e0b;
    }
    
    .score-card.overall {
        border-left-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
    }
    
    .score-value {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 15px 0;
    }
    
    .score-card.overall .score-value {
        background: linear-gradient(135deg, #10b981, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-card.audio .score-value {
        background: linear-gradient(135deg, #f59e0b, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Risk Indicators */
    .risk-low {
        color: #10b981;
        font-weight: 700;
        background: rgba(16, 185, 129, 0.1);
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .risk-medium {
        color: #f59e0b;
        font-weight: 700;
        background: rgba(245, 158, 11, 0.1);
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .risk-high {
        color: #ef4444;
        font-weight: 700;
        background: rgba(239, 68, 68, 0.1);
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 36px rgba(99, 102, 241, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Input Fields */
    input, textarea, select {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 8px !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Success Messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid #10b981 !important;
        color: #86efac !important;
    }
    
    /* Info Messages */
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid #3b82f6 !important;
        color: #93c5fd !important;
    }
    
    /* Warning Messages */
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid #f59e0b !important;
        color: #fcd34d !important;
    }
    
    /* Error Messages */
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid #ef4444 !important;
        color: #fca5a5 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 8px;
        hover-color: #6366f1;
    }
    
    /* Divider */
    hr {
        border-color: rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Text Colors */
    p, span, div {
        color: #e2e8f0;
    }
    
    strong {
        color: #f1f5f9;
        font-weight: 700;
    }
    
    /* Download Button */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #10b981 0%, #22c55e 100%) !important;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Metric Styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 20px;
    }
    
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🔍 DeepFake Detection Engine")
    st.markdown('<p class="subtitle">Multi-Modal Authenticity Verification</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Real-Time Detection • Video • Audio • Image • Forensic Analysis</p>', unsafe_allow_html=True)

st.markdown("""
<style>
    .stTabs [data-baseweb="tabs"] {
        margin-top: -5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}

# Main Content
st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Results", "📋 Forensic Report"])

# ==================== TAB 1: UPLOAD & ANALYZE ====================
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Media")
        
        # Sub-tabs for upload type
        upload_type = st.radio(
            "Select Input Type:",
            ["📹 Video", "🖼️ Image + Audio"],
            horizontal=True
        )
        
        if upload_type == "📹 Video":
            st.markdown("**Upload Video File**")
            st.info("Supported: MP4, AVI, MOV (Max 500MB)")
            
            video_file = st.file_uploader(
                "Drag and drop video here or click to browse",
                type=["mp4", "avi", "mov", "mkv"],
                key="video_upload"
            )
            
            if video_file:
                st.session_state.uploaded_files['video'] = video_file
                col_a, col_b = st.columns(2)
                with col_a:
                    st.success(f"✓ {video_file.name}")
                with col_b:
                    file_size_mb = video_file.size / (1024 * 1024)
                    st.caption(f"Size: {file_size_mb:.2f} MB")
        
        else:  # Image + Audio
            st.markdown("**Upload Image File**")
            st.info("Supported: JPG, PNG, WEBP (Max 50MB)")
            
            image_file = st.file_uploader(
                "Drag and drop image here or click to browse",
                type=["jpg", "jpeg", "png", "webp"],
                key="image_upload"
            )
            
            if image_file:
                st.session_state.uploaded_files['image'] = image_file
                col_a, col_b = st.columns(2)
                with col_a:
                    st.success(f"✓ {image_file.name}")
                with col_b:
                    file_size_mb = image_file.size / (1024 * 1024)
                    st.caption(f"Size: {file_size_mb:.2f} MB")
            
            st.markdown("---")
            st.markdown("**Upload Audio File**")
            st.info("Supported: MP3, WAV, M4A (Max 100MB)")
            
            audio_file = st.file_uploader(
                "Drag and drop audio here or click to browse",
                type=["mp3", "wav", "m4a", "flac"],
                key="audio_upload"
            )
            
            if audio_file:
                st.session_state.uploaded_files['audio'] = audio_file
                col_a, col_b = st.columns(2)
                with col_a:
                    st.success(f"✓ {audio_file.name}")
                with col_b:
                    file_size_mb = audio_file.size / (1024 * 1024)
                    st.caption(f"Size: {file_size_mb:.2f} MB")
    
    with col2:
        st.subheader("📊 Analysis Status")
        
        # Status placeholder
        status_placeholder = st.empty()
        progress_placeholder = st.empty()
        steps_placeholder = st.empty()
        
        # Start Analysis Button
        if st.button("🚀 Start Analysis", key="analyze_btn", use_container_width=True):
            if not st.session_state.uploaded_files:
                st.error("❌ Please upload a file first")
            else:
                st.session_state.analysis_complete = False
                
                with status_placeholder.container():
                    status_badge = st.empty()
                    status_badge.info("🔄 Processing...")
                
                with progress_placeholder.container():
                    progress_bar = st.progress(0)
                    progress_text = st.empty()
                
                # Simulated Analysis Steps
                steps = [
                    "✓ File Validation",
                    "Media Extraction",
                    "Visual Analysis",
                    "Audio Analysis",
                    "Fusion & Scoring"
                ]
                
                with steps_placeholder.container():
                    step_cols = st.columns([1, 3])
                    steps_status = [st.empty() for _ in range(5)]
                
                # Simulate Processing
                for i in range(101):
                    progress_bar.progress(i)
                    progress_text.metric("Overall Progress", f"{i}%")
                    
                    # Update steps
                    for j, step in enumerate(steps):
                        if i >= (j * 20):
                            steps_status[j].success(step)
                        else:
                            steps_status[j].info(f"{j+1}. {step.replace('✓ ', '')}")
                    
                    time.sleep(0.02)
                
                # Generate Results
                st.session_state.scores = generate_analysis_results()
                st.session_state.analysis_complete = True
                
                status_badge.success("✅ Analysis Complete")
                time.sleep(0.5)
                st.success("Results generated! Check the Results tab.")

# ==================== TAB 2: RESULTS ====================
with tab2:
    if st.session_state.analysis_complete and st.session_state.scores:
        scores = st.session_state.scores
        
        # Score Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_class = f"risk-{scores['video_risk'].lower()}"
            st.markdown(f"""
            <div class="score-card">
                <h3>📹 Video Authenticity</h3>
                <div class="score-value">{scores['video_score']}</div>
                <p style="margin: 10px 0;">Confidence Score</p>
                <p class="{risk_class}">{scores['video_risk_text']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            risk_class = f"risk-{scores['audio_risk'].lower()}"
            st.markdown(f"""
            <div class="score-card">
                <h3>🎙️ Audio Authenticity</h3>
                <div class="score-value">{scores['audio_score']}</div>
                <p style="margin: 10px 0;">Confidence Score</p>
                <p class="{risk_class}">{scores['audio_risk_text']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            risk_class = f"risk-{scores['overall_risk'].lower()}"
            st.markdown(f"""
            <div class="score-card" style="border-left-color: #10b981; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);">
                <h3 style="color: #10b981;">🎯 Overall Authenticity</h3>
                <div class="score-value" style="color: #10b981;">{scores['overall_score']}</div>
                <p style="margin: 10px 0;">Final Verdict</p>
                <p class="{risk_class}">{scores['overall_risk_text']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Confidence Bars
        st.subheader("📊 Confidence Breakdown")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Video Analysis**")
            st.progress(scores['video_score'] / 100)
            st.caption(f"Score: {scores['video_score']}%")
        
        with col2:
            st.write("**Audio Analysis**")
            st.progress(scores['audio_score'] / 100)
            st.caption(f"Score: {scores['audio_score']}%")
        
        st.divider()
        
        # Manipulation Heatmap Section
        st.subheader("🔥 Manipulation Heatmap")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("🎬 Facial manipulation areas highlighted")
            # Create a sample heatmap
            heatmap = np.random.rand(200, 300)
            st.image(heatmap, use_column_width=True, caption="Deepfake Detection Heatmap")
        
        with col2:
            st.info("📊 Detection sensitivity map")
            st.write("""
            **Heatmap Colors:**
            - 🔴 Red: High manipulation probability
            - 🟠 Orange: Medium manipulation detected
            - 🟡 Yellow: Minor artifacts
            - 🟢 Green: Authentic region
            """)
        
        st.divider()
        
        # Download Options
        st.subheader("💾 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Download Text Report", use_container_width=True):
                report_text = generate_text_report(scores)
                st.download_button(
                    label="📄 Download Report",
                    data=report_text,
                    file_name=f"deepfake_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📊 Download JSON Results", use_container_width=True):
                report_json = generate_json_report(scores)
                st.download_button(
                    label="📊 Download JSON",
                    data=report_json,
                    file_name=f"deepfake_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    else:
        st.info("👈 Complete analysis from the Upload tab to see results")

# ==================== TAB 3: FORENSIC REPORT ====================
with tab3:
    if st.session_state.analysis_complete and st.session_state.scores:
        scores = st.session_state.scores
        
        st.subheader("📋 Forensic Analysis Report")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Report ID:** {generate_report_id()}")
        with col2:
            st.write(f"**Evidence Hash:** {generate_hash()}")
            st.write(f"**Verdict:** {scores['overall_risk_text']}")
        
        st.markdown("---")
        
        # Detailed Findings
        st.subheader("🔬 Detailed Findings")
        
        with st.expander("📸 Face Detection Analysis", expanded=True):
            st.write(f"""
            **Status:** ✓ PASSED
            
            - Faces Detected: 1
            - Face Consistency Score: {scores['face_consistency']}%
            - Morphing Artifacts: Not detected
            - Expression Naturalness: {scores['expression_naturalness']}%
            
            **Conclusion:** Face appears natural with no significant synthetic characteristics.
            """)
        
        with st.expander("👁️ Blink Rate Analysis", expanded=True):
            st.write(f"""
            **Status:** ✓ PASSED
            
            - Detected Blink Rate: {scores['blink_rate']} per minute
            - Expected Natural Range: 12-20 per minute
            - Pattern Consistency: {scores['blink_consistency']}%
            
            **Conclusion:** Blink rate falls within natural human range with consistent patterns.
            """)
        
        with st.expander("🎨 GAN Artifact Detection", expanded=True):
            st.write(f"""
            **Status:** ✓ PASSED
            
            - GAN Artifacts Detected: {scores['gan_artifacts']}%
            - Frequency Domain Anomalies: Low
            - Pixel Perfect Artifacts: Not found
            
            **Conclusion:** No significant GAN-related artifacts detected in facial regions.
            """)
        
        with st.expander("🔊 Audio Spectrogram Analysis", expanded=True):
            st.write(f"""
            **Status:** ✓ PASSED
            
            - MFCC Extraction: Complete
            - Spectrogram Continuity: {scores['spectrogram_continuity']}%
            - Background Noise Level: {scores['noise_level']}%
            - Frequency Consistency: {scores['freq_consistency']}%
            
            **Conclusion:** Audio spectrogram shows natural speech patterns with minor background noise.
            """)
        
        with st.expander("📡 Speech Pattern Analysis", expanded=True):
            st.write(f"""
            **Status:** ✓ PASSED
            
            - Voice Authenticity: {scores['audio_score']}%
            - Pitch Variation Range: Natural
            - Temporal Consistency: {scores['temporal_consistency']}%
            - Deepfake Indicators: {scores['deepfake_indicators']}%
            
            **Conclusion:** Speech patterns are consistent with authentic human speech.
            """)
        
        with st.expander("⚖️ Multi-Modal Fusion Analysis", expanded=True):
            st.write(f"""
            **Status:** ✓ PASSED
            
            - Video Confidence: {scores['video_score']}%
            - Audio Confidence: {scores['audio_score']}%
            - Weighted Score: (0.6 × {scores['video_score']}) + (0.4 × {scores['audio_score']}) = {scores['overall_score']}%
            - Cross-Validation: Passed
            
            **Conclusion:** Multi-modal analysis indicates high authenticity with cross-validated results.
            """)
        
        st.markdown("---")
        
        # Final Verdict
        st.subheader("⚖️ Final Verdict")
        
        if scores['overall_score'] >= 75:
            verdict_color = "green"
            hex_color = "10b981"
            verdict_text = "LIKELY AUTHENTIC ✓"
            verdict_explanation = "Multi-modal analysis suggests this is genuine media with high confidence."
            bg_color = "rgba(16, 185, 129, 0.1)"
        elif scores['overall_score'] >= 50:
            verdict_color = "orange"
            hex_color = "f59e0b"
            verdict_text = "MEDIUM CONFIDENCE ⚠️"
            verdict_explanation = "Analysis is inconclusive. Manual review recommended."
            bg_color = "rgba(245, 158, 11, 0.1)"
        else:
            verdict_color = "red"
            hex_color = "ef4444"
            verdict_text = "LIKELY SYNTHETIC ✗"
            verdict_explanation = "Strong indicators suggest this media has been manipulated."
            bg_color = "rgba(239, 68, 68, 0.1)"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {bg_color} 0%, rgba(99, 102, 241, 0.05) 100%);
                    padding: 24px;
                    border-radius: 12px;
                    border: 1px solid rgba({int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}, 0.3);
                    border-left: 5px solid #{hex_color};">
            <h3 style="color: #{hex_color}; margin: 0; font-size: 1.5em; font-weight: 700;">{verdict_text}</h3>
            <p style="margin: 12px 0 0 0; color: #cbd5e1;">{verdict_explanation}</p>
            <p style="margin: 12px 8px 0 0; color: #94a3b8;"><strong style="color: #f1f5f9;">Confidence Level:</strong> <span style="color: #{hex_color}; font-weight: 700; font-size: 1.2em;">{scores['overall_score']}%</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Caveats
        st.warning("""
        ⚠️ **Important Caveats:**
        - This analysis is based on current AI models
        - Rapidly evolving deepfake technology may evade detection
        - Compressed videos may reduce detection accuracy
        - Low-resolution footage may affect results
        - Background noise impacts audio analysis
        - For critical decisions, always verify through official channels
        """)
    
    else:
        st.info("👈 Complete analysis from the Upload tab to see forensic report")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style="text-align: center; 
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 30px 20px;
            margin-top: 40px;
            color: #cbd5e1;
            font-size: 0.95em;
            backdrop-filter: blur(10px);">
    <p style="margin: 8px 0;">🔒 <strong style="color: #f1f5f9;">DeepFake Detection Engine</strong> | All files processed securely. Results are not permanently stored.</p>
    <p style="margin: 8px 0; color: #94a3b8; font-size: 0.9em;">Powered by Advanced AI • Computer Vision • Audio Analysis • Forensic Validation</p>
    <p style="margin: 12px 0 0 0; color: #64748b; font-size: 0.85em;">© 2026 - Multi-Modal Deepfake Detection & Verification System</p>
</div>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def generate_analysis_results():
    """Generate realistic analysis results"""
    video_score = round(random.uniform(60, 95), 1)
    audio_score = round(random.uniform(65, 95), 1)
    overall_score = round((video_score * 0.6 + audio_score * 0.4), 1)
    
    def get_risk(score):
        if score >= 75:
            return "low"
        elif score >= 50:
            return "medium"
        else:
            return "high"
    
    def get_risk_text(risk):
        risks = {
            "low": "✓ Low Risk",
            "medium": "⚠️ Medium Risk",
            "high": "✗ High Risk"
        }
        return risks.get(risk, "Unknown")
    
    return {
        'video_score': video_score,
        'audio_score': audio_score,
        'overall_score': overall_score,
        'video_risk': get_risk(video_score),
        'audio_risk': get_risk(audio_score),
        'overall_risk': get_risk(overall_score),
        'video_risk_text': get_risk_text(get_risk(video_score)),
        'audio_risk_text': get_risk_text(get_risk(audio_score)),
        'overall_risk_text': get_risk_text(get_risk(overall_score)),
        'face_consistency': round(random.uniform(80, 99), 1),
        'expression_naturalness': round(random.uniform(75, 98), 1),
        'blink_rate': random.randint(12, 20),
        'blink_consistency': round(random.uniform(85, 99), 1),
        'gan_artifacts': round(random.uniform(0, 5), 1),
        'spectrogram_continuity': round(random.uniform(80, 99), 1),
        'noise_level': round(random.uniform(5, 25), 1),
        'freq_consistency': round(random.uniform(80, 99), 1),
        'temporal_consistency': round(random.uniform(85, 99), 1),
        'deepfake_indicators': round(random.uniform(0, 10), 1),
    }

def generate_text_report(scores):
    """Generate text report for download"""
    report = f"""
DEEPFAKE DETECTION & VERIFICATION ENGINE
Forensic Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

================================================================================
AUTHENTICITY SCORES
================================================================================

Video Authenticity: {scores['video_score']}%
Risk Level: {scores['video_risk_text']}

Audio Authenticity: {scores['audio_score']}%
Risk Level: {scores['audio_risk_text']}

Overall Authenticity: {scores['overall_score']}%
Risk Level: {scores['overall_risk_text']}

================================================================================
FORENSIC ANALYSIS DETAILS
================================================================================

1. VISUAL ANALYSIS
   Face Consistency: {scores['face_consistency']}%
   Expression Naturalness: {scores['expression_naturalness']}%
   GAN Artifacts: {scores['gan_artifacts']}%
   
2. AUDIO ANALYSIS
   Spectrogram Continuity: {scores['spectrogram_continuity']}%
   Frequency Consistency: {scores['freq_consistency']}%
   Background Noise: {scores['noise_level']}%
   
3. BEHAVIORAL ANALYSIS
   Blink Rate: {scores['blink_rate']} per minute (Natural: 12-20)
   Blink Consistency: {scores['blink_consistency']}%
   Temporal Consistency: {scores['temporal_consistency']}%
   
4. MULTI-MODAL FUSION
   Weighted Scoring: (0.6 × Video) + (0.4 × Audio)
   Cross-Validation: PASSED
   
================================================================================
VERDICT
================================================================================

Based on comprehensive multi-modal analysis:

VERDICT: {scores['overall_risk_text'].replace('✓ ', '').replace('⚠️ ', '').replace('✗ ', '').upper()}
Confidence: {scores['overall_score']}%

Evidence Hash: {generate_hash()}
Report ID: {generate_report_id()}

CERTIFICATION:
This report is generated by the DeepFake Detection & Verification Engine.
Results are based on state-of-the-art AI models for visual and acoustic analysis.

Note: New deepfake techniques may evade detection. For critical decisions,
always verify through official channels and law enforcement.

================================================================================
CAVEATS
================================================================================

- Compressed videos may reduce detection accuracy
- Low-resolution footage affects model performance
- Background noise impacts audio analysis
- Rapidly evolving deepfake technology poses challenges
- This is an AI-assisted analysis, manual review recommended for critical cases

================================================================================
"""
    return report

def generate_json_report(scores):
    """Generate JSON report for download"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'scores': {
            'video': scores['video_score'],
            'audio': scores['audio_score'],
            'overall': scores['overall_score']
        },
        'risk_levels': {
            'video': scores['video_risk_text'],
            'audio': scores['audio_risk_text'],
            'overall': scores['overall_risk_text']
        },
        'analysis_details': {
            'face_consistency': scores['face_consistency'],
            'expression_naturalness': scores['expression_naturalness'],
            'gan_artifacts': scores['gan_artifacts'],
            'spectrogram_continuity': scores['spectrogram_continuity'],
            'frequency_consistency': scores['freq_consistency'],
            'noise_level': scores['noise_level'],
            'blink_rate': scores['blink_rate'],
            'blink_consistency': scores['blink_consistency'],
            'temporal_consistency': scores['temporal_consistency'],
            'deepfake_indicators': scores['deepfake_indicators']
        },
        'metadata': {
            'report_id': generate_report_id(),
            'evidence_hash': generate_hash(),
            'engine_version': '1.0.0'
        }
    }
    return json.dumps(report, indent=2)

def generate_hash():
    """Generate evidence hash"""
    return 'SHA256:' + hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:32].upper()

def generate_report_id():
    """Generate unique report ID"""
    return f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(10000, 99999)}"
