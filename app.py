import os
import json
import requests
import streamlit as st

# ---------------------------------------------------------
# UI Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Google Flow Cinematic AI Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .flow-card {
        background: linear-gradient(135deg, #131824 0%, #0d121c 100%);
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #00c853;
        margin-bottom: 14px;
    }
    .dialogue-card {
        background-color: #161b26;
        padding: 14px;
        border-radius: 8px;
        border-left: 4px solid #f39c12;
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ระบบดึงพร่อมสดเฉพาะ Google Flow ผ่าน Gemini API
# ---------------------------------------------------------
@st.cache_data(ttl=86400)
def fetch_google_flow_prompts():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt_query = """
    You are an elite cinematic prompt engineer specializing EXCLUSIVELY in Google Flow (Google Veo Video Engine).
    Generate 5 cinematic, ultra-stable video generation prompts tailored strictly to Google Flow's architecture.
    
    Rules for Google Flow Prompts:
    1. Structure: [Camera Rig & Motion] + [Subject & Subtle Physics] + [Environment & Volumetric Light] + [Cinematic Specs].
    2. Focus on realistic motion dynamics to prevent limb morphing and temporal glitches.
    3. Include technical tags: "shot on 35mm", "temporal stability", "realistic cloth physics", "photorealistic 8k".
    
    Return strictly a valid JSON array of objects with keys:
    - "scene_name": Short Thai title
    - "camera_setup": Specific camera rig and lens
    - "flow_prompt": Ready-to-use English prompt for Google Flow
    - "video_result": Explanation in Thai describing exactly how the video will move in Google Flow
    
    Do not output markdown backticks or code blocks, return raw JSON only.
    """
    
    data = {"contents": [{"parts": [{"text": prompt_query}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        raw_text = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0].replace("json", "").strip()
        return json.loads(raw_text)
    except Exception:
        return None

# ---------------------------------------------------------
# ระบบฐานข้อมูลโปรเจกต์ (projects_db.json)
# ---------------------------------------------------------
DB_FILE = "projects_db.json"

def load_projects():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "มหาศึกหุ่นรบแดนร้าง (Google Flow Project)": {
            "genre": "ไซไฟ / เอาชีวิตรอด (Sci-Fi Action)",
            "logline": "โลกหลังล่มสลาย ทหารลาดตระเวนคนสุดท้ายต้องส่งสัญญาณเตือนภัยผ่านแดนพายุแม่เหล็ก",
            "style": "Cinematic 35mm Film (Kodak Portra, Arri Alexa)",
            "lighting": "Golden hour dusty rays, volumetric smoke",
            "aspect_ratio": "16:9 (Landscape Cinema)",
            "char_name": "SGT_KAI",
            "char_look": "28-year-old Asian male, tactical fade hair, sharp jawline, small scar on left eyebrow",
            "char_persona": "เคร่งขรึม ระแวดระวัง การเคลื่อนไหวกระชับ เงียบกริบ",
            "char_voice": "เสียงทุ้มต่ำ แหบห้าว พูดคำสั้น ชัดถ้อยชัดคำ",
            "char_outfit": "Matte-black tactical combat vest over dark olive uniform",
            "scenes": [
                {
                    "title": "เปิดฉาก: สัญญาณเตือนภัยกลางซากเมือง",
                    "action": "ก้าวเดินช้าๆ ลัดเลาะซากตึกร้าง มือประคองอาวุธระแวดระวัง",
                    "env": "ซากตึกสูงระฟ้าที่ถูกเถาวัลย์ปกคลุม มีละอองฝุ่นลอยในอากาศ",
                    "dialogue": "สัญญาณเตือนถูกตัดขาดทั้งหมด... เราต้องเดินเท้าต่อ",
                    "voice_direction": "[กระซิบผ่านไมค์วิทยุ หายใจสม่ำเสมอ น้ำเสียงเคร่งขรึม]"
                }
            ]
        }
    }

def save_projects(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

# ---------------------------------------------------------
# Sidebar: Project Hub
# ---------------------------------------------------------
with st.sidebar:
    st.image("[https://img.icons8.com/color/96/clapperboard.png](https://img.icons8.com/color/96/clapperboard.png)", width=55)
    st.title("🎬 Studio Hub")
    
    project_list = list(st.session_state.projects.keys())
    selected_project_name = st.selectbox("📂 เลือกโปรเจกต์:", project_list)
    
    st.divider()
    with st.expander("➕ สร้างโปรเจกต์ใหม่"):
        new_title = st.text_input("ชื่อเรื่อง (Title)")
        new_genre = st.selectbox("แนวภาพยนตร์", [
            "ไซไฟ / เอาชีวิตรอด (Sci-Fi)",
            "อนิเมะแฟนตาซี (Fantasy Anime)",
            "สืบสวนระทึกขวัญ (Noir Thriller)",
            "นิทาน 3D (Animation)",
            "แอ็กชันสงคราม (Tactical Military)"
        ])
        new_logline = st.text_area("เรื่องย่อหลัก (Logline)")
        if st.button("✨ ยืนยันสร้างโปรเจกต์", use_container_width=True):
            if new_title.strip():
                st.session_state.projects[new_title] = {
                    "genre": new_genre,
                    "logline": new_logline,
                    "style": "Cinematic 35mm Film (Arri Alexa)",
                    "lighting": "Volumetric sunlight, atmospheric dust",
                    "aspect_ratio": "16:9 (Landscape Cinema)",
                    "char_name": "HERO_LEAD",
                    "char_look": "25-year-old Asian male, athletic build, messy hair",
                    "char_persona": "สุขุม เด็ดเดี่ยว",
                    "char_voice": "เสียงทุ้ม อบอุ่น หนักแน่น",
                    "char_outfit": "Dark utility jacket over black shirt",
                    "scenes": [{
                        "title": "ฉากที่ 1: การเริ่มต้น",
                        "action": "ยืนมองเส้นขอบฟ้า ก้าวเดินไปข้างหน้าอย่างช้าๆ",
                        "env": "ทุ่งกว้าง มีสายหมอกบางเบา",
                        "dialogue": "การเดินทางเพิ่งเริ่มต้น...",
                        "voice_direction": "[พูดช้าๆ แววตามุ่งมั่น]"
                    }]
                }
                save_projects(st.session_state.projects)
                st.success("สร้างสำเร็จ!")
                st.rerun()

    if len(project_list) > 1:
        if st.button("🗑️ ลบโปรเจกต์นี้", type="secondary"):
            del st.session_state.projects[selected_project_name]
            save_projects(st.session_state.projects)
            st.rerun()

current_proj = st.session_state.projects[selected_project_name]

# ---------------------------------------------------------
# Main Interface
# ---------------------------------------------------------
st.title(f"📽️ {selected_project_name}")
st.caption(f"**ประเภท:** {current_proj.get('genre', '')} | **เรื่องย่อ:** {current_proj.get('logline', '')}")

tab_flow, tab_scenes, tab_char, tab_audio, tab_export = st.tabs([
    "🚀 1. คลังพร่อม Google Flow สด (Auto)",
    "🎬 2. ผู้กำกับฉาก & บทพูด (Director)",
    "👤 3. DNA ตัวละคร & น้ำเสียง (Locker)",
    "🎵 4. ดนตรีประกอบ & ซาวด์ดีไซน์",
    "📋 5. เล่มบทภาพยนตร์ (Master Export)"
])

# =========================================================
# TAB 1: Google Flow Live Prompts
# =========================================================
with tab_flow:
    st.subheader("⚡ Google Flow / Veo Video Prompt Vault")
    st.caption("ระบบดึงสูตรคำสั่งที่ปรับแต่งสำหรับสถาปัตยกรรม Google Flow โดยเฉพาะ (อัปเดตอัตโนมัติ)")
    
    col_r1, col_r2 = st.columns([2, 5])
    with col_r1:
        if st.button("🔄 ดึงสูตร Google Flow ใหม่เดี๋ยวนี้"):
            st.cache_data.clear()
            st.rerun()
            
    flow_prompts = fetch_google_flow_prompts()
    
    if flow_prompts:
        for idx, item in enumerate(flow_prompts):
            with st.expander(f"📍 ช็อตที่ {idx+1}: {item.get('scene_name')} ({item.get('camera_setup')})", expanded=True):
                st.markdown("**📋 พร่อมพร้อมคัดลอกลง Google Flow:**")
                st.code(item.get("flow_prompt"), language="text")
                st.markdown(f"**🎬 การเคลื่อนไหวของวิดีโอ:** {item.get('video_result')}")
                st.markdown(f"**🎥 อุปกรณ์กล้อง:** `{item.get('camera_setup')}`")
    else:
        st.warning("ระบบกำลังรอเชื่อมต่อ API: กรุณาตรวจสอบว่าใส่ `GEMINI_API_KEY` ใน Environment Variables บน Render เรียบร้อยแล้ว")

# =========================================================
# TAB 2: Scene & Dialogue Director
# =========================================================
with tab_scenes:
    st.subheader("🎬 จัดการฉากและบทพูดต่อเนื่อง")
    
    if st.button("➕ เพิ่มฉากถัดไป"):
        new_idx = len(current_proj["scenes"]) + 1
        current_proj["scenes"].append({
            "title": f"ฉากที่ {new_idx}: เหตุการณ์ต่อเนื่อง",
            "action": "ก้าวเดินไปข้างหน้าอย่างระแวดระวัง",
            "env": "พื้นที่กว้าง มีหมอกจางๆ",
            "dialogue": "",
            "voice_direction": "[พูดด้วยน้ำเสียงสุขุม]"
        })
        save_projects(st.session_state.projects)
        st.rerun()

    ar_tag = current_proj.get("aspect_ratio", "16:9").split(" ")[0]
    char_token = f"[{current_proj.get('char_name','HERO')}: {current_proj.get('char_look','')}, wearing {current_proj.get('char_outfit','')}]"

    for i, sc in enumerate(current_proj["scenes"]):
        st.markdown(f"---")
        st.markdown(f"### 📍 ฉากที่ {i+1}: {sc.get('title', '')}")
        c_a, c_b = st.columns(2)
        with c_a:
            sc["action"] = st.text_input(f"การกระทำ #{i+1}", sc.get("action", ""), key=f"act_{i}")
            sc["dialogue"] = st.text_input(f"บทพูดตัวละคร #{i+1}", sc.get("dialogue", ""), key=f"dia_{i}")
        with c_b:
            sc["env"] = st.text_input(f"สถานที่ #{i+1}", sc.get("env", ""), key=f"env_{i}")
            sc["voice_direction"] = st.text_input(f"อารมณ์และจังหวะเสียง #{i+1}", sc.get("voice_direction", ""), key=f"vdir_{i}")

        st.markdown("**🎯 เลือกลักษณะกล้องสำหรับฉากนี้:**")
        tab_opt1, tab_opt2, tab_opt3 = st.tabs([
            "✨ Dolly Push-in (ซึ้ง/อารมณ์)",
            "🔍 Steadicam Follow (ลึกลับ/สำรวจ)",
            "🔥 Low-Angle Dynamic (แอ็กชัน/กดดัน)"
        ])
        
        with tab_opt1:
            p_a = f"Google Flow Prompt: Cinematic slow push-in dolly shot, {char_token}, {sc['action']}, location: {sc['env']}, {current_proj.get('lighting','')}, {current_proj.get('style','')}, 50mm lens, temporal stability --ar {ar_tag}"
            st.code(p_a, language="text")
        with tab_opt2:
            p_b = f"Google Flow Prompt: Steadicam tracking follow shot, {char_token}, {sc['action']}, location: {sc['env']}, deep shadows, {current_proj.get('lighting','')}, {current_proj.get('style','')}, 35mm anamorphic --ar {ar_tag}"
            st.code(p_b, language="text")
        with tab_opt3:
            p_c = f"Google Flow Prompt: Low-angle dynamic tracking shot, {char_token}, {sc['action']}, location: {sc['env']}, flying particles, dramatic rim light, {current_proj.get('style','')}, IMAX quality --ar {ar_tag}"
            st.code(p_c, language="text")

    if st.button("💾 บันทึกฉากและบทพูดทั้งหมด"):
        save_projects(st.session_state.projects)
        st.toast("บันทึกข้อมูลเรียบร้อย!", icon="✅")

# =========================================================
# TAB 3: Character & Voice DNA
# =========================================================
with tab_char:
    st.subheader("👤 Character DNA & Voice Anchor (ล็อกหน้าตาและเสียง)")
    ca, cb = st.columns(2)
    with ca:
        current_proj["char_name"] = st.text_input("รหัสตัวละคร", current_proj.get("char_name", "HERO_LEAD"))
        current_proj["char_look"] = st.text_area("โครงหน้า / จุดเด่นบนใบหน้า", current_proj.get("char_look", ""))
        current_proj["char_persona"] = st.text_input("บุคลิกภาพประจำตัว", current_proj.get("char_persona", ""))
    with cb:
        current_proj["char_outfit"] = st.text_area("ชุดประจำตัว (ห้ามเปลี่ยน)", current_proj.get("char_outfit", ""))
        current_proj["char_voice"] = st.text_area("ลักษณะเสียงและสำเนียงพูด", current_proj.get("char_voice", ""))
        
    if st.button("💾 บันทึกข้อมูลตัวละคร"):
        save_projects(st.session_state.projects)
        st.toast("บันทึก DNA สำเร็จ!", icon="✅")

# =========================================================
# TAB 4: Music & Sound Score
# =========================================================
with tab_audio:
    st.subheader("🎵 Film Score & Sound Design Guide")
    audio_mood = st.selectbox("เลือกโทนอารมณ์ดนตรีของช่วงนี้:", [
        "1. ดราม่า เวิ้งว้าง สิ้นหวัง (55-65 BPM)",
        "2. ลึกลับ กดดัน สั่นประสาท (80-95 BPM)",
        "3. ปะทะเดือด แอ็กชันหนักหน่วง (130-150 BPM)",
        "4. ความหวัง ชัยชนะ คลี่คลาย (90-110 BPM)"
    ])
    
    if "1. ดราม่า" in audio_mood:
        st.code("cinematic film score, sorrowful solo cello, slow melancholy reverberant piano, atmospheric wind ambient, Hans Zimmer style, 60 bpm, no vocals", language="text")
    elif "2. ลึกลับ" in audio_mood:
        st.code("cinematic thriller suspense, dark pulsing sub-bass, anxious ticking clock rhythm, screeching dissonant violins, heart thumping bassline, 85 bpm, instrumental", language="text")
    elif "3. ปะทะเดือด" in audio_mood:
        st.code("epic blockbuster action score, massive cinematic percussion, roaring brass horn braam, aggressive hybrid synth, war drums, 140 bpm, instrumental", language="text")
    elif "4. ความหวัง" in audio_mood:
        st.code("triumphant cinematic anthem, uplifting orchestral strings, soaring angelic choir harmonies, inspirational French horn, Interstellar style, 100 bpm, instrumental", language="text")

# =========================================================
# TAB 5: Master Script Export
# =========================================================
with tab_export:
    st.subheader("📋 Hollywood Master Production Script")
    script_txt = f"==================================================\n"
    script_txt += f"PROJECT: {selected_project_name.upper()}\n"
    script_txt += f"GENRE: {current_proj.get('genre','')}\n"
    script_txt += f"CHARACTER: {current_proj.get('char_name','')} ({current_proj.get('char_voice','')})\n"
    script_txt += f"==================================================\n\n"
    
    for idx, sc in enumerate(current_proj["scenes"]):
        script_txt += f"SCENE {idx+1}: {sc.get('title','').upper()}\n"
        script_txt += f"LOCATION: {sc.get('env','')}\n"
        script_txt += f"ACTION: {sc.get('action','')}\n"
        if sc.get("dialogue"):
            script_txt += f"  {current_proj.get('char_name','CHARACTER')}: {sc.get('voice_direction','')} \"{sc.get('dialogue')}\"\n"
        script_txt += f"--------------------------------------------------\n\n"
        
    st.text_area("เล่มบทภาพยนตร์สมบูรณ์", script_txt, height=280)
    st.download_button("📥 ดาวน์โหลดไฟล์บท (.txt)", data=script_txt, file_name=f"{selected_project_name}.txt")
