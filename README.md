# StyleSense AI

An outfit suggestion app for Indian college students. Fill a short form
(occasion, style, fit, colours, budget) and get 2 complete looks with an
estimated cost.

**Live app:** https://stylesense-ai-gzchg6juq4dxrrl3zngshq.streamlit.app/

## How it works
1. Python filters a hand-made list of clothes by occasion, style and coverage.
2. Gemini AI picks items only from that shortlist and writes the explanation.
3. Python checks the AI's answer and adds up the cost, so prices are never invented.
4. If the AI fails, the app shows a rule-based "Basic suggestion".

## Tech
Python, Streamlit, Pydantic, Gemini API.

## Run locally
    pip install -r requirements.txt
    set GEMINI_API_KEY=your-key
    set GEMINI_MODEL=model-id
    streamlit run app.py

Prices are team estimates, not live prices.