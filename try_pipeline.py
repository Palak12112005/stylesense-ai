from engine.models import InputProfile
from engine.pipeline import recommend

p = InputProfile(occasion='college', style='ethnic-fusion', fit='regular',
                 budget_inr=1000,
                 owned_item_ids=['bottom_jeans_straight', 'bag_tote_canvas'])
r = recommend(p)
for x in r['looks']:
    print(x['look'].title, [i['name'] for i in x['items']],
          x['cost_lo'], x['cost_hi'], x['status'])