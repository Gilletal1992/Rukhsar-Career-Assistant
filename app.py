import json
from datetime import date, datetime, timedelta
from pathlib import Path

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

st.set_page_config(
    page_title="Rukhsar Academic + Church + Finnish Assistant",
    page_icon="🌿",
    layout="wide",
)

BASE = Path(__file__).parent
SKILLS = ["Reading", "Writing", "Listening", "Speaking", "Grammar", "Vocabulary"]
PROFILE = {
    "name": "Rukhsar Zakria",
    "role": "Doctoral researcher / PhD student in Biblical Studies, University of Eastern Finland",
    "location": "Finland / Helsinki area",
    "finnish": "Beginner",
    "target": "Independent Finnish / eventual YKI",
    "course": "26S2F · Konepajan aikuislukio · Myllypuro",
    "research": "Gendered metaphors of suffering in the Book of Hosea and their contemporary reception in the Pakistani Christian context.",
    "academic_focus": "Biblical Studies · Hebrew Bible / Old Testament · Hosea · prophetic literature · biblical metaphors · gender and biblical interpretation · reception studies · contextual theology · Christianity in Pakistan · religion, migration and minority Christianity",
    "church_focus": "Church and parish work · ecumenical organisations · Christian education · international/intercultural church work · integration/community projects · outreach · faith-based NGOs · project/programme coordination",
}

st.markdown(
    """
    <style>
    .stApp {background:linear-gradient(180deg,#061429 0%,#081A34 100%);}
    section[data-testid="stSidebar"] {background:#071831;border-right:1px solid #17345E;}
    div[data-testid="stMetric"] {background:#0D2345;border:1px solid #183C69;padding:14px 16px;border-radius:13px;box-shadow:0 8px 24px rgba(0,0,0,.16);}
    div[data-testid="stMetric"] label {color:#AFC3E3 !important;font-weight:600;}
    div[data-testid="stMetricValue"] {color:#F5F8FF !important;}
    .dashboard-card {background:#0D2345;border:1px solid #183C69;border-radius:14px;padding:14px 16px 12px;margin-bottom:14px;box-shadow:0 8px 24px rgba(0,0,0,.14);}
    .dashboard-title {font-size:16px;font-weight:750;color:#F5F8FF;margin-bottom:6px;}
    .dashboard-sub {font-size:12px;color:#AFC3E3;margin-bottom:8px;}
    .capacity-note {padding:10px 12px;border-radius:10px;background:#102B55;border:1px solid #1E4D82;color:#DDEBFF;margin-bottom:10px;}
    .profile-box {background:#0D2345;border:1px solid #183C69;border-radius:14px;padding:16px;margin-bottom:14px;}
    .ring-wrap{display:flex;justify-content:center;align-items:center;padding:8px 0 4px;}
    .ring{width:140px;height:140px;border-radius:50%;display:flex;align-items:center;justify-content:center;position:relative;}
    .ring:after{content:'';position:absolute;width:104px;height:104px;border-radius:50%;background:#0D2345;}
    .ring-value{position:relative;z-index:2;font-size:30px;font-weight:800;color:#F5F8FF;}
    .meter-shell{height:85px;overflow:hidden;position:relative;margin-top:8px;}
    .meter{width:170px;height:170px;border-radius:50%;margin:auto;position:relative;}
    .meter:after{content:'';position:absolute;width:122px;height:122px;border-radius:50%;background:#0D2345;left:24px;top:24px;}
    .meter-label{position:relative;text-align:center;margin-top:-35px;font-size:25px;font-weight:800;color:#F5F8FF;z-index:4;}
    .donut-wrap{display:flex;justify-content:center;align-items:center;padding:6px 0;}
    .donut{width:150px;height:150px;border-radius:50%;position:relative;}
    .donut:after{content:'';position:absolute;width:92px;height:92px;border-radius:50%;background:#0D2345;left:29px;top:29px;}
    hr {border-color:#17345E !important;}
    </style>
    """,
    unsafe_allow_html=True,
)


def load_json(path, default):
    try:
        return json.loads((BASE / path).read_text(encoding="utf-8"))
    except Exception:
        return default


def load_applications():
    return load_json("data/applications_2026.json", [])


def load_opportunities():
    return load_json(
        "data/opportunities_2026.json",
        {"church": [], "academic": [], "funding": [], "other": []},
    )


def load_research_radar():
    return load_json("data/research_radar_2026.json", {"updated": "Not listed", "items": []})


def application_rank(app):
    text = (app.get("status", "") + " " + app.get("result", "")).lower()
    if any(x in text for x in ["unsuccessful", "rejected", "not selected", "not chosen"]):
        return 9
    if "interview" in text:
        return 0
    if any(x in text for x in ["offer", "accepted", "selected", "shortlist"]):
        return 1
    if any(x in text for x in ["waiting", "reply", "review"]):
        return 2
    if "applied" in text:
        return 3
    return 5


def status_badge(app):
    rank = application_rank(app)
    if rank == 9:
        return "🔴 Not selected"
    if rank == 0:
        return "🎤 Interview"
    text = (app.get("status", "") + " " + app.get("result", "")).lower()
    if any(x in text for x in ["offer", "accepted", "selected"]):
        return "🏆 Accepted / selected"
    if "shortlist" in text:
        return "🟢 Shortlisted"
    if any(x in text for x in ["reply", "email"]):
        return "📧 Email reply"
    if "waiting" in text:
        return "⏳ Waiting"
    if "applied" in text:
        return "✅ Applied"
    return "⚪ " + app.get("status", "Not applied")


def level_from_score(score):
    if score < 35:
        return "A1.1"
    if score < 50:
        return "A1.2"
    if score < 62:
        return "A1.3 / early A2"
    if score < 72:
        return "A2"
    if score < 82:
        return "A2.2 / early B1"
    if score < 90:
        return "B1"
    return "B1+ / approaching B2"


def speaking_score(text):
    if not text:
        return 0, 0, 0, 0
    words = text.split()
    lower = text.lower()
    markers = [
        "minä", "olen", "asun", "suomessa", "helsingissä", "opiskelen", "suomea",
        "yliopisto", "tutkimus", "kirja", "kirkko", "ystävä", "perhe", "ja", "mutta", "koska",
    ]
    hits = sum(1 for x in markers if x in lower)
    length = min(100, len(words) * 4)
    finnish = min(100, 25 + hits * 7)
    variety = min(100, len(set(w.strip(".,!?").lower() for w in words)) * 5)
    overall = round(length * 0.35 + finnish * 0.40 + variety * 0.25)
    return overall, length, finnish, variety


cookie_manager = stx.CookieManager(key="rukhsar_cookie_manager")


def cookie_json(name):
    raw = cookie_manager.get(cookie=name)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def save_cookie_json(name, value, key_suffix="save"):
    cookie_manager.set(
        name,
        json.dumps(value),
        expires_at=datetime.now() + timedelta(days=3650),
        key=f"{name}_{key_suffix}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
    )


def ensure_state():
    today = date.today().isoformat()
    if "finnish_history" not in st.session_state:
        st.session_state.finnish_history = cookie_json("rukhsar_finnish_progress")
    if st.session_state.get("daily_date") != today:
        saved = st.session_state.finnish_history.get(today, {})
        st.session_state.daily_date = today
        st.session_state.daily_scores = saved.get("scores", {x: 0 for x in SKILLS})
        st.session_state.daily_done = saved.get("done", {x: False for x in SKILLS})
        st.session_state.daily_attempts = saved.get("attempts", {x: 0 for x in SKILLS})
        st.session_state.daily_points = saved.get("points", {x: 0 for x in SKILLS})
        st.session_state.daily_capacity = saved.get("capacity", "Standard · 2 rounds per skill")
    if "career_history" not in st.session_state:
        st.session_state.career_history = cookie_json("rukhsar_career_progress")
    if "opportunity_pipeline" not in st.session_state:
        st.session_state.opportunity_pipeline = cookie_json("rukhsar_opportunity_pipeline")


def add_skill_result(skill, score):
    st.session_state.daily_attempts[skill] = st.session_state.daily_attempts.get(skill, 0) + 1
    st.session_state.daily_points[skill] = st.session_state.daily_points.get(skill, 0) + score
    st.session_state.daily_scores[skill] = round(
        st.session_state.daily_points[skill] / st.session_state.daily_attempts[skill]
    )
    st.session_state.daily_done[skill] = True
    save_finnish()


def save_finnish():
    today = date.today().isoformat()
    history = st.session_state.get("finnish_history", {})
    completed = sum(st.session_state.daily_attempts.values())
    history[today] = {
        "scores": dict(st.session_state.daily_scores),
        "done": dict(st.session_state.daily_done),
        "attempts": dict(st.session_state.daily_attempts),
        "points": dict(st.session_state.daily_points),
        "capacity": st.session_state.get("daily_capacity", "Standard · 2 rounds per skill"),
        "tasks_completed": completed,
        "overall": round(sum(st.session_state.daily_scores.values()) / len(SKILLS)),
    }
    st.session_state.finnish_history = history
    save_cookie_json("rukhsar_finnish_progress", history, today)


def snapshot_career():
    today = date.today().isoformat()
    apps = load_applications()
    opps = load_opportunities()
    pipeline = st.session_state.get("opportunity_pipeline", {})
    snapshot = {
        "church": len(opps.get("church", [])),
        "academic": len(opps.get("academic", [])),
        "funding": len(opps.get("funding", [])),
        "other": len(opps.get("other", [])),
        "applications": len(apps) + sum(1 for x in pipeline.values() if x.get("stage") != "Not applied"),
        "waiting": sum("waiting" in a.get("status", "").lower() for a in apps),
        "interviews": sum("interview" in a.get("status", "").lower() for a in apps)
        + sum(x.get("stage") == "Interview" for x in pipeline.values()),
        "accepted": sum(application_rank(a) == 1 for a in apps)
        + sum(x.get("stage") == "Accepted / Selected" for x in pipeline.values()),
        "rejected": sum(application_rank(a) == 9 for a in apps)
        + sum(x.get("stage") == "Rejected / Not selected" for x in pipeline.values()),
    }
    history = st.session_state.get("career_history", {})
    if history.get(today) != snapshot:
        history[today] = snapshot
        st.session_state.career_history = history
        save_cookie_json("rukhsar_career_progress", history, today)


def range_days(label):
    return {"7 days": 7, "30 days": 30, "3 months": 90, "1 year": 365, "All time": None}[label]


def filter_history(history, days):
    rows = []
    cutoff = date.today() - timedelta(days=days - 1) if days else None
    for day, data in sorted(history.items()):
        try:
            d = datetime.strptime(day, "%Y-%m-%d").date()
        except Exception:
            continue
        if cutoff and d < cutoff:
            continue
        rows.append((day, data))
    return rows


def skill_df(rows, skill):
    out = []
    for day, data in rows:
        score = data.get("scores", {}).get(skill)
        if score is not None:
            out.append({"Date": pd.to_datetime(day), "Score": score})
    return pd.DataFrame(out)


def card_title(title, subtitle=""):
    st.markdown(
        f"<div class='dashboard-card'><div class='dashboard-title'>{title}</div><div class='dashboard-sub'>{subtitle}</div>",
        unsafe_allow_html=True,
    )


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def ring(value):
    value = max(0, min(100, int(value)))
    deg = round(value * 3.6)
    st.markdown(
        f"<div class='ring-wrap'><div class='ring' style='background:conic-gradient(#55D6BE 0deg {deg}deg,#213B67 {deg}deg 360deg)'><div class='ring-value'>{value}%</div></div></div>",
        unsafe_allow_html=True,
    )


def meter(value, label):
    value = max(0, min(100, int(value)))
    deg = round(value * 1.8)
    st.markdown(
        f"<div class='meter-shell'><div class='meter' style='background:conic-gradient(from 270deg,#55D6BE 0deg {deg}deg,#213B67 {deg}deg 180deg,transparent 180deg 360deg)'></div></div><div class='meter-label'>{value}%</div><div class='dashboard-sub' style='text-align:center'>{label}</div>",
        unsafe_allow_html=True,
    )


def donut(values, labels):
    total = sum(values) or 1
    colors = ["#55D6BE", "#FFBE55", "#FF7285", "#7BCFFF"]
    start = 0
    parts = []
    for i, value in enumerate(values):
        end = start + (value / total) * 360
        parts.append(f"{colors[i % len(colors)]} {start:.1f}deg {end:.1f}deg")
        start = end
    st.markdown(
        f"<div class='donut-wrap'><div class='donut' style='background:conic-gradient({','.join(parts)})'></div></div>",
        unsafe_allow_html=True,
    )
    st.caption(" · ".join(f"{label}: {value}" for label, value in zip(labels, values)))


def line_chart(df, y="Score", height=180, min_y=None, max_y=None):
    if df.empty:
        st.caption("No history yet for this period.")
        return
    kwargs = {"height": height}
    if min_y is not None:
        kwargs["y_min"] = min_y
    if max_y is not None:
        kwargs["y_max"] = max_y
    st.line_chart(df.set_index("Date"), y=y, use_container_width=True, **kwargs)


def link_table(rows):
    if not rows:
        st.info("No verified items have been added yet.")
        return
    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
        column_config={"Official Link": st.column_config.LinkColumn("Official Link", display_text="Open")},
    )


PIPELINE_STAGES = [
    "Not applied",
    "Applied",
    "Email reply received",
    "Interview",
    "Shortlisted",
    "Accepted / Selected",
    "Rejected / Not selected",
]
PIPELINE_BADGES = {
    "Not applied": "⚪ Not applied",
    "Applied": "✅ Applied",
    "Email reply received": "📧 Email reply",
    "Interview": "🎤 Interview",
    "Shortlisted": "🟢 Shortlisted",
    "Accepted / Selected": "🏆 Accepted / Selected",
    "Rejected / Not selected": "🔴 Rejected / Not selected",
}


def opportunity_key(kind, item):
    link = (item.get("link") or "").strip()
    title = item.get("title") or item.get("position") or item.get("programme") or "Untitled"
    owner = item.get("organisation") or item.get("institution") or item.get("funder") or ""
    return f"{kind}|{link or (title + '|' + owner).lower()}"


def opportunity_stage(kind, item):
    rec = st.session_state.get("opportunity_pipeline", {}).get(opportunity_key(kind, item), {})
    return rec.get("stage", "Not applied")


def save_opportunity_stage(kind, item, stage, note=""):
    data = st.session_state.get("opportunity_pipeline", {})
    key = opportunity_key(kind, item)
    previous = data.get(key, {})
    history = previous.get("history", [])
    history.append(
        {
            "stage": stage,
            "note": note.strip(),
            "updated": datetime.now().isoformat(timespec="seconds"),
        }
    )
    data[key] = {
        "kind": kind,
        "title": item.get("title") or item.get("position") or item.get("programme") or "Untitled",
        "organisation": item.get("organisation") or item.get("institution") or item.get("funder") or "",
        "country": item.get("country", ""),
        "deadline": item.get("deadline", "Not listed"),
        "link": item.get("link") or "",
        "stage": stage,
        "note": note.strip(),
        "applied_date": previous.get("applied_date") or (date.today().isoformat() if stage == "Applied" else ""),
        "updated": datetime.now().isoformat(timespec="seconds"),
        "history": history,
    }
    st.session_state.opportunity_pipeline = data
    save_cookie_json("rukhsar_opportunity_pipeline", data, "pipeline")


def render_opportunity_tracker(kind, items):
    if not items:
        return
    st.markdown("### 🧭 My status tracker")
    st.caption("Update the application stage or add a note. This history is kept separately from Finnish progress.")
    counts = {stage: 0 for stage in PIPELINE_STAGES}
    for item in items:
        counts[opportunity_stage(kind, item)] += 1
    a, b, c, d, e = st.columns(5)
    a.metric("Applied", counts["Applied"])
    b.metric("Email replies", counts["Email reply received"])
    c.metric("Interviews", counts["Interview"])
    d.metric("Accepted", counts["Accepted / Selected"])
    e.metric("Rejected", counts["Rejected / Not selected"])

    for idx, item in enumerate(items):
        title = item.get("title") or item.get("position") or item.get("programme") or "Untitled"
        org = item.get("organisation") or item.get("institution") or item.get("funder") or ""
        stage = opportunity_stage(kind, item)
        with st.expander(f"{PIPELINE_BADGES.get(stage, stage)} · {title} · {org}"):
            keybase = f"pipe_{kind}_{idx}"
            existing = st.session_state.get("opportunity_pipeline", {}).get(opportunity_key(kind, item), {})
            note = st.text_input(
                "Optional note / reply detail",
                value=existing.get("note", ""),
                key=keybase + "_note",
            )
            selected = st.selectbox(
                "Current stage",
                PIPELINE_STAGES,
                index=PIPELINE_STAGES.index(stage),
                format_func=lambda x: PIPELINE_BADGES[x],
                key=keybase + "_stage",
            )
            if st.button("Save status", key=keybase + "_save", use_container_width=True):
                save_opportunity_stage(kind, item, selected, note)
                st.success(f"Saved: {PIPELINE_BADGES[selected]}")
                st.rerun()


def opportunity_rows(kind, items):
    rows = []
    for item in items:
        common = {
            "Opening date": item.get("start_date", "Not listed"),
            "Deadline": item.get("deadline", "Not listed"),
            "Fit": f"{item.get('fit', 0)}% {item.get('fit_label', '')}" if item.get("fit") is not None else "Needs verification",
            "Recommended action": item.get("status", "Needs verification"),
            "My stage": PIPELINE_BADGES.get(opportunity_stage(kind, item), opportunity_stage(kind, item)),
            "Official Link": item.get("link"),
        }
        if kind == "church":
            common.update({
                "Position": item.get("title", "Not listed"),
                "Organisation": item.get("organisation", "Not listed"),
                "City / Country": " · ".join(x for x in [item.get("city", ""), item.get("country", "")] if x) or "Not listed",
                "Language": item.get("language", "Not listed"),
                "Employment type": item.get("employment_type", "Not listed"),
                "Contact": item.get("contact", "Not listed"),
            })
        elif kind == "academic":
            common.update({
                "Position": item.get("title", "Not listed"),
                "Institution": item.get("institution", "Not listed"),
                "Department / Group": item.get("department", item.get("group", "Not listed")),
                "Country": item.get("country", "Not listed"),
                "Duration": item.get("duration", "Not listed"),
                "Salary": item.get("salary", "Not listed"),
                "Contact / PI": item.get("contact", "Not listed"),
            })
        elif kind == "funding":
            common.update({
                "Programme / Call": item.get("title", item.get("programme", "Not listed")),
                "Funder": item.get("funder", "Not listed"),
                "Amount / Duration": item.get("amount", "Not listed"),
                "Eligibility": item.get("eligibility", "Not listed"),
                "Career stage": item.get("career_stage", "Not listed"),
                "Contact": item.get("contact", "Not listed"),
            })
        else:
            common.update({
                "Opportunity": item.get("title", "Not listed"),
                "Organisation": item.get("organisation", "Not listed"),
                "Type": item.get("type", "Not listed"),
                "Country": item.get("country", "Not listed"),
            })
        rows.append(common)
    return rows


ensure_state()
opps = load_opportunities()
apps = load_applications()
research_radar = load_research_radar()
snapshot_career()

st.title("🌿 Rukhsar Academic + Church + Finnish Assistant")
st.caption("Biblical Studies research · church/ecumenical career · Finnish development · funding · applications")

section = st.sidebar.radio(
    "Navigation",
    [
        "📊 Command Centre",
        "🇫🇮 Daily Finnish Trainer",
        "📈 Finnish Progress",
        "⛪ Church & Ecumenical",
        "🎓 Academic Jobs",
        "💶 Funding & Grants",
        "🌍 Other Opportunities",
        "📋 My Applications",
        "📊 Career Progress",
        "📚 Research Radar",
        "🧬 Rukhsar's Profile",
    ],
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Rukhsar Zakria**")
st.sidebar.write("PhD · Biblical Studies · UEF")
st.sidebar.caption("Church/community opportunities receive strong priority while Finnish develops.")

if section == "📊 Command Centre":
    daily = round(sum(st.session_state.daily_scores.values()) / len(SKILLS))
    pipeline = st.session_state.get("opportunity_pipeline", {})
    applied_count = len(apps) + sum(1 for x in pipeline.values() if x.get("stage") != "Not applied")
    interviews = sum(application_rank(a) == 0 for a in apps) + sum(x.get("stage") == "Interview" for x in pipeline.values())
    waiting = sum("waiting" in a.get("status", "").lower() for a in apps) + sum(x.get("stage") in ["Applied", "Email reply received", "Shortlisted"] for x in pipeline.values())

    a, b, c, d, e, f = st.columns(6)
    a.metric("Finnish level", level_from_score(daily) if daily else PROFILE["finnish"])
    b.metric("Today's Finnish", f"{daily}/100")
    c.metric("Applications", applied_count)
    d.metric("Church", len(opps.get("church", [])))
    e.metric("Academic", len(opps.get("academic", [])))
    f.metric("Funding", len(opps.get("funding", [])))

    left, right = st.columns([2, 1])
    with left:
        st.subheader("📚 Biblical Studies Research Radar")
        st.caption(f"Tailored research intelligence · Updated {research_radar.get('updated', 'Not listed')}")
        radar_items = research_radar.get("items", [])[:3]
        if radar_items:
            cols = st.columns(len(radar_items))
            for col, item in zip(cols, radar_items):
                with col:
                    with st.container(border=True):
                        st.caption(f"{item.get('category', 'Research')} · {item.get('date', '')}")
                        st.markdown(f"**{item.get('headline', 'Untitled')}**")
                        st.write(item.get("summary", item.get("why_it_matters", "")))
                        if item.get("why_it_matters"):
                            st.caption("Why it matters: " + item.get("why_it_matters"))
                        st.caption("Source: " + item.get("source", "Not listed"))
                        if item.get("link"):
                            st.link_button("Open source ↗", item["link"], use_container_width=True)
        else:
            st.info("Research Radar is ready. Verified publications, conferences and research developments can be added by the daily updater later.")
    with right:
        st.subheader("📋 Current pipeline")
        p1, p2 = st.columns(2)
        p1.metric("Waiting", waiting)
        p2.metric("Interviews", interviews)
        st.info("Church/community roles are prioritized first, followed by academic opportunities and PhD funding.")

elif section == "🇫🇮 Daily Finnish Trainer":
    st.header("🇫🇮 Adaptive Daily Finnish Trainer")
    st.markdown(
        "<div class='capacity-note'>Choose today's study capacity. You can complete multiple rounds in every skill and continue beyond the suggested target. The daily score uses all completed rounds.</div>",
        unsafe_allow_html=True,
    )
    capacity_map = {
        "Light · 1 round per skill": 1,
        "Standard · 2 rounds per skill": 2,
        "Focused · 3 rounds per skill": 3,
        "Intensive · 5 rounds per skill": 5,
    }
    previous_capacity = st.session_state.get("daily_capacity", "Standard · 2 rounds per skill")
    default_index = list(capacity_map).index(previous_capacity) if previous_capacity in capacity_map else 1
    capacity_label = st.selectbox("Today's study capacity", list(capacity_map.keys()), index=default_index)
    target_rounds = capacity_map[capacity_label]
    st.session_state.daily_capacity = capacity_label
    completed = sum(st.session_state.daily_attempts.values())
    target_total = target_rounds * len(SKILLS)
    a, b, c = st.columns(3)
    a.metric("Tasks completed today", completed)
    b.metric("Suggested target", target_total)
    c.metric("Completion", f"{min(100, round(100 * completed / max(1, target_total)))}%")
    st.progress(min(1.0, completed / max(1, target_total)))

    reading_bank = [
        ("Rukhsar asuu Suomessa. Hän opiskelee suomea ja tekee väitöskirjaa. Illalla hän lukee kirjaa.", "Mitä Rukhsar tekee?", ["Hän tekee väitöskirjaa.", "Hän ajaa bussia.", "Hän työskentelee kaupassa.", "Hän nukkuu koko päivän."], "Hän tekee väitöskirjaa."),
        ("Anna menee sunnuntaina kirkkoon. Messun jälkeen hän juo kahvia ystävien kanssa.", "Minne Anna menee sunnuntaina?", ["Kirjastoon", "Kirkkoon", "Kauppaan", "Asemalle"], "Kirkkoon"),
        ("Mikko opiskelee yliopistossa. Hän menee aamulla bussilla kampukselle ja palaa kotiin iltapäivällä.", "Millä Mikko menee kampukselle?", ["Junalla", "Bussilla", "Autolla", "Kävellen"], "Bussilla"),
        ("Laura käy lauantaina torilla. Hän ostaa omenoita, perunoita ja leipää.", "Missä Laura käy?", ["Torilla", "Koulussa", "Työssä", "Kirkossa"], "Torilla"),
        ("Maria matkustaa perjantaina Joensuuhun junalla. Hän palaa Helsinkiin sunnuntaina.", "Milloin Maria palaa Helsinkiin?", ["Perjantaina", "Lauantaina", "Sunnuntaina", "Maanantaina"], "Sunnuntaina"),
    ]
    listen_bank = [
        ("Tänään menen iltapäivällä kirjastoon opiskelemaan suomea.", "Minne henkilö menee?", ["Kauppaan", "Kirjastoon", "Kouluun", "Kotiin"], "Kirjastoon"),
        ("Sunnuntaina tapaamme ystäviä kirkon jälkeen kahvilassa kello kaksi.", "Missä he tapaavat?", ["Kahvilassa", "Asemalla", "Puistossa", "Koulussa"], "Kahvilassa"),
        ("Huomenna aamulla menen lääkärille ja sen jälkeen yliopistolle.", "Minne henkilö menee ensin?", ["Yliopistolle", "Lääkärille", "Kauppaan", "Kotiin"], "Lääkärille"),
        ("Bussi lähtee pysäkiltä kello kahdeksan kaksikymmentä ja saapuu keskustaan yhdeksältä.", "Mihin bussi saapuu?", ["Lentokentälle", "Keskustaan", "Kotiin", "Kouluun"], "Keskustaan"),
        ("Illalla teen ruokaa, luen kirjaa ja harjoittelen suomea.", "Mitä henkilö tekee illalla?", ["Matkustaa", "Tekee ruokaa", "Menee töihin", "Nukkuu"], "Tekee ruokaa"),
    ]
    grammar_bank = [
        (["Minä juon kahvi.", "Minä juon kahvia.", "Minä juon kahvin."], "Minä juon kahvia."),
        (["Minulla ei ole auto.", "Minulla ei ole autoa.", "Minulla ei ole auton."], "Minulla ei ole autoa."),
        (["Syön kaksi omenaa.", "Syön kaksi omenat.", "Syön kaksi omenan."], "Syön kaksi omenaa."),
        (["Menen kirkkoon.", "Menen kirkossa.", "Menen kirkosta."], "Menen kirkkoon."),
        (["Olen yliopistossa.", "Olen yliopistoon.", "Olen yliopistosta."], "Olen yliopistossa."),
    ]
    vocab_sets = [
        (["maito", "juna", "leipä", "kahvi", "opettaja", "omena"], {"maito", "leipä", "kahvi", "omena"}, "Select food/drink words:"),
        (["bussi", "juna", "omena", "metro", "kirja", "pyörä"], {"bussi", "juna", "metro", "pyörä"}, "Select transport words:"),
        (["aamu", "ilta", "kauppa", "yö", "päivä", "auto"], {"aamu", "ilta", "yö", "päivä"}, "Select time-of-day words:"),
        (["lääkäri", "sairaanhoitaja", "banaani", "opettaja", "tutkija", "metro"], {"lääkäri", "sairaanhoitaja", "opettaja", "tutkija"}, "Select professions:"),
        (["kirkko", "raamattu", "juna", "seurakunta", "rukous", "kahvi"], {"kirkko", "raamattu", "seurakunta", "rukous"}, "Select church/religion words:"),
    ]

    tabs = st.tabs(["📖 Reading", "✍️ Writing", "🎧 Listening", "🎙️ Speaking", "🧩 Grammar", "🧠 Vocabulary"])
    day_seed = date.today().toordinal()

    with tabs[0]:
        round_no = st.session_state.daily_attempts.get("Reading", 0) + 1
        item = reading_bank[(day_seed + round_no - 1) % len(reading_bank)]
        st.caption(f"Round {round_no} · Continue as long as you want.")
        st.write("**Teksti:** " + item[0])
        ans = st.radio(item[1], item[2], index=None, key=f"read_{date.today()}_{round_no}")
        if st.button("Submit reading round", key=f"read_btn_{round_no}"):
            add_skill_result("Reading", 100 if ans == item[3] else 0)
            st.rerun()

    with tabs[1]:
        round_no = st.session_state.daily_attempts.get("Writing", 0) + 1
        prompts = [
            "Write 3–4 Finnish sentences about your morning.",
            "Write 4–5 Finnish sentences about your studies.",
            "Write 4–5 sentences about your weekend plans.",
            "Describe your home in 5 Finnish sentences.",
            "Write a short Finnish message to a friend about meeting tomorrow.",
        ]
        st.caption(f"Round {round_no}")
        text = st.text_area(prompts[(day_seed + round_no - 1) % len(prompts)], key=f"write_{round_no}")
        if st.button("Submit writing round", key=f"write_btn_{round_no}"):
            words = len(text.split())
            sentences = text.count(".") + text.count("!") + text.count("?")
            score = min(100, words * 3 + sentences * 10)
            add_skill_result("Writing", score)
            st.rerun()

    with tabs[2]:
        round_no = st.session_state.daily_attempts.get("Listening", 0) + 1
        item = listen_bank[(day_seed + round_no - 1) % len(listen_bank)]
        st.caption(f"Round {round_no}")
        sentence = item[0].replace("'", "\\'")
        components.html(
            f'''<button onclick="speechSynthesis.cancel();let u=new SpeechSynthesisUtterance('{sentence}');u.lang='fi-FI';u.rate=.82;speechSynthesis.speak(u);">▶ Play Finnish</button>''',
            height=45,
        )
        ans = st.radio(item[1], item[2], index=None, key=f"listen_{round_no}")
        if st.button("Submit listening round", key=f"listen_btn_{round_no}"):
            add_skill_result("Listening", 100 if ans == item[3] else 0)
            st.rerun()

    with tabs[3]:
        round_no = st.session_state.daily_attempts.get("Speaking", 0) + 1
        prompts = [
            "Kerro itsestäsi: kuka olet, missä asut ja mitä opiskelet?",
            "Kerro tavallisesta päivästäsi aamusta iltaan.",
            "Kerro viikonlopustasi: minne menet ja mitä teet?",
            "Kuvaile kotiasi ja asuinaluettasi.",
            "Kerro opiskelustasi ja miksi opiskelet suomea.",
        ]
        st.caption(f"Round {round_no}")
        st.write("Speak for 30–60 seconds: *" + prompts[(day_seed + round_no - 1) % len(prompts)] + "*")
        spoken = speech_to_text(
            language="fi",
            start_prompt="🎙️ Start speaking Finnish",
            stop_prompt="⏹️ Stop & transcribe",
            just_once=False,
            use_container_width=False,
            key=f"rukhsar_finnish_asr_{round_no}",
        )
        if spoken:
            st.success(spoken)
            score, length, finnish, variety = speaking_score(spoken)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Round score", f"{score}/100")
            c2.metric("Length", f"{length}/100")
            c3.metric("Finnish markers", f"{finnish}/100")
            c4.metric("Vocabulary", f"{variety}/100")
            if st.button("Save speaking round", key=f"speak_btn_{round_no}"):
                add_skill_result("Speaking", score)
                st.rerun()

    with tabs[4]:
        round_no = st.session_state.daily_attempts.get("Grammar", 0) + 1
        item = grammar_bank[(day_seed + round_no - 1) % len(grammar_bank)]
        st.caption(f"Round {round_no}")
        ans = st.radio("Choose correctly:", item[0], index=None, key=f"gram_{round_no}")
        if st.button("Submit grammar round", key=f"gram_btn_{round_no}"):
            add_skill_result("Grammar", 100 if ans == item[1] else 0)
            st.info(f"Correct answer: {item[1]}")
            st.rerun()

    with tabs[5]:
        round_no = st.session_state.daily_attempts.get("Vocabulary", 0) + 1
        item = vocab_sets[(day_seed + round_no - 1) % len(vocab_sets)]
        st.caption(f"Round {round_no}")
        ans = st.multiselect(item[2], item[0], key=f"vocab_{round_no}")
        if st.button("Submit vocabulary round", key=f"vocab_btn_{round_no}"):
            chosen = set(ans)
            raw = max(0, len(chosen & item[1]) - len(chosen - item[1]))
            score = round(100 * raw / len(item[1]))
            add_skill_result("Vocabulary", score)
            st.rerun()

    st.markdown("---")
    cols = st.columns(6)
    for i, skill in enumerate(SKILLS):
        cols[i].metric(skill, f"{st.session_state.daily_scores[skill]}/100", f"{st.session_state.daily_attempts[skill]} rounds")
    overall = round(sum(st.session_state.daily_scores.values()) / len(SKILLS))
    st.subheader(f"Today's overall score: {overall}/100")
    st.progress(overall)

elif section == "📈 Finnish Progress":
    st.header("📈 Finnish Progress")
    period = st.selectbox("Time range", ["7 days", "30 days", "3 months", "1 year", "All time"], index=1)
    history = st.session_state.get("finnish_history", {})
    rows = filter_history(history, range_days(period))
    current = round(sum(st.session_state.daily_scores.values()) / len(SKILLS))
    vals = [data.get("overall", 0) for _, data in rows]
    avg = round(sum(vals) / len(vals)) if vals else 0
    practice_days = sum(any(data.get("done", {}).values()) for _, data in rows)
    total_tasks = sum(data.get("tasks_completed", sum(data.get("attempts", {}).values())) for _, data in rows)
    skill_avgs = {
        skill: round(sum(d.get("scores", {}).get(skill, 0) for _, d in rows) / len(rows)) if rows else 0
        for skill in SKILLS
    }
    best_skill = max(SKILLS, key=skill_avgs.get)
    weakest_skill = min(SKILLS, key=skill_avgs.get)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Today", f"{current}%")
    m2.metric(f"{period} avg", f"{avg}%")
    m3.metric("Practice days", practice_days)
    m4.metric("Exercises", total_tasks)
    m5.metric("Best skill", best_skill)
    m6.metric("Level estimate", level_from_score(current))

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        card_title("Overall Finnish", "Current practice score")
        ring(current)
        card_end()
    with c2:
        card_title("Skill balance", "Average in selected period")
        st.bar_chart(pd.DataFrame({"Score": list(skill_avgs.values())}, index=list(skill_avgs.keys())), height=210)
        card_end()
    with c3:
        card_title("Overall progress", f"Daily trend · {period}")
        overall_df = pd.DataFrame([{"Date": pd.to_datetime(day), "Overall": data.get("overall", 0)} for day, data in rows])
        line_chart(overall_df, "Overall", 210, 0, 100)
        card_end()

    row1 = st.columns(3)
    row2 = st.columns(3)
    for col, skill in zip(row1 + row2, SKILLS):
        with col:
            card_title(f"{skill} Progress", f"{period} trend")
            line_chart(skill_df(rows, skill), "Score", 160, 0, 100)
            card_end()
    st.caption(f"Skill needing most attention in this period: {weakest_skill}.")

elif section == "⛪ Church & Ecumenical":
    st.header("⛪ Church & Ecumenical Opportunities")
    st.caption("Priority: English-speaking church, parish, ecumenical, Christian organisation, community, integration and project roles in Finland.")
    items = opps.get("church", [])
    link_table(opportunity_rows("church", items))
    render_opportunity_tracker("church", items)

elif section == "🎓 Academic Jobs":
    st.header("🎓 Academic Opportunities")
    st.caption("Biblical Studies, theology, Hebrew Bible / Old Testament, gender & religion, reception studies, contextual theology and related humanities research.")
    items = opps.get("academic", [])
    link_table(opportunity_rows("academic", items))
    render_opportunity_tracker("academic", items)

elif section == "💶 Funding & Grants":
    st.header("💶 Funding & Grants")
    st.caption("Priority: doctoral funding, working grants, travel/conference grants, theological foundations, Finnish foundations, UEF and Nordic/European opportunities.")
    items = opps.get("funding", [])
    link_table(opportunity_rows("funding", items))
    render_opportunity_tracker("funding", items)

elif section == "🌍 Other Opportunities":
    st.header("🌍 Other Opportunities")
    items = opps.get("other", [])
    link_table(opportunity_rows("other", items))
    render_opportunity_tracker("other", items)

elif section == "📋 My Applications":
    st.header("📋 My Applications")
    pipeline = st.session_state.get("opportunity_pipeline", {})
    merged = []
    for app in apps:
        merged.append({
            "Position / Grant": app.get("position", app.get("title", "Untitled")),
            "Organisation": app.get("institution", app.get("organisation", "")),
            "Category": app.get("category", "Existing application"),
            "Country": app.get("country", ""),
            "Deadline": app.get("deadline", "Not listed"),
            "Applied date": app.get("applied", ""),
            "Current stage": status_badge(app),
            "Result / history": app.get("result", ""),
            "Contact": app.get("contact", "Not listed"),
            "Official Link": app.get("link") or None,
            "_rank": application_rank(app),
        })
    for rec in pipeline.values():
        if rec.get("stage") == "Not applied":
            continue
        merged.append({
            "Position / Grant": rec.get("title", "Untitled"),
            "Organisation": rec.get("organisation", ""),
            "Category": rec.get("kind", "Opportunity").title(),
            "Country": rec.get("country", ""),
            "Deadline": rec.get("deadline", "Not listed"),
            "Applied date": rec.get("applied_date", ""),
            "Current stage": PIPELINE_BADGES.get(rec.get("stage"), rec.get("stage")),
            "Result / history": rec.get("note", ""),
            "Contact": "Not listed",
            "Official Link": rec.get("link") or None,
            "_rank": 9 if rec.get("stage") == "Rejected / Not selected" else 0 if rec.get("stage") == "Interview" else 2,
        })
    merged = sorted(merged, key=lambda x: (x["_rank"], x.get("Deadline") or "9999"))
    total = len(merged)
    waiting = sum(any(x in row["Current stage"] for x in ["Applied", "Email reply", "Shortlisted"]) for row in merged)
    interviews = sum("Interview" in row["Current stage"] for row in merged)
    rejected = sum("Rejected" in row["Current stage"] or "Not selected" in row["Current stage"] for row in merged)
    a, b, c, d = st.columns(4)
    a.metric("Total tracked", total)
    b.metric("Waiting / active", waiting)
    c.metric("Interview", interviews)
    d.metric("Rejected", rejected)
    filt = st.selectbox("Show", ["All", "Applied / waiting", "Email reply", "Interview", "Accepted", "Rejected"])
    filtered = []
    for row in merged:
        stage = row["Current stage"]
        if filt == "Applied / waiting" and not any(x in stage for x in ["Applied", "Shortlisted"]):
            continue
        if filt != "All" and filt != "Applied / waiting" and filt not in stage:
            continue
        filtered.append({k: v for k, v in row.items() if not k.startswith("_")})
    link_table(filtered)

elif section == "📊 Career Progress":
    st.header("📊 Career Progress")
    period = st.selectbox("Time range", ["7 days", "30 days", "3 months", "1 year", "All time"], index=1, key="career_period")
    hist = st.session_state.get("career_history", {})
    rows = filter_history(hist, range_days(period))
    latest = rows[-1][1] if rows else {"church": 0, "academic": 0, "funding": 0, "other": 0, "applications": 0, "waiting": 0, "interviews": 0, "accepted": 0, "rejected": 0}
    total_apps = max(1, latest.get("applications", 0))
    interview_rate = round(100 * latest.get("interviews", 0) / total_apps)
    success_rate = round(100 * latest.get("accepted", 0) / total_apps)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Church", latest.get("church", 0))
    m2.metric("Academic", latest.get("academic", 0))
    m3.metric("Funding", latest.get("funding", 0))
    m4.metric("Applications", latest.get("applications", 0))
    m5.metric("Interviews", latest.get("interviews", 0))
    m6.metric("Accepted", latest.get("accepted", 0))

    left, mid, right = st.columns([2, 1, 1])
    with left:
        card_title("Career activity", f"Trends · {period}")
        multi = pd.DataFrame([
            {
                "Date": pd.to_datetime(day),
                "Church": data.get("church", 0),
                "Academic": data.get("academic", 0),
                "Funding": data.get("funding", 0),
                "Applications": data.get("applications", 0),
            }
            for day, data in rows
        ])
        if multi.empty:
            st.caption("No career history yet for this period.")
        else:
            st.line_chart(multi.set_index("Date"), height=240)
        card_end()
    with mid:
        card_title("Application mix", "Current tracked outcomes")
        donut(
            [latest.get("waiting", 0), latest.get("interviews", 0), latest.get("accepted", 0), latest.get("rejected", 0)],
            ["Waiting", "Interview", "Accepted", "Rejected"],
        )
        card_end()
    with right:
        card_title("Interview meter", "Interview rate")
        meter(interview_rate, "Interview rate")
        card_end()

    a, b, c = st.columns(3)
    with a:
        card_title("Opportunity mix", "Church vs academic vs funding vs other")
        mix = pd.DataFrame(
            {"Count": [latest.get("church", 0), latest.get("academic", 0), latest.get("funding", 0), latest.get("other", 0)]},
            index=["Church", "Academic", "Funding", "Other"],
        )
        st.bar_chart(mix, height=210)
        card_end()
    with b:
        card_title("Success meter", "Accepted / selected share")
        meter(success_rate, "Success rate")
        card_end()
    with c:
        card_title("Pipeline", "Waiting, interview, accepted, rejected")
        pipe = pd.DataFrame(
            {"Count": [latest.get("waiting", 0), latest.get("interviews", 0), latest.get("accepted", 0), latest.get("rejected", 0)]},
            index=["Waiting", "Interview", "Accepted", "Rejected"],
        )
        st.bar_chart(pipe, height=210)
        card_end()

elif section == "📚 Research Radar":
    st.header("📚 Biblical Studies Research Radar")
    st.caption("Academic/research intelligence tailored to Rukhsar's doctoral work — not generic Christian news.")
    items = research_radar.get("items", [])
    st.caption(f"Last updated: {research_radar.get('updated', 'Not listed')}")
    if not items:
        st.info("No verified research items have been added yet. This page is ready for the future daily updater.")
    for item in items:
        with st.container(border=True):
            st.caption(f"{item.get('date', 'Not listed')} · {item.get('category', 'Research')}")
            st.subheader(item.get("headline", "Untitled"))
            st.write(item.get("summary", ""))
            if item.get("why_it_matters"):
                st.markdown("**Why this matters to Rukhsar's research:** " + item["why_it_matters"])
            st.caption("Source: " + item.get("source", "Not listed"))
            if item.get("link"):
                st.link_button("Open source ↗", item["link"])

elif section == "🧬 Rukhsar's Profile":
    st.header("🧬 Rukhsar's Profile")
    st.markdown("<div class='profile-box'>", unsafe_allow_html=True)
    st.markdown(f"**Name:** {PROFILE['name']}")
    st.markdown(f"**Current role:** {PROFILE['role']}")
    st.markdown(f"**Location:** {PROFILE['location']}")
    st.markdown(f"**Finnish course:** {PROFILE['course']}")
    st.markdown(f"**Finnish target:** {PROFILE['target']}")
    st.markdown(f"**Doctoral research:** {PROFILE['research']}")
    st.markdown(f"**Academic focus:** {PROFILE['academic_focus']}")
    st.markdown(f"**Church/community focus:** {PROFILE['church_focus']}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("Search priority: Helsinki / Espoo / Vantaa first for church/community roles, then the rest of Finland. English-speaking roles should be prioritized while Finnish develops.")

st.markdown("---")
st.caption("History is currently stored in this browser. Clearing site data or switching browser/device can remove it. The storage keys are separated from Touqeer's dashboard so the two dashboards do not mix data.")
