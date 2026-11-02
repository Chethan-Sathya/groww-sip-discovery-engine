import csv
from collections import Counter
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Groww SIP Discovery Engine", page_icon="🔎", layout="wide")
DATA = Path(__file__).parent / "data" / "validated_20_records.csv"

@st.cache_data
def load_data():
    with DATA.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

rows = load_data()
st.title("Groww SIP Continuity — Discovery Engine")
st.caption("Evidence-first product discovery | 20 curated public observations | Human-adjudicated themes")
st.warning("Exploratory, non-representative sample. Public statements are not verified investor outcomes; no verified 12-month active-SIP outcomes. Do not infer investor status from missing information.")
a, b, c = st.columns(3)
a.metric("Research observations", len(rows))
b.metric("Research themes", len(set(r["final_theme_adjudicated"] for r in rows)))
c.metric("Verified 12-month active SIPs", sum(r.get("month_12_active_SIP_confirmed","").strip().lower()=="yes" for r in rows))
tabs = st.tabs(["Evidence explorer", "Research questions", "Themes & QA", "Methodology"])
with tabs[0]:
    themes = sorted(set(r["final_theme_adjudicated"] for r in rows))
    selected = st.multiselect("Filter themes", themes, default=themes)
    search = st.text_input("Search evidence, source, behaviours and unmet needs")
    filtered = [r for r in rows if r["final_theme_adjudicated"] in selected and search.lower() in (" ".join(str(x) for x in r.values())).lower()]
    st.write(f"Showing {len(filtered)} observations")
    for r in filtered:
        with st.expander(f'{r["record_id"]} · {r["final_theme_adjudicated"]}'):
            st.write("**Observation:**", r["observation_paraphrase"])
            st.write("**Investor stage:**", r.get("first_time_status","Unknown"))
            st.write("**Reported behaviour:**", r.get("behavior_change","Not stated"))
            st.write("**Product relevance:**", r.get("platform_relevance","Not stated"))
            st.write("**Potential unmet need:**", r.get("unmet_need_hypothesis","Not stated"))
            st.write("**Limitations:**", r.get("evidence_limitations","Not stated"))
            st.markdown(f'**Source:** [Open original discussion]({r["source_url"]})')
with tabs[1]:
    questions = {
        "Q1 · Why start SIPs, and with what expectations?":"starting_motivation",
        "Q2 · How does behaviour change?":"behavior_change",
        "Q3 · Why pause, reduce, or stop?":"pause_stop_trigger",
        "Q4 · What do investors check?":"checking_behavior",
        "Q5 · What confuses them inside apps?":"app_confusion",
        "Q6 · Where do they seek outside help?":"external_help",
        "Q7 · Who continues versus drops off?":"continuation_status",
        "Q8 · How do segments differ?":"segment_evidence",
        "Q9 · What unmet needs appear?":"unmet_need_hypothesis",
    }
    selected_q = st.selectbox("Explore a research question", list(questions))
    field = questions[selected_q]
    st.caption("These are recorded observations and human interpretations, not statistically representative findings or causal answers.")
    for r in rows:
        val = r.get(field,"").strip()
        if val and val.lower() not in ("not stated","unknown","not established","not applicable"):
            with st.expander(f'{r["record_id"]} · {r["final_theme_adjudicated"]}'):
                st.write(val)
                st.write("Source context:",r["observation_paraphrase"])
                st.markdown(f'[Source discussion]({r["source_url"]})')
with tabs[2]:
    counts = Counter(r["final_theme_adjudicated"] for r in rows)
    st.bar_chart(dict(counts), horizontal=True)
    evaluated = [r for r in rows if r.get("initial_agreement") in ("Match","Mismatch")]
    matched = sum(r["initial_agreement"]=="Match" for r in evaluated)
    st.write(f"Historical AI/manual initial-label agreement: **{matched}/{len(evaluated)}**. This is not a blinded independent benchmark.")
    st.dataframe([{"ID":r["record_id"],"Original manual label":r["manual_label_original"],"AI label":r["AI_label_original"],"Agreement":r["initial_agreement"],"Human-adjudicated final theme":r["final_theme_adjudicated"]} for r in rows],hide_index=True)
with tabs[3]:
    st.markdown("""### Research workflow
1. Identify public SIP-related conversations and record original source links.
2. Paraphrase observations without inventing dates, investor attributes, or outcomes.
3. Apply preliminary thematic coding and manually adjudicate disagreements.
4. Explore nine discovery questions, with source-level traceability.
5. Validate hypotheses via user interviews before deciding product priorities.

**Limitations:** This is the publicly accessible evidence-review experience. It does not run live AI classification or call a model. The separate full local prototype supports optional AI providers; its provider keys are not published. This dataset is a curated convenience sample, not representative evidence of SIP continuation at month 12.
""")
st.download_button("Download validated evidence CSV", DATA.read_bytes(), "groww_sip_validated_20.csv", "text/csv")
