from typing import Literal
from pydantic import BaseModel, Field

Occasion = Literal['college', 'interview', 'party', 'festival']
Style = Literal['ethnic', 'western', 'ethnic-fusion', 'casual-minimal']
Fit = Literal['relaxed', 'regular', 'fitted']
Coverage = Literal['no-preference', 'moderate', 'full']

class InputProfile(BaseModel):  # what the form collects
    occasion: Occasion
    style: Style
    fit: Fit
    coverage: Coverage = 'no-preference'
    colours: list[str] = []
    budget_inr: int = Field(ge=0)
    owned_item_ids: list[str] = []

class Look(BaseModel):  # one outfit the AI returns
    title: str
    item_ids: list[str]
    colour_story: str
    why_it_fits: str
    alternative_item_ids: list[str]

class LookSet(BaseModel):
    looks: list[Look]