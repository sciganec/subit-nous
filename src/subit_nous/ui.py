"""Streamlit Web UI for SUBIT-NOUS v4.0.0 with dark theme, classifier, knobs, and presets."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from subit_nous.core import text_to_subit, subit_to_name, get_mode, text_to_soft
from subit_nous.agent import run_agent, classify_and_run
from subit_nous.search import search, index_folder
from subit_nous.subit_algebra import Subit

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="SUBIT-NOUS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3498db, #2ecc71, #f1c40f, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .mode-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def soft_to_radar_chart(soft_vec: np.ndarray) -> go.Figure:
    """Create radar chart for 8-bit soft vector."""
    categories = ['b7 (WHO₁)', 'b6 (WHO₂)', 'b5 (WHERE₁)', 'b4 (WHERE₂)',
                  'b3 (WHEN₁)', 'b2 (WHEN₂)', 'b1 (MODE₁)', 'b0 (MODE₂)']
    fig = go.Figure(data=go.Scatterpolar(
        r=soft_vec.tolist(),
        theta=categories,
        fill='toself',
        marker=dict(color='#3498db', size=8),
        line=dict(color='#3498db', width=2)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[-1, 1], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=10))
        ),
        showlegend=False,
        title="SUBIT Soft Vector Profile",
        height=500
    )
    return fig

def get_target_subit(mode: str, who: str) -> Subit:
    """Create Subit object from mode and who selections."""
    mode_map = {"STATE": 2, "VALUE": 3, "FORM": 1, "FORCE": 0}
    who_map = {"ME": 2, "WE": 3, "YOU": 1, "THEY": 0}
    return Subit.from_coords(
        who=who_map.get(who, 2),
        where=2,  # EAST default
        when=2,   # SPRING default
        mode=mode_map.get(mode, 2)
    )

# ----------------------------------------------------------------------
# Dark theme toggle in sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    theme = st.selectbox("🎨 Theme", ["Light", "Dark"], index=0, help="Switch between light and dark theme")
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1e1e2e;
            color: #cdd6f4;
        }
        .stMarkdown, .stText, .stSelectbox, .stSlider, .stButton {
            color: #cdd6f4;
        }
        .main-header {
            background: linear-gradient(90deg, #89b4fa, #a6e3a1, #f9e2af, #cba6f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("🧠 SUBIT‑NOUS")
    st.markdown("### v4.0.0")
    st.markdown("---")

    # Model settings
    st.subheader("⚙️ Model Settings")
    model = st.selectbox(
        "Ollama Model",
        ["llama3.2:3b", "llama3.2:8b", "mistral:7b", "gemma3:12b", "llama3.2:1b"],
        index=0,
        help="Model for agent generation. Larger models = better quality but slower."
    )

    st.markdown("---")

    # Control Panel
    st.subheader("🎮 Control Panel")

    # Presets
    preset = st.selectbox(
        "Quick Presets",
        [
            "Custom",
            "📊 Analyst (STATE/ME)",
            "🎨 Poet (FORM/YOU)",
            "⚡ Leader (FORCE/WE)",
            "🤝 Mediator (VALUE/WE)",
            "🔬 Researcher (STATE/WE)",
            "🎭 Artist (FORM/ME)",
            "🏛️ Strategist (FORCE/THEY)"
        ],
        help="Select a preset to automatically configure MODE and WHO"
    )

    # Handle preset selection
    if preset == "📊 Analyst (STATE/ME)":
        mode_value = "STATE"
        who_value = "ME"
    elif preset == "🎨 Poet (FORM/YOU)":
        mode_value = "FORM"
        who_value = "YOU"
    elif preset == "⚡ Leader (FORCE/WE)":
        mode_value = "FORCE"
        who_value = "WE"
    elif preset == "🤝 Mediator (VALUE/WE)":
        mode_value = "VALUE"
        who_value = "WE"
    elif preset == "🔬 Researcher (STATE/WE)":
        mode_value = "STATE"
        who_value = "WE"
    elif preset == "🎭 Artist (FORM/ME)":
        mode_value = "FORM"
        who_value = "ME"
    elif preset == "🏛️ Strategist (FORCE/THEY)":
        mode_value = "FORCE"
        who_value = "THEY"
    else:
        mode_value = st.selectbox("MODE", ["STATE", "VALUE", "FORM", "FORCE"], index=0,
                                   help="STATE: logical/factual | VALUE: ethical/communal | FORM: aesthetic/emotional | FORCE: willful/strategic")
        who_value = st.selectbox("WHO", ["ME", "WE", "YOU", "THEY"], index=0,
                                  help="ME: first person | WE: collective | YOU: addressing reader | THEY: third person")

    # Display current target
    target = get_target_subit(mode_value, who_value)
    who_coord = target.project("WHO")
    where_coord = target.project("WHERE")
    when_coord = target.project("WHEN")
    mode_coord = target.project("MODE")

    who_display = {2: "ME", 3: "WE", 1: "YOU", 0: "THEY"}.get(who_coord, "?")
    where_display = {2: "EAST", 3: "SOUTH", 1: "WEST", 0: "NORTH"}.get(where_coord, "?")
    when_display = {2: "SPRING", 3: "SUMMER", 1: "AUTUMN", 0: "WINTER"}.get(when_coord, "?")
    mode_display = {2: "STATE", 3: "VALUE", 1: "FORM", 0: "FORCE"}.get(mode_coord, "?")

    st.info(f"🎯 **Target:** {target.to_human()}\n\n`{target.bits:08b}` = {target.bits}\n\n"
            f"- **Mode:** {mode_display}\n"
            f"- **Who:** {who_display}\n"
            f"- **Where:** {where_display}\n"
            f"- **When:** {when_display}")

    st.markdown("---")

    # Search indexing
    st.subheader("📁 Search Index")
    index_path = st.text_input("Folder to index", value="./demo", help="Path to folder containing documents to index")
    if st.button("📇 Index Folder", type="secondary", use_container_width=True):
        with st.spinner(f"Indexing {index_path}..."):
            try:
                count = index_folder(index_path)
                st.success(f"✅ Indexed {count} documents")
                st.session_state['indexed'] = True
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.caption("Built with 🧠 | [GitHub](https://github.com/sciganec/subit-nous)")

# ----------------------------------------------------------------------
# Main header
# ----------------------------------------------------------------------
st.markdown('<div class="main-header">SUBIT‑NOUS</div>', unsafe_allow_html=True)
st.markdown("*Formal algebraic coordinate system for meaning*")

# ----------------------------------------------------------------------
# Tabs (6 tabs)
# ----------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Analyze", "🤖 Agents", "🔎 Search", "📊 Profile", "🎮 Control", "🧠 Classify"
])

# ============================================================
# TAB 1: Analyze
# ============================================================
with tab1:
    st.subheader("Text Analysis")
    st.caption("Analyze text using marker-based SUBIT classification.")
    text_input = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="I think logically about the east in spring..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)

    if analyze_btn and text_input:
        with st.spinner("Analyzing..."):
            subit_id = text_to_subit(text_input)
            name = subit_to_name(subit_id)
            mode = get_mode(subit_id)
            soft = text_to_soft(text_input)

        st.success("Analysis complete!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Archetype ID", subit_id)
        with col2:
            st.metric("Name", name)
        with col3:
            st.metric("Mode", mode or "Mixed")

        st.subheader("Soft Profile (8-bit vector)")
        soft_df = pd.DataFrame({
            "Bit": [f"b{i}" for i in range(8)],
            "Value": soft.tolist()
        })
        st.bar_chart(soft_df.set_index("Bit"))

        fig = soft_to_radar_chart(soft)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: Agents
# ============================================================
with tab2:
    st.subheader("Agent Generation")
    st.caption("Generate or transform text using SUBIT-controlled agents (requires Ollama).")

    agent_text = st.text_area(
        "Input text:",
        height=100,
        placeholder="Write a story about AI...",
        key="agent_text"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        agent_mode = st.selectbox(
            "Agent Mode",
            ["auto", "STATE", "VALUE", "FORM", "FORCE"],
            help="auto – detect mode automatically from text"
        )
    with col2:
        agent_model = st.selectbox(
            "Model",
            ["llama3.2:3b", "llama3.2:8b", "mistral:7b"],
            index=0,
            key="agent_model",
            help="Ollama model for generation"
        )

    if st.button("🤖 Generate", type="primary", use_container_width=True):
        if agent_text:
            with st.spinner(f"Running {agent_mode.upper()} agent..."):
                try:
                    if agent_mode == "auto":
                        result = classify_and_run(agent_text, agent_model)
                        st.info(f"📊 Detected mode: {result['original_mode']} (archetype: {result['original_archetype']})")
                        response = result['agent_response']
                    else:
                        response = run_agent(agent_text, agent_mode, agent_model)

                    st.subheader("📝 Response")
                    st.markdown(f"> {response}")
                except Exception as e:
                    st.error(f"Error: {e}\n\nMake sure Ollama is running and the model is downloaded.")
        else:
            st.warning("Please enter some text")

# ============================================================
# TAB 3: Search
# ============================================================
with tab3:
    st.subheader("Hybrid Search")
    st.caption("Search indexed documents by semantic similarity + SUBIT filter.")

    search_query = st.text_input("Search query:", placeholder="climate change")

    col1, col2 = st.columns(2)
    with col1:
        search_mode = st.selectbox("Mode filter", ["Any", "STATE", "VALUE", "FORM", "FORCE"],
                                    help="Filter by semantic mode")
    with col2:
        search_who = st.selectbox("Who filter", ["Any", "ME", "WE", "YOU", "THEY"],
                                   help="Filter by perspective")

    col1, col2, col3 = st.columns(3)
    with col1:
        top_k = st.slider("Number of results", 1, 20, 10)
    with col2:
        alpha = st.slider("Semantic weight", 0.0, 1.0, 0.5,
                          help="Higher = more semantic similarity, lower = more SUBIT filter")

    if st.button("🔎 Search", type="primary", use_container_width=True):
        if search_query:
            with st.spinner("Searching..."):
                try:
                    results = search(
                        search_query,
                        mode=search_mode if search_mode != "Any" else None,
                        who=search_who if search_who != "Any" else None,
                        top_k=top_k,
                        alpha=alpha
                    )
                except Exception as e:
                    st.error(f"Search error: {e}\n\nMake sure you've indexed a folder first.")
                    results = []

            if results:
                st.success(f"Found {len(results)} results")
                for i, r in enumerate(results, 1):
                    with st.expander(f"{i}. {Path(r['path']).name}"):
                        st.write(f"**Path:** `{r['path']}`")
                        st.write(f"**Score:** {r['score']:.4f}")
                        st.write(f"**Similarity:** {r['similarity']:.4f}")
                        mode_name = {0: "FORCE", 1: "FORM", 2: "STATE", 3: "VALUE"}.get(r['mode'], "?")
                        who_name = {0: "THEY", 1: "YOU", 2: "ME", 3: "WE"}.get(r['who'], "?")
                        st.write(f"**Mode:** {mode_name} | **Who:** {who_name}")
            else:
                st.warning("No results found")
        else:
            st.warning("Please enter a search query")

# ============================================================
# TAB 4: Profile (Radar Chart)
# ============================================================
with tab4:
    st.subheader("Soft Profile Visualization")
    st.caption("Visualize the 8-bit soft vector of any text as a radar chart.")

    profile_text = st.text_area(
        "Enter text to visualize:",
        height=100,
        placeholder="Any text...",
        key="profile_text"
    )

    if st.button("📊 Generate Radar Chart", type="primary", use_container_width=True):
        if profile_text:
            soft = text_to_soft(profile_text)
            fig = soft_to_radar_chart(soft)
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("Raw Values"):
                for i, val in enumerate(soft):
                    st.write(f"**bit{i}:** {val:.4f}")
        else:
            st.warning("Please enter some text")

# ============================================================
# TAB 5: Control Generation (with knobs)
# ============================================================
with tab5:
    st.subheader("Interactive Control Generation")
    st.caption("Adjust knobs to control the semantic style of generated text (requires Ollama).")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎛️ Knobs")
        control_mode = st.selectbox("MODE", ["STATE", "VALUE", "FORM", "FORCE"], key="control_mode",
                                      help="STATE: logical/factual | VALUE: ethical | FORM: artistic | FORCE: strategic")
        control_who = st.selectbox("WHO", ["ME", "WE", "YOU", "THEY"], key="control_who",
                                    help="ME: first person | WE: collective | YOU: reader | THEY: third person")
        control_model = st.selectbox("Model", ["llama3.2:3b", "llama3.2:8b"], key="control_model")

    with col2:
        st.markdown("### 📍 Current Target")
        
        # Показуємо тільки те, що вибрано knobs, без зайвої магії
        mode_display = control_mode
        who_display = control_who
        
        # Обчислюємо біти для інформації
        mode_map = {"STATE": 0b10, "VALUE": 0b11, "FORM": 0b01, "FORCE": 0b00}
        who_map = {"ME": 0b10, "WE": 0b11, "YOU": 0b01, "THEY": 0b00}
        
        who_bits = who_map.get(control_who, 0b10)
        where_bits = 0b10  # EAST
        when_bits = 0b10   # SPRING
        mode_bits = mode_map.get(control_mode, 0b10)
        
        bits = (who_bits << 6) | (where_bits << 4) | (when_bits << 2) | mode_bits
        
        st.info(f"**{control_mode} / {control_who}**\n\n"
                f"`{bits:08b}` = {bits}\n\n"
                f"- **Mode:** {control_mode}\n"
                f"- **Who:** {control_who}\n"
                f"- **Where:** EAST (default)\n"
                f"- **When:** SPRING (default)")

    control_text = st.text_area(
        "Input text to transform:",
        height=100,
        placeholder="Solar energy is good for the environment...",
        key="control_text"
    )

    if st.button("🎮 Generate", type="primary", use_container_width=True):
        if control_text:
            with st.spinner(f"Generating in {control_mode}/{control_who} mode..."):
                try:
                    from subit_nous.control import apply_subit
                    response = apply_subit(control_text, target, control_model)
                    st.subheader("📝 Result")
                    st.markdown(f"> {response}")
                except Exception as e:
                    st.error(f"Error: {e}\n\nMake sure Ollama is running: `ollama serve`")
        else:
            st.warning("Please enter some text")

# ============================================================
# TAB 6: Classify (Neural Classifier)
# ============================================================
with tab6:
    st.subheader("Neural SUBIT Classifier")
    st.caption("Predict SUBIT archetype using fine-tuned DistilBERT (80-85% accuracy).")

    model_path = Path("./subit_model")
    model_available = model_path.exists() and (model_path / "config.json").exists()

    if not model_available:
        st.warning("⚠️ Classifier model not found. Training in progress or not started yet.")
        st.info("📌 Train the classifier with:\n```bash\npython scripts/train_classifier.py\n```")

        st.markdown("---")
        st.markdown("### 🔄 Fallback Mode (Marker-based)")
        st.caption("Using rule-based classification while model trains.")

        classify_text_input = st.text_area(
            "Enter text to classify (fallback mode):",
            height=100,
            placeholder="I think logically about the east in spring...",
            key="classify_fallback_text"
        )

        if st.button("🔍 Classify (Fallback)", type="primary", use_container_width=True, key="classify_fallback_btn"):
            if classify_text_input:
                subit_id = text_to_subit(classify_text_input)
                name = subit_to_name(subit_id)
                mode = get_mode(subit_id)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("SUBIT ID", subit_id)
                with col2:
                    st.metric("Archetype", name)
                with col3:
                    st.metric("Mode", mode or "Mixed")

                st.code(f"Bits: {subit_id:08b}", language="text")
            else:
                st.warning("Please enter some text")
    else:
        st.success("✅ Classifier model loaded! Using fine-tuned DistilBERT.")

        classify_text_input = st.text_area(
            "Enter text to classify:",
            height=100,
            placeholder="I think logically about the east in spring...",
            key="classify_text"
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            return_probs = st.checkbox("Show probabilities", value=False,
                                        help="Show top 5 predictions with confidence scores")
        with col2:
            classify_btn = st.button("🧠 Classify", type="primary", use_container_width=True)

        if classify_btn and classify_text_input:
            try:
                from subit_nous.classifier import SubitClassifier

                with st.spinner("Classifying..."):
                    classifier = SubitClassifier("./subit_model")
                    result = classifier.classify(classify_text_input, return_probs=return_probs)

                st.success("Classification complete!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("SUBIT ID", result['subit'])
                with col2:
                    name_short = result['archetype'][:20] + "..." if len(result['archetype']) > 20 else result['archetype']
                    st.metric("Archetype", name_short)
                with col3:
                    st.metric("Mode", result['mode'])

                st.subheader("Binary Representation")
                bits = result['bits']
                cols = st.columns(8)
                for i, (col, bit) in enumerate(zip(cols, bits)):
                    color = "#2ecc71" if bit == "1" else "#95a5a6"
                    col.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: {color};'>{bit}</div>", unsafe_allow_html=True)
                    col.caption(f"b{7-i}")
                st.caption("b7-b6: WHO | b5-b4: WHERE | b3-b2: WHEN | b1-b0: MODE")

                st.subheader("Coordinates")
                coord_cols = st.columns(4)
                with coord_cols[0]:
                    st.metric("WHO", result['who'])
                with coord_cols[1]:
                    st.metric("WHERE", result['where'])
                with coord_cols[2]:
                    st.metric("WHEN", result['when'])
                with coord_cols[3]:
                    st.metric("MODE", result['mode'])

                if return_probs and "top_classes" in result:
                    st.subheader("Top Predictions")
                    prob_data = []
                    for i, (idx, prob) in enumerate(result["top_classes"], 1):
                        from subit_nous.core import subit_to_name
                        prob_data.append({
                            "Rank": i,
                            "SUBIT": idx,
                            "Archetype": subit_to_name(idx),
                            "Confidence": f"{prob:.2%}"
                        })
                    st.dataframe(prob_data, use_container_width=True)

                    df = pd.DataFrame({
                        "Archetype": [subit_to_name(idx)[:20] for idx, _ in result["top_classes"][:5]],
                        "Confidence": [prob for _, prob in result["top_classes"][:5]]
                    })
                    fig = px.bar(df, x="Archetype", y="Confidence", title="Confidence Distribution")
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Classification error: {e}")
                st.info("Make sure the model is trained. Run: `python scripts/train_classifier.py`")
        elif classify_btn and not classify_text_input:
            st.warning("Please enter some text")

# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<center><small>SUBIT‑NOUS v4.0.0 — Formal algebraic coordinate system for meaning | "
    "<a href='https://github.com/sciganec/subit-nous' target='_blank'>GitHub</a> | "
    "<a href='https://pypi.org/project/subit-nous' target='_blank'>PyPI</a> | "
    "<a href='https://github.com/sciganec/subit-nous/blob/main/SUBIT_v3.md' target='_blank'>Specification</a></small></center>",
    unsafe_allow_html=True
)