import os
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)


def generate_pdf_report(
    fabric_analysis,
    fashion_design,
    collection_plan,
    generated_image=None
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#7B3F61"),
        fontSize=22,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#7B3F61"),
        spaceBefore=14,
        spaceAfter=8
    )

    story = []

    def add_paragraph(text, style=styles["BodyText"]):
        story.append(Paragraph(str(text), style))
        story.append(Spacer(1, 7))

    def add_list(items):
        for item in items:
            add_paragraph(f"&bull; {item}")

    # Report title
    story.append(Paragraph("FABRIC-TO-FASHION AI", title_style))
    add_paragraph("Intelligent Fashion Design and Collection Planning Report")
    story.append(Spacer(1, 15))

    # 1. Fabric analysis
    story.append(Paragraph("1. Fabric Analysis", heading_style))

    fabric_details = [
        ["Property", "Analysis"],
        ["Fabric Type", fabric_analysis.fabric_type],
        ["Primary Colour", fabric_analysis.primary_color],
        ["Secondary Colours", ", ".join(fabric_analysis.secondary_colors)],
        ["Pattern", fabric_analysis.pattern],
        ["Texture", fabric_analysis.texture],
        ["Suitable Seasons", ", ".join(fabric_analysis.suitable_seasons)],
        ["Suitable Clothing", ", ".join(fabric_analysis.suitable_clothing)]
    ]

    table = Table(fabric_details, colWidths=[130, 330])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7B3F61")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(table)
    story.append(Spacer(1, 10))
    add_paragraph(fabric_analysis.description)

    # 2. Fashion design
    story.append(Paragraph("2. Fashion Design Recommendations", heading_style))

    sections = [
        ("Garment Recommendations", fashion_design.garment_recommendations),
        ("Design Concepts", fashion_design.design_concepts),
        ("Colour Combinations", fashion_design.color_combinations),
        ("Styling Suggestions", fashion_design.styling_suggestions),
        ("Occasion Suitability", fashion_design.occasion_suitability)
    ]

    for heading, items in sections:
        add_paragraph(f"<b>{heading}</b>")
        add_list(items)

    add_paragraph(fashion_design.design_summary)

    # 3. Collection plan
    story.append(Paragraph("3. Complete Fashion Collection", heading_style))

    add_paragraph(f"<b>Collection Name:</b> {collection_plan.collection_name}")
    add_paragraph(f"<b>Collection Theme:</b> {collection_plan.collection_theme}")

    add_paragraph("<b>Selected Outfits</b>")
    add_list(collection_plan.selected_outfits)

    add_paragraph("<b>Collection Colour Palette</b>")
    add_list(collection_plan.color_palette)

    add_paragraph(f"<b>Target Customer:</b> {collection_plan.target_customer}")

    add_paragraph("<b>Estimated Budget Breakdown</b>")
    add_list(collection_plan.budget_breakdown)

    add_paragraph(collection_plan.collection_summary)

    # 4. AI-generated image
    if generated_image:
        story.append(Paragraph("4. AI-Generated Fashion Design", heading_style))

        image_buffer = BytesIO(generated_image)
        fashion_image = Image(
            image_buffer,
            width=4 * inch,
            height=5 * inch
        )
        fashion_image.hAlign = "CENTER"
        story.append(fashion_image)

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()