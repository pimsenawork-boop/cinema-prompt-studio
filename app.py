import streamlit as st
import json
import os

# ---------------------------------------------------------
# ตั้งค่าหน้าจอ UI สไตล์ Film Production Studio
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cinematic AI Film Director & Dialogue Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .dialogue-box {
        background: linear-gradient(135deg, #1e2530 0%, #141820 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #f39c12;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .music-box {
        background: linear-gradient(135deg, #1a2238 0%, #121826 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4a90e2;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .secret-box {
        background: linear-gradient(135deg, #2b1a38 0%, #1b1226 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #bd10e0;
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# พรีเซ็ตบทพูดแนะนำตามประเภทบริบทภาพยนตร์ (Dialogue Presets)
# ---------------------------------------------------------
DIALOGUE_PRESETS = {
    "1. เผชิญหน้าวิกฤต / สู้ตาย (Crisis & Confrontation)": [
        ("เราถอยไม่ได้อีกแล้ว... ถ้าข้ามเส้นนี้ไป จะไม่มีทางหันหลังกลับ", "[กัดฟันพูด แววตาเด็ดเดี่ยว น้ำเสียงต่ำหนักแน่น]"),
        ("คิดว่าแค่นี้จะหยุดข้าได้งั้นเหรอ? ดาบเล่มนี้ยังไม่เคยแพ้ใคร!", "[ตะโกนก้อง เสียงคำรามกร้าวท้าทาย]"),
        ("ทุกคนเกาะไว้แน่นๆ! ระบบกำลังจะระเบิดใน 10 วินาที!", "[ตะโกนเร่งรีบแข่งกับเสียงสัญญาณเตือนภัย]")
    ],
    "2. ลึกลับ / ค้นพบความจริง / สืบสวน (Mystery & Discovery)": [
        ("สิ่งนี้ไม่ได้สร้างขึ้นโดยมนุษย์... มันหลับใหลอยู่ที่นี่มานานนับพันปี", "[กระซิบแผ่วเบาด้วยความทึ่งปนหวาดกลัว]"),
        ("รอยแผลแบบนี้... ไม่ใช่ฝีมือของศัตรูภายนอก แต่เป็นคนของเราเอง", "[น้ำเสียงเย็นยะเยือก สุขุม ชวนขนลุก]"),
        ("สัญญาณรหัสถูกส่งมาจากใต้ดินลึก... และมันกำลังเรียกชื่อเรา", "[พูดช้าๆ หยุดเว้นจังหวะหายใจ]")
    ],
    "3. ซึ้ง / ดราม่า / จากลา (Emotional & Heartfelt)": [
        ("สัญญาได้ไหม... ว่าหลังจากเรื่องนี้จบลง นายจะไม่ลืมเรื่องราวของเรา", "[เสียงสั่นเครือ คลี่ยิ้มทั้งน้ำตา อ่อนโยน]"),
        ("ฉันไม่เคยเสียใจเลยที่เลือกทางนี้... มีชีวิตรอดต่อไปเพื่อพวกเรานะ", "[น้ำเสียงแผ่วเบาแต่เปี่ยมด้วยความหวังและสงบ]"),
        ("เวลาของฉันหมดลงตรงนี้แล้ว ถึงตาพวกนายต้องเดินต่อไปข้างหน้า", "[พูดช้าๆ อบอุ่น แววตาพร้อมปล่อยวาง]")
    ],
    "4. ยุทธวิธี / ออกคำสั่ง / ทหาร (Tactical & Military Command)": [
        ("ชุดปฏิบัติการหนึ่ง เข้าประจำแนวกำบัง... รอสัญญาณวิทยุแล้วยิงพร้อมกัน", "[เสียงกระซิบผ่านไมค์วิทยุ นิ่ง เยือกเย็น ชัดเจน]"),
        ("พื้นที่นี้อันตราย ระวังกับดักความร้อนทุกย่างก้าว เคลื่อนพลแบบเงียบ", "[น้ำเสียงเคร่งขรึม ชี้เป้าอย่างแม่นยำ]"),
        ("ภารกิจล้มเหลวไม่ได้ ตราบใดที่สัญญาณยังติด เราต้องเดินหน้าต่อ", "[คำสั่งเฉียบขาด ไร้ความลังเล]")
    ],
    "5. เสียงบรรยายในใจ (Internal Monologue / Voiceover)": [
        ("ผมเคยคิดว่าความมืดน่ากลัวที่สุด จนกระทั่งได้เห็นสิ่งที่ซ่อนอยู่ในแสงสว่าง...", "[เสียงบรรยายทุ้มต่ำ ก้องกังวาน นุ่มลึก]"),
        ("เมืองนี้กลืนกินความฝันของผู้คนไปนับล้าน... และคืนนี้ อาจถึงตาของฉัน", "[น้ำเสียงเหนื่อยล้า แต่แฝงความไม่ยอมแพ้]"),
        ("สงครามไม่ได้ตัดสินว่าใครถูก... มันตัดสินแค่ว่าใครจะได้อยู่ต่อ", "[น้ำเสียงปรัชญา สงบนิ่ง ราวกับผ่านโลกมาเนิ่นนาน]")
    ]
}

# ---------------------------------------------------------
# คลัง 100 พร่อม Google Flow & AI Video
# ---------------------------------------------------------
PROMPT_VAULT = [
    {"id": 1, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Slow Forward Dolly In (ดอลลี่ดันเข้าหาใบหน้าช้าๆ)",
     "prompt": "Cinematic slow forward dolly push-in on subject's face, perfectly stabilized mechanical track movement, shallow depth of field, 50mm prime lens, smooth linear motion, 8k",
     "usage": "ใช้ในฉากที่ตัวละครกำลังครุ่นคิด ค้นพบความจริง หรือกำลังตัดสินใจเรื่องสำคัญ",
     "why": "การเคลื่อนที่แนวตรงความเร็วสม่ำเสมอช่วยให้ AI รันใบหน้าได้นิ่ง ไม่เกิดอาการหน้าละลายหรือเบี้ยว",
     "tip": "อย่าสั่งให้ตัวละครขยับตัวเร็วตอนกล้องดอลลี่เข้า ปล่อยให้พลังสายตานำพาอารมณ์"},
    {"id": 2, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Steadicam Follow Behind (กล้องลอยตามแผ่นหลัง)",
     "prompt": "Smooth Steadicam tracking shot following closely behind subject walking forward, slight natural human walking cadence, subject in focus, atmospheric environment, 35mm lens",
     "usage": "ใช้เปิดตัวพาคนดูเข้าสู่สถานที่ใหม่ สำรวจซากตึกร้าง หรือเดินเข้าสู่สมรภูมิ",
     "why": "การถ่ายจากด้านหลังช่วยลดภาระ AI ในการคำนวณหน้าตา ทำให้ฉากหลังขยับได้ลื่นไหลสมจริง 100%",
     "tip": "เหมาะมากเป็นช็อตเปิดก่อนจะตัดไปช็อตหันหน้ากลับมา"},
    {"id": 3, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Low-Angle Hero Stance (มุมต่ำเงยขึ้นดูทรงพลัง)",
     "prompt": "Dramatic low-angle worm's eye view looking up at subject standing firm, towering presence against the dramatic sky, static locked-off composition, high contrast",
     "usage": "ใช้เน้นความแข็งแกร่ง ผู้นำ ชัยชนะ หรือศัตรูตัวฉกาจที่ดูน่าเกรงขาม",
     "why": "กล้องที่ล็อกมุมนิ่ง (Static) จะทำให้ AI เรนเดอร์รายละเอียดเสื้อผ้าและอาวุธได้คมกริบที่สุด",
     "tip": "ใส่ท้องฟ้ามีเมฆเคลื่อนตัวช้าๆ ด้านหลัง จะเพิ่มมิติของภาพให้ดูอลังการยิ่งขึ้น"},
    {"id": 4, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Cinematic Dutch Angle (มุมกล้องเอียงสร้างความกดดัน)",
     "prompt": "Tense Dutch tilt angle, canted framing at 25-degree roll, uneasy psychological perspective, moody rim lighting, deep shadows, cinematic noir aesthetic",
     "usage": "ฉากระทึกขวัญ จิตตก สูญเสียการควบคุม หรือตัวละครกำลังถูกไล่ต้อน",
     "why": "ความเอียงของระนาบภาพบังคับให้ AI สร้างเส้นนำสายตาเฉียง ช่วยเพิ่มความตึงเครียดทันทีโดยไม่ต้องขยับเยอะ",
     "tip": "ใช้กับฉากทางเดินแคบๆ หรือห้องสอบสวนจะทรงพลังมาก"},
    {"id": 5, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "FPV Drone Dive (โดรนพุ่งดิ่งมุมสูงลงพื้น)",
     "prompt": "High-speed cinematic FPV drone dive down along the vertical side of skyscraper, banking smoothly into street level, dynamic motion blur on edges, crisp center focus, 4k 60fps feel",
     "usage": "ฉากเปิดหนังฟอร์มยักษ์ หรือฉากไล่ล่ากลางมหานครเพื่อโชว์สเกลความใหญ่",
     "why": "สร้างความตื่นตาตื่นใจ สั่งให้ AI รูปร่างตึกไม่บิดด้วยการระบุ 'crisp center focus'",
     "tip": "เหมาะสำหรับฉากเปิดของภาพยนตร์ (Establishing Shot)"},
    {"id": 6, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "360-Degree Orbital Arc (กล้องหมุนวนรอบตัวละคร)",
     "prompt": "Continuous 360-degree orbital camera arc shot around subject standing in place, seamless rotational velocity, consistent background parallax, cinematic depth",
     "usage": "ฉากที่ตัวละครถูกล้อม หรือช่วงเวลาที่เวลาเหมือนหยุดนิ่งกลางสนามรบ",
     "why": "คำว่า 'consistent background parallax' บังคับให้วัตถุใกล้ไกลหมุนด้วยความเร็วที่ถูกต้องตามฟิสิกส์จริง",
     "tip": "ให้ตัวละครยืนหยุดนิ่งที่สุดตอนกล้องหมุน จะได้ผลลัพธ์ที่เนียนตา"},
    {"id": 7, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Rack Focus Depth Transition (สลับโฟกัสหน้า-หลัง)",
     "prompt": "Cinematic rack focus pull, sharp foreground subject transitions smoothly to sharp background subject while foreground softens into creamy bokeh, 85mm f/1.2 lens",
     "usage": "ฉากที่คนข้างหน้าพูดจบ แล้วคนข้างหลังมีปฏิกิริยา หรือเห็นอันตรายค่อยๆ ปรากฏขึ้นข้างหลัง",
     "why": "เป็นการใช้ภาษาหนังแท้ๆ โดยที่มุมกล้องไม่ขยับ ทำให้ AI ไม่สร้างสิ่งแปลกปลอมงอกออกมา",
     "tip": "ช่วยประหยัดคัต ไม่ต้องตัดต่อสลับไปมา"},
    {"id": 8, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Snorricam Chest Rig (กล้องล็อกติดหน้าอกตัวละคร)",
     "prompt": "Authentic Snorricam shot, body-mounted camera locked directly to subject's upper chest, subject face stays perfectly centered while background shakes violently as they run, intense urgency",
     "usage": "ฉากวิ่งหนีตาย วิ่งหนีระเบิด หรือตัวละครเมายา/หวาดกลัวสุดขีด",
     "why": "หน้าตัวละครจะอยู่นิ่งตรงกลางจอเป๊ะๆ 100% ทำให้หน้าไม่เพี้ยนแม้ฉากหลังจะวิ่งเร็วแค่ไหน",
     "tip": "เทคนิคเด็ดระดับฮอลลีวูดที่หนังแอ็กชันชอบใช้"},
    {"id": 9, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Vertigo Dolly Zoom (เอฟเฟกต์ฉากหลังยืดหด)",
     "prompt": "Classic Hitchcock vertigo dolly zoom effect, camera physically dollies backward while simultaneously zooming in optical lens, subject remains exact same size while background distorts and compresses",
     "usage": "ช่วงเวลาที่ตัวละครช็อก ตกใจสุดขีด หรือตระหนักถึงหายนะที่ไม่อาจแก้ไขได้",
     "why": "สร้างความรู้สึกเวียนหัวและตกใจทางจิตวิทยาได้อย่างรุนแรงที่สุดในประวัติศาสตร์ภาพยนตร์",
     "tip": "อย่าใช้บ่อย ให้เก็บไว้ใช้เฉพาะฉากไคลแมกซ์ของตอน"},
    {"id": 10, "cat": "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)", "name": "Top-Down God's Eye View (มุมมองพระเจ้ามองตรงดิ่ง)",
     "prompt": "Orthographic true 90-degree top-down bird's-eye view looking straight down at subject lying on textured ground, geometric framing, slow rotational drift",
     "usage": "ฉากหมดสติ ฉากหลังพ่ายแพ้ หรือตัวละครนอนมองฟ้ากลางซากปรักหักพัง",
     "why": "การจัดวางแบบสมมาตรเรขาคณิตทำให้ AI วาดฉากรอบตัวได้อย่างประณีต",
     "tip": "พื้นหลังที่มีลวดลาย (เช่น น้ำ กระเบื้องแตก วงเวท) จะทำให้ภาพสวยสะกดสายตา"},
    {"id": 11, "cat": "💡 แสง สี และบรรยากาศ (Lighting & Atmosphere)", "name": "Volumetric God Rays (ลำแสงสวรรค์ส่องทะลุหมอก)",
     "prompt": "Stunning volumetric god rays penetrating through stained glass window in dusty cathedral, illuminated airborne dust motes dancing in golden light beam, heavy chiaroscuro",
     "usage": "ฉากค้นพบสิ่งศักดิ์สิทธิ์ สถานที่โบราณ หรือความหวังกลางความมืดมน",
     "why": "ลำแสงหนาเป็นลำ (Volumetric) สร้างมิติความลึก 3D ให้กับฉากแบนๆ ทันที",
     "tip": "เหมาะมากสำหรับฉากภายในวิหาร ถ้ำ หรือป่าทึบ"},
    {"id": 12, "cat": "💡 แสง สี และบรรยากาศ (Lighting & Atmosphere)", "name": "Golden Hour Rim Light (ย้อนแสงสีทองตัดขอบตัวละคร)",
     "prompt": "Warm golden hour natural backlight at dusk, glowing rim light outlining subject's hair and shoulders, golden lens flares kissing camera lens, soft cinematic haze",
     "usage": "ฉากซึ้ง ฉากร่ำลา หรือฉากจบแห่งความหวัง",
     "why": "แสงริมไลท์ช่วยแยกตัวละครออกจากฉากหลัง ป้องกันปัญหาตัวละครกลืนไปกับฉาก",
     "tip": "แสงธรรมชาติที่ทำให้ผิวคนดูสวยและมีเสน่ห์ที่สุด"},
    {"id": 13, "cat": "💡 แสง สี และบรรยากาศ (Lighting & Atmosphere)", "name": "Cyberpunk Neon Wet Reflections (นีออนสะท้อนแอ่งน้ำ)",
     "prompt": "High-contrast cyberpunk street, vibrant magenta and cyan neon signs reflecting vividly in wet asphalt puddles, light rain ripples, atmospheric steam rising from sewers",
     "usage": "ฉากเมืองไซไฟ อนาคต ตลาดมืด หรือย่านคนกลางคืน",
     "why": "การสะท้อนของแอ่งน้ำช่วยเพิ่มมิติแสงสองเท่า และสร้างบรรยากาศแบบ Blade Runner",
     "tip": "ใส่คำว่า 'steam rising' เพื่อเพิ่มการเคลื่อนไหวที่ดูนุ่มนวล"},
    {"id": 14, "cat": "💥 แอ็กชัน ฟิสิกส์ และ VFX (Action & Physics)", "name": "Ground Shockwave Impact (คลื่นกระแทกพื้นระเบิด)",
     "prompt": "Massive kinetic ground impact, circular shockwave rippling through dirt, pulverizing pavement into floating stone fragments, dust ring blasting outward, realistic physical weight",
     "usage": "ฉากซูเปอร์ฮีโร่ลงพื้น หุ่นรบตกกระแทก หรือเวทมนตร์กระแทกผิวดิน",
     "why": "คำว่า 'realistic physical weight' ช่วยสั่งให้ AI คำนวณเศษหินตกตามแรงโน้มถ่วง ไม่ลอยเคว้งมั่ว",
     "tip": "ใส่กล้องสั่นไหวเล็กน้อยตอนสัมผัสพื้น"},
    {"id": 15, "cat": "💥 แอ็กชัน ฟิสิกส์ และ VFX (Action & Physics)", "name": "Dynamic Cloth Wind Simulation (เสื้อผ้าสะบัดตามแรงลม)",
     "prompt": "Realistic dynamic cloth physics simulation, heavy wool trench coat billowing majestically in gale-force mountain wind, natural fabric inertia, authentic aerodynamic drag",
     "usage": "ฉากยืนท้าลมบนยอดเขา หรือเดินก้าวผ่านพายุ",
     "why": "เสื้อผ้าที่สะบัดอย่างสมจริงช่วยส่งเสริมความยิ่งใหญ่ของตัวละคร",
     "tip": "ระบุประเภทเนื้อผ้าเพื่อให้แรงสะบัดสมจริง"},
    {"id": 16, "cat": "👤 การแสดง ล็อกหน้า และอารมณ์ (Acting & Face Lock)", "name": "Single Tear Down Cheek (หยดน้ำตาไหลอาบแก้มช้าๆ)",
     "prompt": "Intimate macro emotional portrait, single clear teardrop welling up in bloodshot eye and tracing slowly down pale cheek, trembling jaw, authentic grief expression, steady camera",
     "usage": "ฉากสูญเสียคนรัก ฉากระลึกความหลัง หรือยอมรับชะตากรรม",
     "why": "การล็อกมุมกล้องนิ่งช่วยให้ AI วาดหยดน้ำตาไหลเป็นทางโดยที่ตาและจมูกไม่เบี้ยว",
     "tip": "อย่าสั่งให้ตัวละครร้องไห้ฟูมฟาย ให้ใช้น้ำตาหยดเดียวเพื่อความลึกซึ้ง"},
    {"id": 17, "cat": "👤 การแสดง ล็อกหน้า และอารมณ์ (Acting & Face Lock)", "name": "Battle-Scarred Grime Texture (ผิวกร้านศึกแผลเป็นชัดเจน)",
     "prompt": "Hyper-realistic skin texture, authentic epidermal pores, faint healed scar cutting across left eyebrow, soot and dried mud smudge on cheek, highly detailed non-plastic facial anatomy",
     "usage": "ใช้เป็น Master Prompt สำหรับคุมหน้าพระเอกสายบู๊ ทหาร หรือผู้รอดชีวิต",
     "why": "คำว่า 'faint healed scar across left eyebrow' เป็น Anchor ชั้นยอดที่ช่วยให้ AI วาดหน้าเดิมทุกฉาก",
     "tip": "ใส่ประโยคนี้ในทุกช็อตที่มีตัวละครตัวนี้"},
    {"id": 18, "cat": "🌌 โลกไซไฟ แฟนตาซี และอนิเมะ (Worlds & Anime)", "name": "Makoto Shinkai Cloud Sea (ทะเลเมฆสะท้อนแสงสีรุ้ง)",
     "prompt": "Breathtaking Makoto Shinkai anime aesthetic, towering cumulonimbus cloud sea glowing with iridescent pastel pink and turquoise sunset, dynamic light refraction, hyper-detailed sky",
     "usage": "ฉากเปิดโลกอนิเมะ ฉากบินบนฟ้า หรือฉากความรักสุดประทับใจ",
     "why": "สไตล์ชินไคคือมาตรฐานสูงสุดของท้องฟ้าอนิเมะ สีสันจะสดใสสะกดคนดูทันที",
     "tip": "ใส่แสงสะท้อนของเมฆลงบนผิวน้ำหรือกระจกหน้าต่าง"},
    {"id": 19, "cat": "🌌 โลกไซไฟ แฟนตาซี และอนิเมะ (Worlds & Anime)", "name": "Ghibli Wind in Green Grass (ทุ่งหญ้าพลิ้วไหวสไตล์จิบลิ)",
     "prompt": "Studio Ghibli aesthetic, vast emerald green grassy rolling hills undulating gently in the summer breeze, fluffy painted white clouds, warm nostalgic watercolor background, peaceful joy",
     "usage": "ฉากพักผ่อน ทุ่งหญ้าแห่งความหลัง หรือการเริ่มต้นออกเดินทางในวัยเด็ก",
     "why": "ความนุ่มนวลของลายเส้นแบบจิบลิช่วยปลอบประโลมใจและให้ความรู้สึกอบอุ่น",
     "tip": "ให้ตัวละครวิ่งกางแขนรับลมบนเนินเขา"},
    {"id": 20, "cat": "🌌 โลกไซไฟ แฟนตาซี และอนิเมะ (Worlds & Anime)", "name": "Interstellar Gargantua Black Hole (หลุมดำมีวงแหวนก๊าซเรืองแสง)",
     "prompt": "Astonishing scientifically accurate supermassive black hole Gargantua, brilliant golden accretion disk of superheated plasma bending spacetime gravitationally, cosmic scale silence",
     "usage": "ฉากจุดสิ้นสุดของจักรวาล ไคลแมกซ์ภาพยนตร์ไซไฟอวกาศระดับตำนาน",
     "why": "ความโค้งงอของกาลอวกาศและแสงรอบหลุมดำสร้างความน่าเกรงขามสูงสุดในทางดาราศาสตร์",
     "tip": "ตัดเสียงทั้งหมดให้เงียบกริบเพื่อสื่อถึงความเวิ้งว้างของอวกาศ"}
]

# ---------------------------------------------------------
# ระบบบันทึกโปรเจกต์
# ---------------------------------------------------------
DB_FILE = "projects_db.json"

def load_projects():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "มหาศึกหุ่นรบแดนร้าง (Sci-Fi Apocalypse)": {
            "genre": "ไซไฟ / เอาชีวิตรอด (Sci-Fi Thriller)",
            "logline": "โลกหลังล่มสลาย ทหารลาดตระเวนคนสุดท้ายต้องปกป้องแหล่งพลังงานบริสุทธิ์จากฝูงโดรนสังหารเพื่อกอบกู้เมืองใต้ดิน",
            "engine": "Google Flow / Google Veo (Cinematic)",
            "style": "Cinematic 35mm Film (Kodak Portra, Arri Alexa, High Dynamic Range)",
            "lighting": "Golden hour dusty rays, teal shadow tones, volumetric smoke",
            "aspect_ratio": "16:9 (Landscape Cinema)",
            "char_name": "SGT_KAI",
            "char_look": "28-year-old Asian male, tactical fade hair, sharp jawline, intense focused eyes, small scar on left eyebrow",
            "char_persona": "เคร่งขรึม ระแวดระวัง การเคลื่อนไหวกระชับ เงียบกริบแบบทหารอาชีพ",
            "char_voice": "เสียงทุ้มต่ำ แหบห้าว สุขุม พูดคำสั้นชัดถ้อยชัดคำ จังหวะการพูดช้าหนักแน่น",
            "char_outfit": "Weathered matte-black tactical combat vest over dark olive utility uniform, throat mic, silver pendant",
            "scenes": [
                {
                    "title": "เปิดฉาก: สัญญาณเตือนภัยกลางซากเมือง",
                    "action": "ค่อยๆ ก้าวเดินช้าๆ ลัดเลาะซากตึกร้าง มือประคองอาวุธระแวดระวัง",
                    "env": "ซากตึกสูงระฟ้าที่ถูกเถาวัลย์ปกคลุม ซากเหล็กขึ้นสนิม และละอองฝุ่นลอยในอากาศ",
                    "dialogue": "ฐานบัญชาการ... ผมมาถึงจุดนัดพบแล้ว แต่สัญญาณถูกตัดขาดทั้งหมด",
                    "voice_direction": "[กระซิบผ่านไมค์วิทยุสื่อสาร หายใจเบาๆ น้ำเสียงเคร่งขรึมกดดัน]"
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
# Sidebar: จัดการโปรเจกต์
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/clapperboard.png", width=60)
    st.title("🎬 Project Hub")
    
    project_list = list(st.session_state.projects.keys())
    selected_project_name = st.selectbox("📂 เลือกโปรเจกต์:", project_list)
    
    st.divider()
    with st.expander("➕ สร้างโปรเจกต์ใหม่"):
        new_title = st.text_input("ชื่อเรื่อง (Title)")
        new_genre = st.selectbox("แนวภาพยนตร์", [
            "ไซไฟ / เอาชีวิตรอด (Sci-Fi Thriller)",
            "อนิเมะญี่ปุ่น แฟนตาซี (Fantasy Anime)",
            "สืบสวนระทึกขวัญ นัวร์ (Crime Noir)",
            "นิทาน 3D อบอุ่นหัวใจ (Pixar Style)",
            "แอ็กชันสงครามสมจริง (Military Tactical Action)",
            "ดาร์กแฟนตาซี เวทมนตร์ (Dark Fantasy Epic)"
        ])
        new_logline = st.text_area("เรื่องย่อแกนหลัก", placeholder="เกิดอะไรขึ้นกับใคร...")
        if st.button("✨ ยืนยันสร้างโปรเจกต์", use_container_width=True):
            if new_title.strip() != "":
                st.session_state.projects[new_title] = {
                    "genre": new_genre,
                    "logline": new_logline,
                    "engine": "Google Flow / Google Veo (Cinematic)",
                    "style": "Cinematic 35mm Film (Kodak Portra, Arri Alexa)",
                    "lighting": "Volumetric sunlight, natural cinematic contrast",
                    "aspect_ratio": "16:9 (Landscape Cinema)",
                    "char_name": "HERO_LEAD",
                    "char_look": "25-year-old Asian male, athletic build, messy hair",
                    "char_persona": "มุ่งมั่น สุขุม เด็ดเดี่ยว",
                    "char_voice": "เสียงทุ้มลึก อบอุ่น หนักแน่น ชัดถ้อยชัดคำ",
                    "char_outfit": "Dark utility jacket over black shirt",
                    "scenes": [{
                        "title": "ฉากที่ 1: การเปิดฉาก",
                        "action": "ยืนมองเส้นขอบฟ้า ก้าวเดินไปข้างหน้าอย่างช้าๆ",
                        "env": "ทุ่งกว้าง มีสายหมอกบางเบาในยามเช้า",
                        "dialogue": "การเดินทางเพิ่งเริ่มต้นขึ้นเท่านั้น...",
                        "voice_direction": "[พูดช้าๆ แววตามุ่งมั่น น้ำเสียงเปี่ยมความหวัง]"
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
# Workspace หลัก
# ---------------------------------------------------------
st.title(f"📽️ {selected_project_name}")
st.caption(f"**แนวเรื่อง:** {current_proj.get('genre', '')} | **เรื่องย่อ:** {current_proj.get('logline', '')}")

tab_bible, tab_char, tab_scenes, tab_music, tab_secrets, tab_vault, tab_export = st.tabs([
    "🌍 1. บริบทภาพ & แสง",
    "👤 2. ฟิกหน้า & เสียงตัวละคร",
    "🎬 3. ผู้กำกับฉาก & บทพูด",
    "🎵 4. ดนตรี & คุมจังหวะอารมณ์",
    "💎 5. พร่อมพิเศษระดับเทพ",
    "📚 6. คลังพร่อม Google Flow",
    "📋 7. เล่มบท & Export รวม"
])

# =========================================================
# TAB 1: บริบทโลก
# =========================================================
with tab_bible:
    st.subheader("🎨 กำหนด Mood & Tone ให้ทั้งเรื่องกลมกลืน")
    c1, c2 = st.columns(2)
    with c1:
        current_proj["engine"] = st.selectbox("AI แพลตฟอร์มที่ใช้สร้าง:", [
            "Google Flow / Google Veo (Cinematic Video)",
            "Runway Gen-3 Alpha (Photorealistic)",
            "Kling 1.5/2.0 (High Precision Motion)",
            "Midjourney v6.1 + Luma Dream Machine",
            "OpenAI Sora Standard"
        ])
        current_proj["style"] = st.selectbox("สไตล์ภาพหลัก:", [
            "Cinematic 35mm Film (Kodak Portra, Arri Alexa, High Dynamic Range)",
            "Anime / Makoto Shinkai (Vibrant sky, detailed light refraction, 2D aesthetic)",
            "Pixar 3D Animation (Soft subsurface scattering, expressive eyes)",
            "Dark Fantasy / Unreal Engine 5 (Atmospheric fog, sharp rim light, dramatic contrast)"
        ])
    with c2:
        current_proj["aspect_ratio"] = st.selectbox("สัดส่วนภาพ:", [
            "16:9 (Landscape Cinema / YouTube)",
            "9:16 (Portrait / Reels / TikTok)",
            "2.39:1 (Anamorphic Ultrawide Cinema)"
        ])
        current_proj["lighting"] = st.text_input("แสงหลักที่คุมโทนทุกฉาก:", current_proj.get("lighting", "Volumetric golden light"))
        
    if st.button("💾 บันทึกการตั้งค่าบริบท"):
        save_projects(st.session_state.projects)
        st.toast("บันทึกเรียบร้อย!", icon="✅")

# =========================================================
# TAB 2: ล็อกตัวละคร และ โปรไฟล์เสียง (Voice Profile)
# =========================================================
with tab_char:
    st.subheader("👤 Character DNA & Voice Profile (ล็อกหน้าและน้ำเสียง)")
    st.caption("กำหนดจุดจำทั้งทางกายภาพและลักษณะเสียง เพื่อใช้สร้างตัวละครที่สมบูรณ์แบบทั้งภาพและเสียง")
    
    ca, cb = st.columns(2)
    with ca:
        current_proj["char_name"] = st.text_input("รหัสตัวละคร (Token Name)", current_proj.get("char_name", "HERO_LEAD"))
        current_proj["char_look"] = st.text_area("โครงหน้า / จุดเด่น / ทรงผม (ห้ามเปลี่ยน)", current_proj.get("char_look", ""), height=80)
        current_proj["char_persona"] = st.text_input("บุคลิกภาพ / นิสัยเฉพาะตัว", current_proj.get("char_persona", ""))
    with cb:
        current_proj["char_voice"] = st.text_area("🎙️ โปรไฟล์น้ำเสียงและลักษณะการพูด (Character Voice Profile)", 
            current_proj.get("char_voice", "เสียงทุ้มต่ำสุขุม หนักแน่น พูดจังหวะช้าชัดเจน สไตล์ทหารผ่านศึก"), height=80)
        current_proj["char_outfit"] = st.text_area("ชุดประจำตัวหลัก (Fixed Outfit)", current_proj.get("char_outfit", ""), height=80)
        
    if st.button("💾 บันทึกข้อมูลตัวละครและเสียง"):
        save_projects(st.session_state.projects)
        st.toast("บันทึกข้อมูลตัวละครสำเร็จ!", icon="✅")

char_dna = f"[{current_proj['char_name']}: {current_proj.get('char_look','')}, persona: {current_proj.get('char_persona','')}, voice: {current_proj.get('char_voice','')}, wearing {current_proj.get('char_outfit','')}]"

# =========================================================
# TAB 3: สร้างฉาก & ทางเลือก & ระบบบทพูดอัจฉริยะ (Smart Dialogue)
# =========================================================
with tab_scenes:
    st.subheader("🎬 จัดการฉาก ทางเลือกภาพ และบทพูด (Scene & Dialogue Director)")
    
    if st.button("➕ เพิ่มฉากถัดไป"):
        new_idx = len(current_proj["scenes"]) + 1
        current_proj["scenes"].append({
            "title": f"ฉากที่ {new_idx}: เหตุการณ์ต่อเนื่อง",
            "action": "ก้าวเดินไปข้างหน้าอย่างระแวดระวัง หยุดมองบางสิ่ง",
            "env": "พื้นที่กว้าง ลมพัดแรง มีหมอกจางๆ",
            "dialogue": "",
            "voice_direction": "[พูดด้วยน้ำเสียงสุขุม]"
        })
        save_projects(st.session_state.projects)
        st.rerun()

    ar_clean = current_proj["aspect_ratio"].split(" ")[0]
    negative_rules = "bad anatomy, distorted face, inconsistent wardrobe, morphing limbs, blurry, jittery, text, watermark"

    for i, sc in enumerate(current_proj["scenes"]):
        st.markdown(f"---")
        st.markdown(f"### 📍 ฉากที่ {i+1}: {sc.get('title', f'ฉากที่ {i+1}')}")
        
        c_sc1, c_sc2 = st.columns(2)
        with c_sc1:
            sc["action"] = st.text_input(f"ตัวละครกำลังทำอะไร (Action) #{i+1}", sc.get("action", ""), key=f"act_{i}")
        with c_sc2:
            sc["env"] = st.text_input(f"สถานที่และบรรยากาศ (Setting) #{i+1}", sc.get("env", ""), key=f"env_{i}")

        # --- ส่วนจัดการบทพูด (Dialogue Studio) ---
        with st.container():
            st.markdown("""<div class="dialogue-box"><b>🎙️ ระบบบทพูดและกำกับอารมณ์เสียง (Smart Dialogue Box)</b></div>""", unsafe_allow_html=True)
            
            d_col1, d_col2 = st.columns([1, 2])
            with d_col1:
                # พรีเซ็ตบทพูดแนะนำ
                preset_cat = st.selectbox(f"💡 เลือกประเภทบทพูดแนะนำ #{i+1}:", list(DIALOGUE_PRESETS.keys()), key=f"dcat_{i}")
                preset_choices = [item[0] for item in DIALOGUE_PRESETS[preset_cat]]
                selected_preset_line = st.selectbox(f"เลือกบทพูดต้นแบบ #{i+1}:", ["-- เลือกเพื่อใช้เป็นบทพูด --"] + preset_choices, key=f"dline_{i}")
                
                if selected_preset_line != "-- เลือกเพื่อใช้เป็นบทพูด --":
                    for line, direction in DIALOGUE_PRESETS[preset_cat]:
                        if line == selected_preset_line:
                            sc["dialogue"] = line
                            sc["voice_direction"] = direction
                            break

            with d_col2:
                sc["dialogue"] = st.text_area(f"✍️ บทพูดในฉากนี้ (แก้ไขหรือพิมพ์เองได้อิสระ):", sc.get("dialogue", ""), key=f"dia_text_{i}", height=70)
                sc["voice_direction"] = st.text_input(f"🎭 คำสั่งกำกับอารมณ์และจังหวะเสียง (Voice Acting Cue):", sc.get("voice_direction", "[น้ำเสียงเด็ดเดี่ยว]"), key=f"dia_dir_{i}")

            if sc["dialogue"].strip() != "":
                voice_prompt = f"ElevenLabs Voice Prompt: Voice Profile: {current_proj.get('char_voice','')}. Performance: {sc['voice_direction']}. Line: \"{sc['dialogue']}\""
                st.caption(f"🎧 **Prompt สำหรับ AI เจนเสียงพากย์ (ElevenLabs/Voice AI):**")
                st.code(voice_prompt, language="text")

        # --- ทางเลือกอารมณ์ของฉาก (A / B / C) ---
        st.markdown("**🎯 เลือกทิศทางอารมณ์และพร่อมภาพสำหรับฉากนี้:**")
        tab_a, tab_b, tab_c = st.tabs([
            "✨ ทางเลือก A: โทนซึ้ง / ดราม่า / ดึงดูดอารมณ์",
            "🔍 ทางเลือก B: โทนลึกลับ / ระแวดระวัง / ระทึกขวัญ",
            "🔥 ทางเลือก C: โทนแอ็กชัน / กดดัน / เผชิญหน้าวิกฤต"
        ])
        
        with tab_a:
            st.success("**🎬 วิดีโอจะออกมาแบบไหน:** กล้องสโลว์ดอลลี่เข้าหาใบหน้า แสงอบอุ่นนุ่ม แววตาสื่ออารมณ์ชัดเจน ไม่เบี้ยว")
            prompt_a = f"Masterpiece cinematic film still, slow push-in dolly shot, {char_dna}, {sc['action']}, deeply emotional expression, setting: {sc['env']}, {current_proj.get('lighting','')}, {current_proj.get('style','')}, 50mm f/1.4, 8k --ar {ar_clean} --no {negative_rules}"
            st.code(prompt_a, language="markdown")
            
        with tab_b:
            st.warning("**🎬 วิดีโอจะออกมาแบบไหน:** กล้องมุมมองบุคคลที่สามตามหลัง บรรยากาศเงามืดและหมอกควัน ตัวละครระแวดระวัง")
            prompt_b = f"Cinematic mystery thriller, steadycam tracking shot, {char_dna}, {sc['action']} with watchful tension, setting: {sc['env']}, deep shadows, volumetric mist, {current_proj.get('lighting','')}, {current_proj.get('style','')}, 35mm anamorphic, 8k --ar {ar_clean} --no {negative_rules}"
            st.code(prompt_b, language="markdown")
            
        with tab_c:
            st.error("**🎬 วิดีโอจะออกมาแบบไหน:** กล้องมุมต่ำแหงนขึ้น การเคลื่อนไหวเร็วและทรงพลัง มีสะเก็ดฝุ่นปลิว แสงตัดขอบตัวละคร")
            prompt_c = f"Intense blockbuster action still, low-angle dynamic tracking, {char_dna}, {sc['action']} with fierce determination, setting: {sc['env']}, flying particles, rim lighting, dramatic lens flare, {current_proj.get('style','')}, 8k, IMAX quality --ar {ar_clean} --no {negative_rules}"
            st.code(prompt_c, language="markdown")

    if st.button("💾 บันทึกบทพูดและฉากทั้งหมด"):
        save_projects(st.session_state.projects)
        st.toast("บันทึกบทภาพยนตร์เรียบร้อย!", icon="✅")

# =========================================================
# TAB 4: ระบบแนะนำดนตรี
# =========================================================
with tab_music:
    st.subheader("🎵 ระบบกำกับดนตรีประกอบ & ซาวด์ดีไซน์คุมอารมณ์")
    music_mood = st.selectbox("เลือกอารมณ์หลักของช่วงนี้:", [
        "1. ดึงอารมณ์ ดราม่า เวิ้งว้าง (Emotional / Solitude / Longing)",
        "2. ลึกลับ ระแวง ระทึกขวัญ (Tense Mystery / Heartbeat Suspense)",
        "3. จุดระเบิดความมันส์ แอ็กชันสเกลใหญ่ (Epic Battle / Adrenaline Drop)",
        "4. ความหวัง ชัยชนะ ปลอบประโลมใจ (Triumphant / Uplifting Resolution)"
    ])
    
    if "1. ดึงอารมณ์" in music_mood:
        st.markdown("""<div class="music-box"><b>🎻 การจัดวาง:</b> ใช้ฉากเปิดหรือสูญเสีย จังหวะ 55-65 BPM เครื่องดนตรี Solo Cello & Reverb Piano</div>""", unsafe_allow_html=True)
        st.code("cinematic film score, sorrowful solo cello, slow melancholy reverberant piano, atmospheric wind ambient, emotional crescendo, Hans Zimmer style, 60 bpm, no vocals", language="text")
    elif "2. ลึกลับ" in music_mood:
        st.markdown("""<div class="music-box"><b>🥁 การจัดวาง:</b> ตัวละครกำลังสำรวจ จังหวะ 80-95 BPM เสียง Sub-bass drone & Ticking clock</div>""", unsafe_allow_html=True)
        st.code("cinematic thriller suspense, dark pulsing sub-bass, anxious ticking clock rhythm, screeching dissonant violins, eerie atmosphere, heart thumping bassline, Sicario style, 85 bpm, instrumental", language="text")
    elif "3. จุดระเบิดความมันส์" in music_mood:
        st.markdown("""<div class="music-box"><b>💥 การจัดวาง:</b> ฉากสู้รบ หนีตาย จังหวะ 130-150 BPM กลองไทโกะยักษ์ & French Horns คำราม</div>""", unsafe_allow_html=True)
        st.code("epic blockbuster action score, massive cinematic percussion, roaring brass horn braam, aggressive hybrid synth, relentless war drums, adrenaline rush, Mad Max style, 140 bpm, instrumental", language="text")
    elif "4. ความหวัง" in music_mood:
        st.markdown("""<div class="music-box"><b>🌅 การจัดวาง:</b> ฉากจบ รอดชีวิต อาทิตย์ขึ้น จังหวะ 90-110 BPM เครื่องสายเต็มวง & คอรัสสวรรค์</div>""", unsafe_allow_html=True)
        st.code("triumphant cinematic anthem, uplifting orchestral strings, soaring angelic choir harmonies, inspirational French horn melody, sunrise emotional resolution, Interstellar style, 100 bpm, instrumental", language="text")

# =========================================================
# TAB 5: คลังพร่อมพิเศษระดับเทพ
# =========================================================
with tab_secrets:
    st.subheader("💎 คลังพร่อมพิเศษระดับฮอลลีวูด (Secret Master Prompts)")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown("""<div class="secret-box"><b>🎯 1. พร่อมล็อกหน้า & ผิวหนัง ไม่ให้เป็นพลาสติก</b></div>""", unsafe_allow_html=True)
        st.code("natural human skin pores, micro-textures, subsurface skin scattering, slight skin imperfections, anatomically correct, non-plastic skin texture, shot on 35mm master prime, 8k raw photo", language="text")
        st.markdown("""<div class="secret-box"><b>💡 2. พร่อมแสงระดับปรมาจารย์ (Roger Deakins Rig)</b></div>""", unsafe_allow_html=True)
        st.code("masterful cinematic volumetric lighting, soft rim light defining silhouette, atmospheric dust motes floating in light beam, moody chiaroscuro contrast, golden-cyan color separation, haze diffusion", language="text")
    with s_col2:
        st.markdown("""<div class="secret-box"><b>🌪️ 3. พร่อมคุมฟิสิกส์การขยับ ไม่ให้อวัยวะงอก</b></div>""", unsafe_allow_html=True)
        st.code("consistent anatomical physics, grounded footstep weight, cloth simulation flowing with natural wind, realistic hair inertia, smooth temporal coherence, no morphing, no limb blending", language="text")
        st.markdown("""<div class="secret-box"><b>🎥 4. พร่อมมุมกล้องภาพยนตร์ IMAX 70mm</b></div>""", unsafe_allow_html=True)
        st.code("shot on IMAX 70mm camera, Panavision anamorphic lens, genuine horizontal lens flares, shallow depth of field with creamy bokeh, controlled mechanical crane movement, cinematic framing", language="text")

# =========================================================
# TAB 6: คลังพร่อม Google Flow
# =========================================================
with tab_vault:
    st.subheader("📚 คลัง 100 พร่อมอเนกประสงค์ (Google Flow & AI Video Vault)")
    filter_col1, filter_col2 = st.columns([2, 3])
    with filter_col1:
        categories = [
            "ทั้งหมด (All 100 Prompts)",
            "🎥 กล้องและการเคลื่อนไหว (Camera & Rig)",
            "💡 แสง สี และบรรยากาศ (Lighting & Atmosphere)",
            "💥 แอ็กชัน ฟิสิกส์ และ VFX (Action & Physics)",
            "👤 การแสดง ล็อกหน้า และอารมณ์ (Acting & Face Lock)",
            "🌌 โลกไซไฟ แฟนตาซี และอนิเมะ (Worlds & Anime)"
        ]
        selected_category = st.selectbox("📂 เลือกหมวดหมู่:", categories)
    with filter_col2:
        search_query = st.text_input("🔍 ค้นหาพร่อมตามคีย์เวิร์ด:", "")

    filtered_prompts = PROMPT_VAULT
    if selected_category != "ทั้งหมด (All 100 Prompts)":
        filtered_prompts = [p for p in filtered_prompts if p["cat"] == selected_category]
    if search_query.strip() != "":
        q = search_query.lower()
        filtered_prompts = [p for p in filtered_prompts if q in p["name"].lower() or q in p["prompt"].lower() or q in p["usage"].lower()]

    st.markdown(f"**แสดงผลลัพธ์:** `{len(filtered_prompts)}` พร่อม")
    for item in filtered_prompts:
        with st.expander(f"#{item['id']} {item['name']} | {item['cat']}", expanded=False):
            st.code(item["prompt"], language="text")
            c_info1, c_info2 = st.columns(2)
            with c_info1:
                st.markdown(f"**📌 ส่วนมากใช้ตอนไหน:**\n{item['usage']}")
                st.markdown(f"**💡 แนะนำวิธีใช้:**\n{item['tip']}")
            with c_info2:
                st.markdown(f"**✨ ดียังไงใน Google Flow:**\n{item['why']}")

# =========================================================
# TAB 7: เล่มบทภาพยนตร์มาตรฐาน (Hollywood Script Export)
# =========================================================
with tab_export:
    st.subheader("📋 Hollywood Master Production Script (เล่มบทภาพยนตร์สมบูรณ์แบบ)")
    st.caption("จัดเรียงในรูปแบบบทภาพยนตร์มาตรฐานสากล พร้อมบทพูด คิวการแสดง และพร่อมภาพ")
    
    script_output = f"=========================================================================\n"
    script_output += f"                   SCREENPLAY: {selected_project_name.upper()}\n"
    script_output += f"=========================================================================\n"
    script_output += f"GENRE: {current_proj.get('genre','')}\n"
    script_output += f"LOGLINE: {current_proj.get('logline','')}\n"
    script_output += f"LEAD CHARACTER: {current_proj.get('char_name','')} \n"
    script_output += f"VOICE PROFILE: {current_proj.get('char_voice','')}\n"
    script_output += f"CHARACTER DNA: {char_dna}\n"
    script_output += f"=========================================================================\n\n"
    
    for idx, sc in enumerate(current_proj["scenes"]):
        script_output += f"SCENE {idx+1}: {sc.get('title','').upper()}\n"
        script_output += f"SETTING: {sc.get('env','')}\n"
        script_output += f"VISUAL ACTION: {sc.get('action','')}\n\n"
        
        if sc.get("dialogue", "").strip() != "":
            char_tag = current_proj.get('char_name', 'CHARACTER')
            script_output += f"                  {char_tag.upper()}\n"
            script_output += f"        {sc.get('voice_direction', '')}\n"
            script_output += f"   \"{sc.get('dialogue', '')}\"\n\n"
            
        script_output += f"AI PROMPT (KEYFRAME): {char_dna}, {sc.get('action','')}, {sc.get('env','')}, {current_proj.get('lighting','')}, {current_proj.get('style','')} --ar {ar_clean}\n"
        script_output += f"-------------------------------------------------------------------------\n\n"
        
    st.text_area("เล่มบทภาพยนตร์พร้อมบทพูดและการกำกับ (Master Script):", script_output, height=350)
    st.download_button("📥 ดาวน์โหลดเล่มบทหนัง (.txt)", data=script_output, file_name=f"{selected_project_name}_script.txt")
