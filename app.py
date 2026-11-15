import streamlit as st
from engine.models import InputProfile
from engine.pipeline import recommend, OWNABLE

st.set_page_config(page_title='StyleSense AI', page_icon='👗')
st.title('StyleSense AI')
st.caption('Your style. Your comfort. Your choice.')

def show_result(result):
    if result.get('error'):
        st.error(result['error'])
        return
    looks = result['looks']
    if looks[0]['look'].title == 'Basic suggestion':
        st.info('Basic suggestion: AI was unavailable, so this look is rule-based.')
    tabs = st.tabs([f'Look {n + 1}' for n in range(len(looks))])
    for tab, card in zip(tabs, looks):
        with tab:
            look = card['look']
            st.subheader(look.title)
            for item in card['items']:
                st.write(f"• {item['name']} ({item['category']})")
            st.write('**Colour story:** ' + look.colour_story)
            st.write('**Why it fits:** ' + look.why_it_fits)
            st.write(f"**Estimated cost:** ₹{card['cost_lo']} to ₹{card['cost_hi']} (estimated, not live prices)")
            if card['status'] == 'fits':
                st.success('Fits your budget')
            elif card['status'] == 'tight':
                st.warning('Tight: may fit, depends on what you buy')
            else:
                st.error('Over budget')
            if card['alternatives']:
                with st.expander('Alternatives'):
                    for item in card['alternatives']:
                        st.write(f"• {item['name']}")

with st.form('profile'):
    occasion = st.selectbox('Occasion', ['college', 'interview', 'party', 'festival'])
    style = st.selectbox('Style', ['ethnic', 'western', 'ethnic-fusion', 'casual-minimal'])
    fit = st.select_slider('Fit', ['relaxed', 'regular', 'fitted'], value='regular')
    coverage = st.radio('Coverage', ['no-preference', 'moderate', 'full'], horizontal=True)
    colours = st.multiselect('Colours you like', ['maroon', 'white', 'black', 'beige', 'teal', 'mustard'])
    budget = st.number_input('Budget (₹)', min_value=0, max_value=20000, value=1000, step=100)
    owned = st.multiselect('Already own', list(OWNABLE))
    go = st.form_submit_button('Style me')

if go:
    profile = InputProfile(occasion=occasion, style=style, fit=fit,
                           coverage=coverage, colours=colours,
                           budget_inr=int(budget),
                           owned_item_ids=[OWNABLE[n] for n in owned])
    with st.spinner('Styling...'):
        try:
            st.session_state['result'] = recommend(profile)
        except Exception:
            st.session_state['result'] = {'looks': [], 'error': 'Something went wrong. Please try again.'}

if 'result' in st.session_state:
    show_result(st.session_state['result'])