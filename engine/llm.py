import os, time
from google import genai

def call_llm(prompt, schema, retries=2):
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
    for attempt in range(retries + 1):
        try:
            r = client.models.generate_content(
                model=os.environ['GEMINI_MODEL'],
                contents=prompt,
                config={'response_mime_type': 'application/json',
                        'response_schema': schema,
                        'temperature': 0.7},
            )
            if r.parsed is not None:
                return r.parsed
        except Exception as e:
            print('LLM error:', e)
        time.sleep(2 ** attempt)
    return None

def build_prompt(profile, candidates, owned_items):
    owned = '\n'.join(f"{i['id']} | {i['name']}" for i in owned_items) or 'none'
    shortlist = '\n'.join(
        f"{i['id']} | {i['name']} | {i['category']} | {', '.join(i['colours'])} | Rs {i['price_band_inr'][0]}-{i['price_band_inr'][1]}"
        for i in candidates)
    colours = ', '.join(profile.colours) or 'any'
    return f"""You are a fashion stylist for Indian college students.
USER: occasion={profile.occasion}, style={profile.style}, fit preference={profile.fit}, coverage={profile.coverage}, liked colours={colours}, budget=₹{profile.budget_inr}
ALREADY OWNED (cost ₹0, prefer these):
{owned}
SHORTLIST (use ONLY these ids, or the owned ids):
{shortlist}

Build exactly 2 different complete looks. Each look has one top and one bottom (or one one-piece), footwear, a bag, and 1 to 2 jewellery items.
For each look return: title, item_ids, colour_story (1 sentence), why_it_fits (max 2 sentences), alternative_item_ids (max 2).
Rules: use only ids from the lists above. Do not write prices in your text, but choose items so the total of the higher prices of items the user does not already own stays within the budget if possible. Do not comment on the user's body or appearance. Colour advice is a suggestion, not a rule."""