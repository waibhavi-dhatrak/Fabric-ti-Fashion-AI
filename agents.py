import os
import base64

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from schemas import FabricAnalysis, FashionDesign, CollectionPlan 


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

fabric_model = llm.with_structured_output(FabricAnalysis)


def analyze_fabric(image_file):
    image_bytes = image_file.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    image_url = f"data:{image_file.type};base64,{encoded_image}"

    response = fabric_model.invoke([
        HumanMessage(content=[
            {
                "type": "text",
                "text": """
                You are an expert textile analyst.

                Analyze the uploaded fabric image.

                Identify:
                - Likely fabric type
                - Primary colour
                - Secondary colours
                - Pattern
                - Texture
                - Suitable seasons
                - Suitable clothing styles
                - Overall description

                Only identify properties visible or reasonably inferable.
                Do not claim exact fibre composition can be confirmed visually.
                Mention uncertainty where necessary.
                """
            },
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        ])
    ])

    return response

def generate_fashion_design(fabric_analysis, occasion, audience, budget):

    fashion_model = llm.with_structured_output(FashionDesign)

    prompt = f"""
    You are an expert fashion designer.

    Fabric Analysis:
    {fabric_analysis.model_dump()}

    Occasion: {occasion}
    Target Audience: {audience}
    Budget: ₹{budget}

    Generate:
    1. Garment recommendations.
    2. Creative design concepts.
    3. Colour combinations.
    4. Styling and accessory suggestions.
    5. Suitable occasions.

    Keep recommendations realistic and within the budget.
    Do not invent exact market prices.
    """

    response = fashion_model.invoke(prompt)

    return response

def generate_collection_plan(
    fabric_analysis,
    fashion_design,
    occasion,
    audience,
    budget
):

    collection_model = llm.with_structured_output(CollectionPlan)

    prompt = f"""
    You are an expert fashion collection planner.

    Create a coordinated fashion collection using the
    following information.

    FABRIC ANALYSIS:
    {fabric_analysis.model_dump()}

    FASHION DESIGN RECOMMENDATIONS:
    {fashion_design.model_dump()}

    OCCASION: {occasion}
    TARGET AUDIENCE: {audience}
    TOTAL BUDGET: ₹{budget}

    Generate:

    1. A creative collection name.
    2. An overall collection theme.
    3. A coordinated list of outfits.
    4. A consistent colour palette.
    5. A description of the target customer.
    6. A realistic estimated budget breakdown.
    7. A summary of the complete collection.

    IMPORTANT:
    - Keep the collection within the given budget.
    - Make the outfits suitable for the selected occasion.
    - Use the analysed fabric characteristics.
    - Do not invent exact market prices.
    - Clearly label costs as estimates.
    """

    response = collection_model.invoke(prompt)

    return response