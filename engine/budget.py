def cost_range(look, by_id, owned):
    lo = hi = 0
    for iid in look.item_ids:
        if iid in owned:
            continue  # already owned = free
        a, b = by_id[iid]['price_band_inr']
        lo += a
        hi += b
    return lo, hi

def budget_status(lo, hi, budget):
    if hi <= budget:
        return 'fits'
    if lo <= budget:
        return 'tight'
    return 'over'