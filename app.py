# -*- coding: utf-8 -*-
"""
AI Film & Cinematic Prompt Studio (Google Flow Edition)
- แยกฟังก์ชันการทำงานชัดเจน (Modular Functions)
- นำเมนูสร้างคลิปออก
- ตัวเลือกแนวทางสร้างภาพยนตร์ 30 ตัวเลือกต่อหมวด (รวม 120 ตัวเลือก)
- คลังพรอพต์ระดับสตูดิโอ 30 รูปแบบ พร้อมช่องค้นหา
- จัดการ API Key และลบ External Image URL ที่ทำให้แอปแครช
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
            
    if not api_key:
        with st.sidebar:
            st.warning("⚠️ ไม่พบ GEMINI_API_KEY ใน Environment Variables")
            api_key = st.text_input("กรอก GEMINI_API_KEY เพื่อทดสอบ:", type="password")
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
            {"name": "จ่าสิบเอกเอกภาพ", "role": "ผู้นำหน่วยลาดตระเวน", "trait": "สุขุม ชำนาญยุทธวิธี โดนหลอกหลอนด้วยอดีตสงคราม ชุดเกราะภาคสนามถลอก", "voice": "ทุ้มต่ำ นิ่ง หนักแน่น สั่งการเด็ดขาด"},
            {"name": "โอเมก้า-07", "role": "หุ่นรบ AI ลาดตระเวน", "trait": "เกราะเหล็กคอมโพสิตดำด้าน รอยกระสุนและคราบเขม่าดินปืน ดวงตาเซนเซอร์ฟ้า", "voice": "เสียงสังเคราะห์คลื่นสั้น มีเสียงวิทยุแทรก"}
        ]

# ==========================================
# 4. ชุดข้อมูลตัวเลือก (30 รายการต่อหมวด) และ 30 พรอพต์
# ==========================================
def get_preset_data():
    # 30 แนวภาพยนตร์ (Movie Genres)
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
        "10. กำลังภายในแฟนตาซีร่วมสมัย (Cyber-Wuxia Epic)",
        "11. ฮาร์ดไซไฟสำรวจอวกาศลึก (Hard Sci-Fi Deep Space Exploration)",
        "12. สัตว์ประหลาดยักษ์ถล่มเมือง (Kaiju Disaster & Titan Siege)",
        "13. แอ็กชันเรโทรซินธ์เวฟ 80s (Retro 80s Synthwave Action)",
        "14. โกธิกสยองขวัญเหนือธรรมชาติ (Gothic Supernatural Horror)",
        "15. การกลายพันธุ์และชีวภาพ (Biopunk Genetic Mutants)",
        "16. โลกจารกรรมสายลับสงครามเย็น (Espionage Cold War Infiltration)",
        "17. ดีเซลพังก์สงครามสนามเพลาะ (Dieselpunk Heavy Armored Trench War)",
        "18. สยองขวัญคอสมิกจักรวาล (Cosmic Lovecraftian Horror)",
        "19. วิกฤตซอมบี้ปิดล้อมเมือง (Zombie Outbreak Quarantine Zone)",
        "20. สงครามครูเสดและปิดล้อมปราสาท (Medieval Siege & Crusades)",
        "21. มหันตภัยพายุสุริยะล้างโลก (Solar Storm & Natural Cataclysm)",
        "22. ไซไฟสำรวจใต้สมุทรลึก (Abyssal Deep-Sea Sci-Fi)",
        "23. คาวบอยอวกาศล่าค่าหัว (Space Western Bounty Hunter)",
        "24. ระทึกขวัญวงวนมิติคู่ขนาน (Time Loop Paradox Thriller)",
        "25. หุ่นยนต์ก่อกบฏยึดครองโลก (AI Uprising & Android Rebellion)",
        "26. สืบสวนเวทมนตร์ในเมืองหลวง (Urban Fantasy Occult Detective)",
        "27. โจรกรรมไฮเทควางแผนปล้น (High-Stakes Heist & Infiltration)",
        "28. วิวัฒนาการข้ามขีดมนุษย์ (Post-Human Transhumanist Odyssey)",
        "29. สงครามทวยเทพและเทวตำนาน (Ancient Mythology & God Wars)",
        "30. สังเวียนเดนตายประลองชีวิต (Gladiator Deathmatch & Prison Arena)"
    ]

    # 30 โทนและอารมณ์ (Tone & Mood)
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
        "10. เหนือจริง ฝันร้าย ภาพหลอน (Surreal, Psychedelic & Nightmare)",
        "11. สงบนิ่งก่อนพายุใหญ่ (Ominous Calm Before the Storm)",
        "12. ดุดัน กระหายเลือด ไร้ความปรานี (Ruthless, Brutal & Visceral)",
        "13. หม่นหมอง อาลัยอาวรณ์ซากอดีต (Nostalgic, Mournful & Haunting)",
        "14. บีบคั้นหัวใจ วิกฤติความเป็นความตาย (Heart-Wrenching Survival Agony)",
        "15. ตลกร้าย เย้ยหยันชะตากรรม (Dark Humorous & Cynical Satire)",
        "16. ตื่นตาตื่นใจ มหัศจรรย์เหนือจินตนาการ (Awe-Inspiring & Sense of Wonder)",
        "17. วังเวง เย็นยะเยือก ขนหัวลุก (Chilling, Spine-Tingling Dread)",
        "18. เคว้งคว้าง สูญเสียตัวตน (Disoriented, Existential Vacuum)",
        "19. เร้าใจระเบิดอารมณ์ ปะทะเดือด (Adrenaline-Fueled Explosive Action)",
        "20. ศักดิ์สิทธิ์ ขลัง ทรงพลังอำนาจ (Sacred, Ritualistic & Mythical Reverence)",
        "21. สวยงามบนความพังทลาย (Poetic Tragedy & Beautiful Decay)",
        "22. ทะเยอทะยาน คลั่งแค้น บ้าคลั่ง (Obsessive, Vengeful Madness)",
        "23. สืบสวนค้นหาความจริงอย่างใจจดใจจ่อ (Suspenseful Investigative Urgency)",
        "24. หนักแน่น สุขุม เด็ดเดี่ยว (Stoic, Disciplined & Resolute)",
        "25. โดดเดี่ยวเวิ้งว้างในจักรวาล (Desolate Cosmic Isolation)",
        "26. มึนเมา คลุมเครือ เสมือนอยู่ในภวังค์ (Hypnotic, Dreamlike & Trance)",
        "27. ตื่นตระหนก วิ่งหนีตายสุดชีวิต (Panic-Stricken Desperate Flight)",
        "28. เผด็จการ บีบคั้น ไร้เสรีภาพ (Oppressive, Authoritarian & Suffocating)",
        "29. ซื่อตรง เสียสละ มิตรภาพร่วมรบ (Loyal, Camaraderie & Brotherhood)",
        "30. สูญสิ้นมนุษยธรรม กลืนกินสู่ความมืด (Descent into Absolute Moral Nihilism)"
    ]

    # 30 สไตล์มุมกล้อง (Cinematography & Camera)
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
        "10. มุมมองจากกล้องวงจรปิด/อินฟราเรด (CCTV / Thermal Night Vision Feed)",
        "11. มุมมองนกมองลงมาดิ่งตรง (Bird's Eye Top-Down God Perspective)",
        "12. มุมหนอนมองเสยต่ำน่าเกรงขาม (Extreme Low-Angle Worm's Eye View)",
        "13. ช็อตดัตช์แองเกิลกล้องเอียงสร้างความปั่นป่วน (Dutch Angle Disorienting Tilt)",
        "14. ช็อตหมุนควง 360 องศารอบตัวละคร (360-Degree Circular Orbit Cam)",
        "15. ช็อตซูมดอลลี่เวอร์ทิโก (Dolly Zoom / Vertigo Hitchcock Effect)",
        "16. มุมมองผ่านกล้องเล็งสไนเปอร์ (Sniper Scope Crosshair Overlay)",
        "17. แครนช็อตยกกล้องจากพื้นสู่มุมสูง (Sweeping Crane Overhead Jib Shot)",
        "18. ช็อตเทคยาวลองเทคไร้รอยต่อ (Continuous One-Take Long Shot)",
        "19. เลนส์ตาปลาบิดเบี้ยวระยะประชิด (Distorted Ultra-Wide Fisheye Lens)",
        "20. ช็อตสปลิตไดออปเตอร์โฟกัสหน้าหลังพร้อมกัน (Split-Diopter Dual Focus Shot)",
        "21. มุมมองผ่านกระจกเงาและเงาสะท้อน (Mirror & Glass Reflection Shot)",
        "22. กล้องติดกระบอกปืนสะบัดตามแรงยิง (Weapon-Mounted Barrel Cam Recoil)",
        "23. ช็อตเคลื่อนที่ผ่านช่องแคบหรือซอกกำแพง (Slit Crevice Micro-Probe Cam)",
        "24. มุมมองดาวเทียมสอดแนมทางทหาร (Military Satellite Aerial Recon Feed)",
        "25. ช็อตเปิดเผยตัวละครแบบแส้ตวัด (Cinematic Whip Pan Reveal)",
        "26. มุมมองระดับผิวน้ำ/โคลนประชิด (Water-Level / Mud-Level Surface Cam)",
        "27. มุมมองข้ามหัวไหล่แบบภาพยนตร์ (Over-The-Shoulder Dialogue Framing)",
        "28. กล้องติดหน้ารถแข่งความเร็วสูง (Low-Slung Chassis Bumper Cam)",
        "29. ภาพไฮเปอร์แลปส์กาลเวลาผ่านไป (Hyperlapse Dynamic Passage of Time)",
        "30. มุมมองสะท้อนกระจกหมวกนักบิน (Helmet Visor Interior Cockpit Reflection)"
    ]

    # 30 การจัดแสงและบรรยากาศ (Lighting & Atmosphere)
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
        "10. แสงสะท้อนประกายเชื่อมโลหะอุตสาหกรรม (Industrial Welding Sparks & Flare)",
        "11. แสงส่องผ่านม่านฝุ่นลำแสงโกดิก (God Rays / Crepuscular Sun Beams)",
        "12. แสงคบเพลิงลุกโชนสะท้อนผนังหินถ้ำ (Flickering Torches & Fire Embers)",
        "13. แสงไฟนีออนเสียกะพริบถี่ในทางเดินร้าง (Flickering Fluorescent Hallway Buzz)",
        "14. แสงออโรร่าเรืองรองขั้วโลกเหนือ (Ethereal Emerald Aurora Borealis)",
        "15. แสงฟ้าผ่าฟาดเปรี้ยงสว่างวาบชั่วขณะ (Blinding Lightning Strikes & Storm Silhouette)",
        "16. แสงไฟหน้ากระจกรถยนต์ส่องตัดฝนตกหนัก (High-Beam Car Headlights in Downpour)",
        "17. แสงเปลวไฟระเบิดสีส้มอาบท้องฟ้าราตรี (Fiery Orange Explosion Blast Radiance)",
        "18. แสงเลเซอร์สีเขียวและแดงตัดม่านควัน (Tactical Laser Grids Cutting Smoke)",
        "19. แสงยามเช้าบลูฮาวเออร์หนาวเหน็บ (Freezing Cold Blue Hour Dawn)",
        "20. แสงเรืองสารเคมีชีวภาพพิษเรืองแสง (Toxic Bioluminescent Green Slime Glow)",
        "21. แสงสะท้อนจากเตาปฏิกรณ์พลังงานนิวเคลียร์ (Cherenkov Radiation Electric Cyan Glow)",
        "22. แสงย้อนหลังซิลูเอทมืดทึบไร้รายละเอียด (Hard Backlit Jet-Black Silhouette)",
        "23. แสงเงาตะคุ่มจากตะเกียงน้ำมันเก่า (Moody Vintage Kerosene Lantern Glow)",
        "24. แสงแฟลร์เลนส์อะนามอร์ฟิกสีฟ้าแนวนอน (Anamorphic Blue Horizontal Streak Flares)",
        "25. แสงมืดสลัวใต้แสงดาวระยิบระยับเต็มฟ้า (Bioluminescent Starlight Milky Way Expanse)",
        "26. แสงไฟโซเดียมสีส้มเก่าริมทางหลวง (Dim Orange Sodium Vapor Highway Lamps)",
        "27. แสงประกายไฟช็อตและสายไฟขาด (Sparking Electrical Arcs & Short Circuit)",
        "28. แสงแดดสะท้อนหิมะขาวโพลนสะท้อนตา (Blinding Whiteout Blizzard Glare)",
        "29. แสงสุริยุปราคาคราสมืดมิดขอบทอง (Solar Eclipse Ring of Fire Halo)",
        "30. แสงเงาเทียนไขสั่นไหวในพิธีกรรมโบราณ (Candlelit Occult Chamber Atmosphere)"
    ]

    # 30 คลังพรอพต์ระดับพรีเมียม (Cinematic Prompt Templates)
    prompts = [
        {
            "title": "1. ภาพเปิดเมืองสงครามล่มสลาย (Establishing Ruined Metropolis)",
            "prompt": "Cinematic establishing wide shot of a ruined futuristic metropolis at dusk, thick black smoke rising, burning wreckage, distant searchlights sweeping through toxic smog, hyper-realistic, photorealistic, 8K, directed by Denis Villeneuve."
        },
        {
            "title": "2. หุ่นรบยักษ์เปิดระบบพร้อมรบ (Mecha Titan Boot-up)",
            "prompt": "Low-angle dramatic shot of a 20-meter heavy armored combat mech activating in a dark industrial hangar, internal cyan LED lights booting up, pressurized steam hissing from joint vents, ultra-detailed metallic scratches, 8K resolution, IMAX camera."
        },
        {
            "title": "3. การปะทะยุทธวิธีภาคพื้นดิน (Tactical SpecOps Firefight)",
            "prompt": "Combat cameraman perspective, elite tactical operative squad moving swiftly through concrete ruins under heavy suppression fire, muzzle flashes cutting through dense concrete dust, intense dynamic motion blur, hyper-detailed gear."
        },
        {
            "title": "4. โคลสอัพแววตานักบินในห้องควบคุม (Cockpit Tension & Eye Reflection)",
            "prompt": "Extreme macro close-up of a battle-hardened pilot's eyes inside a dimly lit vibrating cockpit, sweat dripping down forehead, green holographic flight telemetry reflections flickering across the visor, claustrophobic atmosphere, 8K."
        },
        {
            "title": "5. โดรนความเร็วสูงบินไล่ล่า (FPV Drone High-Speed Pursuit)",
            "prompt": "High-speed continuous FPV drone dive tracking a futuristic combat hover-bike racing through narrow neon-lit alleys, dynamic camera rolling, wet asphalt reflecting glaring holographic billboards, high-octane action sequence."
        },
        {
            "title": "6. ห้องบัญชาการวางแผนศึก (War Room Hologram Table)",
            "prompt": "Medium shot of military commanders gathered around a glowing 3D holographic tactical map of a besieged city, cold blue volumetric lighting, sharp shadows, serious facial expressions, cinematic depth of field."
        },
        {
            "title": "7. เผชิญหน้าสืบสวนเงามืด (Neo-Noir Rainy Confrontation)",
            "prompt": "High-contrast neo-noir cinematic scene, two trench-coated figures standing beneath a flickering streetlight in heavy pouring rain, steam rising from sewer manholes, backlit silhouettes by blinding yellow car headlights, puddle reflections."
        },
        {
            "title": "8. ลาดตระเวนมุมมองกล้องกลางคืน (Thermal Night Vision Patrol)",
            "prompt": "First-person thermal infrared night vision view, scanning a silent dark pine forest, green phosphor hue, enemy mechanical targets glowing bright white-hot among dense trees, tactical HUD overlay with digital rangefinder."
        },
        {
            "title": "9. ฉากระเบิดและการอพยพเดือด (Heavy Extraction Under Fire)",
            "prompt": "Wide cinematic shot, military tilt-rotor gunship landing in a hostile warzone to extract wounded soldiers, massive explosion shockwave kicking up dust and debris behind them, golden hour lens flare, high realism."
        },
        {
            "title": "10. ภาพปิดท้าย ยืนมองซากสมรภูมิ (Post-Battle Sunset Vigil)",
            "prompt": "Back-view silhouette of a lone exhausted soldier standing atop a massive hill of rubble, looking out at a burning battlefield against a fiery orange and crimson sunset sky, wind blowing a tattered cape, melancholic and epic mood."
        },
        {
            "title": "11. กองเรือรบอวกาศกระโดดมิติ (Hyperspace Fleet Arrival)",
            "prompt": "A massive fleet of interstellar dreadnoughts dropping out of hyperspace above an alien planet, glowing blue shockwaves rippling across space vacuum, cosmic nebulae background, majestic scale, hyper-detailed hull plating, 8K."
        },
        {
            "title": "12. อสูรไคจูขนาดยักษ์ตื่นขึ้น (Kaiju Awakening from Ocean)",
            "prompt": "Extreme low-angle shot from a pitching naval destroyer, an immense bioluminescent sea titan rising from raging stormy waves, lightning illuminating its armored spine, pouring rain, sirens wailing, colossal cinematic scale."
        },
        {
            "title": "13. แฮกเกอร์เจาะเครือข่ายใต้ดิน (Cyberpunk Hacker Den)",
            "prompt": "Interior tracking shot of a subterranean cyber-den, a hooded hacker surrounded by floating multi-screen green terminal data, tangle of optic cables on the floor, neon magenta backlight, smoke curling from a cigarette, moody atmosphere."
        },
        {
            "title": "14. นักรบซามูไรท่ามกลางพายุหิมะ (Cyber-Samurai Blizzard Duel)",
            "prompt": "Wide cinematic duel shot, a lone cyber-samurai with glowing red katana confronting an armored assassin in a frozen bamboo forest during a heavy blizzard, snowflakes whipping past the lens, intense stillness before strike."
        },
        {
            "title": "15. ดิ่งพสุธาจากชั้นบรรยากาศ (Orbital Halo Drop Insertion)",
            "prompt": "First-person POV falling from upper orbit through red-hot re-entry clouds, helmet HUD showing altitude counting down rapidly, distant burning surface of the planet below, plasma heat shield burning bright orange, sheer adrenaline."
        },
        {
            "title": "16. โรงงานจักรกลร้าง (Abandoned Megastructure Factory)",
            "prompt": "Slow tracking crane shot moving through a colossal abandoned automated tank factory, rust and vines covering giant robotic assembly arms, dusty golden god rays piercing through shattered skylights, eerie post-industrial silence."
        },
        {
            "title": "17. การไล่ล่าบนหลังคารถไฟความเร็วสูง (High-Speed Train Rooftop Duel)",
            "prompt": "Dynamic side tracking shot of two combatants fighting atop a maglev train speeding at 400 km/h through a mountain gorge, clothes whipping violently in the wind, sparks flying from clashing weapons, motion-blurred background."
        },
        {
            "title": "18. ห้องทดลองชีวภาพรั่วไหล (Bioweapon Laboratory Breach)",
            "prompt": "Steadicam shot creeping through a dark sterile science facility, shattered glass containment tube dripping glowing green mutagen onto tiled floor, red rotating alarm lights casting rhythmic shadows, bloodstained hazmat suits."
        },
        {
            "title": "19. ขบวนคาราวานทะเลทรายเวิ้งว้าง (Wasteland War Rig Convoy)",
            "prompt": "High-angle drone shot skimming above a heavily armed post-apocalyptic truck convoy tearing across endless red sand dunes, massive dust clouds trailing behind, exhaust pipes spewing black smoke and fire, Mad Max style cinematic."
        },
        {
            "title": "20. สไนเปอร์บนยอดตึกระฟ้า (High-Rise Sniper Concealment)",
            "prompt": "Over-the-shoulder shot of a camouflaged sniper lying prone on the edge of an 80th-floor rooftop in heavy rain, crosshair focused on a limousine in the neon streets below, raindrops hitting the heavy rifle barrel, cold blue tones."
        },
        {
            "title": "21. ป่าเรืองแสงแห่งดวงดาวลึกลับ (Alien Bioluminescent Jungle)",
            "prompt": "Slow dolly shot through a dense extraterrestrial jungle at night, exotic fungi and towering alien trees pulsing with cyan and violet bioluminescence, gentle glowing spores drifting like stardust, magical sense of wonder, 8K."
        },
        {
            "title": "22. อุโมงค์ใต้ดินหนีตายจากฝูงสัตว์ประหลาด (Subway Swarm Terror)",
            "prompt": "Shaky handheld camera running backward down a dark flooded subway tunnel, flashlight beam wildly illuminating dozens of chittering subterranean creatures crawling along walls and ceiling, frantic survival horror."
        },
        {
            "title": "23. การซ่อมแซมหุ่นยนต์ฉุกเฉิน (Field Repair Under Fire)",
            "prompt": "Medium close-up shot of an engineer desperately welding the cracked chest armor of a damaged bipedal mech, blinding white electrical sparks splashing on the camera lens, companion firing rifle overhead to hold perimeter."
        },
        {
            "title": "24. สุริยุปราคาเหนือมหาพีระมิดโบราณ (Solar Eclipse Over Cyber-Pyramid)",
            "prompt": "Wide static shot of a monolithic black obsidian pyramid glowing with circuit-like golden hieroglyphs, a total solar eclipse forming a fiery diamond ring in the dark violet sky, awe-inspiring sci-fi mythology, 8K."
        },
        {
            "title": "25. ฐานทัพใต้น้ำลึกเผชิญแรงดัน (Deep-Sea Trench Station Breach)",
            "prompt": "View inside an abyssal oceanic observation dome, cracks spreading across the heavy reinforced glass as water jets burst through, outside darkness illuminated by deep-sea creature's enormous yellow eye, rising panic."
        },
        {
            "title": "26. บาร์อันธพาลไซเบอร์พังก์ (Seedy Cyberpunk Cantina)",
            "prompt": "Smooth 360-degree pan inside a crowded, smoky underworld tavern, alien mercenaries, cyborg bounty hunters, flickering holographic dancers, dirty neon signs reflecting in murky glasses of synthetic liquor."
        },
        {
            "title": "27. การลอบสังหารในงานเต้นรำหรูหรา (Black-Tie Gala Silent Takedown)",
            "prompt": "Slick cinematic medium shot in a grand crystal chandelier ballroom, elite agent in tailored tuxedo discreetly disarming a target behind marble pillars, glamorous guests oblivious in background, opulent high society vibe."
        },
        {
            "title": "28. ยุทธการประชิดในรังศัตรู (Breach and Clear CQB)",
            "prompt": "Low-angle tactical camera following point man breaching a reinforced steel door with shotgun, stun grenade flash exploding in blinding white light, soldiers flooding inside with raised carbines, tactical perfection."
        },
        {
            "title": "29. แดนสุสานยานรบอวกาศ (Starship Graveyard Dunes)",
            "prompt": "Cinematic wide panorama of a scavenger walking across white salt flats beside the half-buried wreckage of a kilometer-long crashed dreadnought, rusted turrets pointing at sky, twin moons rising on the horizon, quiet epic."
        },
        {
            "title": "30. ปลุกจิตสำนึกหุ่นยนต์แอนดรอยด์ (Android Awakening Transcendence)",
            "prompt": "Extreme macro portrait of a synthetic android face, synthetic skin peeling back to reveal gleaming chrome hydraulics, a single drop of human-like tear falling from artificial iris, soft cinematic backlighting, philosophical tone."
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
คุณเป็นผู้กำกับภาพยนตร์และนักเขียนบทระดับมืออาชีพ
จงวิเคราะห์ไอเดียเรื่องต่อไปนี้ และแตกออกเป็น 5 ฉากสำคัญสำหรับทำ Storyboard และ Video Prompts:
แนวเรื่อง: {genre}
โทนอารมณ์: {tone}
สไตล์มุมกล้องหลัก: {camera}
การจัดแสงและบรรยากาศ: {lighting}

เรื่องย่อ: {pitch}

กรุณาตอบเป็น JSON รูปแบบ Array โดยแต่ละฉากมีโครงสร้างดังนี้:
[
  {{
    "scene_number": 1,
    "title": "ชื่อฉาก",
    "description": "เรื่องย่อและแอ็กชันในฉากอย่างละเอียด",
    "camera_direction": "คำแนะนำมุมกล้องและการเคลื่อนไหว",
    "lighting_and_atmosphere": "บรรยากาศและแสงสี",
    "audio_cue": "เสียงดนตรีและซาวด์เอฟเฟกต์",
    "image_prompt": "English prompt for image generation (Cinematic, photorealistic, 8k)",
    "video_prompt": "English prompt for video generation (Cinematic camera motion, dynamic action)"
  }}
]
ตอบเฉพาะโค้ด JSON เท่านั้น ไม่มีข้อความเกริ่นนำหรือปิดท้าย
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
    st.caption("ระบบวิเคราะห์โครงเรื่อง แตกฉากภาพยนตร์ และคลังพรอพต์ระดับมืออาชีพสำหรับ AI Video")
    
    if not api_key:
        st.error("⚠️ ไม่พบ GEMINI_API_KEY กรุณาใส่ใน Render Environment หรือกรอกในเมนูด้านข้างเพื่อเปิดใช้งาน AI")
    else:
        st.success("🟢 เชื่อมต่อ AI Engine พร้อมทำงานแล้ว")

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
            height=130
        )
        st.session_state.story_pitch = pitch

    with col2:
        selected_genre = st.selectbox("🎯 แนวภาพยนตร์ (30 สไตล์):", genres)
        selected_tone = st.selectbox("🎭 โทนและอารมณ์ (30 โทน):", tones)

    col3, col4 = st.columns(2)
    with col3:
        selected_camera = st.selectbox("📹 สไตล์มุมกล้องหลัก (30 สไตล์):", cameras)
    with col4:
        selected_lighting = st.selectbox("💡 สไตล์แสงและบรรยากาศ (30 รูปแบบ):", lightings)

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
                
                st.markdown("**พรอพต์ภาษาอังกฤษ (สำหรับเจนภาพ/วิดีโอ):**")
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
            st.text_area(f"บทพูดและไดอะล็อก (ฉากที่ {idx+1})", height=85, key=f"dialogue_{idx}",
                         value="[วิทยุสื่อสาร]: ศูนย์บัญชาการ เราพบการเคลื่อนไหวของวัตถุจักรกลที่พิกัด 9 ขออนุมัติติดตาม...")
        with col_dir2:
            st.text_area(f"โน้ตกำกับการแสดง / บันทึกหน้ากอง (ฉากที่ {idx+1})", height=85, key=f"note_{idx}",
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
# 10. แท็บที่ 4: คลังพรอพต์สำเร็จรูป 30 พรอพต์ (Tab 4)
# ==========================================
def render_tab_prompt_vault(prompts):
    st.subheader("⚡ 4. คลังพรอพต์ระดับพรีเมียม (30 Cinematic Templates)")
    st.caption("ชุดพรอพต์มาตรฐานภาพยนตร์ฮอลลีวูด 30 สไตล์ คัดลอกไปเจนใน Runway, Sora, Kling, Veo, Midjourney ได้ทันที")

    search_keyword = st.text_input("🔍 ค้นหาพรอพต์ตามคีย์เวิร์ด (เช่น Mecha, Spy, Drone, Cyberpunk):")
    filtered_prompts = [p for p in prompts if search_keyword.lower() in p["title"].lower() or search_keyword.lower() in p["prompt"].lower()]

    for item in filtered_prompts:
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
        st.info("ยังไม่มีข้อมูลฉากสำหรับการส่งออก กรุณาวิเคราะห์ฉากในแท็บที่ 1 ก่อน")
        return

    full_script = "# มหาสึกหุ่นรบแดนดีพิมฟ์ (Master Script)\n\n"
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

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💡 1. วิเคราะห์แตกฉาก (AI Story)",
        "🎬 2. ฉาก & บทพูด (ผู้กำกับ)",
        "👤 3. DNA ตัวละคร (Locker)",
        "⚡ 4. คลังพรอพต์ 30 สไตล์ (Prompt Vault)",
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
