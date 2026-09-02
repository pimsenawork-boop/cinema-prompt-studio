# -*- coding: utf-8 -*-
"""
AI Film & Cinematic Prompt Studio (Google Flow Edition)
- แยกฟังก์ชันการทำงานอย่างชัดเจน (Modular Design)
- ตัดเมนูสร้างคลิปออก
- ขยายตัวเลือกแนวทางสร้างภาพยนตร์หมวดละ 10 สไตล์
- เพิ่มคลังพรอพต์สำเร็จรูป 10 รายการ
- แก้ปัญหา MediaFileStorageError และจัดการ GEMINI_API_KEY ให้ปลอดภัย
"""

import os
import json
import streamlit as st

# ==========================================
# 1. การตั้งค่าหน้าเว็บ (Page Configuration)
# ==========================================
def setup_page_config():
    st.set_page_config(
        page_title="AI Cinematic Studio & Storyboard",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # ปรับสไตล์ Dark Mode ให้ดูทันสมัยและสะอาดตา
    st.markdown("""
        <style>
        .main { background-color: #0e1117; color: #f0f2f6; }
        .stButton>button {
            width: 100%;
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #ff2b2b;
            color: white;
        }
        .scene-box {
            background-color: #1a1c24;
            border-left: 4px solid #ff4b4b;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. การจัดการ API Key (API Management)
# ==========================================
def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None
            
    # กรณีไม่ได้ตั้งค่าใน Render ให้กรอกผ่านแถบ Sidebar ชั่วคราวได้
    if not api_key:
        with st.sidebar:
            st.warning("⚠️ ไม่พบ GEMINI_API_KEY ใน Environment")
            api_key = st.text_input("กรอก GEMINI_API_KEY:", type="password")
            if api_key:
                st.success("เชื่อมต่อ API Key เรียบร้อย")
    return api_key

# ==========================================
# 3. จัดการ Session State (State Management)
# ==========================================
def init_session_state():
    if "story_pitch" not in st.session_state:
        st.session_state.story_pitch = ""
    if "scenes_data" not in st.session_state:
        st.session_state.scenes_data = []
    if "characters" not in st.session_state:
        st.session_state.characters = [
            {"name": "จ่าสิบเอกเอกภาพ", "role": "ผู้นำหน่วยลาดตระเวน", "trait": "สุขุม ชำนาญยุทธวิธี เกราะรบยับเยินจากสมรภูมิ", "voice": "ทุ้มต่ำ นิ่ง หนักแน่น"},
            {"name": "โอเมก้า-07", "role": "หุ่นรบ AI ลาดตระเวน", "trait": "เกราะเหล็กคอมโพสิตดำด้าน รอยกระสุนและคราบสนิม", "voice": "เสียงสังเคราะห์ มีคลื่นแทรก"}
        ]

# ==========================================
# 4. ชุดข้อมูลตัวเลือกและพรอพต์ (Presets & Prompts)
# ==========================================
def get_preset_data():
    genres = [
        "1. ไซไฟดิสโทเปีย / ไซเบอร์พังก์ (Cyberpunk & High-Tech Dystopia)",
        "2. หุ่นรบจักรกลและสงครามอวกาศ (Mecha & Space Warfare)",
        "3. ยุทธการทหารสมจริง (Military Tactical & Gritty Warfare)",
        "4. สืบสวนนีโอนัวร์ (Neo-Noir Crime Thriller)",
        "5. ดาร์กแฟนตาซีมหากาพย์ (Dark Fantasy & Medieval Epic)",
        "6. โลกหลังล่มสลายเอาชีวิตรอด (Post-Apocalyptic Survival)",
        "7. จิตวิทยาระทึกขวัญ (Psychological Suspense)",
        "8. สตีมพังก์และประวัติศาสตร์สมมติ (Steampunk Alternate History)",
        "9. แอ็กชันเดือดล้างแค้น (High-Octane Revenge Action)",
        "10. กำลังภายในแฟนตาซีร่วมสมัย (Cyber-Wuxia Epic)"
    ]

    tones = [
        "1. ดิบเถื่อน ตึงเครียด กดดันสูง (Gritty, Tense & High-Stakes)",
        "2. มืดมน สิ้นหวัง เปล่าเปลี่ยว (Dark, Bleak & Melancholic)",
        "3. มหากาพย์ ยิ่งใหญ่ ทรงพลัง (Grand, Majestic & Epic Scale)",
        "4. โกลาหล ฉับไว ตื่นเต้นระทึกใจ (Chaotic, Fast-Paced & Energetic)",
        "5. เงียบงัน ลึกลับ ซ่อนเงื่อน (Mysterious, Eerie & Atmospheric)",
        "6. มีความหวัง ฮึกเหิม ทรงเกียรติ (Inspiring, Heroic & Hopeful)",
        "7. เยือกเย็น ไฮเทค ไร้อารมณ์ (Cold, Clinical & Minimalist)",
        "8. หวาดระแวง ไม่น่าไว้วางใจ (Paranoid & Claustrophobic)",
        "9. อบอุ่น ซึ้งกินใจ ปรัชญาชีวิต (Emotional, Poetic & Philosophical)",
        "10. เหนือจริง ฝันร้าย ภาพหลอน (Surreal, Psychedelic & Nightmare)"
    ]

    cameras = [
        "1. มุมมองบุคคลที่หนึ่ง กล้องบอดี้แคม (Bodycam / First-Person Tactical POV)",
        "2. สารคดีสงคราม กล้องมือถือสั่นไหวสมจริง (Handheld Shaky-cam War Doc)",
        "3. ภาพยนตร์บล็อกบัสเตอร์ มุมกว้างอลังการ (Anamorphic Widescreen 8K Cinematic)",
        "4. สเตดี้แคมเคลื่อนที่ตามตัวละคร (Smooth Steadicam Tracking Shot)",
        "5. โดรนความเร็วสูงโฉบเฉี่ยว (Dynamic FPV Drone Chase)",
        "6. แสงเงามืดตัดชัดเจน นัวร์จัดจ้าน (High-Contrast Chiaroscuro Lighting)",
        "7. โคลสอัพจับอารมณ์ดวงตาและใบหน้า (Extreme Macro Close-up Portrait)",
        "8. สโลว์โมชันแอ็กชันรายละเอียดสูง (Phantom High-Speed 1000fps Slow-mo)",
        "9. เลนส์ฟิล์มเกรนย้อนยุค (Vintage 35mm Film Grain / 70s Cinema)",
        "10. มุมมองจากกล้องวงจรปิด/อินฟราเรด (CCTV / Thermal Night Vision Feed)"
    ]

    lightings = [
        "1. แสงนีออนสะท้อนพื้นถนนเปียกฝน (Neon Rain Cyberpunk Reflections)",
        "2. โกลเด้นฮาวเออร์ ย้อนแสงอบอุ่น (Golden Hour Rim Lighting)",
        "3. แสงหม่นหมองในม่านหมอกควันสงคราม (Volumetric Fog & Smoky Haze)",
        "4. แสงแฟลชปากกระบอกปืนในเงามืด (Muzzle Flash in Pitch Black)",
        "5. แสงจันทร์เย็นยะเยือกตัดเงาดำ (Cold Moonlight Chiaroscuro)",
        "6. แสงไฟฉุกเฉินสีแดงไซเรนกะพริบ (Pulsing Red Emergency Siren Lights)",
        "7. แสงแดดแผดเผากลางทะเลทรายเวิ้งว้าง (Harsh Overhead Sun & Heatwaves)",
        "8. แสงโฮโลแกรมเรืองแสงสีฟ้าในห้องมืด (Bioluminescent Holographic Glow)",
        "9. แสงไฟสปอร์ตไลต์ส่องตรวจค้นจากเฮลิคอปเตอร์ (Helicopter Searchlight Beam)",
        "10. แสงสะท้อนประกายเชื่อมโลหะอุตสาหกรรม (Industrial Welding Sparks & Flare)"
    ]

    prompts = [
        {
            "title": "1. ภาพเปิดเมืองสงครามล่มสลาย (Establishing Shot)",
            "prompt": "Cinematic establishing wide shot of a ruined futuristic metropolis at dusk, thick black smoke rising, burning wreckage, distant searchlights sweeping through smog, hyper-realistic, photorealistic, 8K, directed by Denis Villeneuve."
        },
        {
            "title": "2. หุ่นรบยักษ์เปิดระบบพร้อมรบ (Mecha Boot-up)",
            "prompt": "Low-angle dramatic shot of a 20-meter heavy armored combat mech activating in a dark hangar, internal blue LED lights firing up, hydraulic steam releasing from joint vents, ultra-detailed metallic scratches, 8K resolution, IMAX camera."
        },
        {
            "title": "3. การปะทะยุทธวิธีภาคพื้นดิน (Tactical Firefight)",
            "prompt": "Combat cameraman perspective, elite tactical operative squad moving swiftly through concrete ruins under heavy suppression fire, muzzle flashes cutting through concrete dust, intense dynamic motion blur, hyper-detailed gear."
        },
        {
            "title": "4. โคลสอัพแววตานักบินในห้องควบคุม (Cockpit Tension)",
            "prompt": "Extreme macro close-up of a battle-hardened pilot's eyes inside a dimly lit cockpit, sweat dripping, green holographic flight telemetry reflections flickering across the visor, claustrophobic atmosphere, intense cinematic lighting."
        },
        {
            "title": "5. โดรนความเร็วสูงบินไล่ล่า (FPV Drone Chase)",
            "prompt": "High-speed continuous FPV drone dive tracking a futuristic combat hover-bike racing through narrow neon-lit alleys, dynamic camera rolling, wet asphalt reflecting bright neon signs, high-octane action sequence."
        },
        {
            "title": "6. ห้องบัญชาการวางแผนศึก (War Room Hologram)",
            "prompt": "Medium shot of military commanders gathered around a glowing 3D holographic tactical map of a besieged city, cold blue lighting, sharp shadows, serious facial expressions, cinematic depth of field."
        },
        {
            "title": "7. เผชิญหน้าสืบสวนเงามืด (Neo-Noir Confrontation)",
            "prompt": "High-contrast cinematic scene, two figures in long coats standing under a flickering street lamp in heavy pouring rain, smoke rising from a manhole, silhouettes backlit by car headlights, wet reflection."
        },
        {
            "title": "8. ลาดตระเวนมุมมองกล้องมองกลางคืน (Night Vision Patrol)",
            "prompt": "First-person thermal infrared night vision view, scanning a silent dark forest, green phosphor hue, enemy mechanical targets glowing white-hot among dense trees, tactical HUD overlay."
        },
        {
            "title": "9. ฉากระเบิดและการอพยพเดือด (Heavy Extraction)",
            "prompt": "Wide cinematic shot, military tilt-rotor aircraft landing in a hostile warzone to extract wounded soldiers, massive explosion shockwave kicking up dust behind them, golden hour lens flare, high realism."
        },
        {
            "title": "10. ภาพปิดท้าย ยืนมองซากสมรภูมิ (Post-Battle Sunset)",
            "prompt": "Back-view silhouette of a lone exhausted soldier standing on a hill of rubble, looking out at a burning battlefield against a fiery orange and crimson sunset sky, wind blowing a tattered cape, melancholic and epic mood."
        }
    ]

    return genres, tones, cameras, lightings, prompts

# ==========================================
# 5. ฟังก์ชันเชื่อมต่อ AI วิเคราะห์แตกฉาก (AI Logic)
# ==========================================
def generate_story_breakdown(pitch, genre, tone, camera, lighting, api_key):
    if not api_key:
        return None, "กรุณาระบุ GEMINI_API_KEY ใน Render หรือแถบด้านข้างก่อนดำเนินการ"

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = f"""
คุณเป็นผู้กำกับภาพยนตร์และนักเขียนบทมืออาชีพ
จงวิเคราะห์ไอเดียเรื่องต่อไปนี้ และแตกออกเป็น 5 ฉากสำคัญสำหรับ Storyboard & AI Video Prompt
แนวเรื่อง: {genre}
โทนอารมณ์: {tone}
มุมกล้อง: {camera}
การจัดแสง: {lighting}

เรื่องย่อ: {pitch}

ตอบเป็น JSON รูปแบบ Array โดยแต่ละฉากมีโครงสร้างดังนี้:
[
  {{
    "scene_number": 1,
    "title": "ชื่อฉาก",
    "description": "เรื่องย่อและแอ็กชันในฉาก",
    "camera_direction": "คำแนะนำมุมกล้อง",
    "lighting_and_atmosphere": "บรรยากาศและแสงสี",
    "audio_cue": "เสียงดนตรีและซาวด์เอฟเฟกต์",
    "image_prompt": "English prompt for image generation (Cinematic, 8k)",
    "video_prompt": "English prompt for video generation (Cinematic motion)"
  }}
]
ตอบเฉพาะโค้ด JSON เท่านั้น ไม่มีข้อความอธิบายอื่น
"""
        response = model.generate_content(system_prompt)
        text_resp = response.text.strip()
        if text_resp.startswith("```json"):
            text_resp = text_resp[7:]
        if text_resp.startswith("```"):
            text_resp = text_resp[3:]
        if text_resp.endswith("```"):
            text_resp = text_resp[:-3]
        text_resp = text_resp.strip()

        data = json.loads(text_resp)
        return data, None
    except Exception as e:
        return None, f"เกิดข้อผิดพลาดในการเชื่อมต่อ AI: {str(e)}"

# ==========================================
# 6. ส่วนหัวของเว็บ (Header Component)
# ==========================================
def render_header(api_key):
    st.markdown("## 🎬 มหาสึกหุ่นรบแดนดีพิมฟ์ (Google Flow Project)")
    st.caption("ระบบวิเคราะห์โครงเรื่อง แตกฉากภาพยนตร์ และคลังพรอพต์ระดับโปรสำหรับ AI Video")
    
    if not api_key:
        st.error("⚠️ คุณสามารถเชื่อมต่อ API ได้อีกครั้งในการใส่ GEMINI_API_KEY ใน Render อีกครั้ง หรือกรอกผ่าน Sidebar")
    else:
        st.success("🟢 เชื่อมต่อ AI Engine เรียบร้อยแล้ว พร้อมสำหรับการประมวลผล")

# ==========================================
# 7. แท็บที่ 1: วิเคราะห์แตกฉาก (Tab 1)
# ==========================================
def render_tab_story(api_key, genres, tones, cameras, lightings):
    st.subheader("💡 1. ป้อนไอเดียหนังให้ AI วิเคราะห์โครงเรื่องและแตกฉาก")

    col1, col2 = st.columns([2, 1])
    with col1:
        pitch = st.text_area(
            "เล่าไอเดียหรือเรื่องราวสำคัญในเรื่อง (Story Pitch):",
            value=st.session_state.story_pitch or "ขบวนการลาดตระเวนสุดท้ายของเหล่าสารสืบผ่านกฎหมายเมืองที่มีการเผยแพร่อาวุธสัตว์ประหลาดจักรกลกลางซากปรักหักพัง",
            height=120
        )
        st.session_state.story_pitch = pitch

    with col2:
        selected_genre = st.selectbox("🎯 แนวภาพยนตร์ (10 สไตล์):", genres)
        selected_tone = st.selectbox("🎭 โทนและอารมณ์ (10 โทน):", tones)

    col3, col4 = st.columns(2)
    with col3:
        selected_camera = st.selectbox("📹 สไตล์มุมกล้องหลัก (10 สไตล์):", cameras)
    with col4:
        selected_lighting = st.selectbox("💡 สไตล์แสงและบรรยากาศ (10 รูปแบบ):", lightings)

    if st.button("✨ ให้ AI วิเคราะห์แตกเป็นฉากๆ (Generate Storyboard)"):
        with st.spinner("AI กำลังวิเคราะห์โครงเรื่อง ลำดับฉาก และสร้างชุดคำสั่งพรอพต์..."):
            scenes, error = generate_story_breakdown(
                pitch, selected_genre, selected_tone, selected_camera, selected_lighting, api_key
            )
            if error:
                st.error(error)
            elif scenes:
                st.session_state.scenes_data = scenes
                st.success(f"วิเคราะห์สำเร็จ! แตกฉากออกมาทั้งหมด {len(scenes)} ฉาก")

    # แสดงผลฉากที่แตกออกมา
    if st.session_state.scenes_data:
        st.markdown("---")
        st.markdown("### 👁️ องค์ประกอบฉากที่ AI แนะนำ (ดูตัวอย่างและรีวิว)")
        for sc in st.session_state.scenes_data:
            with st.expander(f"📍 ฉากที่ {sc.get('scene_number', '-')}: {sc.get('title', 'ไม่มีชื่อฉาก')}", expanded=True):
                st.markdown(f"**เนื้อเรื่องย่อ:** {sc.get('description', '')}")
                c_a, c_b = st.columns(2)
                with c_a:
                    st.markdown(f"🎥 **มุมกล้อง:** `{sc.get('camera_direction', '')}`")
                    st.markdown(f"💡 **แสง/บรรยากาศ:** `{sc.get('lighting_and_atmosphere', '')}`")
                with c_b:
                    st.markdown(f"🔊 **ดนตรี/เสียง:** `{sc.get('audio_cue', '')}`")
                
                st.markdown("**พรอพต์ภาษาอังกฤษ (พร้อมใช้งาน):**")
                st.code(sc.get("video_prompt", sc.get("image_prompt", "")), language="markdown")

# ==========================================
# 8. แท็บที่ 2: ฉากและบทพูดผู้กำกับ (Tab 2)
# ==========================================
def render_tab_director():
    st.subheader("🎬 2. ฉาก & บทพูด (ห้องควบคุมผู้กำกับ)")
    if not st.session_state.scenes_data:
        st.info("ยังไม่มีข้อมูลฉาก กรุณากดวิเคราะห์ฉากในแท็บที่ 1 ก่อน")
        return

    for idx, sc in enumerate(st.session_state.scenes_data):
        st.markdown(f"#### ฉากที่ {idx+1}: {sc.get('title')}")
        col_dir1, col_dir2 = st.columns([1, 1])
        with col_dir1:
            st.text_area(f"บทพูดและไดอะล็อก (ฉากที่ {idx+1})", height=80, key=f"dialogue_{idx}",
                         value="[วิทยุสื่อสาร]: ศูนย์บัญชาการ เราพบการเคลื่อนไหวของวัตถุจักรกลที่พิกัด 9 ขออนุมัติติดตาม...")
        with col_dir2:
            st.text_area(f"โน้ตกำกับการแสดง / บันทึกหน้ากอง (ฉากที่ {idx+1})", height=80, key=f"note_{idx}",
                         value="เน้นความตึงเครียด แสงเงาคมชัด กล้องสั่นไหวเล็กน้อยสไตล์สารคดีสงคราม")
        st.markdown("---")

# ==========================================
# 9. แท็บที่ 3: คาแรกเตอร์และเสียง (Tab 3)
# ==========================================
def render_tab_characters():
    st.subheader("👤 3. DNA ตัวละคร & คลังเสียง (Locker)")
    st.caption("บันทึกลักษณะเฉพาะของตัวละครเพื่อคุมความสม่ำเสมอของภาพ (Consistency) ตลอดทั้งเรื่อง")

    for i, char in enumerate(st.session_state.characters):
        with st.container():
            st.markdown(f"**ตัวละครที่ {i+1}: {char['name']}** ({char['role']})")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input(f"ชื่อและบทบาท", value=f"{char['name']} - {char['role']}", key=f"char_name_{i}")
                st.text_input(f"โทนเสียงและบุคลิกเสียง", value=char['voice'], key=f"char_voice_{i}")
            with c2:
                st.text_area(f"รูปลักษณ์และชุดแต่งกาย (Visual DNA Prompt)", value=char['trait'], key=f"char_trait_{i}", height=100)
            st.markdown("---")

# ==========================================
# 10. แท็บที่ 4: คลังพรอพต์สำเร็จรูป (Tab 4)
# ==========================================
def render_tab_prompt_vault(prompts):
    st.subheader("⚡ 4. คลังพรอพต์ระดับพรีเมียม (10 Cinematic Templates)")
    st.caption("พรอพต์สากลระดับสตูดิโอ พร้อมคัดลอกไปเจนวิดีโอใน Runway, Sora, Kling, Veo และ Midjourney")

    for item in prompts:
        with st.container():
            st.markdown(f"##### 🎯 {item['title']}")
            st.code(item['prompt'], language="markdown")
            st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 11. แท็บที่ 5: ส่งออกบทภาพยนตร์ (Tab 5)
# ==========================================
def render_tab_export():
    st.subheader("🎞️ 5. ส่งออกบทภาพยนตร์และมาสเตอร์สคริปต์ (Export Master Script)")
    st.caption("รวบรวมข้อมูลฉาก ไดอะล็อก และพรอพต์ทั้งหมดเป็นไฟล์สคริปต์ฉบับสมบูรณ์")

    if not st.session_state.scenes_data:
        st.info("ยังไม่มีข้อมูลฉากสำหรับการส่งออก")
        return

    full_script = f"# มหาสึกหุ่นรบแดนดีพิมฟ์ (Master Script)\n\n"
    full_script += f"**เรื่องย่อหลัก:** {st.session_state.story_pitch}\n\n"
    full_script += "## รายละเอียดฉากและพรอพต์\n\n"

    for sc in st.session_state.scenes_data:
        full_script += f"### ฉากที่ {sc.get('scene_number')}: {sc.get('title')}\n"
        full_script += f"- **เนื้อหา:** {sc.get('description')}\n"
        full_script += f"- **มุมกล้อง:** {sc.get('camera_direction')}\n"
        full_script += f"- **การจัดแสง:** {sc.get('lighting_and_atmosphere')}\n"
        full_script += f"- **เสียง:** {sc.get('audio_cue')}\n"
        full_script += f"- **Prompt:** `{sc.get('video_prompt', sc.get('image_prompt', ''))}`\n\n"

    st.text_area("สคริปต์ภาพยนตร์ฉบับเต็ม (Markdown):", value=full_script, height=320)
    st.download_button(
        label="📥 ดาวน์โหลดมาสเตอร์สคริปต์ (.md)",
        data=full_script,
        file_name="master_screenplay.md",
        mime="text/markdown"
    )

# ==========================================
# 12. ฟังก์ชันหลัก (Main Orchestrator)
# ==========================================
def main():
    setup_page_config()
    init_session_state()
    api_key = get_api_key()
    genres, tones, cameras, lightings, prompts = get_preset_data()

    render_header(api_key)

    # แบ่งแท็บการทำงาน (ไม่มีเมนูสร้างคลิปแล้ว)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💡 1. วิเคราะห์แตกฉาก (AI Story)",
        "🎬 2. ฉาก & บทพูด (ผู้กำกับ)",
        "👤 3. DNA ตัวละคร (Locker)",
        "⚡ 4. คลังพรอพต์ (Prompt Vault)",
        "🎞️ 5. ส่งออกบทภาพยนตร์ (Master Script)"
    ])

    with tab1:
        render_tab_story(api_key, genres, tones, cameras, lightings)
    with tab2:
        render_tab_director()
    with tab3:
        render_tab_characters()
    with tab4:
        render_tab_prompt_vault(prompts)
    with tab5:
        render_tab_export()

if __name__ == "__main__":
    main()
