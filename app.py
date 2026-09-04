import json
from datetime import date, datetime, timedelta
from pathlib import Path

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="Rukhsar Career + Finnish Assistant", page_icon="🌸", layout="wide")
BASE = Path(__file__).parent
SKILLS = ["Reading", "Writing", "Listening", "Speaking", "Grammar", "Vocabulary"]
PROFILE = {
    "name": "Rukhsar Zakria",
    "role": "Doctoral researcher / PhD student in Biblical Studies, University of Eastern Finland",
    "location": "Finland / Helsinki area",
    "finnish": "A1 beginner · started from 0",
    "target": "A2.2",
    "course": "26S2F · Konepajan aikuislukio · Myllypuro",
    "research": "Gendered metaphors of suffering in the Book of Hosea and their contemporary reception in the Pakistani Christian context.",
    "education": "PhD Biblical Studies (UEF, in progress) · MPhil Biblical Studies / Old Testament · BS Education",
    "academic_focus": "Biblical Studies · Hebrew Bible / Old Testament · Hosea · prophetic literature · suffering · gender and biblical interpretation · reception studies · contextual theology · Christianity in Pakistan · Biblical Hebrew",
    "church_focus": "Church/parish work · ecumenical organisations · Christian education · intercultural church work · integration/community projects · outreach · faith-based NGOs · project/programme coordination",
    "strengths": "Biblical Hebrew · Koine Greek · teaching · academic advising · Urdu↔English translation · grant/proposal preparation · preaching · Sunday School ministry",
    "scope": "Jobs/employment: FINLAND ONLY. Outside Finland: conferences, workshops, summer/winter schools, short training, research visits and mobility only.",
}

st.markdown("""
<style>
:root {
  --rose-950:#3C1530;
  --rose-900:#54203F;
  --rose-800:#6E2A50;
  --rose-700:#8E3B66;
  --rose-600:#B24579;
  --rose-500:#D95A91;
  --rose-400:#EE86AF;
  --rose-300:#F6B4CF;
  --rose-200:#FAD7E6;
  --rose-100:#FDEAF2;
  --rose-50:#FFF7FB;
  --cream:#FFFDFC;
  --text:#3A2032;
  --muted:#76536A;
  --border:#EFC3D6;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
  background:
    radial-gradient(circle at 82% 8%, rgba(238,134,175,.22), transparent 28%),
    radial-gradient(circle at 18% 92%, rgba(246,180,207,.24), transparent 30%),
    linear-gradient(180deg,#FFF9FC 0%,#FDF0F6 52%,#FFF8FB 100%) !important;
  color:var(--text) !important;
}

[data-testid="stHeader"] {background:rgba(255,249,252,.96) !important;}
[data-testid="stToolbar"] {color:var(--rose-900) !important;}

section[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#FDE8F1 0%,#F8D8E6 100%) !important;
  border-right:1px solid #E8AFC7 !important;
}
section[data-testid="stSidebar"] * {color:var(--rose-950) !important;}
section[data-testid="stSidebar"] [role="radiogroup"] label {
  padding:7px 9px;
  border-radius:10px;
  margin:2px 0;
}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
  background:rgba(255,255,255,.58);
}

h1,h2,h3,h4,h5,h6,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
.stCaptionContainer,
.stCaptionContainer p,
label,
.stText, .stMarkdown,
p, span {color:var(--text);}

h1 {
  color:var(--rose-950) !important;
  font-weight:800 !important;
  letter-spacing:-0.02em;
}
h2,h3 {color:var(--rose-900) !important; font-weight:750 !important;}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {color:var(--muted) !important;}

/* KPI cards */
div[data-testid="stMetric"] {
  background:rgba(255,255,255,.92) !important;
  border:1px solid var(--border) !important;
  padding:15px 16px !important;
  border-radius:16px !important;
  box-shadow:0 10px 26px rgba(105,45,78,.10) !important;
}
div[data-testid="stMetric"] label {color:var(--rose-700) !important; font-weight:700 !important;}
div[data-testid="stMetricValue"] {color:var(--rose-950) !important; font-weight:800 !important;}
div[data-testid="stMetricDelta"] {color:var(--rose-700) !important;}

/* Containers / cards */
[data-testid="stVerticalBlockBorderWrapper"] {
  background:rgba(255,255,255,.78) !important;
  border:1px solid var(--border) !important;
  border-radius:16px !important;
  box-shadow:0 8px 22px rgba(105,45,78,.07) !important;
}
.card {
  background:rgba(255,255,255,.92);
  border:1px solid var(--border);
  border-radius:16px;
  padding:16px;
  margin-bottom:14px;
  box-shadow:0 10px 24px rgba(105,45,78,.08);
}
.soft {color:var(--muted) !important;}
.note {
  padding:13px 15px;
  border-radius:14px;
  background:linear-gradient(135deg,#FCE2ED 0%,#FFF4F8 100%);
  border:1px solid #EFAFC9;
  color:var(--rose-950) !important;
  margin-bottom:14px;
  box-shadow:0 6px 18px rgba(105,45,78,.07);
}
.note * {color:var(--rose-950) !important;}

/* Info / success / warning boxes */
[data-testid="stAlert"] {
  background:#FFF8FB !important;
  border:1px solid var(--border) !important;
  color:var(--text) !important;
  border-radius:14px !important;
}
[data-testid="stAlert"] * {color:var(--text) !important;}

/* Tabs */
button[data-baseweb="tab"] {color:var(--muted) !important; font-weight:700 !important;}
button[data-baseweb="tab"][aria-selected="true"] {color:var(--rose-900) !important;}
[data-baseweb="tab-highlight"] {background:var(--rose-500) !important;}

/* Inputs */
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea {
  background:#FFFFFF !important;
  color:var(--text) !important;
  border-color:var(--border) !important;
}
input, textarea {color:var(--text) !important;}

/* Buttons */
.stButton > button, .stDownloadButton > button, [data-testid="stLinkButton"] a {
  background:linear-gradient(135deg,var(--rose-600),var(--rose-500)) !important;
  color:white !important;
  border:0 !important;
  border-radius:11px !important;
  font-weight:700 !important;
  box-shadow:0 6px 16px rgba(178,69,121,.22) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stLinkButton"] a:hover {
  background:linear-gradient(135deg,var(--rose-700),var(--rose-600)) !important;
  color:white !important;
}

/* Expanders */
[data-testid="stExpander"] {
  background:rgba(255,255,255,.82) !important;
  border:1px solid var(--border) !important;
  border-radius:13px !important;
}
[data-testid="stExpander"] summary * {color:var(--rose-900) !important; font-weight:700 !important;}

/* Dataframes and charts */
[data-testid="stDataFrame"] {
  background:white !important;
  border:1px solid var(--border) !important;
  border-radius:14px !important;
  overflow:hidden;
}

hr {border-color:#EAB7CD !important;}
a {color:var(--rose-700) !important;}

/* Make the page breathe */
.block-container {padding-top:2.2rem !important; padding-bottom:2.5rem !important;}
</style>
""", unsafe_allow_html=True)

def load_json(path, default):
    try: return json.loads((BASE/path).read_text(encoding="utf-8"))
    except Exception: return default

def load_apps(): return load_json("data/applications_2026.json", [])
def load_opps(): return load_json("data/opportunities_2026.json", {"church":[],"academic":[],"funding":[],"other":[]})
def load_radar(): return load_json("data/research_radar_2026.json", {"updated":"Not listed","items":[]})

cookie=stx.CookieManager(key="rukhsar_cookie_manager")
def get_cookie(name):
    raw=cookie.get(cookie=name)
    try: return json.loads(raw) if raw else {}
    except Exception: return {}
def put_cookie(name,value): cookie.set(name,json.dumps(value),expires_at=datetime.now()+timedelta(days=3650),key=f"{name}_{datetime.now().timestamp()}")

def init_state():
    today=date.today().isoformat()
    if "finnish_history" not in st.session_state: st.session_state.finnish_history=get_cookie("rukhsar_finnish_progress")
    if st.session_state.get("daily_date")!=today:
        saved=st.session_state.finnish_history.get(today,{})
        st.session_state.daily_date=today
        st.session_state.scores=saved.get("scores",{s:0 for s in SKILLS})
        st.session_state.attempts=saved.get("attempts",{s:0 for s in SKILLS})
        st.session_state.points=saved.get("points",{s:0 for s in SKILLS})
    if "pipeline" not in st.session_state: st.session_state.pipeline=get_cookie("rukhsar_opportunity_pipeline")

def save_score(skill,score):
    st.session_state.attempts[skill]+=1; st.session_state.points[skill]+=score
    st.session_state.scores[skill]=round(st.session_state.points[skill]/st.session_state.attempts[skill])
    today=date.today().isoformat(); h=st.session_state.finnish_history
    h[today]={"scores":dict(st.session_state.scores),"attempts":dict(st.session_state.attempts),"points":dict(st.session_state.points),"tasks_completed":sum(st.session_state.attempts.values()),"overall":round(sum(st.session_state.scores.values())/6)}
    st.session_state.finnish_history=h; put_cookie("rukhsar_finnish_progress",h)

def level(score):
    if score<25:return "A1.1"
    if score<45:return "A1.2"
    if score<62:return "A1.3"
    if score<80:return "A2.1"
    return "A2.2"

def item_key(kind,x): return f"{kind}|{x.get('link') or x.get('title') or x.get('position') or x.get('organisation','')}"
STAGES=["Not applied","Applied","Email reply received","Interview","Shortlisted","Accepted / Selected","Rejected / Not selected"]
def tracker(kind,items):
    if not items: return
    st.markdown("### 🧭 My status tracker")
    for i,x in enumerate(items):
        k=item_key(kind,x); rec=st.session_state.pipeline.get(k,{}); stage=rec.get("stage","Not applied")
        title=x.get("title") or x.get("position") or x.get("organisation") or "Untitled"
        with st.expander(f"{stage} · {title}"):
            new=st.selectbox("Stage",STAGES,index=STAGES.index(stage),key=f"stage_{kind}_{i}")
            note=st.text_input("Note",value=rec.get("note",""),key=f"note_{kind}_{i}")
            if st.button("Save status",key=f"save_{kind}_{i}"):
                st.session_state.pipeline[k]={"kind":kind,"title":title,"organisation":x.get("institution") or x.get("funder") or x.get("organisation","") ,"country":x.get("country",""),"deadline":x.get("deadline","Not listed"),"link":x.get("link","") ,"stage":new,"note":note,"updated":datetime.now().isoformat(timespec="seconds")}
                put_cookie("rukhsar_opportunity_pipeline",st.session_state.pipeline); st.success("Saved")

def table(kind,items):
    rows=[]
    for x in items:
        rows.append({"Title":x.get("title") or x.get("position") or "Not listed","Organisation":x.get("institution") or x.get("funder") or x.get("organisation") or "Not listed","Country":x.get("country","Not listed"),"Deadline":x.get("deadline","Not listed"),"Fit":f"{x.get('fit','—')}%" if x.get('fit') is not None else "—","Action":x.get("status") or x.get("action") or "Needs review","Official Link":x.get("link")})
    if rows: st.dataframe(rows,use_container_width=True,hide_index=True,column_config={"Official Link":st.column_config.LinkColumn("Official Link",display_text="Open")})
    else: st.info("No verified items have been added yet.")

init_state(); opps=load_opps(); apps=load_apps(); radar=load_radar()
st.title("🌸 Rukhsar Career + Finnish Assistant")
st.caption("Biblical Studies · church/ecumenical career · Finland-only employment · Finnish 0 → A2.2 · funding · research radar")
nav=["📊 Command Centre","🇫🇮 Daily Finnish Trainer","📈 Finnish Progress","⛪ Church & Ecumenical","🎓 Academic Jobs","💶 Funding & Grants","🌍 Conferences & Schools","📋 My Applications","📊 Career Progress","📚 Research Radar","🧬 Rukhsar's Profile"]
section=st.sidebar.radio("Navigation",nav)
st.sidebar.markdown("---"); st.sidebar.markdown("**Rukhsar Zakria**"); st.sidebar.write("PhD · Biblical Studies · UEF"); st.sidebar.caption("Employment: Finland only · Finnish goal: A2.2")

if section=="📊 Command Centre":
    daily=round(sum(st.session_state.scores.values())/6); applied=sum(r.get("stage")!="Not applied" for r in st.session_state.pipeline.values())+len(apps)
    c=st.columns(6); c[0].metric("Finnish level",level(daily) if daily else "A1 beginner"); c[1].metric("Today's Finnish",f"{daily}/100"); c[2].metric("Applications",applied); c[3].metric("Church",len(opps.get("church",[]))); c[4].metric("Academic",len(opps.get("academic",[]))); c[5].metric("Funding",len(opps.get("funding",[])))
    st.markdown("<div class='note'><b>Career rule:</b> jobs and employment are searched only in Finland. International conferences, workshops, summer/winter schools, short training, research visits and mobility are welcome.</div>",unsafe_allow_html=True)
    st.subheader("📚 Biblical Studies Research Radar")
    for x in radar.get("items",[])[:3]:
        with st.container(border=True): st.caption(f"{x.get('date','')} · {x.get('category','Research')}"); st.markdown(f"**{x.get('headline','Untitled')}**"); st.write(x.get("why_it_matters") or x.get("summary", ""))
    if not radar.get("items"): st.info("Research Radar is ready for verified daily items tailored to Rukhsar's doctoral work.")

elif section=="🇫🇮 Daily Finnish Trainer":
    st.header("🇫🇮 Finnish Trainer · Beginner → A2.2")
    st.markdown("<div class='note'>Rukhsar started Finnish from zero. Tasks stay practical and beginner-friendly, then gradually progress through A1.1 → A1.2 → A1.3 → A2.1 → A2.2.</div>",unsafe_allow_html=True)
    banks={
      "Reading":("Minna asuu Helsingissä. Hän menee bussilla kouluun.","Miten Minna menee kouluun?",["Bussilla","Junalla","Autolla"],"Bussilla"),
      "Listening":("Tänään menen kauppaan ja ostan maitoa.","Minne henkilö menee?",["Kauppaan","Kirkkoon","Kouluun"],"Kauppaan"),
      "Grammar":("Choose the correct sentence",["Minulla ei ole auto.","Minulla ei ole autoa.","Minulla ei ole auton."],"Minulla ei ole autoa."),
      "Vocabulary":("Select food/drink words",["maito","juna","leipä","kahvi","opettaja"],{"maito","leipä","kahvi"})}
    tabs=st.tabs(["📖 Reading","✍️ Writing","🎧 Listening","🎙️ Speaking","🧩 Grammar","🧠 Vocabulary"])
    with tabs[0]:
        t,q,opts,correct=banks["Reading"]; st.write(t); a=st.radio(q,opts,index=None,key="read");
        if st.button("Score reading"): save_score("Reading",100 if a==correct else 0); st.rerun()
    with tabs[1]:
        txt=st.text_area("Write 3–5 simple Finnish sentences about yourself, your family, studies or today.")
        if st.button("Score writing"):
            w=len(txt.split()); save_score("Writing",min(100,w*5)); st.rerun()
    with tabs[2]:
        sentence,q,opts,correct=banks["Listening"]; components.html(f'''<button onclick="let u=new SpeechSynthesisUtterance('{sentence}');u.lang='fi-FI';u.rate=.8;speechSynthesis.speak(u)">▶ Play Finnish</button>''',height=45); a=st.radio(q,opts,index=None,key="listen")
        if st.button("Score listening"): save_score("Listening",100 if a==correct else 0); st.rerun()
    with tabs[3]:
        st.write("Speak for 20–45 seconds: **Kerro itsestäsi: kuka olet, missä asut ja mitä opiskelet?**")
        spoken=speech_to_text(language="fi",start_prompt="🎙️ Start speaking",stop_prompt="⏹️ Stop",just_once=False,key="rukhsar_asr")
        if spoken:
            st.success(spoken); words=len(spoken.split()); score=min(100,25+words*4)
            if st.button("Save speaking score"): save_score("Speaking",score); st.rerun()
    with tabs[4]:
        q,opts,correct=banks["Grammar"]; a=st.radio(q,opts,index=None,key="grammar")
        if st.button("Score grammar"): save_score("Grammar",100 if a==correct else 0); st.rerun()
    with tabs[5]:
        q,opts,correct=banks["Vocabulary"]; a=set(st.multiselect(q,opts))
        if st.button("Score vocabulary"): save_score("Vocabulary",round(100*len(a&correct)/len(correct)) if not (a-correct) else max(0,round(100*(len(a&correct)-len(a-correct))/len(correct)))); st.rerun()
    cols=st.columns(6)
    for i,s in enumerate(SKILLS): cols[i].metric(s,f"{st.session_state.scores[s]}/100",f"{st.session_state.attempts[s]} rounds")

elif section=="📈 Finnish Progress":
    st.header("📈 Finnish Progress · Goal A2.2"); h=st.session_state.finnish_history
    rows=[]
    for d,x in sorted(h.items()): rows.append({"Date":pd.to_datetime(d),"Overall":x.get("overall",0),**x.get("scores",{})})
    df=pd.DataFrame(rows); overall=round(sum(st.session_state.scores.values())/6)
    c=st.columns(4); c[0].metric("Current estimate",level(overall)); c[1].metric("Target","A2.2"); c[2].metric("Practice days",len(h)); c[3].metric("Exercises",sum(x.get("tasks_completed",0) for x in h.values()))
    if not df.empty: st.line_chart(df.set_index("Date"),height=300)
    else: st.info("Complete Finnish exercises to start the progress history.")

elif section=="⛪ Church & Ecumenical":
    st.header("⛪ Church & Ecumenical Opportunities · Finland"); st.caption("English-speaking church, parish, ecumenical, Christian education, community, integration and project roles in Finland only."); items=opps.get("church",[]); table("church",items); tracker("church",items)
elif section=="🎓 Academic Jobs":
    st.header("🎓 Academic Jobs · Finland only"); st.caption("Biblical Studies, theology, Hebrew Bible / Old Testament, gender & religion, contextual theology, Biblical Hebrew and related humanities roles in Finland."); items=opps.get("academic",[]); table("academic",items); tracker("academic",items)
elif section=="💶 Funding & Grants":
    st.header("💶 Funding & Grants"); st.caption("Doctoral funding, working grants, Finnish/theological foundations, UEF opportunities, and eligible travel/conference/mobility funding."); items=opps.get("funding",[]); table("funding",items); tracker("funding",items)
elif section=="🌍 Conferences & Schools":
    st.header("🌍 Conferences, Workshops & Summer/Winter Schools"); st.caption("International opportunities are allowed here for short academic development only — no jobs outside Finland."); items=opps.get("other",[]); table("other",items); tracker("other",items)
elif section=="📋 My Applications":
    st.header("📋 My Applications"); rows=[]
    for a in apps: rows.append({"Position / Grant":a.get("position") or a.get("title"),"Organisation":a.get("institution") or a.get("organisation"),"Country":a.get("country"),"Deadline":a.get("deadline"),"Stage":a.get("status"),"History":a.get("result"),"Official Link":a.get("link")})
    for r in st.session_state.pipeline.values():
        if r.get("stage")!="Not applied": rows.append({"Position / Grant":r.get("title"),"Organisation":r.get("organisation"),"Country":r.get("country"),"Deadline":r.get("deadline"),"Stage":r.get("stage"),"History":r.get("note"),"Official Link":r.get("link")})
    if rows: st.dataframe(rows,use_container_width=True,hide_index=True,column_config={"Official Link":st.column_config.LinkColumn("Official Link",display_text="Open")})
    else: st.info("No applications tracked yet.")
elif section=="📊 Career Progress":
    st.header("📊 Career Progress"); pipe=list(st.session_state.pipeline.values()); c=st.columns(5); c[0].metric("Tracked",len(pipe)+len(apps)); c[1].metric("Applied",sum(x.get("stage")=="Applied" for x in pipe)); c[2].metric("Replies",sum(x.get("stage")=="Email reply received" for x in pipe)); c[3].metric("Interviews",sum(x.get("stage")=="Interview" for x in pipe)); c[4].metric("Accepted",sum(x.get("stage")=="Accepted / Selected" for x in pipe)); mix=pd.DataFrame({"Count":[len(opps.get("church",[])),len(opps.get("academic",[])),len(opps.get("funding",[])),len(opps.get("other",[]))]},index=["Church","Academic","Funding","Academic development"]); st.bar_chart(mix)
elif section=="📚 Research Radar":
    st.header("📚 Biblical Studies Research Radar"); st.caption("Old Testament/Hebrew Bible · Hosea/prophets · suffering · gender · contextual interpretation · Pakistani Christianity · Finnish theology · conferences and methods"); st.caption(f"Updated: {radar.get('updated','Not listed')}")
    if not radar.get("items"): st.info("No verified research items added yet.")
    for x in radar.get("items",[]):
        with st.container(border=True): st.caption(f"{x.get('date','Not listed')} · {x.get('category','Research')}"); st.subheader(x.get("headline","Untitled")); st.write(x.get("summary","")); st.markdown("**Why it matters:** "+x.get("why_it_matters","Needs review")); st.caption("Source: "+x.get("source","Not listed"));
elif section=="🧬 Rukhsar's Profile":
    st.header("🧬 Rukhsar's CV-based Profile")
    for label,key in [("Name","name"),("Current role","role"),("Location","location"),("Education","education"),("Finnish","finnish"),("Finnish course","course"),("Finnish target","target"),("Doctoral research","research"),("Academic focus","academic_focus"),("Church/community focus","church_focus"),("Profile strengths","strengths"),("Opportunity scope","scope")]: st.markdown(f"**{label}:** {PROFILE[key]}")
    st.info("Employment search rule: FINLAND ONLY. Prioritize Helsinki / Espoo / Vantaa, then the rest of Finland. Outside Finland include only conferences, workshops, summer/winter schools, short training, research visits and mobility.")

st.markdown("---"); st.caption("Rukhsar's Finnish and application history uses separate rukhsar_* browser-storage keys, so it does not mix with Touqeer's dashboard data.")
