import json
from pathlib import Path
from .models import Look, LookSet
from .rules import shortlist
from .llm import call_llm, build_prompt
from .budget import cost_range, budget_status

ITEMS = json.loads((Path(__file__).parent.parent / 'data' / 'items.json').read_text(encoding='utf-8'))
BY_ID = {i['id']: i for i in ITEMS}
OWNABLE = {i['name']: i['id'] for i in ITEMS if i.get('ownable')}

def valid(result, allowed):
    return (result is not None and len(result.looks) == 2
            and all(set(l.item_ids) <= allowed for l in result.looks))

def make_card(look, owned, budget):
    lo, hi = cost_range(look, BY_ID, owned)
    return {
        'look': look,
        'items': [BY_ID[i] for i in look.item_ids],
        'alternatives': [BY_ID[i] for i in look.alternative_item_ids if i in BY_ID],
        'cost_lo': lo, 'cost_hi': hi,
        'status': budget_status(lo, hi, budget),
    }

def fallback(profile, candidates, owned):
    def first(cat):
        return next((i['id'] for i in candidates if i['category'] == cat), None)
    top, bottom = first('top'), first('bottom')
    ids = [top, bottom] if top and bottom else [first('one-piece')]
    ids += [first('footwear'), first('bag'), first('jewellery')]
    ids = [i for i in ids if i]
    look = Look(title='Basic suggestion', item_ids=ids,
                colour_story='A simple combination that matches your occasion and style.',
                why_it_fits='Picked by rules because the AI was unavailable.',
                alternative_item_ids=[])
    return {'looks': [make_card(look, owned, profile.budget_inr)], 'error': None}

def recommend(profile):
    owned = {o for o in profile.owned_item_ids if o in BY_ID}
    candidates = shortlist(profile, ITEMS)
    cats = {i['category'] for i in candidates}
    if 'one-piece' not in cats and not {'top', 'bottom'} <= cats:
        return {'looks': [], 'error': 'No clothes match these choices. Try a different coverage or style.'}
    allowed = {i['id'] for i in candidates} | owned
    prompt = build_prompt(profile, candidates, [BY_ID[o] for o in owned])
    result = None
    for _ in range(2):  # first try + one retry
        result = call_llm(prompt, LookSet)
        if valid(result, allowed):
            break
        result = None
    if result is None:
        return fallback(profile, candidates, owned)
    return {'looks': [make_card(l, owned, profile.budget_inr) for l in result.looks],
            'error': None}