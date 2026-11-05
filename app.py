
import streamlit as st
import os

for key in ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"]:
    if key in st.secrets:
        os.environ[key] = st.secrets[key]

from image_generator import generate_fashion_image
from types import SimpleNamespace
from io import BytesIO
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as PDFImage
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Fabric-to-Fashion AI",
    page_icon="👗",
    layout="wide"
)

# --------------------------------------------------
# LUXURY THEME
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');

.stApp {
    background: #F8F5F0;
    color: #49352F;
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #49352F !important;
}

section[data-testid="stSidebar"] {
    background: #EEE6DC;
}

.stButton > button,
.stDownloadButton > button {
    background: #713D4B;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.65rem 1.2rem;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #542B37;
    color: white;
}

.demo-banner {
    background: #EFE8DE;
    border-left: 4px solid #B69A72;
    padding: 14px;
    border-radius: 5px;
    margin-bottom: 20px;
}

.metric-card {
    background: white;
    border: 1px solid #DED3C6;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------

FABRIC_ANALYSIS = {
    "fabric_type": "Silk / Silk-blend (sample classification)",
    "primary_color": "Based on the selected design palette",
    "secondary_colors": ["Ivory", "Antique Gold", "Deep Burgundy"],
    "pattern": "Traditional woven-inspired pattern",
    "texture": "Smooth, elegant drape (sample description)",
    "seasons": ["Winter", "Autumn", "Festive occasions"],
    "clothing": ["Anarkali", "Saree blouse", "Lehenga", "Kurta set"],
    "description": (
        "This sample analysis demonstrates how fabric characteristics "
        "can be translated into fashion design possibilities. "
        "It is not an AI analysis of the uploaded photograph."
    )
}

DESIGN_CONCEPTS = [
    "Contemporary silk Anarkali with subtle antique-gold detailing",
    "Structured festive blouse with elegant sleeve detailing",
    "Flowing A-line kurta with coordinated embroidered accents"
]

GARMENTS = [
    "Silk Anarkali suit",
    "Contemporary festive blouse",
    "Coordinated dupatta"
]

STYLING = [
    "Antique gold statement earrings",
    "Minimal gold bangles",
    "Embellished traditional footwear"
]

COLLECTION_OUTFITS = [
    "01 — Signature Silk Anarkali",
    "02 — Modern Festive Ensemble",
    "03 — Classic Coordinated Kurta Set",
    "04 — Statement Occasion Wear"
]

# --------------------------------------------------
# PDF GENERATOR
# --------------------------------------------------

def create_pdf(fabric_image, occasion, audience, budget):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "LuxuryTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        textColor=colors.HexColor("#713D4B"),
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "LuxuryHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#713D4B"),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = styles["BodyText"]

    story = []

    story.append(Paragraph("FABRIC-TO-FASHION AI", title_style))
    story.append(Paragraph(
        "Fashion Design & Collection Planning Report",
        styles["Heading2"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>DEMO REPORT — SAMPLE RESULTS, NOT LIVE AI OUTPUT</b>",
        body_style
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph("Project Details", heading_style))

    details = [
        ["Occasion", occasion],
        ["Target Audience", audience],
        ["Collection Budget", f"INR {budget:,}"],
        ["Report Date", str(date.today())]
    ]

    table = Table(details, colWidths=[150, 320])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFE8DE")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#49352F")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DED3C6")),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    story.append(table)

    if fabric_image:
        story.append(Paragraph("Uploaded Fabric Photograph", heading_style))
        try:
            uploaded = PDFImage(
                BytesIO(fabric_image),
                width=2.5 * inch,
                height=2.5 * inch,
                kind="proportional"
            )
            story.append(uploaded)
        except Exception:
            story.append(Paragraph(
                "Fabric photograph could not be embedded.",
                body_style
            ))

    story.append(Paragraph("Fabric Analysis", heading_style))
    story.append(Paragraph(
        FABRIC_ANALYSIS["description"],
        body_style
    ))

    story.append(Paragraph("Fashion Design Recommendations", heading_style))

    for item in DESIGN_CONCEPTS:
        story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 5))

    story.append(Paragraph("Recommended Garments", heading_style))

    for item in GARMENTS:
        story.append(Paragraph(f"• {item}", body_style))

    story.append(Paragraph("Collection Plan", heading_style))

    for item in COLLECTION_OUTFITS:
        story.append(Paragraph(f"• {item}", body_style))

    story.append(Paragraph("Estimated Budget Allocation", heading_style))

    budget_rows = [
        ["Category", "Allocation"],
        ["Fabric and material", f"INR {budget * 0.40:,.0f}"],
        ["Stitching and construction", f"INR {budget * 0.25:,.0f}"],
        ["Embroidery and detailing", f"INR {budget * 0.20:,.0f}"],
        ["Accessories and finishing", f"INR {budget * 0.15:,.0f}"]
    ]

    budget_table = Table(budget_rows, colWidths=[260, 210])

    budget_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#713D4B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DED3C6")),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(budget_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "This report demonstrates the proposed project workflow "
        "using predefined sample fashion recommendations.",
        body_style
    ))

    document.build(story)

    return buffer.getvalue()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("ATELIER")
st.sidebar.caption("FABRIC-TO-FASHION AI")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Design Studio", "About Project"]
)

st.sidebar.divider()
st.sidebar.caption("AI Fashion Design & Collection Planning")

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.title("Fabric to Fashion AI")
    st.subheader("Where fabric inspiration meets intelligent design.")

    st.markdown("""
    Transform fabric inspiration into fashion possibilities
    through an interactive fashion design and collection
    planning experience.
    """)

    st.markdown("""
    <div class="demo-banner">
    <b>Presentation Demo Mode</b><br>
    This online demonstration uses predefined sample results.
    Live Gemini and Cloudflare API calls are disabled.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Fabric Analysis")
        st.write("Explore fabric characteristics and design possibilities.")

        st.markdown("### Fashion Design")
        st.write("Discover garment concepts, colours and styling.")

    with col2:
        st.markdown("### Collection Planning")
        st.write("Build coordinated outfits for selected occasions.")

        st.markdown("### PDF Reports")
        st.write("Export a sample fashion collection report.")

    st.info("Select Design Studio from the sidebar to begin.")

# --------------------------------------------------
# DESIGN STUDIO
# --------------------------------------------------

elif page == "Design Studio":

    st.title("The Design Studio")
    st.caption("Transform your fabric inspiration into a fashion collection.")

    st.markdown("""
    <div class="demo-banner">
    <b>Demo Mode:</b> The results below are predefined examples.
    They are not generated by live AI models.
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.1, 0.9])

    with left:

        st.subheader("01. Upload Your Fabric")

        uploaded_file = st.file_uploader(
            "Choose a fabric photograph",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:
            st.image(
                uploaded_file,
                caption="Your Uploaded Fabric",
                use_container_width=True
            )

    with right:

        st.subheader("02. Collection Preferences")

        occasion = st.selectbox(
            "Select Occasion",
            [
                "Festive Wear",
                "Wedding Wear",
                "Casual Wear",
                "Formal Wear",
                "Party Wear"
            ]
        )

        audience = st.selectbox(
            "Target Audience",
            [
                "Women",
                "Men",
                "Unisex",
                "Young Adults"
            ]
        )

        budget = st.number_input(
            "Collection Budget (INR)",
            min_value=1000,
            max_value=1000000,
            value=25000,
            step=1000
        )

    st.divider()

    if st.button("Generate Sample Fashion Collection", use_container_width=True):

        if not uploaded_file:
            st.warning("Please upload a fabric photograph first.")

        else:
            st.session_state.demo_ready = True
            st.session_state.demo_image = uploaded_file.getvalue()
            st.session_state.demo_occasion = occasion
            st.session_state.demo_audience = audience
            st.session_state.demo_budget = budget

    if st.session_state.get("demo_ready", False):

        fabric_image = st.session_state.demo_image
        occasion = st.session_state.demo_occasion
        audience = st.session_state.demo_audience
        budget = st.session_state.demo_budget

        st.success("Your sample fashion collection is ready!")

        fabric_tab, design_tab, collection_tab = st.tabs([
            "Fabric Analysis",
            "Fashion Design",
            "Collection Plan"
        ])

        with fabric_tab:

            st.subheader("Fabric Analysis — Sample")

            st.write("**Fabric Type:**", FABRIC_ANALYSIS["fabric_type"])
            st.write("**Primary Colour:**", FABRIC_ANALYSIS["primary_color"])
            st.write("**Secondary Colours:**", ", ".join(FABRIC_ANALYSIS["secondary_colors"]))
            st.write("**Pattern:**", FABRIC_ANALYSIS["pattern"])
            st.write("**Texture:**", FABRIC_ANALYSIS["texture"])

            st.write("**Suitable Seasons:**")
            for item in FABRIC_ANALYSIS["seasons"]:
                st.write(f"- {item}")

            st.write("**Suitable Clothing:**")
            for item in FABRIC_ANALYSIS["clothing"]:
                st.write(f"- {item}")

            st.info(FABRIC_ANALYSIS["description"])

        with design_tab:

            st.subheader("Fashion Design Recommendations")

            st.write("**Occasion:**", occasion)
            st.write("**Target Audience:**", audience)

            st.write("### Design Concepts")
            for item in DESIGN_CONCEPTS:
                st.write(f"- {item}")

            st.write("### Garment Recommendations")
            for item in GARMENTS:
                st.write(f"- {item}")

            st.write("### Styling Suggestions")
            for item in STYLING:
                st.write(f"- {item}")

        with collection_tab:

            st.subheader("The Modern Heritage Collection")

            st.write(
                "A sample collection combining traditional inspiration "
                "with contemporary silhouettes."
            )

            st.write("### Selected Outfits")

            for item in COLLECTION_OUTFITS:
                st.write(f"- {item}")

            st.write("### Collection Colour Palette")
            st.write("Ivory | Antique Gold | Burgundy | Champagne")

            st.write("### Target Customer")
            st.write(audience)

            st.write("### Estimated Budget Breakdown")

            allocations = [
                ("Fabric and Material", 0.40),
                ("Stitching and Construction", 0.25),
                ("Embroidery and Detailing", 0.20),
                ("Accessories and Finishing", 0.15)
            ]

            for name, percentage in allocations:
                st.write(
                    f"- {name}: INR {budget * percentage:,.0f}"
                )

            st.write(f"**Total Budget: INR {budget:,.0f}**")

        st.divider()

        st.header("Your Collection Report")
        st.header("AI Fashion Image Generator")

if st.button("Generate Fashion Picture"):
    try:
        fabric_data = SimpleNamespace(
            fabric_type="Silk",
            primary_color="Burgundy",
            secondary_colors=["Ivory", "Antique Gold"],
            pattern="Traditional woven pattern",
            texture="Smooth and elegant"
        )

        design_data = SimpleNamespace(
            design_concepts=[
                "Luxury burgundy silk Anarkali with antique gold embroidery"
            ],
            garment_recommendations=["Silk Anarkali"],
            styling_suggestions=["Antique gold jewellery"]
        )

        with st.spinner("AI is creating your fashion design..."):
            image = generate_fashion_image(
                fabric_data,
                design_data,
                "Festive",
                "Contemporary women"
            )

            st.session_state.generated_fashion_image = image.getvalue()

    except Exception as e:
        st.error(f"Image generation failed: {e}")

if st.session_state.get("generated_fashion_image"):
    st.image(
        st.session_state.generated_fashion_image,
        caption="AI Generated Fashion Design",
        use_container_width=True
    )

    st.download_button(
        "Download Fashion Image",
        data=st.session_state.generated_fashion_image,
        file_name="fashion_design.png",
        mime="image/png"
    )

    pdf_data = create_pdf(
    st.session_state.get("demo_image"),
    occasion,
    audience,
    budget
    )

    st.download_button(
        "Download Collection Report (PDF)",
        data=pdf_data,
        file_name="Fabric_to_Fashion_Demo_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )     
# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

else:

    st.title("About the Project")

    st.subheader(
        "An Intelligent Fashion Design and Collection Planning Agent"
    )

    st.write("""
    Fabric-to-Fashion AI is an academic project that demonstrates
    how artificial intelligence technologies can support fabric
    analysis, fashion design and coordinated collection planning.
    """)

    st.header("Technology Stack")

    technologies = [
        ["Technology", "Purpose"],
        ["Python", "Core programming"],
        ["Streamlit", "Interactive web interface"],
        ["LangChain", "LLM integration in the full AI version"],
        ["LangGraph", "Multi-agent orchestration in the full AI version"],
        ["Google Gemini", "Fabric analysis and design recommendations"],
        ["Cloudflare Workers AI", "Fashion image generation"],
        ["Pydantic", "Structured data validation"]
    ]

    technology_table = st.table(technologies)

    st.header("Three-Agent Architecture")

    st.markdown("""
    1. **Fabric Analysis Agent** — analyses fabric characteristics.
    2. **Fashion Design Agent** — recommends garment designs.
    3. **Collection Planning Agent** — coordinates the final collection.
    """)

    st.info(
        "The full AI-powered workflow is available in the local project. "
        "This online version is a sample demonstration and does not call "
        "the live AI agents."
    )

    st.caption("Developed as an academic project — Fabric-to-Fashion AI.")
