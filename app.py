# 3. Sidebar for Settings (Production Ready - No Manual Input)

def get_api_key():
    """Fetch API key ONLY from Streamlit secrets."""
    try:
        return st.secrets["HUGGING_FACE_API_KEY"]
    except KeyError:
        return None

api_key = get_api_key()

with st.sidebar:
    # --- Founder Branding Section ---
    if os.path.exists("founder.png"):
        st.image("founder.png", width=150)
        st.markdown('<div class="founder-name">Founder & Lead Dev</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; margin-bottom:20px;">
            <div style="
                width:120px;
                height:120px;
                background:#ddd;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:12px;
                border:4px solid #1a1a1a;">
                YOUR LOGO
            </div>
            <div class="founder-name" style="margin-top:10px;">
                Founder & Lead Dev
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- Settings ---
    st.header("⚙️ Settings")

    # ✅ Show status instead of input
    if api_key:
        st.success("✅ AI Connected")
    else:
        st.error("❌ API Key Missing (Check Streamlit Secrets)")

    # --- Model Selection ---
    model_choice = st.selectbox(
        "🧠 Select AI Model",
        [
            "meta-llama/Llama-3.3-70B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "google/gemma-2-9b-it"
        ]
    )

    st.divider()
