"""Streamlit Web UI for SUBIT-NOUS"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import os

# Додаємо src до шляху, щоб імпорти працювали
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Тепер імпортуємо як звичайний модуль (без крапки)
from subit_nous.core import text_to_subit, subit_to_name, get_mode, text_to_soft
from subit_nous.agent import run_agent, classify_and_run
from subit_nous.search import search, index_folder

# Функція для радарної діаграми (додаємо локально, щоб уникнути залежностей)
def soft_to_radar_chart(soft_vec: np.ndarray) -> go.Figure:
    """Створює радарну діаграму для 8-бітного soft-вектора."""
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

# Сторінка конфігурації
st.set_page_config(
    page_title="SUBIT-NOUS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS для кращого вигляду
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
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🧠 SUBIT‑NOUS")
    st.markdown("### v3.0")
    st.markdown("---")
    
    # Налаштування моделі
    st.subheader("⚙️ Settings")
    model = st.selectbox(
        "Ollama Model",
        ["llama3.2:3b", "llama3.2:8b", "mistral:7b", "gemma3:12b"],
        index=0
    )
    
    # Індекс для пошуку
    st.markdown("---")
    st.subheader("📁 Search Index")
    index_path = st.text_input("Folder to index", value="./demo")
    if st.button("📇 Index Folder", type="secondary"):
        with st.spinner(f"Indexing {index_path}..."):
            count = index_folder(index_path)
            st.success(f"Indexed {count} documents")
            st.session_state['indexed'] = True

# Головна сторінка
st.markdown('<div class="main-header">SUBIT‑NOUS</div>', unsafe_allow_html=True)
st.markdown("*Formal algebraic coordinate system for meaning*")

# Таби
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Analyze", "🤖 Agents", "🔎 Search", "📊 Profile"])

# ============================================================
# TAB 1: Analyze
# ============================================================
with tab1:
    st.subheader("Text Analysis")
    text_input = st.text_area("Enter text to analyze:", height=150, placeholder="I think logically about the east...")
    
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
        
        # Soft profile
        st.subheader("Soft Profile (8-bit vector)")
        soft_df = pd.DataFrame({
            "Bit": [f"b{i}" for i in range(8)],
            "Value": soft.tolist()
        })
        st.bar_chart(soft_df.set_index("Bit"))
        
        # Radar chart
        fig = soft_to_radar_chart(soft)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: Agents
# ============================================================
with tab2:
    st.subheader("Agent Generation")
    
    agent_text = st.text_area("Input text:", height=100, placeholder="Write a story about AI...", key="agent_text")
    
    agent_mode = st.selectbox(
        "Select Mode",
        ["auto", "STATE", "VALUE", "FORM", "FORCE"],
        help="auto – detect mode automatically"
    )
    
    if st.button("🤖 Generate", type="primary", use_container_width=True):
        if agent_text:
            with st.spinner(f"Running {agent_mode.upper()} agent..."):
                if agent_mode == "auto":
                    result = classify_and_run(agent_text, model)
                    st.info(f"Detected mode: {result['original_mode']}")
                    response = result['agent_response']
                else:
                    response = run_agent(agent_text, agent_mode, model)
            
            st.subheader("Response")
            st.markdown(f"> {response}")
        else:
            st.warning("Please enter some text")

# ============================================================
# TAB 3: Search
# ============================================================
with tab3:
    st.subheader("Hybrid Search")
    
    search_query = st.text_input("Search query:", placeholder="climate change")
    
    col1, col2 = st.columns(2)
    with col1:
        search_mode = st.selectbox("Mode filter", ["Any", "STATE", "VALUE", "FORM", "FORCE"])
    with col2:
        search_who = st.selectbox("Who filter", ["Any", "ME", "WE", "YOU", "THEY"])
    
    top_k = st.slider("Number of results", 1, 20, 10)
    alpha = st.slider("Semantic weight (alpha)", 0.0, 1.0, 0.5, help="Higher = more semantic similarity")
    
    if st.button("🔎 Search", type="primary", use_container_width=True):
        if search_query:
            with st.spinner("Searching..."):
                results = search(
                    search_query,
                    mode=search_mode if search_mode != "Any" else None,
                    who=search_who if search_who != "Any" else None,
                    top_k=top_k,
                    alpha=alpha
                )
            
            if results:
                st.success(f"Found {len(results)} results")
                for i, r in enumerate(results, 1):
                    with st.expander(f"{i}. {Path(r['path']).name}"):
                        st.write(f"**Path:** {r['path']}")
                        st.write(f"**Score:** {r['score']:.3f}")
                        st.write(f"**Similarity:** {r['similarity']:.3f}")
                        st.write(f"**Mode:** {['FORCE','FORM','STATE','VALUE'][r['mode']] if r['mode'] in [0,1,2,3] else '?'}")
                        st.write(f"**Who:** {['THEY','YOU','ME','WE'][r['who']] if r['who'] in [0,1,2,3] else '?'}")
            else:
                st.warning("No results found")
        else:
            st.warning("Please enter a search query")

# ============================================================
# TAB 4: Profile
# ============================================================
with tab4:
    st.subheader("Soft Profile Visualization")
    
    profile_text = st.text_area("Enter text to visualize:", height=100, placeholder="Any text...", key="profile_text")
    
    if st.button("📊 Generate Radar Chart", type="primary", use_container_width=True):
        if profile_text:
            soft = text_to_soft(profile_text)
            fig = soft_to_radar_chart(soft)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Raw Values")
            for i, val in enumerate(soft):
                st.write(f"**bit{i}:** {val:.3f}")
        else:
            st.warning("Please enter some text")

# Footer
st.markdown("---")
st.markdown(
    "<center><small>SUBIT‑NOUS v3.0 — Formal algebraic coordinate system for meaning</small></center>",
    unsafe_allow_html=True
)