from pydantic import BaseModel, Field
from typing import List


class FabricAnalysis(BaseModel):

    fabric_type: str = Field(description="Likely type of fabric")
    primary_color: str = Field(description="Main colour of the fabric")
    secondary_colors: List[str] = Field(description="Other colours visible")
    pattern: str = Field(description="Pattern of the fabric")
    texture: str = Field(description="Visible texture")
    suitable_seasons: List[str] = Field(description="Suitable seasons")
    suitable_clothing: List[str] = Field(description="Suitable clothing")
    description: str = Field(description="Overall fabric description")


class FashionDesign(BaseModel):

    garment_recommendations: List[str] = Field(description="Recommended garments")
    design_concepts: List[str] = Field(description="Clothing design concepts")
    color_combinations: List[str] = Field(description="Recommended colour combinations")
    styling_suggestions: List[str] = Field(description="Accessories and styling")
    occasion_suitability: List[str] = Field(description="Suitable occasions")
    design_summary: str = Field(description="Overall design summary")


class CollectionPlan(BaseModel):

    collection_name: str = Field(description="Name of the fashion collection")
    collection_theme: str = Field(description="Overall collection theme")
    selected_outfits: List[str] = Field(description="Outfits in the collection")
    color_palette: List[str] = Field(description="Collection colour palette")
    target_customer: str = Field(description="Description of target customer")
    budget_breakdown: List[str] = Field(description="Estimated budget allocation")
    collection_summary: str = Field(description="Overall collection summary")