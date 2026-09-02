import streamlit as st

# ตั้งค่าหน้าเว็บสไตล์ Cinema Studio
st.set_page_config(
    page_title="Cinematic AI Film Director Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS ตกแต่งหน้าตาให้อารมณ์สตูดิโอฮอลลีวูดระดับพรีเมียม
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1c24;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: #ffffff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e50914 !important;
        color: white !important;
        font-weight: bold;
    }
    .shot-box {
        background-color: #161a23;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #e50914;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Blockbuster AI Film Director Studio")
st.caption("ระบบสร้างคัมภีร์ภาพยนตร์ (Film Bible) และ Prompt มาตรฐานฮอลลีวูด ป้องกันหน้าเพี้ยน ฉากหลุด ฟิสิกส์เบี้ยว")

# ==========================================
# 1. MASTER UNIVERSE BIBLE (แถบด้านข้าง)
# ==========================================
with st.sidebar:
    st.header("📽️ Master Film Bible")
    
    film_engine = st.selectbox("🎯 Target AI Engine", [
        "Google Flow / Google Veo (Cinematic Video)",
        "Runway Gen-3 Alpha (Photorealistic)",
        "Kling 1.5/2.0 (High Precision Motion)",
        "Midjourney v6.1 + Luma Dream Machine",
        "Sora Cinematic Standard"
    ])
    
    director_preset = st.selectbox("🎥 Director & Visual Aesthetic", [
        "Denis Villeneuve (Dune / Blade Runner 2049) - Brutalist, massive scale, atmospheric haze",
        "Christopher Nolan (Oppenheimer / Interstellar) - 70mm IMAX, practical lighting, muted high contrast",
        "Makoto Shinkai (Your Name) - Hyper-detailed anime, dynamic light refraction, vivid sky",
        "Studio Ghibli (Hayao Miyazaki) - Hand-drawn warmth, lush nature, watercolor skies",
        "Cyberpunk Neo-Noir - Rain-soaked reflections, high-density neon, deep teal & amber",
        "Dark Fantasy Epic (Elden Ring style) - Volumetric grim fog, gothic architecture, rim light"
    ])
    
    lens_type = st.selectbox("📸 Camera Lens & Sensor Rig", [
        "Panavision C-Series 35mm Anamorphic (Cinematic oval bokeh, horizontal blue lens flare)",
        "ARRI ALEXA 65 + 50mm Prime (Clean sharp texture, natural human eye perspective)",
        "85mm Portrait Lens, f/1.4 (Ultra-shallow depth of field, creamy background blur)",
        "14mm Ultra-Wide IMAX (Towering perspective, epic environmental grandeur)"
    ])
    
    color_grade = st.text_input("🎨 Master Color Grade / LUT", "Kodak Vision3 5219 film stock, warm skin tones, desaturated shadows")
    aspect_ratio = st.selectbox("📐 Aspect Ratio", ["2.39:1 (Anamorphic Widescreen Cinema)", "16:9 (Standard Film / YouTube)", "9:16 (Cinematic Short / TikTok)"])
    
    st.divider()
    anti_glitch_toggle = st.checkbox("🛡️ บังคับใช้ Anti-Glitch Protocol (กันหน้าเบี้ยว/แขนงอก)", value=True)

# ==========================================
# 2. CHARACTER DNA VAULT (ล็อกอัตลักษณ์)
# ==========================================
with st.expander("👤 1. Character Identity Locker (DNA ตัวละคร - กันหน้าเปลี่ยน)", expanded=True):
    col_a, col_b, col_c = st.columns([2, 3, 3])
    with col_a:
        char_tag = st.text_input("รหัสตัวละคร (Token Tag)", "HERO_LEAD")
        char_gender_age = st.text_input("เพศและอายุ", "28-year-old East Asian male")
    with col_b:
        char_face = st.text_input("โครงหน้าและจุดเด่น (ห้ามสุ่มเปลี่ยน)", "Chiseled jawline, messy textured taper fade hair, faint scar over left eyebrow, piercing dark eyes")
    with col_c:
        char_wardrobe = st.text_input("ชุดแต่งกายหลัก (Fixed Wardrobe)", "Matte black tactical high-collar trench coat over slate grey shirt, silver dog tag")
    
    wardrobe_state = st.select_slider("สภาพตัวละครในฉากนี้ (State of Wear)", options=["สะอาด/ปกติ (Pristine)", "เหงื่อซึม/เปียกฝน (Sweaty/Wet)", "เปื้อนฝุ่น/คราบควัน (Grimy/Dusty)", "บาดเจ็บ/เสื้อผ้าฉีกขาด (Battle-damaged)"])

# รวมร่าง DNA
character_anchor = f"[{char_tag}: {char_gender_age}, {char_face}, wearing {char_wardrobe}, condition: {wardrobe_state}]"

# ==========================================
# 3. SEQUENCE STORYBOARD MATRIX
# ==========================================
st.subheader("🎬 2. Sequence Storyboard Builder (สร้างฉากต่อเนื่อง)")
num_shots = st.slider("จำนวนฉากต่อเนื่อง (Sequence Shots)", min_value=1, max_value=6, value=3)

shots_data = []

for i in range(num_shots):
    with st.container():
        st.markdown(f"#### 📌 Shot #{i+1}")
        c1, c2, c3, c4 = st.columns([2, 3, 3, 2])
        
        with c1:
            cam_scale = st.selectbox(f"ขนาดภาพ (Shot Scale) #{i+1}", [
                "Extreme Wide Shot (Master Landscape)",
                "Wide Establishing Shot",
                "Medium Cowboy Shot (เอวขึ้นไป)",
                "Close-Up (เน้นสายตา/อารมณ์)",
                "Extreme Close-Up (ดีเทลวัตถุ/แววตา)"
            ], key=f"scale_{i}")
            cam_move = st.selectbox(f"การเคลื่อนกล้อง (Rig Move) #{i+1}", [
                "Static Lock-off (กล้องนิ่ง เพิ่มพลังอารมณ์)",
                "Slow Forward Push Dolly (ดึงอารมณ์เข้าหาตัวละคร)",
                "Steadicam Tracking Forward (เดินตามตัวละคร)",
                "Low-Angle Vertigo Zoom / Dolly Zoom",
                "Cinematic Pan & Tilt Reveal"
            ], key=f"move_{i}")
            
        with c2:
            action_desc = st.text_area(f"การกระทำและการแสดงอารมณ์ (Action & Emotion) #{i+1}", 
                "ก้าวเท้าช้าๆ ผ่านซากปรักหักพัง หยุดมองขึ้นไปบนฟ้าด้วยสายตาที่เปี่ยมไปด้วยความหวังปนเหนื่อยล้า", key=f"act_{i}", height=100)
            
        with c3:
            env_desc = st.text_area(f"สถานที่และแสงเฉพาะฉาก (Environment & Light) #{i+1}", 
                "ซากมหานครร้างหลังสงคราม แสงแดดยามเย็นส่องทะลุผ่านช่องตึก มีละอองฝุ่นและประกายควันลอยในอากาศ", key=f"env_{i}", height=100)
            
        with c4:
            sound_cue = st.text_input(f"เสียงพากย์ / Foley #{i+1}", "เสียงลมหวีดหวิว และคำพูด: 'เรามาไกลเกินจะถอยแล้ว'", key=f"snd_{i}")
            transition = st.selectbox(f"คัตต่อไป (Cut Style) #{i+1}", ["Hard Cut", "Match Cut (เชื่อมรูปทรง)", "Whip Pan (สะบัดกล้อง)"], key=f"cut_{i}")

        shots_data.append({
            "num": i+1,
            "scale": cam_scale,
            "move": cam_move,
            "action": action_desc,
            "env": env_desc,
            "sound": sound_cue,
            "transition": transition
        })

# ==========================================
# 4. EXPORT & PRODUCTION DELIVERY PACKS
# ==========================================
st.divider()
st.header("🚀 3. Master Production Delivery Packs")

# กฎ Anti-Glitch Universal
negative_tokens = "bad anatomy, extra limbs, fused fingers, distorted face, inconsistent costume, morphing background, 3D render plastic look, oversaturated, text, watermark, jittery motion, abrupt camera jump"

tab_a, tab_b, tab_c = st.tabs([
    "🖼️ Step 1: Keyframe Prompts (เจนภาพนิ่งเพื่อล็อกหน้า)",
    "🎥 Step 2: Video Motion Prompts (คำสั่งแปลงเป็นวิดีโอ)",
    "📄 Step 3: Sound & Director Sheet (เล่มคิวเสียง/ตัดต่อ)"
])

# แยกสัดส่วนเป็นตัวเลข
ar_tag = aspect_ratio.split(" ")[0]

with tab_a:
    st.info("💡 **ขั้นตอนระดับฮอลลีวูด:** คัดลอก Prompt ด้านล่างนี้ไปเจนเป็น 'ภาพนิ่ง' ก่อนเสมอ เมื่อได้ภาพที่หน้าเป๊ะ แสงตรงใจ ให้เซฟภาพนั้นไว้เป็น **Reference Keyframe**")
    for s in shots_data:
        full_keyframe = (
            f"Cinematic masterpiece, film still from {director_preset.split(' - ')[0]} movie, "
            f"{s['scale']}, {character_anchor}, {s['action']}, "
            f"location: {s['env']}, cinematography: shot on {lens_type}, {color_grade}, "
            f"volumetric lighting, photorealistic 8k, hyper-detailed texture --ar {ar_tag} --no {negative_tokens}"
        )
        st.markdown(f"**🎬 Shot #{s['num']} Keyframe Prompt:**")
        st.code(full_keyframe, language="markdown")

with tab_b:
    st.info("💡 **นำภาพนิ่งจาก Step 1 ไปอัปโหลดเข้า AI Video (Google Flow/Veo, Runway, Kling)** แล้วใส่คำสั่งด้านล่างนี้ในช่อง Motion/Prompt เพื่อให้ตัวละครเคลื่อนไหวสมจริงโดยที่หน้าไม่เปลี่ยนรูป")
    for s in shots_data:
        full_motion = (
            f"**[SHOT {s['num']} MOTION SCRIPT]**\n"
            f"• **Camera Movement:** {s['move']}\n"
            f"• **Physical Action:** Subject maintains identity, {s['action']}\n"
            f"• **Atmospheric Physics:** Consistent realistic physics, soft wind blowing hair, natural cloth simulation, subtle floating environmental particles\n"
            f"• **Continuity:** Lock facial structure and wardrobe from input image. Smooth temporal motion, no morphing."
        )
        st.code(full_motion, language="markdown")

with tab_c:
    st.markdown("### 📋 Director's Production Breakdown")
    for s in shots_data:
        st.markdown(f"""
        **Shot #{s['num']}** | *Transition: {s['transition']}*
        * **ภาพ:** {s['scale']} | {s['move']}
        * **การแสดง:** {s['action']}
        * **เสียงพากย์ / Foley Effect:** {s['sound']}
        ---
        """)
