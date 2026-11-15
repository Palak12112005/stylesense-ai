CATEGORIES = ['top', 'bottom', 'one-piece', 'footwear', 'bag', 'jewellery']

def shortlist(profile, items):
    def keep(i, need_style):
        if profile.occasion not in i['occasions']:
            return False
        if need_style and 'any' not in i['styles'] and profile.style not in i['styles']:
            return False
        is_clothing = i['category'] in ('top', 'bottom', 'one-piece')
        if is_clothing and profile.coverage == 'full' and i['coverage'] != 'full':
            return False
        return True

    out = [i for i in items if keep(i, True)]
    for c in CATEGORIES:
        if sum(1 for i in out if i['category'] == c) < 2:
            out += [i for i in items
                    if i['category'] == c and keep(i, False) and i not in out]
    return out