import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
import time
import os
from io import BytesIO
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont

# --- Optional Libraries (Try/Except to prevent crashes) ----
try:
    import plotly.express as px
except ImportError:
    px = None
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    from rembg import remove
except ImportError:
    remove = None
try:
    import yt_dlp
except ImportError:
    yt_dlp = None

# --- 1. Page Config ---
st.set_page_config(page_title="Universal Studio Pro", layout="wide", page_icon="❤️")

# --- 2. THEME & CSS ENGINE (Life Tracker Style) ---
st.markdown("""
    <style>
        /* Import Poppins Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            color: #333333;
            background-color: #f0f2f6;
        }
        
        /* Hide Default Streamlit Elements */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* --- SIDEBAR STYLING --- */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }
        section[data-testid="stSidebar"] h1 {
            color: #ff4b4b;
            font-size: 22px;
            padding-top: 20px;
            text-align: center;
        }
        section[data-testid="stSidebar"] p {
            text-align: center;
            color: #666;
            font-size: 13px;
        }
        
        /* Sidebar Radio Buttons */
        section[data-testid="stSidebar"] .stRadio label {
            color: #444 !important;
            font-size: 15px;
            padding: 8px 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }
        section[data-testid="stSidebar"] .stRadio div[role='radiogroup'] > label:hover {
            background-color: #ffe5e5;
            color: #ff4b4b !important;
        }
        
        /* --- CARD/CONTAINER STYLING --- */
        div.css-1r6slb0, .stForm, [data-testid="stMetric"] {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid #f0f0f0;
        }

        /* --- BUTTONS (Gradient Style) --- */
        div.stButton > button {
            background: linear-gradient(90deg, #ff4b4b 0%, #ff914d 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            width: 100%;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(255, 75, 75, 0.2);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        }
        
        /* Secondary/Download Buttons */
        div.stDownloadButton > button {
            background-color: #ffffff;
            color: #ff4b4b;
            border: 2px solid #ff4b4b;
            border-radius: 10px;
            font-weight: bold;
        }
        div.stDownloadButton > button:hover {
            background-color: #ff4b4b;
            color: white;
        }
        
        /* --- HEADERS --- */
        h1.main-title {
            font-weight: 700;
            color: #2c3e50;
            font-size: 32px;
            margin-bottom: 5px;
            border-bottom: 3px solid #ff4b4b;
            display: inline-block;
            padding-bottom: 5px;
        }
        p.subtitle {
            color: #666;
            font-size: 16px;
            margin-bottom: 25px;
            margin-top: 10px;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h1>❤️ Universal <span style='color:#333'>Studio</span></h1>", unsafe_allow_html=True)
    st.markdown("<p>The All-in-One Life Dashboard</p>", unsafe_allow_html=True)
    st.markdown("<p>Developed by Nirmal Raj</p>", unsafe_allow_html=True)
    st.markdown("---")

    # LEVEL 1: Select The Suite
    suite_mode = st.selectbox("📂 CATEGORY", ["🎨 Media Studio", "❤️ Life Tracker", "🛠️ Utility Toolkit"])
    
    st.markdown("---")
    
    # LEVEL 2: Select The Tool (Dynamic based on Suite)
    selected_tool = None
    
    if suite_mode == "🎨 Media Studio":
        st.caption("CREATIVE TOOLS")
        selected_tool = st.radio("Tool", ["Photo Enhancer", "Background Eraser", "Meme Creator", "Video Downloader"], label_visibility="collapsed")
        
    elif suite_mode == "❤️ Life Tracker":
        st.caption("HEALTH & WEALTH")
        selected_tool = st.radio("Tool", ["Weather", "Expenses", "BMI Calculator", "Health Journal"], label_visibility="collapsed")
        
    elif suite_mode == "🛠️ Utility Toolkit":
        st.caption("PRODUCTIVITY")
        selected_tool = st.radio("Tool", ["QR Generator", "PDF Tools", "Resume Builder", "Quick Notes"], label_visibility="collapsed")

    st.markdown("---")
    
    # --- CREDITS SECTION ---
    st.markdown(f"""
        <div style="background:#fff0f0; padding:15px; border-radius:10px; border:1px solid #ffcccc; text-align:center; margin-bottom: 20px;">
            <small style="color:#ff4b4b; font-weight:bold; letter-spacing: 1px;">ACTIVE TOOL</small><br>
            <span style="color:#333; font-weight: 600;">{selected_tool}</span>
        </div>
        

    """, unsafe_allow_html=True)


# ==========================================
#        SUITE 1: MEDIA STUDIO
# ==========================================

if selected_tool == "Photo Enhancer":
    st.markdown("<h1 class='main-title'>Photo Enhancer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Apply professional grade filters and effects.</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        c1, c2 = st.columns([1, 2], gap="large")
        
        with c1:
            st.subheader("Settings")
            filter_type = st.selectbox("Filter", ["Original", "Grayscale", "Black & White", "Sepia", "Blur", "Sharpen", "Invert"])
            if filter_type == "Blur":
                radius = st.slider("Intensity", 1, 10, 2)
                
        # Logic
        if filter_type == "Original": filtered = image
        elif filter_type == "Grayscale": filtered = ImageOps.grayscale(image)
        elif filter_type == "Black & White": filtered = ImageOps.grayscale(image).point(lambda x: 0 if x < 128 else 255, '1').convert('RGB')
        elif filter_type == "Sepia":
             img_np = np.array(image)
             sepia_filter = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
             filtered = Image.fromarray(np.clip(img_np @ sepia_filter.T, 0, 255).astype("uint8"))
        elif filter_type == "Blur": filtered = image.filter(ImageFilter.GaussianBlur(radius))
        elif filter_type == "Sharpen": filtered = image.filter(ImageFilter.SHARPEN)
        elif filter_type == "Invert": filtered = ImageOps.invert(image.convert("RGB"))

        with c2:
            st.image(filtered, caption=f"Result: {filter_type}", use_column_width=True)
            buf = BytesIO()
            filtered.save(buf, format="PNG")
            st.download_button("⬇️ Download Image", buf.getvalue(), "edited.png", "image/png")

elif selected_tool == "Background Eraser":
    st.markdown("<h1 class='main-title'>AI Background Eraser</h1>", unsafe_allow_html=True)
    
    if remove is None:
        st.error("⚠️ `rembg` library missing.")
    else:
        upl = st.file_uploader("Upload Image", type=["jpg", "png"])
        if upl:
            img = Image.open(upl)
            c1, c2 = st.columns(2)
            with c1: st.image(img, caption="Original", use_column_width=True)
            with c2:
                if st.button("✨ Remove Background"):
                    with st.spinner("Processing..."):
                        out = remove(img)
                        st.image(out, caption="No Background", use_column_width=True)
                        buf = BytesIO()
                        out.save(buf, format="PNG")
                        st.download_button("⬇️ Download PNG", buf.getvalue(), "nobg.png", "image/png")

elif selected_tool == "Meme Creator":
    st.markdown("<h1 class='main-title'>Meme Creator</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.5], gap="medium")
    with c1:
        src = st.radio("Source", ["Templates", "Upload"], horizontal=True)
        img = None
        if src == "Templates":
            t_url = st.selectbox("Template", ["https://i.imgflip.com/30b1gx.jpg", "https://i.imgflip.com/1ur9b0.jpg"])
            if t_url: img = Image.open(BytesIO(requests.get(t_url).content)).convert("RGBA")
        else:
            u = st.file_uploader("Upload", type=["jpg", "png"])
            if u: img = Image.open(u).convert("RGBA")
            
        top = st.text_input("Top Text", "WHEN THE CODE")
        bot = st.text_input("Bottom Text", "WORKS FIRST TRY")
        col = st.color_picker("Color", "#FFFFFF")
        
    with c2:
        if img:
            draw = ImageDraw.Draw(img)
            try: font = ImageFont.truetype("arial.ttf", int(img.height*0.1))
            except: font = ImageFont.load_default()
            
            def draw_t(txt, y):
                if txt:
                    bbox = draw.textbbox((0,0), txt, font=font)
                    w = bbox[2]-bbox[0]
                    x = (img.width - w)/2
                    draw.text((x,y), txt, font=font, fill=col, stroke_width=3, stroke_fill="black")
            
            draw_t(top, 10)
            draw_t(bot, img.height - int(img.height*0.15))
            st.image(img, use_column_width=True)

elif selected_tool == "Video Downloader":
    st.markdown("<h1 class='main-title'>Video Downloader</h1>", unsafe_allow_html=True)
    if yt_dlp is None: st.error("⚠️ `yt-dlp` missing.")
    else:
        url = st.text_input("YouTube URL")
        mode = st.radio("Format", ["Video (MP4)", "Audio (M4A)"], horizontal=True)
        if st.button("Download"):
            with st.spinner("Downloading..."):
                try:
                    fmt = 'bestvideo+bestaudio/best' if "Video" in mode else 'bestaudio/best'
                    with yt_dlp.YoutubeDL({'outtmpl': 'downloads/%(title)s.%(ext)s', 'format': fmt}) as ydl:
                        info = ydl.extract_info(url, download=True)
                        f = ydl.prepare_filename(info)
                    with open(f, "rb") as fl:
                        st.download_button("⬇️ Save File", fl.read(), os.path.basename(f))
                except Exception as e: st.error(str(e))


# ==========================================
#        SUITE 2: LIFE TRACKER
# ==========================================

elif selected_tool == "Weather":
    st.markdown("<h1 class='main-title'>Weather Dashboard</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1: city = st.text_input("City", "New York")
    with col2: btn = st.button("Check Weather")
    
    # Replace with your API KEY
    API_KEY = "YOUR_API_KEY"
    
    if btn:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            data = requests.get(url).json()
            if data.get("main"):
                st.metric("Temperature", f"{data['main']['temp']} °C", data['weather'][0]['description'])
                st.success(f"Humidity: {data['main']['humidity']}% | Wind: {data['wind']['speed']} m/s")
            else: st.error("City not found.")
        except: st.warning("Please configure API Key in code.")

elif selected_tool == "Expenses":
    st.markdown("<h1 class='main-title'>Expense Manager</h1>", unsafe_allow_html=True)
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Item", "Category", "Amount"])
        
    with st.form("exp_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1: 
            item = st.text_input("Item")
            amt = st.number_input("Amount", 0.0)
        with c2:
            cat = st.selectbox("Category", ["Food", "Travel", "Bills", "Health"])
            dt = st.date_input("Date")
        if st.form_submit_button("Add Expense"):
            new_row = {"Date": dt, "Item": item, "Category": cat, "Amount": amt}
            st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Saved!")
            
    if not st.session_state.expenses.empty and px:
        fig = px.pie(st.session_state.expenses, values='Amount', names='Category', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(st.session_state.expenses, use_container_width=True)

elif selected_tool == "BMI Calculator":
    st.markdown("<h1 class='main-title'>BMI Calculator</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: w = st.number_input("Weight (kg)", 60.0)
    with c2: h = st.number_input("Height (m)", 1.70)
    
    if st.button("Calculate"):
        bmi = w / (h ** 2)
        state = "Normal" if 18.5 <= bmi < 25 else "Overweight" if bmi >= 25 else "Underweight"
        color = "#2ecc71" if state == "Normal" else "#e67e22"
        st.markdown(f"<div style='background:{color}20; border-left:5px solid {color}; padding:20px; border-radius:10px;'><h3>BMI: {bmi:.2f}</h3><p style='margin:0; font-weight:bold; color:{color}'>{state}</p></div>", unsafe_allow_html=True)

elif selected_tool == "Health Journal":
    st.markdown("<h1 class='main-title'>Health Journal</h1>", unsafe_allow_html=True)
    date = st.date_input("Last Period")
    cycle = st.slider("Cycle Length", 21, 35, 28)
    nxt = date + datetime.timedelta(days=cycle)
    
    st.markdown(f"""
    <div style="background:#e3f2fd; padding:20px; border-radius:12px; border:1px solid #bbdefb; text-align:center;">
        <h3 style="color:#1565c0; margin:0;">Next Predicted Period</h3>
        <h2 style="color:#0d47a1; margin:10px 0;">{nxt.strftime('%B %d, %Y')}</h2>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
#        SUITE 3: UTILITY TOOLKIT
# ==========================================

elif selected_tool == "QR Generator":
    st.markdown("<h1 class='main-title'>QR Code Generator</h1>", unsafe_allow_html=True)
    if qrcode is None: st.error("⚠️ `qrcode` library missing.")
    else:
        txt = st.text_input("Content", "https://example.com")
        col = st.color_picker("Color", "#000000")
        if st.button("Generate"):
            qr = qrcode.QRCode(box_size=10, border=5)
            qr.add_data(txt)
            qr.make(fit=True)
            img = qr.make_image(fill_color=col, back_color="white")
            buf = BytesIO()
            img.save(buf)
            st.image(buf, width=250)
            st.download_button("Download", buf.getvalue(), "qr.png", "image/png")

elif selected_tool == "PDF Tools":
    st.markdown("<h1 class='main-title'>PDF Tools</h1>", unsafe_allow_html=True)
    if PyPDF2 is None: st.error("⚠️ `PyPDF2` missing.")
    else:
        f = st.file_uploader("Upload PDF", type="pdf")
        if f and st.button("Extract Text"):
            reader = PyPDF2.PdfReader(f)
            text = "".join([p.extract_text() for p in reader.pages])
            st.text_area("Content", text, height=300)

elif selected_tool == "Resume Builder":
    st.markdown("<h1 class='main-title'>Professional Resume Builder</h1>", unsafe_allow_html=True)
    if FPDF is None: st.error("⚠️ `fpdf` library missing.")
    else:
        with st.form("resume_form"):
            st.subheader("1. Contact Information")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                linkedin = st.text_input("LinkedIn Profile URL")
            with c2:
                phone = st.text_input("Phone Number")
                location = st.text_input("City, Country")
                role_title = st.text_input("Target Job Title")

            st.markdown("---")
            st.subheader("2. Professional Summary")
            summary = st.text_area("Brief Bio", height=100, placeholder="Experienced professional with...")

            st.markdown("---")
            st.subheader("3. Experience (Latest Role)")
            exp_role = st.text_input("Job Title")
            exp_company = st.text_input("Company Name")
            c3, c4 = st.columns(2)
            with c3: exp_start = st.text_input("Start Date")
            with c4: exp_end = st.text_input("End Date")
            exp_desc = st.text_area("Job Description", height=150)

            st.markdown("---")
            st.subheader("4. Education")
            edu_degree = st.text_input("Degree")
            edu_uni = st.text_input("University")
            edu_year = st.text_input("Graduation Year")

            st.markdown("---")
            st.subheader("5. Skills")
            skills = st.text_area("List your skills (comma separated)")

            submitted = st.form_submit_button("📄 Generate Professional Resume")

        if submitted:
            # PDF Generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Header
            pdf.set_font("Arial", "B", 26)
            pdf.cell(0, 10, name, ln=1)
            pdf.set_font("Arial", "I", 14)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 8, role_title, ln=1)
            
            # Contact Line
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(0, 0, 0)
            contact_line = f"{email} | {phone} | {location}"
            if linkedin: contact_line += f" | {linkedin}"
            pdf.cell(0, 8, contact_line, ln=1, border='B')
            pdf.ln(5)

            # Helper
            def add_section(title, content):
                if content:
                    pdf.set_font("Arial", "B", 12)
                    pdf.set_fill_color(230, 230, 230)
                    pdf.cell(0, 8, title.upper(), ln=1, fill=True)
                    pdf.ln(2)
                    pdf.set_font("Arial", "", 11)
                    pdf.multi_cell(0, 5, content)
                    pdf.ln(5)

            add_section("Professional Summary", summary)
            
            if exp_role:
                pdf.set_font("Arial", "B", 12)
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(0, 8, "EXPERIENCE", ln=1, fill=True)
                pdf.ln(2)
                
                pdf.set_font("Arial", "B", 11)
                pdf.cell(100, 6, f"{exp_role} at {exp_company}")
                pdf.set_font("Arial", "I", 11)
                pdf.cell(0, 6, f"{exp_start} - {exp_end}", ln=1, align='R')
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 5, exp_desc)
                pdf.ln(5)

            if edu_degree:
                add_section("Education", f"{edu_degree}\n{edu_uni} ({edu_year})")

            add_section("Skills", skills)

            html = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.success("Resume Generated Successfully!")
            st.download_button("⬇️ Download PDF", html, f"{name}_Resume.pdf", "application/pdf")

elif selected_tool == "Quick Notes":
    st.markdown("<h1 class='main-title'>Quick Notes</h1>", unsafe_allow_html=True)
    if 'notes' not in st.session_state: st.session_state.notes = []
    
    with st.form("note"):
        txt = st.text_area("New Note")
        if st.form_submit_button("Save"):
            st.session_state.notes.append(f"{datetime.datetime.now().strftime('%H:%M')} - {txt}")
            st.success("Saved")
            
    for n in reversed(st.session_state.notes):

        st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; margin-bottom:10px; border-left:5px solid #ff4b4b; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>{n}</div>", unsafe_allow_html=True)
