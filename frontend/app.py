import streamlit as st
import requests
import time
import random

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SCIBUDDY",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- VIBRANT GLASS THEME ---
st.markdown("""
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
        background: rgba(255, 255, 255, 0.8);
    }
    
    /* Rank Specific Accents */
    .rank-Explorer { border-top: 5px solid #00b894; color: #00b894; }
    .rank-Cadet { border-top: 5px solid #0984e3; color: #0984e3; }
    .rank-Associate { border-top: 5px solid #6c5ce7; color: #6c5ce7; }
    .rank-Fellow { border-top: 5px solid #e17055; color: #e17055; }

    /* Headings */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #0984e3, #6c5ce7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: #2d3436;
        font-weight: 600;
    }

    /* Buttons - Gradient Popping */
    .stButton > button {
        font-family: 'Poppins', sans-serif;
        background: white;
        color: #2d3436;
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s;
        background-size: 200% auto;
    }
    .stButton > button:hover {
        background-position: right center;
        transform: scale(1.05);
        color: white;
        background-image: linear-gradient(to right, #00c6ff 0%, #0072ff 51%, #00c6ff 100%);
        box-shadow: 0 6px 12px rgba(0,114,255,0.3);
    }
    
    /* Delete Button */
    button[key^="del_"] {
        color: #d63031 !important;
    }
    button[key^="del_"]:hover {
        background-image: linear-gradient(to right, #ff416c 0%, #ff4b1f 51%, #ff416c 100%) !important;
        box-shadow: 0 4px 10px rgba(255, 75, 31, 0.4) !important;
    }

    /* Chat Bubbles */
    .chat-user {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 18px 18px 0 18px;
        margin-bottom: 12px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2);
    }
    .chat-bot {
        background: white;
        color: #2d3436;
        padding: 16px 20px;
        border-radius: 18px 18px 18px 0;
        margin-bottom: 12px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.5);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Input */
    .stTextInput > div > div > input {
        border-radius: 15px;
        padding: 12px;
        border: 2px solid transparent;
        background: rgba(255,255,255,0.8);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6c5ce7;
        box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.1);
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([1, 8])
with c1:
    st.image("https://img.icons8.com/fluency/96/science.png", width=80) 
with c2:
    st.markdown("<h1>SCIBUDDY</h1>", unsafe_allow_html=True)
    st.markdown("### *Explore. Discover. Create.*", unsafe_allow_html=True)

# --- STATE & DATA ---
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "student_class" not in st.session_state:
    st.session_state.student_class = None

# Extended Prompt Database (Same as before)
PROMPTS_POOL = {
    "Junior Explorer": [
        "🍃 Why do leaves change color?", "🦖 Why did dinos die out?", "🌧️ How does rain happen?", "🧲 How magnets stick?",
        "☀️ Is the sun on fire?", "🐝 Do bees sleep?", "🌊 Why is ocean salty?", "🦠 What are germs?",
        "🌈 How to make a rainbow?", "🦴 What are bones made of?", "🌑 Where does moon go?", "🌋 Do volcanoes sleep?",
        "🚀 How do rockets fly?", "🕷️ Why spiders spin webs?", "❄️ Are all snowflakes different?", "🎈 Why balloons float?"
    ],
    "Science Cadet": [
        "⚛️ What is an atom?", "🌋 Plate Tectonics explained", "🦠 How vaccines fight virus", "⚡ Static electricity fun",
        "🧬 DNA basics", "🔭 Telescope optics", "🌡️ Solids liquids gases", "🧪 Acid vs Base test",
        "🌬️ Wind energy physics", "💡 Circuit basics", "🎢 Rollercoaster physics", "🌌 What is a galaxy?",
        "🚜 How engines work", "🩸 White blood cells job", "🌲 Photosynthesis steps", "♻️ Recycling chemistry"
    ],
    " রিসার্চ Associate": [ # Research Associate
        "🧬 DNA Replication steps", "🍏 Newton's 3 Laws", "🧪 Covalent vs Ionic bonds", "🌌 Black Hole Event Horizon",
        "⚡ AC vs DC Current", "🦠 Antibiotic Resistance", "☢️ Radioactive Half-life", "🪐 Kepler's Laws",
        "🦾 Enzyme Catalysis", "🌫️ Greenhouse Effect details", "🌊 Thermodynamics 1st Law", "📉 Probability in Genetics"
    ],
    "Innovation Fellow": [
        "🔬 CRISPR Editing mechanism", "🧠 Quantum Superposition", "🚀 Ion Propulsion Engines", "♻️ Carbon Capture Tech",
        "🕸️ Neural Networks described", "☀️ Nuclear Fusion hurdles", "🌌 Dark Matter evidence", "🧬 Epigenetics markers",
        "🤖 Turing Test validity", "🔋 Solid State Batteries", "🦠 mRNA Vaccine tech", "📐 Relativity: Time Dilation"
    ]
}
RANK_KEY_MAP = {"Research Associate": " রিসার্চ Associate"}

def get_prompts(rank):
    key = RANK_KEY_MAP.get(rank, rank)
    pool = PROMPTS_POOL.get(key, PROMPTS_POOL["Junior Explorer"])
    return random.sample(pool, min(4, len(pool)))

# --- SIDEBAR (MISSION LOG) ---
with st.sidebar:
    st.markdown("## 🕹️ Controls")
    
    if st.button("➕ New Mission", use_container_width=True):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.student_class = None
        st.rerun()

    st.markdown("---")
    st.markdown("## 📜 Mission Log")
    
    try:
        response = requests.get(f"{API_URL}/sessions", timeout=2)
        if response.status_code == 200:
            sessions = response.json()
            if not sessions:
                st.caption("No archives found.")
            
            for s in sessions[:8]: 
                r_name = s['student_class'].split(' ')[-1]
                
                # Dynamic Icon based on rank
                if "Explorer" in r_name: ico = "🌿"
                elif "Cadet" in r_name: ico = "⚡"
                elif "Associate" in r_name: ico = "🧬"
                elif "Fellow" in r_name: ico = "🚀"
                else: ico = "💠"
                
                label = f"{ico} {r_name} #{s['id']}"
                
                c1, c2 = st.columns([4, 1])
                with c1:
                    if st.button(label, key=f"sess_{s['id']}", use_container_width=True):
                        st.session_state.session_id = s['id']
                        st.session_state.student_class = s['student_class']
                        hist_res = requests.get(f"{API_URL}/history/{s['id']}")
                        if hist_res.status_code == 200:
                            st.session_state.messages = hist_res.json()
                        st.rerun()
                with c2:
                    if st.button("🗑️", key=f"del_{s['id']}"):
                        requests.delete(f"{API_URL}/sessions/{s['id']}")
                        st.rerun()
    except:
        st.error("Network Error")

# --- SELECTION SCREEN ---
if not st.session_state.session_id and not st.session_state.student_class:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2d3436; margin-bottom: 30px;'>Select Your Grade</h2>", unsafe_allow_html=True)
    
    ranks = [
        {"rank": "Junior Explorer", "color": "Explorer", "icon": "🌿", "desc": "Curious & Brave (5th-6th)"},
        {"rank": "Science Cadet", "color": "Cadet", "icon": "⚡", "desc": "Ready to Learn (7th-8th)"},
        {"rank": "Research Associate", "color": "Associate", "icon": "🧬", "desc": "Deep Analysis (9th-10th)"},
        {"rank": "Innovation Fellow", "color": "Fellow", "icon": "🚀", "desc": "Visionary (11th-12th)"}
    ]
    
    cols = st.columns(4)
    for i, r in enumerate(ranks):
        with cols[i]:
            # Colorful Glass Card
            st.markdown(f"""
            <div class="glass-card rank-{r['color']}">
                <div style="font-size: 3.5em; margin-bottom: 15px;">{r['icon']}</div>
                <h3 style="margin-bottom: 8px;">{r['rank']}</h3>
                <p style="color: #636e72; font-size: 0.9em;">{r['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button
            if st.button(f"Start {r['rank']}", key=f"btn_{i}", use_container_width=True):
                 try:
                    res = requests.post(f"{API_URL}/sessions", json={"student_class": r['rank']})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.session_id = data["id"]
                        st.session_state.student_class = data["student_class"]
                        st.session_state.messages.append({"role": "model", "content": f"**Access Granted.** Welcome, {r['rank']}! \n*System initialized. Ready for input.*"})
                        st.session_state.current_prompts = get_prompts(r['rank'])
                        st.rerun()
                    else:
                         st.error("Server Error")
                 except Exception as e:
                     st.error(f"Connection Error: {e}")

# --- CHAT INTERFACE ---
else:
    # Top Bar - Colorful Pill
    rank_color = "#636e72"
    if "Explorer" in st.session_state.student_class: rank_color = "#00b894" # Green
    elif "Cadet" in st.session_state.student_class: rank_color = "#0984e3" # Blue
    elif "Associate" in st.session_state.student_class: rank_color = "#6c5ce7" # Purple
    elif "Fellow" in st.session_state.student_class: rank_color = "#e17055" # Orange

    st.markdown(f"""
    <div style="
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 25px; background: rgba(255,255,255,0.8); backdrop-filter: blur(10px);
        padding: 15px 30px; border-radius: 50px; border: 1px solid white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    ">
        <div style="display:flex; align-items:center;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: {rank_color}; margin-right: 15px; box-shadow: 0 0 10px {rank_color};"></div>
            <span style="font-weight: 700; color: #2d3436; font-size: 1.1em; letter-spacing: 0.5px;">{st.session_state.student_class.upper()}</span>
        </div>
        <div style="color: #b2bec3; font-weight: 600; font-family: monospace;">SESSION ID: {st.session_state.session_id}</div>
    </div>
    """, unsafe_allow_html=True)

    # Messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role, avatar="🧑‍🔬" if role=="user" else "🤖"):
            st.markdown(f'<div class="chat-{"user" if role=="user" else "bot"}">{content}</div>', unsafe_allow_html=True)

    # Input and Logic
    if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
    else:
        prompt = st.chat_input("Type your question here...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🔬"):
            st.markdown(f'<div class="chat-user">{prompt}</div>', unsafe_allow_html=True)

        with st.chat_message("model", avatar="🤖"):
             msg_placeholder = st.empty()
             full_resp = ""
             with st.spinner("Analyzing..."):
                 try:
                    payload = {"message": prompt, "session_id": st.session_state.session_id, "student_class": st.session_state.student_class}
                    res = requests.post(f"{API_URL}/chat", json=payload)
                    if res.status_code == 200:
                        ans = res.json()["message"]
                        for bit in ans.split(' '):
                            full_resp += bit + " "
                            time.sleep(0.04)
                            msg_placeholder.markdown(f'<div class="chat-bot">{full_resp}</div>', unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "model", "content": ans})
                        st.session_state.current_prompts = get_prompts(st.session_state.student_class)
                        st.rerun()
                 except:
                     st.error("Connection Failed")

    # --- POWER UPS ---
    if len(st.session_state.messages) < 15:
        st.markdown("---")
        st.markdown("### ⚡ Quick Discoveries")
        
        if "current_prompts" not in st.session_state:
             st.session_state.current_prompts = get_prompts(st.session_state.student_class)

        cols = st.columns(2)
        for i, p in enumerate(st.session_state.current_prompts):
            with cols[i % 2]:
                if st.button(f"🔭 {p}", use_container_width=True):
                    st.session_state.pending_prompt = p
                    st.session_state.current_prompts = get_prompts(st.session_state.student_class)
                    st.rerun()
