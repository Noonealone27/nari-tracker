import io
import textwrap
from typing import List

import feedparser
from PIL import Image, ImageDraw, ImageFont
import streamlit as st


# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="🚩 माझी लाडकी बहीण सहाय्यक (२०२६)",
    layout="centered",
    page_icon="🚩",
)


# ---------------------------
# Global styles (Haldi-Kumkum theme)
# ---------------------------
def inject_global_styles() -> None:
    custom_css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFF8E1 100%);
    }

    .main-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #D35400;
        text-align: center;
        margin-bottom: 0.25rem;
    }

    .sub-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        background: #fff0f0;
        color: #2b0c0c;
        font-size: 0.8rem;
        border: 1px solid #ffcdd2;
        margin-bottom: 0.75rem;
    }

    button[data-baseweb="tab"] {
        font-weight: 700;
        color: #000000 !important;
    }

    .nari-card {
        background: #ffffffcc;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid #ff9ec9;
        box-shadow: 0 4px 10px rgba(214, 51, 132, 0.18);
        margin-bottom: 1rem;
    }

    .nari-card h3 {
        color: #D35400;
        margin-top: 0;
        margin-bottom: 0.35rem;
    }

    .pink-button > button {
        background: linear-gradient(135deg, #D63384, #f06292) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .green-button > button {
        background: #27ae60 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .news-marquee-wrapper {
        background: #ffebee;
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
        border: 1px solid #ef5350;
        margin-bottom: 0.75rem;
    }

    .news-marquee-title {
        font-weight: 700;
        color: #c62828;
        font-size: 0.8rem;
        text-transform: uppercase;
    }

    .news-marquee-text {
        color: #b71c1c;
        font-size: 0.8rem;
    }

    .footer-text {
        font-size: 0.8rem;
        color: #2b0c0c;
        text-align: center;
        margin-top: 2rem;
    }

    /* High-contrast text across the app */
    body, p, li {
        color: #2b0c0c !important;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #2b0c0c !important;
    }

    label, .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #2b0c0c !important;
        font-weight: 600;
    }

    /* Info / success boxes with dark text */
    div.stAlert {
        color: #2b0c0c !important;
    }

    div.stAlert p, div.stAlert li, div.stAlert span {
        color: #2b0c0c !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


inject_global_styles()


# ---------------------------
# News Engine (Google News RSS)
# ---------------------------
@st.cache_data(show_spinner=False)
def fetch_news() -> List[str]:
    try:
        rss_url = (
            "https://news.google.com/rss/search?q=Majhi+Ladki+Bahin&hl=mr&gl=IN&ceid=IN:mr"
        )
        feed = feedparser.parse(rss_url)
        headlines: List[str] = []
        for entry in feed.entries[:10]:
            title = entry.get("title", "").strip()
            if title:
                headlines.append(title)
        return headlines
    except Exception:
        return []


def render_news_marquee() -> None:
    headlines = fetch_news()
    if not headlines:
        st.markdown(
            """
            <div class="news-marquee-wrapper">
                <span class="news-marquee-title">महत्वाची माहिती:</span>
                <span class="news-marquee-text"> माझी लाडकी बहीण २०२६ योजनेबाबत ताज्या अपडेट्ससाठी अधिकृत संकेतस्थळ व स्थानिक शासकीय सूचना पाहत रहा.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    news_text = " | ".join(headlines)
    marquee_html = f"""
    <div class="news-marquee-wrapper">
        <div class="news-marquee-title">माझी लाडकी बहीण - ताज्या बातम्या</div>
        <marquee behavior="scroll" direction="left" scrollamount="4" class="news-marquee-text">
            {news_text}
        </marquee>
    </div>
    """
    st.markdown(marquee_html, unsafe_allow_html=True)


# ---------------------------
# Image-based PDF helper
# ---------------------------
def create_blank_form_pdf(title: str, body: str, footer: str) -> bytes:
    """
    Generates a single-page A4 white PDF by drawing Marathi text
    onto an image using MarathiFont.ttf.
    """
    # A4 at high resolution (portrait)
    width, height = 2480, 3508
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load Marathi font; fall back if missing
    try:
        header_font = ImageFont.truetype("MarathiFont.ttf", 56)  # ~20-24 pt
        body_font = ImageFont.truetype("MarathiFont.ttf", 45)    # slightly larger body
        footer_font = ImageFont.truetype("MarathiFont.ttf", 45)
    except Exception:
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
        st.warning("MarathiFont.ttf सापडले नाही. PDF मध्ये डीफॉल्ट फॉन्ट वापरला जाईल.")

    current_y = 260

    # Header (center)
    if title:
        bbox = draw.textbbox((0, 0), title, font=header_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        header_x = (width - text_w) // 2
        draw.text((header_x, current_y), title, font=header_font, fill="black")
        current_y += text_h + 120

    # Body: wrap text (center each line)
    max_chars_per_line = 60
    body_line_height = body_font.size + 20  # extra spacing so sisters can write in blanks
    for para in body.split("\n"):
        if not para.strip():
            current_y += body_line_height
            continue
        wrapped_lines = textwrap.wrap(para, width=max_chars_per_line)
        for line in wrapped_lines:
            bbox = draw.textbbox((0, 0), line, font=body_font)
            line_w = bbox[2] - bbox[0]
            line_x = (width - line_w) // 2
            draw.text((line_x, current_y), line, font=body_font, fill="black")
            current_y += body_line_height
        current_y += 10

    # Footer placement: just below body text (not forced to bottom)
    if footer:
        line_height = footer_font.size + 8

        # Case 1: "left    right" format for date/signature alignment
        if "    " in footer:
            left_text, right_text = footer.split("    ", 1)

            # Wrap left/right parts independently
            left_lines = textwrap.wrap(left_text, width=30) or [""]
            right_lines = textwrap.wrap(right_text, width=30) or [""]
            block_lines = max(len(left_lines), len(right_lines))
            # Place footer a little below the end of the body
            footer_y = current_y + 200

            for i in range(block_lines):
                y = footer_y + i * line_height

                # Left side
                if i < len(left_lines):
                    left_line = left_lines[i]
                    left_x = 260
                    draw.text((left_x, y), left_line, font=footer_font, fill="black")

                # Right side
                if i < len(right_lines):
                    right_line = right_lines[i]
                    bbox_r = draw.textbbox((0, 0), right_line, font=footer_font)
                    right_w = bbox_r[2] - bbox_r[0]
                    right_x = width - right_w - 260
                    draw.text((right_x, y), right_line, font=footer_font, fill="black")

        # Case 2: single centered footer text with wrapping
        else:
            wrapped_footer = textwrap.wrap(footer, width=max_chars_per_line) or [""]
            footer_y = current_y + 200

            for line in wrapped_footer:
                bbox = draw.textbbox((0, 0), line, font=footer_font)
                line_w = bbox[2] - bbox[0]
                line_x = (width - line_w) // 2
                draw.text((line_x, footer_y), line, font=footer_font, fill="black")
                footer_y += line_height

    pdf_buffer = io.BytesIO()
    image.save(pdf_buffer, "PDF")
    pdf_buffer.seek(0)
    return pdf_buffer.read()


def download_pdf_button(label: str, pdf_bytes: bytes, file_name: str) -> None:
    st.markdown(
        "**Note: Data is processed locally to generate PDF. We do not store your information.**"
    )
    st.download_button(
        label=label,
        data=pdf_bytes,
        file_name=file_name,
        mime="application/pdf",
        use_container_width=True,
        key=file_name,
    )


# ---------------------------
# Static Marathi texts for forms
# ---------------------------
HAMIPATRA_BODY = (
    "मी, ________________________________________________ (नाव)\n"
    "आधार क्र. _____________________________________________\n"
    "राहणार ________________________________________________, शपथपूर्वक लिहून देते की:\n\n"
    "१. माझ्या कुटुंबाचे एकत्रित वार्षिक उत्पन्न रु. २.५० लाख पेक्षा जास्त नाही.\n"
    "२. माझ्या कुटुंबातील कोणीही सदस्य आयकरदाता (Tax Payer) नाही.\n"
    "३. मी स्वतः किंवा माझ्या कुटुंबातील सदस्य सरकारी नोकरीत कार्यरत नाही.\n"
    "४. मी शासनाच्या इतर विभागामार्फत राबविण्यात येणाऱ्या दरमहा रु. १५००/- पेक्षा जास्त "
    "रकमेच्या योजनेचा लाभ घेत नाही.\n"
    "५. माझ्या कुटुंबातील सदस्यांच्या नावावर चारचाकी वाहन (ट्रॅक्टर वगळून) नाही.\n\n"
    "मी दिलेली वरील माहिती खरी असून, ती चुकीची आढळल्यास मी कायदेशीर कार्यवाहीस पात्र राहीन."
)

HAMIPATRA_FOOTER = "दिनांक: _______________    सही: ____________________"

CORRECTION_BODY = (
    "प्रति, अंगणवाडी सेविका / बाल विकास प्रकल्प अधिकारी,\n"
    "__________________________________________ (केंद्र/गाव)\n\n"
    "विषय: 'मुख्यमंत्री - माझी लाडकी बहीण' योजनेच्या अर्जात दुरुस्ती करण्याबाबत.\n\n"
    "महोदय,\n"
    "मी, __________________________________________ (मोबाईल क्र. ____________________), "
    "या योजनेसाठी ऑनलाइन अर्ज केला होता. परंतु अर्ज भरताना माझ्याकडून अनवधानाने खालील चूक "
    "झाली आहे:\n\n"
    "चूक: 'Govt Job' या पर्यायावर 'YES' क्लिक झाले आहे / किंवा इतर: ________________________.\n\n"
    "वास्तविक पाहता, माझ्या घरी कोणीही सरकारी नोकरीत नाही. तरी कृपया माझ्या अर्जात योग्य ती "
    "दुरुस्ती करून माझा अर्ज मंजूर करण्यात यावा. सोबत आधार कार्ड जोडले आहे."
)

CORRECTION_FOOTER = "अर्जदार सही: ____________________"

DBT_BODY = (
    "प्रति, शाखा व्यवस्थापक (Branch Manager),\n"
    "बँकेचे नाव: __________________________________________\n"
    "शाखा: __________________________________________\n\n"
    "विषय: बँक खाते आधार कार्डशी लिंक करणेबाबत (DBT Enable).\n\n"
    "महोदय,\n"
    "माझे आपल्या बँकेत खाते क्रमांक __________________________________________ असून, मला शासनाचे "
    "थेट लाभ (DBT) जमा होण्यासाठी माझे खाते NPCI मॅपरशी लिंक करावे.\n\n"
    "मी याद्वारे माझे आधार कार्ड (क्र. ______________________________) बँक खात्याशी जोडण्यास "
    "संमती देत आहे."
)

DBT_FOOTER = "सही: ____________________    नाव: ____________________"


# ---------------------------
# Tabs
# ---------------------------
def render_tab_status() -> None:
    st.markdown(
        '<div class="nari-card"><h3>ऑनलाइन अर्जाची स्थिती समजून घ्या</h3>'
        "<p>माझी लाडकी बहीण पोर्टलवर तुमच्या अर्जाची स्थिती कशी पाहायची, हे सोप्या भाषेत इथे दिले आहे.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container():
            st.markdown('<div class="green-button">', unsafe_allow_html=True)
            st.link_button(
                "🟢 अधिकृत लॉगिन (Server Link)",
                url="https://ladakibahin.maharashtra.gov.in/",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.caption("महाराष्ट्र शासनाच्या अधिकृत संकेतस्थळावर लॉगिन करून अर्जाची स्थिती तपासा.")

    st.divider()

    st.subheader("स्थिती समजण्यासाठी मार्गदर्शक")

    st.info(
        "🕒 **Pending / Under Process**\n\n"
        "याचा अर्थ: तुमचा अर्ज प्रलंबित असून शासकीय यंत्रणा त्यावर काम करत आहे.\n\n"
        "**काय करायचे?**\n"
        "- कमीतकमी **५ दिवस** प्रतीक्षा करा.\n"
        "- नंतर पुन्हा पोर्टलवर जाऊन स्थिती तपासा."
    )

    st.success(
        "✅ **Approved / Sanctioned**\n\n"
        "याचा अर्थ: तुमचा अर्ज मंजूर झाला आहे.\n\n"
        "**काय करायचे?**\n"
        "- तुमच्या बँक खात्यात थेट DBT रक्कम जमा होईल.\n"
        "- नेट बँकिंग / एटीएम / पासबुक मधून खाते शिल्लक तपासा.\n"
        "- पैसे आले नसतील तर 'आधार लिंक' टॅबमधील फॉर्म वापरा."
    )

    st.error(
        "❌ **Rejected / Not Eligible**\n\n"
        "याचा अर्थ: तुमचा अर्ज नाकारला गेला आहे किंवा आपण पात्र मानले गेलेले नाही.\n\n"
        "**काय करायचे?**\n"
        "- प्रथम स्थानिक अंगणवाडी सेविका / ग्रामपंचायत कार्यालयात चौकशी करा.\n"
        "- त्यानंतर 'दुरुस्ती' टॅबमधील ब्लँक फॉर्म वापरून दुरुस्ती अर्ज सादर करा."
    )


def render_tab_hamipatra() -> None:
    st.markdown(
        '<div class="nari-card"><h3>हमीपत्र (Self Declaration)</h3>'
        "<p>अधिकृत नमुन्यानुसार रिकामा हमीपत्र फॉर्म PDF स्वरूपात डाउनलोड करा.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("📄 हमीपत्र PDF डाउनलोड करा", type="primary"):
        pdf_bytes = create_blank_form_pdf(
            title="हमीपत्र (Self Declaration)",
            body=HAMIPATRA_BODY,
            footer=HAMIPATRA_FOOTER,
        )
        download_pdf_button("⬇️ हमीपत्र PDF सेव्ह करा", pdf_bytes, "hamipatra_blank.pdf")


def render_tab_correction() -> None:
    st.markdown(
        '<div class="nari-card"><h3>अर्ज दुरुस्ती विनंती पत्र</h3>'
        "<p>'Govt Job' अशा चुकीच्या निवडींसाठी वापरता येईल असा रिकामा दुरुस्ती अर्ज डाउनलोड करा.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("📄 दुरुस्ती अर्ज PDF डाउनलोड करा", type="primary"):
        pdf_bytes = create_blank_form_pdf(
            title="अर्ज दुरुस्ती विनंती पत्र",
            body=CORRECTION_BODY,
            footer=CORRECTION_FOOTER,
        )
        download_pdf_button(
            "⬇️ दुरुस्ती अर्ज PDF सेव्ह करा",
            pdf_bytes,
            "correction_application_blank.pdf",
        )


def render_tab_dbt() -> None:
    st.markdown(
        '<div class="nari-card"><h3>आधार लिंकिंग अर्ज (Bank Seeding)</h3>'
        "<p>DBT साठी बँक खात्यात आधार लिंक करण्यासाठी वापरता येणारा रिकामा अर्ज डाउनलोड करा.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("📄 आधार लिंकिंग PDF डाउनलोड करा", type="primary"):
        pdf_bytes = create_blank_form_pdf(
            title="आधार लिंकिंग अर्ज (Bank Seeding)",
            body=DBT_BODY,
            footer=DBT_FOOTER,
        )
        download_pdf_button(
            "⬇️ आधार लिंकिंग PDF सेव्ह करा",
            pdf_bytes,
            "aadhaar_linking_blank.pdf",
        )


def render_tab_help() -> None:
    st.markdown(
        '<div class="nari-card"><h3>मदत व स्थानिक मार्गदर्शन</h3>'
        "<p>ऑनलाइन प्रक्रियेबरोबर प्रत्यक्ष कोणाकडे जावे, कोणाशी संपर्क करावा याबाबतची माहिती.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        **हेल्पलाइन कॉल (१८१):**

        मोबाइलवरून थेट कॉल करण्यासाठी खालील बटणावर क्लिक करा.
        """,
        unsafe_allow_html=False,
    )

    st.markdown(
        """
        <a href="tel:181">
            <button style="
                background: linear-gradient(135deg, #D63384, #f06292);
                color: white;
                border: none;
                border-radius: 999px;
                padding: 0.5rem 1.2rem;
                font-weight: 600;
                cursor: pointer;
            ">
                📞 Call 181 (Helpline)
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        """
        **शारीरिक पडताळणी व स्थानिक मदत:**

        - आपल्या **ग्रामपंचायत कार्यालयात** जाऊन लाडकी बहीण अर्जाबाबत चौकशी करा.\n
        - जवळच्या **अंगणवाडी केंद्रात** सेविका / मदतनीस यांच्याकडून पोर्टलवरील स्थिती समजून घ्या.\n
        - **महिला व बाल विकास, तलाठी कार्यालय** इथेही या योजनेबाबत मार्गदर्शन मिळू शकते.\n
        - **बँक शाखेत** जाऊन DBT व आधार-लिंकिंग प्रक्रियेबद्दल विचारपूस करा (आधार लिंकिंग PDF सोबत घ्या). 
        """,
        unsafe_allow_html=False,
    )


# ---------------------------
# Monetization Footer
# ---------------------------
def render_footer() -> None:
    # Separator and new Help & Finance section
    st.markdown("---")
    st.header("💸 महत्वाची सुविधा (Free Service)")

    col_left, col_right = st.columns(2)

    with col_left:
        st.info("**बँक खाते नाही? (For DBT)**")
        st.markdown('<div class="pink-button">', unsafe_allow_html=True)
        st.link_button(
            "🏦 कोटक झिरो बॅलन्स खाते",
            url="https://bitli.in/QeL2p5a",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.info("**अर्जंट पैशांची गरज आहे?**")
        st.markdown('<div class="pink-button">', unsafe_allow_html=True)
        st.link_button(
            "⚡ Olyv (SmartCoin) लोन",
            url="https://bitli.in/4muBG43",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Existing CTA
    st.markdown(
        """
        <div class="footer-text">
            <p><strong>पैसे आले नाहीत का?</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="pink-button">', unsafe_allow_html=True)
        st.link_button(
            "🏦 Kotak 811 खाते उघडा (Fast DBT)",
            url="https://bitli.in/QeL2p5a",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Final disclaimer
    st.markdown(
        """
        <div class="footer-text">
            <p>Disclaimer: This is an educational tool. Not associated with Govt of Maharashtra.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------
# Main layout
# ---------------------------
def main() -> None:
    st.markdown(
        '<div class="main-title">🚩 माझी लाडकी बहीण सहाय्यक (२०२६)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="text-align:center;"><span class="sub-badge">⚠️ केवळ माहितीसाठी | हे ॲप शासकीय नाही</span></div>',
        unsafe_allow_html=True,
    )

    render_news_marquee()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["स्थिती", "हमीपत्र", "दुरुस्ती", "आधार लिंक", "मदत"]
    )

    with tab1:
        render_tab_status()
    with tab2:
        render_tab_hamipatra()
    with tab3:
        render_tab_correction()
    with tab4:
        render_tab_dbt()
    with tab5:
        render_tab_help()

    render_footer()


if __name__ == "__main__":
    main()

