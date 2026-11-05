import streamlit as st
from pathlib import Path
from workflow import fashion_workflow
from image_generator import generate_fashion_image
from pdf_generator import generate_pdf_report

st.set_page_config(
    page_title="Fabric-to-Fashion AI",
    page_icon="👗",
    layout="wide"
)

# Load luxury fashion theme
css_path = Path("assets/style.css")

with open(css_path, "r") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
    )

# Luxury sidebar navigation
with st.sidebar:
    st.markdown(
        "<h1 style='font-family:Georgia; color:#713D4B;'>ATELIER AI</h1>",
        unsafe_allow_html=True
    )

    st.caption("YOUR PERSONAL FASHION STUDIO")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Design Studio",
            "About Project"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.caption("POWERED BY GEMINI + LANGGRAPH")

# Main application heading
# HOME PAGE
if page == "Home":

    st.title("Welcome to Atelier AI")
    st.subheader("Where fabric meets imagination.")

    st.write(
        "An intelligent fashion design studio that transforms "
        "fabric photographs into creative fashion collections."
    )

    st.divider()

    st.markdown("### Your creative journey")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 01")
        st.write("Fabric Analysis")
        st.caption("Discover fabric characteristics using AI.")

    with col2:
        st.markdown("#### 02")
        st.write("Fashion Design")
        st.caption("Explore creative garment recommendations.")

    with col3:
        st.markdown("#### 03")
        st.write("Collection Planning")
        st.caption("Build a coordinated fashion collection.")

    st.info("Select Design Studio from the sidebar to begin.")
    st.stop()


# ABOUT PROJECT PAGE
elif page == "About Project":

    st.title("About Atelier AI")
    st.subheader("The intelligence behind fashion creativity.")

    st.write(
        "Fabric-to-Fashion AI is an intelligent fashion design "
        "and collection planning system. It analyses fabric images "
        "and generates personalized fashion recommendations."
    )

    st.divider()

    st.markdown("### Technologies used")

    technologies = [
        "Python",
        "Streamlit",
        "LangChain",
        "LangGraph",
        "Google Gemini",
        "Cloudflare Workers AI",
        "ReportLab"
    ]

    for technology in technologies:
        st.write("•", technology)

    st.markdown("### AI Agent Architecture")

    st.write("Agent 1 — Fabric Analysis")
    st.write("Agent 2 — Fashion Design")
    st.write("Agent 3 — Collection Planning")

    st.stop()

    # DESIGN STUDIO PAGE
else:

    st.title("Fabric to Fashion")
    st.subheader("Where fabric meets imagination.")

    st.write(
        "Transform your fabric into a thoughtfully designed fashion collection."
    )

    # Initialize session state
    if "fashion_results" not in st.session_state:
        st.session_state.fashion_results = None

    if "generated_image" not in st.session_state:
        st.session_state.generated_image = None

    st.divider()

    st.markdown("## Your Design Studio")
    st.caption("Begin with a fabric. Let AI imagine the possibilities.")

    st.markdown("### 01 — Upload your fabric")

    fabric_image = st.file_uploader(
        "Choose your fabric photograph",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear photograph of your fabric."
    )

    if fabric_image:
        st.image(
            fabric_image,
            caption="Your selected fabric",
            width=350
        )
        st.success("Fabric uploaded successfully!")

    st.markdown("### 02 — Collection preferences")

    col1, col2 = st.columns(2)

    with col1:
        occasion = st.selectbox(
            "Occasion",
            ["Casual", "Party", "Wedding", "Office", "Summer"]
        )

    with col2:
        audience = st.selectbox(
            "Target audience",
            ["Women", "Men", "Children", "Unisex"]
        )

    budget = st.number_input(
        "Collection budget (₹)",
        min_value=500,
        max_value=100000,
        value=5000,
        step=500
    )
# Generate fashion collection
if st.button("Generate Fashion Collection"):

    if fabric_image is None:
        st.error("Please upload a fabric image first.")

    else:
        try:
            with st.spinner("Running all three AI agents..."):

                result = fashion_workflow.invoke({
                    "fabric_image": fabric_image,
                    "occasion": occasion,
                    "audience": audience,
                    "budget": int(budget)
                })

            st.session_state.fashion_results = result
            st.session_state.generated_image = None

            st.success("Fashion collection generated successfully!")

        except Exception as e:
            st.error(f"Collection generation failed: {e}")

# Display saved results
if st.session_state.fashion_results is not None:

    result = st.session_state.fashion_results

    fabric_result = result["fabric_analysis"]
    fashion_result = result["fashion_design"]
    collection_result = result["collection_plan"]

    st.divider()
    st.header("1. Fabric Analysis Results")

    st.write("**Fabric Type:**", fabric_result.fabric_type)
    st.write("**Primary Colour:**", fabric_result.primary_color)
    st.write("**Secondary Colours:**", ", ".join(fabric_result.secondary_colors))
    st.write("**Pattern:**", fabric_result.pattern)
    st.write("**Texture:**", fabric_result.texture)
    st.write("**Suitable Seasons:**", ", ".join(fabric_result.suitable_seasons))
    st.write("**Suitable Clothing:**", ", ".join(fabric_result.suitable_clothing))
    st.write("**Description:**", fabric_result.description)

    st.divider()
    st.header("2. Fashion Design Recommendations")

    st.subheader("Garment Recommendations")
    for item in fashion_result.garment_recommendations:
        st.write("•", item)

    st.subheader("Design Concepts")
    for item in fashion_result.design_concepts:
        st.write("•", item)

    st.subheader("Colour Combinations")
    for item in fashion_result.color_combinations:
        st.write("•", item)

    st.subheader("Styling Suggestions")
    for item in fashion_result.styling_suggestions:
        st.write("•", item)

    st.subheader("Occasion Suitability")
    for item in fashion_result.occasion_suitability:
        st.write("•", item)

    st.subheader("Design Summary")
    st.write(fashion_result.design_summary)

    st.divider()
    st.header("3. Complete Fashion Collection")

    st.subheader("Collection Name")
    st.write(collection_result.collection_name)

    st.subheader("Collection Theme")
    st.write(collection_result.collection_theme)

    st.subheader("Selected Outfits")
    for item in collection_result.selected_outfits:
        st.write("•", item)

    st.subheader("Collection Colour Palette")
    for color in collection_result.color_palette:
        st.write("•", color)

    st.subheader("Target Customer")
    st.write(collection_result.target_customer)

    st.subheader("Estimated Budget Breakdown")
    for item in collection_result.budget_breakdown:
        st.write("•", item)

    
    st.divider()
    st.header("Your AI Collection Results")
    st.caption("Your fabric, reimagined through artificial intelligence.")

    fabric_tab, design_tab, collection_tab = st.tabs([
        "01 · Fabric Analysis",
        "02 · Fashion Design",
        "03 · Collection Plan"
    ])

    # TAB 1 — FABRIC ANALYSIS
    with fabric_tab:
        st.subheader("Understanding your fabric")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Fabric Type", fabric_result.fabric_type)
            st.metric("Primary Colour", fabric_result.primary_color)

        with col2:
            st.metric("Pattern", fabric_result.pattern)
            st.metric("Texture", fabric_result.texture)

        st.markdown("### Secondary Colours")
        st.write(", ".join(fabric_result.secondary_colors))

        st.markdown("### Suitable Seasons")
        for item in fabric_result.suitable_seasons:
            st.write("•", item)

        st.markdown("### Suitable Clothing")
        for item in fabric_result.suitable_clothing:
            st.write("•", item)

        st.markdown("### Fabric Description")
        st.write(fabric_result.description)

    # TAB 2 — FASHION DESIGN
    with design_tab:
        st.subheader("Your fashion design recommendations")

        st.markdown("### Garment Recommendations")
        for item in fashion_result.garment_recommendations:
            st.write("•", item)

        st.markdown("### Design Concepts")
        for item in fashion_result.design_concepts:
            st.write("•", item)

        st.markdown("### Colour Combinations")
        for item in fashion_result.color_combinations:
            st.write("•", item)

        st.markdown("### Styling Suggestions")
        for item in fashion_result.styling_suggestions:
            st.write("•", item)

        st.markdown("### Occasion Suitability")
        for item in fashion_result.occasion_suitability:
            st.write("•", item)

        st.markdown("### Design Summary")
        st.write(fashion_result.design_summary)

    # TAB 3 — COLLECTION PLAN
    with collection_tab:
        st.subheader(collection_result.collection_name)

        st.markdown("### Collection Theme")
        st.write(collection_result.collection_theme)

        st.markdown("### Selected Outfits")
        for item in collection_result.selected_outfits:
            st.write("•", item)

        st.markdown("### Collection Colour Palette")
        for color in collection_result.color_palette:
            st.write("•", color)

        st.markdown("### Target Customer")
        st.write(collection_result.target_customer)

        st.markdown("### Estimated Budget Breakdown")
        for item in collection_result.budget_breakdown:
            st.write("•", item)

        st.markdown("### Collection Summary")
        st.write(collection_result.collection_summary)

            # LUXURY FASHION IMAGE GALLERY
    st.divider()

    st.header("Your Fashion Editorial")
    st.caption(
        "Discover your fabric transformed into a fashion design."
    )

    if st.button("Generate Fashion Image", key="generate_fashion_image"):
        try:
            with st.spinner("Creating your fashion editorial..."):
                generated_image = generate_fashion_image(
                    fabric_result,
                    fashion_result,
                    occasion,
                    audience
                )

                st.session_state.generated_image = generated_image.getvalue()

            st.success("Your fashion design is ready!")

        except Exception as e:
            st.error(f"Image generation failed: {e}")

    if st.session_state.generated_image is not None:
        st.image(
            st.session_state.generated_image,
            caption="AI-Generated Fashion Editorial",
            use_container_width=True
        )

        st.download_button(
            label="Download Fashion Design",
            data=st.session_state.generated_image,
            file_name="Atelier_AI_Fashion_Design.png",
            mime="image/png",
            key="download_fashion_design"
        )

    # PDF COLLECTION REPORT
    st.divider()

    st.header("Your Collection Report")
    st.caption("Take your complete AI-generated collection with you.")

    pdf_data = generate_pdf_report(
        fabric_result,
        fashion_result,
        collection_result,
        st.session_state.generated_image
    )

    st.download_button(
        label="Download Complete Collection Report (PDF)",
        data=pdf_data,
        file_name="Atelier_AI_Collection_Report.pdf",
        mime="application/pdf",
        key="download_collection_pdf"
    )
