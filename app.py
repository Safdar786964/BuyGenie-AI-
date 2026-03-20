import streamlit as st
from openai import OpenAI
import os
import requests

# 1. Premium Page Configuration
st.set_page_config(
    page_title="BuyGenie AI - Smart Shopping Assistant",
    page_icon="⚡",
    layout="wide"
)

# 2. Custom CSS for Premium Design
st.markdown("""
<style>
/* Main Layout */
.stApp {
    background-color: #f8f9fa;
    font-family: 'Inter', sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #eee;
}

/* Fix CSS Leak - Ensure all styles are here */
.product-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #eee;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.insight-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #3d3d3d 100%);
    color: white;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
    border: 1px solid #444;
}

/* Sidebar Founder Image */
[data-testid="stSidebar"] [data-testid="stImage"] img {
    border-radius: 50% !important;
    border: 4px solid #1a1a1a !important;
    margin-bottom: 5px !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

/* App Description Text */
.app-desc {
    text-align: center;
    font-size: 13px;
    color: #666;
    margin-bottom: 30px;
    padding: 0 10px;
    font-style: italic;
}.founder-name {
    text-align: center;
    font-weight: 800;
    font-size: 12px;
    color: #1a1a1a;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# Branding Header
st.markdown("""
<div style='text-align: center; padding: 10px 0 30px 0;'>
    <h1 style='font-size: 42px; font-weight: 800; color: #1a1a1a; margin-bottom: 10px;'>⚡ BUYGENIE AI</h1>
    <p style='font-size: 18px; color: #555; max-width: 800px; margin: 0 auto; line-height: 1.6; font-weight: 400;'>
        BuyGenie AI transforms shopping decisions with AI-powered insights, product comparisons, and budget-based recommendations.
    </p>
</div>
""", unsafe_allow_html=True)

# 3. Sidebar for Settings
try:
    default_api_key = st.secrets.get("HUGGING_FACE_API_KEY", os.environ.get("HUGGING_FACE_API_KEY", ""))
except Exception:
    default_api_key = os.environ.get("HUGGING_FACE_API_KEY", "")

with st.sidebar:
    # Founder Branding Section
    if os.path.exists("founder.png"):
        st.image("founder.png", width=150)
        st.markdown('<div class="founder-name">Founder & Lead Dev</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                <div style="width:120px; height:120px; background:#ddd; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#666; font-size:12px; border:4px solid #1a1a1a;">
                    LOGOTYPE
                </div>
                <div class="founder-name" style="margin-top:10px;">Founder & Lead Dev</div>
            </div>
        """, unsafe_allow_html=True)

    # Product Description (Requested)
    st.markdown("""
    <div class="app-desc">
        <b>BuyGenie AI:</b> Your 24/7 Smart Shopping Partner & Real-Time Market Analyst.
    </div>
    """, unsafe_allow_html=True)

    st.header("⚙️ Settings")
    api_key = st.text_input("Hugging Face API Key:", value=default_api_key, type="password")
    model_choice = st.selectbox(
        "Choose AI Model:",
        [
            "meta-llama/Llama-3.3-70B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "google/gemma-2-9b-it"
        ],
        index=0
    )
    
    st.divider()
    st.markdown("### 📊 Market Pulse")
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Momentum", "84%", "+2%")
    col_m2.metric("Sentiment", "High", "Bull")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 4. Navigation Tabs
tab_discover, tab_compare, tab_budget, tab_assistant = st.tabs([
    "🔍 Discover", "⚖️ Compare", "💰 Budget", "🤖 Assistant"
])

# --- BUDGET TAB ---
with tab_budget:
    st.markdown("<h2 style='font-weight: 800; margin-bottom: 20px;'>BUDGET PLANNER</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="planner-card">
            <div class="planner-title">Smart Budget Recommendations</div>
            <div class="planner-subtitle">Tell us your budget and what you're looking for. Our AI will find the best value for your money.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input Row for the Budget Planner
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col1:
        budget_val = st.text_input("Budget", value="$ 100")
    with col2:
        category_val = st.selectbox("Category", ["Smartphones", "Laptops", "Headphones", "Gaming", "Wearables"])
    with col3:
        st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) # Spacer
        find_button = st.button("✨ Find Best Value", use_container_width=True)

    if find_button:
        if not api_key:
            st.warning("Please add your Hugging Face API Key in the sidebar.")
        else:
            with st.spinner(f"Genie is searching for the best {category_val} under {budget_val}..."):
                try:
                    client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
                    
                    system_prompt = "You are a professional shopping assistant. Provide a detailed, premium-looking recommendation list for products in the given category and budget. Format your response with markdown, using bold titles, bullet points, and clear pros/cons for each recommendation."
                    user_prompt = f"Find the best 3-5 {category_val} products available for a budget of {budget_val}. Include specific models if possible and explain why they are good choices for this price range."
                    
                    completion = client.chat.completions.create(
                        model=model_choice,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        stream=False
                    )
                    
                    recommendation = completion.choices[0].message.content
                    st.success("Results Found!")
                    
                    # Displaying with Images logic
                    st.markdown("### 📋 Recommended Picks")
                    
                    # We'll show a beautiful image for the category
                    st.image(f"https://loremflickr.com/800/300/{category_val.lower()},tech", caption=f"Top Rated {category_val} in 2026", use_container_width=True)
                    
                    st.markdown(recommendation)
                    
                except Exception as e:
                    st.error(f"Error: {e}")

# --- ASSISTANT TAB ---
with tab_assistant:
    st.markdown("### 🤖 Your AI Shopping Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about shopping..."):
        if not api_key:
            st.warning("Please add your Hugging Face API Key in the sidebar.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                try:
                    with st.spinner("Genie is thinking..."):
                        completion = client.chat.completions.create(
                            model=model_choice,
                            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                            stream=True
                        )
                        for chunk in completion:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                response_placeholder.markdown(full_response + "▌")
                        response_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Error: {e}")

            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Placeholder Tabs ---
with tab_discover:
    st.markdown("<h2 style='font-weight: 800; margin-bottom: 10px;'>🔥 DISCOVER TRENDS</h2>", unsafe_allow_html=True)
    
    # AI Trend Analysis Section
    st.container()
    if api_key:
        try:
            with st.status("Generating Daily Insight...", expanded=False) as status:
                client_disc = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
                insight_prompt = "Provide a 3-sentence summary of the most exciting consumer tech trend for 2026 (e.g., AI-integrated wearables, sustainable folding phones). Make it sound professional and visionary."
                insight_resp = client_disc.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": insight_prompt}],
                    stream=False
                )
                daily_insight = insight_resp.choices[0].message.content
                status.update(label="Insight Ready!", state="complete", expanded=False)
            
            st.markdown(f"""
                <div class="insight-box">
                    <h3 style='margin:0; font-size: 20px; color: #ffcc00;'>✨ Genie's Daily Insight</h3>
                    <p style='margin-top: 10px; font-size: 15px; line-height: 1.6; color: #ddd;'>{daily_insight}</p>
                </div>
            """, unsafe_allow_html=True)
        except:
            st.info("Genie's Forecast: Sustainable tech and AI-assisted shopping are dominating the market landscape today.")
    else:
        st.markdown("""
            <div class="insight-box">
                <h3 style='margin:0; font-size: 20px; color: #ffcc00;'>✨ Genie's Daily Insight</h3>
                <p style='margin-top: 10px; font-size: 15px; line-height: 1.6; color: #ddd;'>Add your API key to unlock real-time market insights from the AI.</p>
            </div>
        """, unsafe_allow_html=True)

    # Fetch products from Fake Store API
    try:
        response = requests.get('https://fakestoreapi.com/products?limit=6')
        products = response.json()
        
        st.markdown("### 📈 Trending Products")
        cols = st.columns(3)
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.markdown(f"""
                    <div style='background: white; padding: 20px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px; transition: transform 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.05);'>
                        <img src='{product["image"]}' style='width: 100%; height: 180px; object-fit: contain; display: block; margin-left: auto; margin-right: auto; margin-bottom: 15px;'>
                        <h4 style='font-size: 14px; color: #1a1a1a; height: 35px; overflow: hidden; font-weight: 700; margin-bottom: 10px;'>{product["title"]}</h4>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='font-size: 16px; font-weight: 800; color: #2ecc71;'>${product["price"]}</span>
                            <span style='background: #f8f9fa; color: #666; padding: 3px 8px; border-radius: 20px; font-size: 10px; border: 1px solid #eee;'>{product["category"].upper()}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("AI Pulse", key=f"pulse_{product['id']}", use_container_width=True):
                    with st.expander("🔮 Market Analysis", expanded=True):
                        if not api_key:
                            st.warning("Needs API Key.")
                        else:
                            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
                            pulse_resp = client.chat.completions.create(
                                model=model_choice,
                                messages=[{"role": "user", "content": f"Briefly explain why '{product['title']}' is a trend-setter."}],
                                stream=False
                            )
                            st.write(pulse_resp.choices[0].message.content)

    except Exception as e:
        st.error(f"Feed error: {e}")
with tab_compare:
    st.title("Compare")
    st.info("Side-by-side product comparison tool is under maintenance.")
