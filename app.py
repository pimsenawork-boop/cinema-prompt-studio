import streamlit as st

st.set_page_config(page_title="Cinematic AI Prompt Director (PRO)", layout="wide")
st.title("🎬 Cinematic AI Director Studio (PRO)")
st.caption("ระบบสร้าง Storyboard Prompt คุมอัตลักษณ์ตัวละคร แสง และมุมกล้อง ป้องกันภาพหลุดเพี้ยน")

# 1. Master Style & Rules
with st.sidebar:
    st.header("👑 Project Master DNA")
    style_genre = st.selectbox("Style & Engine Presets", [
        "Cinematic 35mm Film (Kodak Portra, subtle grain, natural skin tone)",
        "Anime / Makoto Shinkai (Vibrant sky, detailed reflections, cel-shaded)",
        "3D Animation Pixar/Dreamworks (Subsurface scattering, soft ambient light)",
        "Dark Fantasy / Unreal Engine 5 (Hyper-detailed, volumetric fog, rim lighting)"
    ])
    aspect_ratio = st.selectbox("Aspect Ratio", ["16:9 (Landscape / Cinema)", "9:16 (Portrait / Reels / TikTok)"])
    global_lighting = st.text_input("Master Lighting / Palette", "Golden hour light, warm volumetric rays, cyan shadows")
    st.divider()
    st.markdown("💡 **Pro Tip**: การไม่ให้ตัวละครเพี้ยน ต้องใช้ระบบ *Keyframe-to-Video* (เจนภาพนิ่งก่อน แล้วเอาภาพนิ่งไปสร้างการเคลื่อนไหว)")

# 2. Character Anchor
st.subheader("👤 1. Character Identity Locker (ล็อกสเปกตัวละคร)")
col_c1, col_c2 = st.columns(2)
with col_c1:
    char_name = st.text_input("Character Code Name (เช่น Char_A, Alex)", "Protagonist_A")
    char_age_ethnicity = st.text_input("Age & Ethnicity", "25-year-old East Asian")
with col_c2:
    char_clothing = st.text_input("Fixed Outfit (ชุดห้ามเปลี่ยนทั้งเรื่อง)", "Dark olive utility jacket over black turtleneck, silver pendant")
    char_features = st.text_input("Distinctive Facial Features (จุดเด่นบนหน้า)", "Defined jawline, textured fade haircut, slight scar on left eyebrow")

char_dna = f"{char_age_ethnicity}, {char_features}, wearing {char_clothing}"

# 3. Scene Breakdown
st.subheader("📽️ 2. Scene-by-Scene Storyboard")
num_shots = st.slider("จำนวนฉาก (Sequence Shots)", 1, 6, 3)

shots = []
for i in range(num_shots):
    with st.expander(f"📌 Sequence Shot #{i+1}", expanded=True):
        c1, c2, c3 = st.columns([2, 3, 3])
        with c1:
            cam = st.selectbox(f"Camera Shot #{i+1}", [
                "Static Wide Establishing Shot",
                "Medium Tracking Shot (Following Subject)",
                "Extreme Close-Up, Rack Focus",
                "Low Angle Dynamic Push-in Shot"
            ], key=f"cam_{i}")
        with c2:
            act = st.text_input(f"Action & Emotion #{i+1}", "walking through doorway, looking around in awe", key=f"act_{i}")
            trans = st.selectbox(f"Transition #{i+1}", ["Hard cut", "Match cut", "Whip pan", "Fade to black"], key=f"trans_{i}")
        with c3:
            dialogue = st.text_input(f"Voiceover / Dialogue #{i+1}", "ไม่มีทางที่เราจะหันหลังกลับไปได้อีกแล้ว...", key=f"dia_{i}")
            bg = st.text_input(f"Location Details #{i+1}", "abandoned greenhouse, shattered glass, overgrown moss", key=f"bg_{i}")
            
        shots.append({
            "num": i+1,
            "cam": cam,
            "act": act,
            "dialogue": dialogue,
            "bg": bg,
            "trans": trans
        })

# 4. Delivery Outputs
st.divider()
st.subheader("🚀 3. Production Delivery Packs")

tab1, tab2 = st.tabs(["🖼️ Step A: Image Keyframe Prompts (เจนภาพนิ่งเพื่อล็อกหน้า)", "🎥 Step B: Video Motion Prompts (เจนความเคลื่อนไหว)"])

with tab1:
    st.info("นำชุดคำสั่งนี้ไปสร้างภาพนิ่งใน Midjourney, SDXL, หรือ Kling Image เพื่อเลือกภาพที่ดีที่สุดเป็น Master Keyframe")
    for s in shots:
        keyframe_prompt = f"{char_name}, {char_dna}, {s['act']}, {s['bg']}, {global_lighting}, {style_genre}, composition: {s['cam']} --ar {aspect_ratio.split(' ')[0]}"
        st.markdown(f"**Shot {s['num']} Keyframe:**")
        st.code(keyframe_prompt, language="markdown")

with tab2:
    st.info("ใช้ภาพ Keyframe จาก Step A เป็น Image Input แล้วใส่คำสั่งด้านล่างนี้ลงในช่อง Motion / Text Prompt ของ AI Video (Runway, Kling, Luma)")
    for s in shots:
        st.markdown(f"**Shot {s['num']} Video Guide:**")
        st.markdown(f"- **Motion:** {s['act']}, {s['cam']}")
        st.markdown(f"- **Voiceover Script:** \"{s['dialogue']}\"")
        st.markdown(f"- **Cut Transition:** {s['trans']}")
        st.divider()