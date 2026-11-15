import json
from engine.models import InputProfile, LookSet
from engine.rules import shortlist
from engine.llm import call_llm, build_prompt

items = json.load(open('data/items.json', encoding='utf-8'))
p = InputProfile(occasion='college', style='ethnic-fusion', fit='regular', budget_inr=1000)
c = shortlist(p, items)
print(call_llm(build_prompt(p, c, []), LookSet))