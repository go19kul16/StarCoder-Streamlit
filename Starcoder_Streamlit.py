import streamlit as st
import requests

# Hugging Face Inference API details
API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Function to query Hugging Face API
def query_huggingface_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

# --- Streamlit Page Config ---
st.set_page_config(page_title="StarCoder Code Generator", page_icon="🪐", layout="wide")

# --- Custom CSS for Button Style ---
st.markdown("""
    <style>
    .stButton>button {
        background-color: #6C63FF;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #5a54d1;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title & Intro Section ---
st.title("🚀 StarCoder Code Generator")
st.markdown("### Generate code using [BigCode's StarCoder](https://huggingface.co/bigcode/starcoder) via Hugging Face API!")

st.markdown("---")

# --- Tabs for a Better Layout ---
tab1, tab2 = st.tabs(["💡 Generate Code", "ℹ️ About"])

# --- Tab 1: Generate Code ---
with tab1:
    st.header("💬 Enter Your Prompt")

    user_input = st.text_area("What code do you need?", height=200, placeholder="Describe the code you want StarCoder to generate...")

    col1, col2 = st.columns([1, 3])

    with col1:
        max_tokens = st.slider("Max Tokens", min_value=50, max_value=500, value=200, step=50)

    with col2:
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

    generate_btn = st.button("✨ Generate Code!")

    if generate_btn:
        if not user_input:
            st.warning("⚠️ Please enter a prompt first!")
        else:
            with st.spinner("Generating... 🛠️"):
                payload = {
                    "inputs": user_input,
                    "parameters": {
                        "max_new_tokens": max_tokens,
                        "temperature": temperature,
                    }
                }

                result = query_huggingface_api(payload)

                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    generated_text = result[0]['generated_text']
                    st.success("✅ Code generated successfully!")
                    st.code(generated_text, language="python")

# --- Tab 2: About ---
with tab2:
    st.header("ℹ️ About StarCoder & This App")
    st.markdown("""
    - **StarCoder** is an open-source large language model specialized in code generation and understanding.
    - Developed by **BigCode** (Hugging Face + ServiceNow).
    - This app calls the **Hugging Face Inference API** to generate code based on your prompt.
    
    **How It Works**:
    1. Enter your prompt (describe the code you need).
    2. Click **Generate Code**.
    3. Wait for the AI magic! ✨
    
    **Technologies Used**:
    - Streamlit (Frontend UI)
    - Hugging Face Inference API (Model backend)
    """)




