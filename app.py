import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import os
import base64

def load_font_base64(font_path):
    with open(font_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return encoded


# Constants
IMAGE_PATH = "bg2.png"
FONT_PATH = "effra-cc-arbc-semibold.otf"

st.set_page_config(page_title="دعوة للعملاء", layout="centered")
st.title("إنشاء دعوة للعملاء بمعرض سيمليس")

font_base64 = load_font_base64("PingAR+LT-Bold.otf")

st.markdown(f"""
<style>

@font-face {{
    font-family: 'PingAR';
    src: url(data:font/otf;base64,{font_base64}) format('opentype');
}}

/* نطبّق الخط على كل شيء */
html, body, [class*="css"], * {{
    font-family: 'PingAR', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}}

/* عنوان الصفحة */
h1 {{
    font-family: 'PingAR', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: bidi-override !important;
    white-space: nowrap !important;
}}

/* الليبلز */
label, .stTextInput label, .stMarkdown, .css-16idsys p {{
    font-family: 'PingAR', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}}

/* صندوق الإدخال */
input[type="text"], textarea {{
    font-family: 'PingAR', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}}

/* زر التنزيل */
.stButton > button {{
    font-family: 'PingAR', sans-serif !important;
    direction: rtl !important;
    text-align: center !important;
}}

/* الحاويات */
div.stTextInput, 
div.stDownloadButton, 
div.stButton, 
.stImage {{
    font-family: 'PingAR', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}}

</style>
""", unsafe_allow_html=True)


name = st.text_input("ادخل اسم العميل", max_chars=30)

if name:
    # Prepare Arabic text
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    # Load base image
    base_image = Image.open(IMAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(base_image)

    # Load fonts
    font_size_name = 260
    font_size_position = 40
    # font_size_name = 150
    # font_size_position = 100
    font = ImageFont.truetype(FONT_PATH, font_size_name)
    position_font = ImageFont.truetype(FONT_PATH, font_size_position)

    # Calculate name position
    image_width, _ = base_image.size
    name_bbox = font.getbbox(bidi_name)
    name_width = name_bbox[2] - name_bbox[0]
    x_name = (image_width - name_width) / 2
    y_name = 1250
    # y_name = 4300

    # Draw name without shadow
    draw.text((x_name, y_name), bidi_name, font=font, fill="#ffffff") # red

    # Convert to bytes
    img_bytes = io.BytesIO()
    base_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Show image and allow download
    st.image(img_bytes, caption="مشاهدة الدعوة", use_container_width=True)

    st.download_button(
        label="تنزيل الدعوة",
        data=img_bytes,
        file_name=f"eid_greeting_{name}.png",
        mime="image/png"
    )
    

invite_text = f"""
السلام عليكم ورحمة الله وبركاته،

يسعدنا دعوتك لزيارة جناحنا في معرض Seamless، وحياك الله بيننا في بوث الرائدة للتمويل.

يمكنك تسجيل حضورك للمعرض من خلال الرابط التالي:
https://secure.terrapinn.com/V5/step2.aspx?Q=4957299QJLN&TMID=5540046&l=sa

متشوقين للقائك!
"""

# مربع الرسالة
st.markdown(f"""
<div style="
    background-color: #f7f7f7;
    padding: 20px;
    border-radius: 10px;
    border-right: 5px solid #254488;
    font-size: 20px;
    line-height: 1.8;
    direction: rtl;
    text-align: right;
    margin-top: 25px;
">
{invite_text}
</div>
""", unsafe_allow_html=True)

# زر النسخ
import streamlit.components.v1 as components

components.html(f"""
<button onclick="navigator.clipboard.writeText(`{invite_text}`)"
style="
    margin-top: 10px;
    padding: 10px 18px;
    background-color: #254488;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
">
نسخ الرسالة
</button>
""", height=60)
