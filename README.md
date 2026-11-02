# Groww SIP Continuity — AI Discovery Engine

A public, source-linked product research prototype for investigating why first-time mutual-fund investors do or do not continue SIPs.

The app uses a curated, manually adjudicated set of 20 public-conversation observations and a nine-question evidence index. It shows source links, limitations, theme distribution and research gaps. Optional live AI analysis requires an API key and does not run automatically.

## Deploy

1. Open https://share.streamlit.io/ and create an app from this GitHub repository.
2. Select branch `main` and entrypoint `app.py`.
3. Set the visibility to public, and share the generated `*.streamlit.app` URL with mentors.
4. For optional live AI features, add `GROQ_API_KEY` through Streamlit Secrets rather than GitHub.

## Research limitations

This 20-record purposive sample does **not** represent the incidence of issues across all investors and does not contain verified 12-month active SIP outcomes. Source authors, posting dates, and full original context must be manually reverified before making published factual claims. Never treat a failed instalment as proof that the user stopped investing. No specific funds or stocks are recommended.
