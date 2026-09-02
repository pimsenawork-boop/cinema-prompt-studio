import os
import json
import requests
import streamlit as st

# ---------------------------------------------------------
# UI Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cinematic AI Studio - Story & Flow Director",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .story-box {
        background: linear-gradient(135deg, #1c1f2e 0%, #12141f 100%);
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #9c27b0;
        margin-bottom: 15px;
    }
    .preview-card {
        background: #141824;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #232b3e;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ฟังก์ชัน AI วิเคราะห์โครงเรื่องและแตกฉาก (Story Breakdown)
# ---------------------------------------------------------
def analyze_story_and_breakdown(story_pitch, genre, character_name):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt_query = f"""
    You are a Hollywood Script Consultant and Cinematic AI Director.
    Analyze the following movie idea and break it down into 3 to 4 sequential cinematic scenes.
    
    Genre: {genre}
    Lead Character: {character_name}
    Story Pitch: {story_pitch}
    
    For each scene, provide:
    1. "title": Short Scene Title in Thai
    2. "summary": 1-2 sentences summarizing the scene context in Thai (บริบทฉาก)
    3. "emotion": Dominant emotional tone in Thai (อารมณ์ฉาก เช่น ตื่นเต้น หวาดระแวง อบอุ่น)
    4. "action": Physical visual action of the character in Thai (สิ่งที่ตัวละครทำชัดเจน)
    5. "environment": Visual environment description and lighting in Thai (สถานที่และสภาพแสง)
    6. "dialogue": A powerful spoken line or inner monologue in Thai (บทพูด)
    7. "voice_direction": Acting cue for the voice in Thai (เช่น [กระซิบแผ่วเบาด้วยความสับสน])
    8. "camera_move": Recommended cinematic camera movement (เช่น Slow Dolly In, Steadicam Track)
    
    Return strictly a valid JSON array of scene objects. Do not use markdown backticks.
    """
    
    data = {"contents": [{"parts": [{"text": prompt_query}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        raw_text = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0].replace("json", "").strip()
        return json.loads(raw_text)
    except Exception:
        return None

# ---------------------------------------------------------
# ฟังก์ชันดึงพร่อมสดเฉพาะ Google Flow
# ---------------------------------------------------------
@st.cache_data(ttl=86400)
def fetch_google_flow_prompts():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt_query = """
    Generate 4 cutting-edge video generation prompts tailored strictly for Google Flow (Veo Engine).
    Structure: [Camera Rig] + [Subject & Action] + [Environment & Light] + [Technical Specs].
    Return strictly a valid JSON array of objects with keys: "scene_name", "camera_setup", "flow_prompt", "video_result".
    No markdown backticks.
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
# ระบบบันทึกโปรเจกต์ (Database)
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
            "genre": "ไซไฟ / เอาชีวิตรอด",
            "logline": "ทหารลาดตระเวนคนสุดท้ายต้องนำส่งสารลับผ่านซากเมืองร้างที่มีฝูงโดรนสังหารตรวจจับ",
            "style": "Cinematic 35mm Film (Kodak Portra, Arri Alexa)",
            "lighting": "Golden hour dusty rays, teal shadow tones",
            "aspect_ratio": "16:9 (Landscape Cinema)",
            "char_name": "SGT_KAI",
            "char_look": "28-year-old Asian male, tactical fade hair, sharp jawline, small scar on left eyebrow",
            "char_persona": "เคร่งขรึม ระแวดระวัง การเคลื่อนไหวกระชับ เงียบกริบ",
            "char_voice": "เสียงทุ้มต่ำ แหบห้าว พูดคำสั้นชัดเจน",
            "char_outfit": "Matte-black tactical vest over dark olive utility uniform",
            "scenes": [
                {
                    "title": "เปิดฉาก: สัญญาณเตือนภัยกลางซากเมือง",
                    "summary": "ตัวเอกเดินทางมาถึงจุดนัดพบแต่พบเพียงความเงียบและซากปรักหักพัง",
                    "emotion": "ตึงเครียด โดดเดี่ยว และระแวดระวัง",
                    "action": "ก้าวเดินช้าๆ ลัดเลาะซากตึกร้าง มือประคองอาวุธระแวดระวัง",
                    "env": "ซากตึกสูงระฟ้าที่ถูกเถาวัลย์ปกคลุม มีละอองฝุ่นลอยในอากาศ",
                    "dialogue": "สัญญาณเตือนถูกตัดขาดทั้งหมด... เราต้องเดินเท้าต่อ",
                    "voice_direction": "[กระซิบผ่านไมค์วิทยุ หายใจสม่ำเสมอ น้ำเสียงเคร่งขรึม]",
                    "camera_move": "Steadicam Follow"
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
    st.image("https://img.icons8.com/color/96/clapperboard.png", width=55)
    st.title("🎬 Studio Hub")
    
    project_list = list(st.session_state.projects.keys())
    selected_project_name = st.selectbox("📂 เลือกโปรเจกต์ที่ต้องการทำงาน:", project_list)
    
    st.divider()
    with st.expander("➕ สร้างโปรเจกต์ใหม่"):
        new_title = st.text_input("ชื่อเรื่อง (Title)")
        new_genre = st.selectbox("แนวภาพยนตร์", [
            "ไซไฟ / เอาชีวิตรอด",
            "อนิเมะแฟนตาซี",
            "สืบสวนระทึกขวัญ นัวร์",
            "นิทาน 3D อบอุ่น",
            "แอ็กชันสงครามยุทธวิธี"
        ])
        new_logline = st.text_area("เรื่องย่อแกนหลัก")
        if st.button("✨ ยืนยันสร้างโปรเจกต์", use_container_width=True):
            if new_title.strip():
                st.session_state.projects[new_title] = {
                    "genre": new_genre,
                    "logline": new_logline,
                    "style": "Cinematic 35mm Film (Arri Alexa)",
                    "lighting": "Volumetric sunlight, natural contrast",
                    "aspect_ratio": "16:9 (Landscape Cinema)",
                    "char_name": "HERO_LEAD",
                    "char_look": "25-year-old Asian male, athletic build, messy hair",
                    "char_persona": "สุขุม เด็ดเดี่ยว",
                    "char_voice": "เสียงทุ้ม อบอุ่น หนักแน่น",
                    "char_outfit": "Dark utility jacket over black shirt",
                    "scenes": []
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
st.caption(f"**แนวเรื่อง:** {current_proj.get('genre', '')} | **เรื่องย่อ:** {current_proj.get('logline', '')}")

tab_ai_breakdown, tab_scenes, tab_char, tab_flow_vault, tab_export = st.tabs([
    "💡 1. วิเคราะห์พล็อตแตกฉาก (AI Story)",
    "🎬 2. ผู้กำกับฉาก & บทพูด (Director)",
    "👤 3. DNA ตัวละคร & น้ำเสียง (Locker)",
    "⚡ 4. คลังพร่อม Google Flow (Live Vault)",
    "📋 5. ส่งออกบทภาพยนตร์ (Master Script)"
])

# =========================================================
# TAB 1: วิเคราะห์พล็อตแตกฉากอัตโนมัติ (NEW!)
# =========================================================
with tab_ai_breakdown:
    st.subheader("🧠 ป้อนไอเดียหนังให้ AI วิเคราะห์โครงเรื่องและแตกฉาก")
    st.caption("พิมพ์เนื้อเรื่องย่อหรือไอเดียที่คุณคิดไว้ ระบบจะวิเคราะห์อารมณ์ สรุปบริบท และร่างบทพูดให้ตรวจดูก่อนแปลงเป็นพร่อม")
    
    pitch_input = st.text_area(
        "✍️ เล่าไอเดียหรือเหตุการณ์สำคัญในเรื่อง (Story Pitch):",
        value=current_proj.get("logline", ""),
        height=110,
        placeholder="เช่น ตัวเอกเป็นนักสำรวจคนเดียวที่ติดอยู่ในสถานีวิจัยใต้ทะเลลึก กำลังจะขาดออกซิเจน แต่พบสิ่งมีชีวิตเรืองแสงโบราณที่พยายามสื่อสารด้วย..."
    )
    
    col_run, col_status = st.columns([2, 5])
    with col_run:
        btn_analyze = st.button("✨ ให้ AI วิเคราะห์แตกเป็นฉากๆ", use_container_width=True)
        
    if btn_analyze:
        if not pitch_input.strip():
            st.warning("กรุณากรอกไอเดียเรื่องย่อก่อนกดวิเคราะห์")
        else:
            with st.spinner("AI กำลังวิเคราะห์โครงเรื่อง อารมณ์ และบทพูดของแต่ละฉาก..."):
                breakdown_results = analyze_story_and_breakdown(
                    story_pitch=pitch_input,
                    genre=current_proj.get("genre", "Sci-Fi"),
                    character_name=current_proj.get("char_name", "HERO")
                )
                if breakdown_results:
                    current_proj["scenes"] = breakdown_results
                    current_proj["logline"] = pitch_input
                    save_projects(st.session_state.projects)
                    st.success("วิเคราะห์และแตกฉากสำเร็จ! ตรวจดูบริบทด้านล่างและแก้ไขได้ทันที")
                    st.rerun()
                else:
                    st.error("ไม่สามารถเชื่อมต่อ API ได้ โปรดตรวจสอบว่าใส่ GEMINI_API_KEY ใน Render แล้ว")

    if current_proj.get("scenes"):
        st.markdown("---")
        st.markdown("### 👁️ ภาพรวมโครงสร้างฉากที่ AI แนะนำ (Preview & Review)")
        st.info("💡 คุณสามารถอ่านสรุปบริบทและอารมณ์ของแต่ละฉาก หากต้องการแก้ไขคำพูดหรือการกระทำ สามารถปรับได้ทันทีในแท็บ **'🎬 2. ผู้กำกับฉาก & บทพูด'**")
        
        for idx, sc in enumerate(current_proj["scenes"]):
            with st.container():
                st.markdown(f"""
                <div class="preview-card">
                    <h4>📍 ฉากที่ {idx+1}: {sc.get('title', '')}</h4>
                    <p><b>📖 สรุปบริบทฉาก:</b> {sc.get('summary', 'ไม่มีข้อมูลสรุป')}</p>
                    <p><b>🎭 โทนอารมณ์หลัก:</b> <code>{sc.get('emotion', 'สมจริง')}</code> | <b>🎥 มุมกล้องแนะนำ:</b> <code>{sc.get('camera_move', 'Dolly In')}</code></p>
                    <p><b>🏃 สิ่งที่ตัวละครทำ:</b> {sc.get('action', '')}</p>
                    <p><b>🎙️ บทพูด:</b> <i>"{sc.get('dialogue', '')}"</i> <span style="color:#f39c12;">{sc.get('voice_direction', '')}</span></p>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# TAB 2: ปรับแก้ฉาก บทพูด และสร้าง Google Flow Prompts
# =========================================================
with tab_scenes:
    st.subheader("🎬 ปรับแต่งรายละเอียดฉาก บทพูด และสร้างพร่อมภาพยนตร์")
    st.caption("แก้ไข เพิ่มเติม หรือเปลี่ยนบทพูดตามความต้องการ ระบบจะสร้างพร่อม Google Flow ที่สมบูรณ์แบบให้อัตโนมัติ")
    
    col_add, col_save = st.columns([2, 2])
    with col_add:
        if st.button("➕ เพิ่มฉากใหม่ด้วยตนเอง"):
            new_idx = len(current_proj["scenes"]) + 1
            current_proj["scenes"].append({
                "title": f"ฉากที่ {new_idx}: เหตุการณ์ต่อเนื่อง",
                "summary": "ตัวละครเดินทางเข้าสู่พื้นที่ใหม่",
                "emotion": "ลึกลับ ระแวง",
                "action": "ก้าวเดินไปข้างหน้าอย่างช้าๆ มือสัมผัสกำแพงหิน",
                "env": "ทางเดินหินโบราณ มีแสงคบเพลิงส่องสว่างสลัวๆ",
                "dialogue": "ที่นี่ไม่เหมือนสิ่งที่ระบุไว้ในแผนที่...",
                "voice_direction": "[กระซิบเสียงเบา แววตาสับสน]",
                "camera_move": "Steadicam Tracking"
            })
            save_projects(st.session_state.projects)
            st.rerun()

    ar_tag = current_proj.get("aspect_ratio", "16:9").split(" ")[0]
    char_token = f"[{current_proj.get('char_name','HERO')}: {current_proj.get('char_look','')}, wearing {current_proj.get('char_outfit','')}]"

    for i, sc in enumerate(current_proj["scenes"]):
        with st.expander(f"📍 ฉากที่ {i+1}: {sc.get('title', '')}", expanded=True):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                sc["title"] = st.text_input(f"ชื่อฉาก #{i+1}", sc.get("title", ""), key=f"title_{i}")
                sc["action"] = st.text_area(f"🏃 การกระทำของตัวละคร #{i+1}", sc.get("action", ""), key=f"act_{i}", height=75)
                sc["dialogue"] = st.text_input(f"🎙️ บทพูดตัวละคร #{i+1}", sc.get("dialogue", ""), key=f"dia_{i}")
            with col_t2:
                sc["emotion"] = st.text_input(f"🎭 อารมณ์ฉาก #{i+1}", sc.get("emotion", "เข้มข้น"), key=f"emo_{i}")
                sc["env"] = st.text_area(f"🌍 สถานที่และแสง #{i+1}", sc.get("env", ""), key=f"env_{i}", height=75)
                sc["voice_direction"] = st.text_input(f"🎭 คิวการแสดงเสียง #{i+1}", sc.get("voice_direction", "[น้ำเสียงนิ่ง]"), key=f"vdir_{i}")

            st.markdown("**🎥 พร่อม Google Flow พร้อมคำแนะนำกล้อง:**")
            flow_prompt_final = (
                f"Google Flow Prompt: Cinematic {sc.get('camera_move', 'slow dolly in')}, "
                f"{char_token}, {sc.get('action', '')}, setting: {sc.get('env', '')}, "
                f"mood: {sc.get('emotion', '')}, {current_proj.get('lighting', '')}, "
                f"{current_proj.get('style', '')}, shot on 35mm lens, temporal stability, 8k --ar {ar_tag}"
            )
            st.code(flow_prompt_final, language="text")

    if st.button("💾 บันทึกการแก้ไขฉากทั้งหมด", use_container_width=True):
        save_projects(st.session_state.projects)
        st.toast("บันทึกฉากเรียบร้อยแล้ว!", icon="✅")

# =========================================================
# TAB 3: Character & Voice Locker
# =========================================================
with tab_char:
    st.subheader("👤 Character DNA & Voice Anchor (ล็อกตัวละครและเสียง)")
    ca, cb = st.columns(2)
    with ca:
        current_proj["char_name"] = st.text_input("รหัสตัวละคร (Token Name)", current_proj.get("char_name", "HERO_LEAD"))
        current_proj["char_look"] = st.text_area("โครงหน้า / จุดเด่นบนใบหน้า (ห้ามเปลี่ยน)", current_proj.get("char_look", ""))
        current_proj["char_persona"] = st.text_input("บุคลิกภาพประจำตัว", current_proj.get("char_persona", ""))
    with cb:
        current_proj["char_outfit"] = st.text_area("ชุดประจำตัว (Fixed Outfit)", current_proj.get("char_outfit", ""))
        current_proj["char_voice"] = st.text_area("ลักษณะน้ำเสียงและสำเนียงการพูด", current_proj.get("char_voice", ""))
        
    if st.button("💾 บันทึก DNA ตัวละคร"):
        save_projects(st.session_state.projects)
        st.toast("บันทึกข้อมูลตัวละครสำเร็จ!", icon="✅")

# =========================================================
# TAB 4: Google Flow Live Vault
# =========================================================
with tab_flow_vault:
    st.subheader("⚡ Google Flow Live Prompts (สูตรกล้องและแสงสด)")
    if st.button("🔄 ดึงเทรนด์ใหม่เดี๋ยวนี้"):
        st.cache_data.clear()
        st.rerun()
        
    live_prompts = fetch_google_flow_prompts()
    if live_prompts:
        for idx, item in enumerate(live_prompts):
            with st.expander(f"📍 ช็อต: {item.get('scene_name')} ({item.get('camera_setup')})", expanded=True):
                st.code(item.get("flow_prompt"), language="text")
                st.markdown(f"**🎬 การเคลื่อนไหว:** {item.get('video_result')}")
    else:
        st.warning("กรุณาตรวจสอบการตั้งค่า GEMINI_API_KEY ใน Render")

# =========================================================
# TAB 5: Master Script Export
# =========================================================
with tab_export:
    st.subheader("📋 Hollywood Master Production Script")
    script_txt = f"=========================================================================\n"
    script_txt += f"PROJECT: {selected_project_name.upper()}\n"
    script_txt += f"GENRE: {current_proj.get('genre', '')}\n"
    script_txt += f"CHARACTER: {current_proj.get('char_name', '')} ({current_proj.get('char_voice', '')})\n"
    script_txt += f"LOGLINE: {current_proj.get('logline', '')}\n"
    script_txt += f"=========================================================================\n\n"
    
    for idx, sc in enumerate(current_proj["scenes"]):
        script_txt += f"SCENE {idx+1}: {sc.get('title', '').upper()}\n"
        script_txt += f"CONTEXT: {sc.get('summary', '')}\n"
        script_txt += f"MOOD: {sc.get('emotion', '')}\n"
        script_txt += f"LOCATION: {sc.get('env', '')}\n"
        script_txt += f"ACTION: {sc.get('action', '')}\n"
        if sc.get("dialogue"):
            script_txt += f"  {current_proj.get('char_name', 'CHARACTER')}: {sc.get('voice_direction', '')} \"{sc.get('dialogue')}\"\n"
        script_txt += f"GOOGLE FLOW PROMPT:\n"
        script_txt += f"Cinematic {sc.get('camera_move', 'slow dolly in')}, {char_token}, {sc.get('action', '')}, {sc.get('env', '')}, {current_proj.get('lighting', '')}, {current_proj.get('style', '')} --ar {ar_tag}\n"
        script_txt += f"-------------------------------------------------------------------------\n\n"
        
    st.text_area("เล่มบทภาพยนตร์สมบูรณ์", script_txt, height=320)
    st.download_button("📥 ดาวน์โหลดเล่มบท (.txt)", data=script_txt, file_name=f"{selected_project_name}_script.txt")
