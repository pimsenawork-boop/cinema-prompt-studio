import os
import json
import requests
import streamlit as st

# ---------------------------------------------------------
# UI Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Studio: Film Director & Affiliate Creator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .affiliate-card {
        background: linear-gradient(135deg, #1c1f2e 0%, #12141f 100%);
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #ff007f;
        margin-bottom: 14px;
    }
    .flow-card {
        background: #141824;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #232b3e;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ระบบฐานข้อมูลโปรเจกต์หนัง (Database)
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
                    "emotion": "ตึงเครียด โดดเดี่ยว",
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
# ฟังก์ชัน AI สำหรับโหมดหนัง
# ---------------------------------------------------------
def analyze_story_and_breakdown(story_pitch, genre, character_name):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    prompt_query = f"""
    Analyze movie pitch: Genre: {genre}, Lead: {character_name}, Pitch: {story_pitch}.
    Break down into 3-4 scenes in strictly valid JSON array with keys:
    "title", "summary", "emotion", "action", "environment", "dialogue", "voice_direction", "camera_move".
    Output in Thai language. No markdown backticks.
    """
    try:
        res = requests.post(url, headers=headers, json={"contents": [{"parts": [{"text": prompt_query}]}]}, timeout=25)
        txt = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        if txt.startswith("```"):
            txt = txt.split("\n", 1)[1].rsplit("\n", 1)[0].replace("json", "").strip()
        return json.loads(txt)
    except Exception:
        return None

# ---------------------------------------------------------
# เมนูหลักด้านซ้าย (Main Mode Selector)
# ---------------------------------------------------------
with st.sidebar:
    st.image("[https://img.icons8.com/color/96/film-reel.png](https://img.icons8.com/color/96/film-reel.png)", width=60)
    app_mode = st.radio(
        "🎯 เลือกโหมดการทำงาน:",
        ["🎬 สร้างหนัง (Cinematic Studio)", "🛍️ สร้างคลิป (Affiliate Video Creator)"]
    )
    st.divider()

# ==============================================================================
# โหมดที่ 1: สร้างหนัง (CINEMATIC AI DIRECTOR)
# ==============================================================================
if app_mode == "🎬 สร้างหนัง (Cinematic Studio)":
    with st.sidebar:
        st.subheader("📂 จัดการโปรเจกต์ภาพยนตร์")
        project_list = list(st.session_state.projects.keys())
        selected_project_name = st.selectbox("เลือกโปรเจกต์:", project_list)
        
        with st.expander("➕ สร้างเรื่องใหม่"):
            new_t = st.text_input("ชื่อเรื่อง")
            new_g = st.selectbox("แนวหนัง", ["ไซไฟ / เอาชีวิตรอด", "แฟนตาซี แอ็กชัน", "สืบสวน นัวร์", "อนิเมะ"])
            new_log = st.text_area("เรื่องย่อหลัก")
            if st.button("ยืนยันสร้างโปรเจกต์", use_container_width=True):
                if new_t.strip():
                    st.session_state.projects[new_t] = {
                        "genre": new_g, "logline": new_log, "style": "Cinematic 35mm Film",
                        "lighting": "Volumetric sunlight", "aspect_ratio": "16:9",
                        "char_name": "HERO", "char_look": "Asian male, athletic build",
                        "char_persona": "สุขุม เด็ดเดี่ยว", "char_voice": "เสียงทุ้ม หนักแน่น",
                        "char_outfit": "Dark utility jacket", "scenes": []
                    }
                    save_projects(st.session_state.projects)
                    st.rerun()

    current_proj = st.session_state.projects[selected_project_name]
    st.title(f"🎬 กำกับภาพยนตร์: {selected_project_name}")
    st.caption(f"**แนว:** {current_proj.get('genre','')} | **เรื่องย่อ:** {current_proj.get('logline','')}")

    tab_story, tab_scenes, tab_char, tab_export = st.tabs([
        "💡 1. ป้อนไอเดียแตกฉาก (Story Breakdown)",
        "🎬 2. ผู้กำกับฉาก & บทพูด (Scene Director)",
        "👤 3. DNA ตัวละคร & น้ำเสียง (Character Locker)",
        "📋 4. เล่มบทภาพยนตร์ (Master Script)"
    ])

    with tab_story:
        st.subheader("🧠 วิเคราะห์พล็อตหนังและพรีวิวฉาก")
        pitch_in = st.text_area("เล่าไอเดียเรื่องนี้:", value=current_proj.get("logline", ""), height=100)
        if st.button("✨ ให้ AI วิเคราะห์แตกเป็นฉากๆ"):
            with st.spinner("กำลังประมวลผลโครงเรื่อง..."):
                res_breakdown = analyze_story_and_breakdown(pitch_in, current_proj.get("genre", ""), current_proj.get("char_name", "HERO"))
                if res_breakdown:
                    current_proj["scenes"] = res_breakdown
                    current_proj["logline"] = pitch_in
                    save_projects(st.session_state.projects)
                    st.success("วิเคราะห์ฉากสำเร็จ!")
                    st.rerun()

        if current_proj.get("scenes"):
            st.markdown("### 👁️ ภาพรวมฉากก่อนนำไปเจนวิดีโอ")
            for idx, sc in enumerate(current_proj["scenes"]):
                st.markdown(f"""
                <div class="flow-card">
                    <b>ฉากที่ {idx+1}: {sc.get('title', '')}</b> | <i>อารมณ์: {sc.get('emotion', '')}</i><br>
                    • <b>บริบท:</b> {sc.get('summary', '')}<br>
                    • <b>การกระทำ:</b> {sc.get('action', '')}<br>
                    • <b>บทพูด:</b> "{sc.get('dialogue', '')}" <span style="color:#f39c12;">{sc.get('voice_direction', '')}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab_scenes:
        st.subheader("🎬 ปรับแต่งฉากและสร้างพร่อม Google Flow")
        ar_tag = current_proj.get("aspect_ratio", "16:9")
        char_token = f"[{current_proj.get('char_name','HERO')}: {current_proj.get('char_look','')}, wearing {current_proj.get('char_outfit','')}]"
        
        for i, sc in enumerate(current_proj["scenes"]):
            with st.expander(f"📍 ฉากที่ {i+1}: {sc.get('title', '')}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    sc["action"] = st.text_input(f"การกระทำ #{i+1}", sc.get("action", ""), key=f"mv_act_{i}")
                    sc["dialogue"] = st.text_input(f"บทพูด #{i+1}", sc.get("dialogue", ""), key=f"mv_dia_{i}")
                with c2:
                    sc["env"] = st.text_input(f"สถานที่และแสง #{i+1}", sc.get("env", ""), key=f"mv_env_{i}")
                    sc["voice_direction"] = st.text_input(f"คิวเสียง #{i+1}", sc.get("voice_direction", ""), key=f"mv_vd_{i}")

                flow_prompt = f"Google Flow Prompt: Cinematic {sc.get('camera_move', 'dolly in')}, {char_token}, {sc.get('action','')}, location: {sc.get('env','')}, {current_proj.get('lighting','')}, {current_proj.get('style','')}, 35mm lens, temporal stability --ar {ar_tag}"
                st.code(flow_prompt, language="text")

        if st.button("💾 บันทึกการแก้ไขฉากทั้งหมด"):
            save_projects(st.session_state.projects)
            st.toast("บันทึกเรียบร้อย!", icon="✅")

    with tab_char:
        st.subheader("👤 Character DNA & Voice Anchor")
        ca, cb = st.columns(2)
        with ca:
            current_proj["char_name"] = st.text_input("รหัสตัวละคร", current_proj.get("char_name", "HERO"))
            current_proj["char_look"] = st.text_area("โครงหน้า/จุดเด่นบนใบหน้า", current_proj.get("char_look", ""))
        with cb:
            current_proj["char_outfit"] = st.text_area("ชุดประจำตัว", current_proj.get("char_outfit", ""))
            current_proj["char_voice"] = st.text_input("โปรไฟล์เสียงพูด", current_proj.get("char_voice", ""))
        if st.button("💾 บันทึก DNA"):
            save_projects(st.session_state.projects)
            st.toast("บันทึกสำเร็จ!", icon="✅")

    with tab_export:
        st.subheader("📋 เล่มบทภาพยนตร์มาตรฐาน")
        scr = f"PROJECT: {selected_project_name}\n\n"
        for idx, sc in enumerate(current_proj["scenes"]):
            scr += f"SCENE {idx+1}: {sc.get('title','')}\nACTION: {sc.get('action','')}\nDIALOGUE: \"{sc.get('dialogue','')}\"\n---\n"
        st.text_area("Script", scr, height=250)
        st.download_button("📥 ดาวน์โหลดเล่มบท (.txt)", data=scr, file_name=f"{selected_project_name}.txt")

# ==============================================================================
# โหมดที่ 2: สร้างคลิป (AFFILIATE VIDEO CREATOR FOR GOOGLE FLOW)
# ==============================================================================
else:
    st.title("🛍️ Affiliate Video Studio (สร้างคลิปขายของปักตะกร้า)")
    st.caption("ระบบแกะโครงสร้างคลิปที่สร้างยอดขายและค่าคอมหลักล้าน แปลงเป็น Prompt วิดีโอ 9:16 สำหรับ Google Flow")

    # ส่วนกรอกข้อมูลสินค้า
    with st.container():
        st.markdown("""<div class="affiliate-card"><h4>📦 ข้อมูลสินค้าที่จะทำคลิปปักตะกร้า</h4></div>""", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns([2, 2, 2])
        with col_p1:
            prod_name = st.text_input("ชื่อสินค้า", "เซรั่มไฮยาหน้าฉ่ำโกลว์ (Glow Hyaluronic Serum)")
            prod_category = st.selectbox("หมวดหมู่สินค้า", [
                "สกินแคร์ / เครื่องสำอาง (Beauty & Skincare)",
                "ของใช้ในบ้าน / แม่บ้าน (Home & Kitchen)",
                "แกดเจ็ต / ไอที / โต๊ะคอม (Tech & Gadgets)",
                "เสื้อผ้า / แฟชั่น / เครื่องประดับ (Fashion & Lifestyle)",
                "อาหาร / ขนม / เครื่องดื่ม (Food & Snacks)"
            ])
        with col_p2:
            pain_point = st.text_input("ปัญหาหลักที่สินค้าแก้ (Pain Point)", "ผิวแห้งกร้าน แต่งหน้าไม่ติด รูขุมขนกว้าง")
            selling_point = st.text_input("จุดขายที่ว้าวสุด (Selling Point)", "หยดเดียวซึมทันที หน้าฉ่ำเงาแบบผิวกระจกใน 3 วิ")
        with col_p3:
            price_offer = st.text_input("โปรโมชันกระตุ้นซื้อ", "1 แถม 1 วันนี้วันเดียว มีคูปองส่งฟรีในตะกร้า")
            formula_type = st.selectbox("สูตรการเล่าเรื่อง (โครงสร้างยอดขายล้านแตก)", [
                "1. ASMR Macro & Sensory (ซูมลึก เน้นผิวสัมผัสชวนฟิน)",
                "2. ปัญหาพังยับ ➔ กู้ชีพทันที (Before/After พลิกชีวิต)",
                "3. แกะกล่องป้ายยา (Unboxing & First Impression สไตล์ของดีบอกต่อ)",
                "4. ยกระดับชีวิต มินิมอลหรูหรา (Aesthetic Lifestyle สร้างความอยากได้)"
            ])

    st.divider()

    # สร้างข้อมูลฉาก 4 คัตมาตรฐานวิดีโอสั้น 15 วินาที
    if "1. ASMR" in formula_type:
        shots = [
            {
                "time": "0-3s (Hook สะกดนิ้ว)",
                "action": f"โคลสอัพขั้นสุด เนื้อของ {prod_name} กำลังหยดลงบนพื้นผิวอย่างช้าๆ เนื้อสัมผัสใสสะท้อนแสงแวววาว",
                "flow_prompt": f"Macro 8k shot, vertical 9:16, crystal clear viscous droplet of {prod_name} slowly falling and splashing smoothly onto glass surface, studio softbox lighting, satisfying fluid physics, hyper-detailed texture, shot on 100mm macro lens, temporal stability",
                "voice": f"ใครที่กำลังเจอปัญหา {pain_point} หยุดดูคลิปนี้ก่อนเลยค่ะ!",
                "cue": "[พูดน้ำเสียงตื่นเต้น กระแทกเสียงหยุดคนดู]"
            },
            {
                "time": "3-7s (โชว์การใช้งาน)",
                "action": f"มือที่มีผิวเรียบเนียน ลูบเกลี่ยเนื้อ {prod_name} ลงบนผิว เนื้อเซรั่มแตกตัวซึมหายวับทันที",
                "flow_prompt": f"Tight close-up shot, vertical 9:16, elegant hand smoothly massaging glowing {prod_name} into pristine skin, instant absorption effect, glistening dewy moisture trail, natural soft window morning light, realistic skin pores, no distortion",
                "voice": f"ดูความฉ่ำนี้สิคะ {selling_point} ซึมไวมาก ไม่เหนียวเหนอะหนะเลยสักนิด",
                "cue": "[น้ำเสียงกระซิบกึ่ง ASMR ชวนเคลิ้ม]"
            },
            {
                "time": "7-11s (ผลลัพธ์ว้าว)",
                "action": f"ผิวหน้าหันรับแสง สะท้อนเงาโกลว์แบบผิวกระจก มีประกายแสงนุ่มนวล",
                "flow_prompt": f"Medium close-up portrait, vertical 9:16, flawless glowing face turning slightly into soft key light, radiant glass skin reflection, confident gentle smile, cinematic depth of field, commercial cosmetic grade",
                "voice": f"ดูผลลัพธ์สิคะ ผิวเปลี่ยนทันทีเหมือนเข้าสปามาเป็นหมื่น",
                "cue": "[น้ำเสียงทึ่งและมั่นใจสุดขีด]"
            },
            {
                "time": "11-15s (Call To Action ปักตะกร้า)",
                "action": f"ขวด {prod_name} วางคู่กล่องสวยงาม กล้องดอลลี่ดันเข้าหาขวดอย่างนิ่งสงบพร้อมปุ่มชี้มุมซ้ายล่าง",
                "flow_prompt": f"Crisp commercial product display, vertical 9:16, {prod_name} centered on sleek minimalist marble pedestal, slow elegant dolly push-in, bright studio rim light, static camera balance, clean 4k",
                "voice": f"พิกัดอยู่ในตะกร้าเหลืองซ้ายมือแล้วนะ {price_offer} รีบกดก่อนของหมดค่ะ!",
                "cue": "[น้ำเสียงเร่งรีบ ชี้ชวนให้รีบกดตะกร้าทันที]"
            }
        ]
    elif "2. ปัญหาพังยับ" in formula_type:
        shots = [
            {
                "time": "0-3s (Hook ปัญหาหนัก)",
                "action": f"ภาพความเลอะเทอะหรือปัญหา {pain_point} แบบเห็นชัดคาตา สร้างความหงุดหงิดให้คนดู",
                "flow_prompt": f"Dramatic eye-level close-up, vertical 9:16, visible extreme problem of {pain_point} on surface, harsh textured reality, authentic handheld realism, high clarity",
                "voice": f"ถ้าคุณเบื่อกับปัญหา {pain_point} ซ้ำซากแบบนี้...",
                "cue": "[น้ำเสียงเหนื่อยหน่าย เจ็บปวดแทนคนดู]"
            },
            {
                "time": "3-7s (พระเอกขี่ม้าขาว)",
                "action": f"หยิบ {prod_name} ขึ้นมาใช้งาน ปาดเพียงครั้งเดียวจัดการปัญหาเรียบวุธ",
                "flow_prompt": f"Dynamic tracking shot, vertical 9:16, using {prod_name} to wipe across the dirty surface in one single effortless stroke, instant clean contrast line revealed, satisfying physics",
                "voice": f"ตั้งแต่ได้ {prod_name} ตัวนี้มา ชีวิตเปลี่ยนไปคนละเรื่องเลย!",
                "cue": "[น้ำเสียงสดใส โล่งใจ ประทับใจ]"
            },
            {
                "time": "7-11s (ผลลัพธ์สะอาดกริบ)",
                "action": f"มุมกว้างเห็นพื้นที่สะอาดเอี่ยม สะท้อนแสงเงาวับ ไร้ร่องรอยปัญหาเดิม",
                "flow_prompt": f"Wide clean angle, vertical 9:16, spotless sparkling surface, pristine perfection, bright warm sunlight illuminating the flawless outcome, stable camera",
                "voice": f"{selling_point} ทำได้จริง ไม่จกตา ประหยัดเวลาไปได้เยอะมาก",
                "cue": "[น้ำเสียงการันตี ยืนยันความคุ้มค่า]"
            },
            {
                "time": "11-15s (ปิดการขาย)",
                "action": f"โชว์ตัวสินค้า {prod_name} พร้อมนิ้วชี้ลงมุมซ้ายล่างของจอ",
                "flow_prompt": f"Product hero shot, vertical 9:16, {prod_name} standing proudly in center, slow focus pull, clean studio background, sharp packaging text",
                "voice": f"ตะกร้าเหลืองมีคูปองลดพิเศษอยู่ด้วย {price_offer} จิ้มที่มุมซ้ายล่างได้เลย!",
                "cue": "[น้ำเสียงเชิญชวน กระตุ้นให้กดทันที]"
            }
        ]
    else:
        # พรีเซ็ตมาตรฐาน Unboxing / Lifestyle
        shots = [
            {
                "time": "0-3s (Hook แกะกล่อง)",
                "action": f"มือค่อยๆ แกะกล่อง {prod_name} เผยให้เห็นดีไซน์พรีเมียมกระแทกตา",
                "flow_prompt": f"Overhead flat-lay unboxing, vertical 9:16, hands unboxing aesthetic package revealing sleek {prod_name}, crisp shadows, warm Nordic morning light",
                "voice": f"เพิ่งได้ของมาสดๆ ร้อนๆ บอกเลยว่าตัวนี้ของขาดตลาดบ่อยมาก!",
                "cue": "[น้ำเสียงตื่นเต้น ปนกระซิบความลับ]"
            },
            {
                "time": "3-7s (โชว์ฟังก์ชัน)",
                "action": f"ทดลองใช้งาน {prod_name} โชว์ดีเทลการทำงานที่ง่ายดายและสวยงาม",
                "flow_prompt": f"Medium shot, vertical 9:16, operating {prod_name} with fluid natural hand motion, aesthetic living room background, realistic product physics",
                "voice": f"ดีไซน์สวยไม่พอ {selling_point} ใช้งานจริงคือปังมาก",
                "cue": "[น้ำเสียงชื่นชมจากใจ]"
            },
            {
                "time": "7-11s (ความพึงพอใจ)",
                "action": f"โชว์ความสุขในการใช้งาน ตัวสินค้าเข้ากับชีวิตประจำวันได้อย่างลงตัว",
                "flow_prompt": f"Cinematic lifestyle shot, vertical 9:16, subject smiling happily interacting with {prod_name}, cozy golden hour interior, creamy background blur",
                "voice": f"บอกเลยว่าคุ้มเกินราคาไปไกล ใครไม่มีติดบ้านไว้คือพลาดสุดๆ",
                "cue": "[น้ำเสียงมั่นใจ ป้ายยาเต็มที่]"
            },
            {
                "time": "11-15s (จิ้มตะกร้า)",
                "action": f"สินค้าตั้งเด่น กล้องดึงถอยหลังช้าๆ เพื่อให้เห็นภาพรวมพร้อมชี้ไปที่ตะกร้า",
                "flow_prompt": f"Static center-framed commercial, vertical 9:16, {prod_name} prominently featured, subtle warm lighting flare, 8k crisp focus",
                "voice": f"พิกัดแท้แปะไว้ในตะกร้าให้แล้วนะคะ {price_offer} จิ้มตะกร้าเหลืองเลย!",
                "cue": "[น้ำเสียงกระตือรือร้น ย้ำตะกร้าเหลือง]"
            }
        ]

    st.subheader("🎬 สคริปต์และพร่อม Google Flow (พร้อมนำไปสร้างคลิป 15 วินาที)")
    st.info("💡 **วิธีทำเงิน:** นำพร่อมในแต่ละช่วงเวลาไปเจนคลิปแนวตั้ง (9:16) ใน **Google Flow** จากนั้นนำทั้ง 4 คลิปมาต่อกันใน CapCut แล้วอัดเสียงตามบทพากย์ด้านล่าง ปักตะกร้าเหลืองลง TikTok หรือ Shopee Video ได้ทันที")

    for idx, s in enumerate(shots):
        with st.expander(f"📌 ท่อนที่ {idx+1}: {s['time']}", expanded=True):
            col_v1, col_v2 = st.columns([1, 1])
            with col_v1:
                st.markdown(f"**🏃 สิ่งที่เห็นในวิดีโอ:** {s['action']}")
                st.markdown(f"**🎙️ บทพากย์ (Voiceover):**")
                st.markdown(f"*{s['voice']}*")
                st.caption(f"🎭 **คิวอารมณ์เสียง:** {s['cue']}")
            with col_v2:
                st.markdown(f"**📋 Google Flow Prompt (คัดลอกลง Google Flow):**")
                st.code(s["flow_prompt"], language="text")

    # รวมเล่มดาวน์โหลด
    full_affiliate_script = f"=== สคริปต์คลิปปักตะกร้า: {prod_name} ===\nสูตร: {formula_type}\nจุดขาย: {selling_point}\n\n"
    for idx, s in enumerate(shots):
        full_affiliate_script += f"[{s['time']}]\nภาพ: {s['action']}\nเสียง: {s['voice']} {s['cue']}\nPrompt: {s['flow_prompt']}\n\n"

    st.download_button("📥 ดาวน์โหลดสคริปต์คลิปปักตะกร้า (.txt)", data=full_affiliate_script, file_name=f"affiliate_{prod_name}.txt")
