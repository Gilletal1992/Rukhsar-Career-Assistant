import json
from datetime import date, datetime, timedelta
from pathlib import Path
import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="Rukhsar Career + Finnish Assistant", page_icon="🌸", layout="wide")
BASE=Path(__file__).parent
SKILLS=["Reading","Writing","Listening","Speaking","Grammar","Vocabulary"]
PROFILE={"name":"Rukhsar Zakria","role":"Doctoral researcher / PhD student in Biblical Studies, University of Eastern Finland","location":"Finland / Helsinki area","finnish":"Beginner · started from 0","target":"A2.2","course":"26S2F · Konepajan aikuislukio · Myllypuro","research":"Gendered metaphors of suffering in the Book of Hosea and their contemporary reception in the Pakistani Christian context.","education":"PhD Biblical Studies (UEF, in progress) · MPhil Biblical Studies / Old Testament · BS Education","academic_focus":"Biblical Studies · Hebrew Bible / Old Testament · Hosea · prophetic literature · suffering · gender and biblical interpretation · reception studies · contextual theology · Christianity in Pakistan · Biblical Hebrew","church_focus":"Church/parish work · ecumenical organisations · Christian education · intercultural church work · integration/community projects · outreach · faith-based NGOs · project/programme coordination","strengths":"Biblical Hebrew · Koine Greek · teaching · academic advising · Urdu↔English translation · grant/proposal preparation · preaching · Sunday School ministry","scope":"Jobs/employment: FINLAND ONLY. Outside Finland: conferences, workshops, summer/winter schools, short training, research visits and mobility only."}

st.markdown('''<style>
:root{--p:#54203F;--p2:#8E3B66;--pink:#D95A91;--text:#3A2032;--muted:#76536A;--border:#EFC3D6}
html,body,[data-testid="stAppViewContainer"],.stApp{background:radial-gradient(circle at 82% 8%,rgba(238,134,175,.22),transparent 28%),linear-gradient(180deg,#FFF9FC,#FDF0F6 52%,#FFF8FB)!important;color:var(--text)!important}
[data-testid="stHeader"]{background:rgba(255,249,252,.96)!important}section[data-testid="stSidebar"]{background:linear-gradient(180deg,#FDE8F1,#F8D8E6)!important;border-right:1px solid #E8AFC7!important}section[data-testid="stSidebar"] *{color:#3C1530!important}section[data-testid="stSidebar"] [role="radiogroup"] label{padding:7px 9px;border-radius:10px;margin:2px 0}section[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.58)}
h1,h2,h3,h4,h5,h6,p,span,label,[data-testid="stMarkdownContainer"]{color:var(--text)}h1{color:#3C1530!important;font-weight:800!important}h2,h3{color:var(--p)!important;font-weight:750!important}[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:var(--muted)!important}
div[data-testid="stMetric"]{background:rgba(255,255,255,.95)!important;border:1px solid var(--border)!important;padding:15px 16px!important;border-radius:16px!important;box-shadow:0 10px 26px rgba(105,45,78,.10)!important}div[data-testid="stMetric"] label{color:var(--p2)!important;font-weight:700!important}div[data-testid="stMetricValue"]{color:#3C1530!important;font-weight:800!important}
.note,.capacity-note{padding:13px 15px;border-radius:14px;background:linear-gradient(135deg,#FCE2ED,#FFF4F8);border:1px solid #EFAFC9;color:#3C1530!important;margin-bottom:14px;box-shadow:0 6px 18px rgba(105,45,78,.07)}
[data-testid="stAlert"],[data-testid="stExpander"]{background:#FFF8FB!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:14px!important}[data-testid="stAlert"] *{color:var(--text)!important}
button[data-baseweb="tab"]{color:var(--muted)!important;font-weight:700!important}button[data-baseweb="tab"][aria-selected="true"]{color:var(--p)!important}[data-baseweb="tab-highlight"]{background:var(--pink)!important}
.stButton>button,.stDownloadButton>button,[data-testid="stLinkButton"] a{background:linear-gradient(135deg,#B24579,#D95A91)!important;color:white!important;border:0!important;border-radius:11px!important;font-weight:700!important;box-shadow:0 6px 16px rgba(178,69,121,.22)!important}
[data-testid="stDataFrame"]{background:white!important;border:1px solid var(--border)!important;border-radius:14px!important;overflow:hidden}.block-container{padding-top:2.2rem!important;padding-bottom:2.5rem!important}hr{border-color:#EAB7CD!important}a{color:#8E3B66!important}
.level-chip{display:inline-block;padding:6px 10px;border-radius:999px;background:#F8D6E5;border:1px solid #E8AFC7;color:#54203F!important;font-weight:800;font-size:12px;margin-bottom:10px}
.career-hero{background:linear-gradient(135deg,#5A2346,#8D3A68 58%,#C85E8C);color:#FFF9FC!important;border-radius:20px;padding:22px 24px;margin:6px 0 18px;box-shadow:0 14px 34px rgba(92,33,69,.20)}.career-hero *{color:#FFF9FC!important}.career-hero .eyebrow{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;opacity:.78}.career-hero .headline{font-size:24px;font-weight:850}.career-panel{background:#fff;border:1px solid #E7AFC6;border-radius:18px;padding:18px;box-shadow:0 10px 28px rgba(105,45,78,.09);min-height:250px}.career-panel-title{font-size:16px;font-weight:800;color:#54203F!important}.career-panel-sub{font-size:12px;color:#8B647B!important;margin-bottom:16px}.career-bar-row{display:grid;grid-template-columns:150px 1fr 42px;gap:12px;align-items:center;margin:14px 0}.career-bar-label{font-size:13px;font-weight:700}.career-track{height:12px;background:#F7E3EC;border-radius:999px;overflow:hidden;border:1px solid #F0C9D9}.career-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#9E3F70,#E06B9A)}.career-count{font-size:13px;font-weight:800;color:#6F2A50!important;text-align:right}.pipeline-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.pipeline-card{border-radius:14px;padding:13px 14px;background:linear-gradient(180deg,#FFF7FB,#FBE8F1);border:1px solid #EFC3D6}.pipeline-card .num{font-size:26px;font-weight:850;color:#54203F!important}.pipeline-card .lbl{font-size:12px;font-weight:700;color:#8A5874!important}
</style>''',unsafe_allow_html=True)

def load_json(path,default):
    try:return json.loads((BASE/path).read_text(encoding="utf-8"))
    except Exception:return default
def load_apps():return load_json("data/applications_2026.json",[])
def load_opps():return load_json("data/opportunities_2026.json",{"church":[],"academic":[],"funding":[],"other":[]})
def load_radar():return load_json("data/research_radar_2026.json",{"updated":"Not listed","items":[]})

cookie=stx.CookieManager(key="rukhsar_cookie_manager")
def get_cookie(name):
    raw=cookie.get(cookie=name)
    try:return json.loads(raw) if raw else {}
    except Exception:return {}
def put_cookie(name,value):cookie.set(name,json.dumps(value),expires_at=datetime.now()+timedelta(days=3650),key=f"{name}_{datetime.now().timestamp()}")

def init_state():
    today=date.today().isoformat()
    if "finnish_history" not in st.session_state:st.session_state.finnish_history=get_cookie("rukhsar_finnish_progress")
    if st.session_state.get("daily_date")!=today:
        saved=st.session_state.finnish_history.get(today,{})
        st.session_state.daily_date=today;st.session_state.scores=saved.get("scores",{s:0 for s in SKILLS});st.session_state.attempts=saved.get("attempts",{s:0 for s in SKILLS});st.session_state.points=saved.get("points",{s:0 for s in SKILLS});st.session_state.daily_capacity=saved.get("capacity","Standard · 2 rounds per skill")
    if "pipeline" not in st.session_state:st.session_state.pipeline=get_cookie("rukhsar_opportunity_pipeline")
def save_score(skill,score):
    st.session_state.attempts[skill]+=1;st.session_state.points[skill]+=score;st.session_state.scores[skill]=round(st.session_state.points[skill]/st.session_state.attempts[skill]);today=date.today().isoformat();h=st.session_state.finnish_history;h[today]={"scores":dict(st.session_state.scores),"attempts":dict(st.session_state.attempts),"points":dict(st.session_state.points),"capacity":st.session_state.get("daily_capacity","Standard · 2 rounds per skill"),"tasks_completed":sum(st.session_state.attempts.values()),"overall":round(sum(st.session_state.scores.values())/6)};st.session_state.finnish_history=h;put_cookie("rukhsar_finnish_progress",h)
def level(score):
    if score<15:return "Beginner"
    if score<30:return "A1.1"
    if score<45:return "A1.2"
    if score<60:return "A1.3"
    if score<80:return "A2.1"
    return "A2.2"
def training_band():
    overall=round(sum(st.session_state.scores.values())/6)
    attempts=sum(st.session_state.attempts.values())
    if attempts<8:return "Beginner"
    return level(overall)
def speaking_score(text):
    if not text:return 0
    words=text.split();lower=text.lower();markers=["minä","olen","asun","opiskelen","suomea","perhe","kirkko","koulu","menen","tulen","pidän","ja","mutta","koska","tänään","huomenna"]
    hits=sum(1 for x in markers if x in lower);return min(100,round(len(words)*3+hits*5))
def item_key(kind,x):return f"{kind}|{x.get('link') or x.get('title') or x.get('position') or x.get('organisation','')}"
STAGES=["Not applied","Applied","Email reply received","Interview","Shortlisted","Accepted / Selected","Rejected / Not selected"]
def tracker(kind,items):
    if not items:return
    st.markdown("### 🧭 My status tracker")
    for i,x in enumerate(items):
        k=item_key(kind,x);rec=st.session_state.pipeline.get(k,{});stage=rec.get("stage","Not applied");title=x.get("title") or x.get("position") or x.get("organisation") or "Untitled"
        with st.expander(f"{stage} · {title}"):
            new=st.selectbox("Stage",STAGES,index=STAGES.index(stage),key=f"stage_{kind}_{i}");note=st.text_input("Note",value=rec.get("note",""),key=f"note_{kind}_{i}")
            if st.button("Save status",key=f"save_{kind}_{i}"):
                st.session_state.pipeline[k]={"kind":kind,"title":title,"organisation":x.get("institution") or x.get("funder") or x.get("organisation",""),"country":x.get("country",""),"deadline":x.get("deadline","Not listed"),"link":x.get("link",""),"stage":new,"note":note,"updated":datetime.now().isoformat(timespec="seconds")};put_cookie("rukhsar_opportunity_pipeline",st.session_state.pipeline);st.success("Saved")
def table(kind,items):
    rows=[{"Title":x.get("title") or x.get("position") or "Not listed","Organisation":x.get("institution") or x.get("funder") or x.get("organisation") or "Not listed","Country":x.get("country","Not listed"),"Deadline":x.get("deadline","Not listed"),"Fit":f"{x.get('fit','—')}%" if x.get('fit') is not None else "—","Action":x.get("status") or x.get("action") or "Needs review","Official Link":x.get("link")} for x in items]
    if rows:st.dataframe(rows,use_container_width=True,hide_index=True,column_config={"Official Link":st.column_config.LinkColumn("Official Link",display_text="Open")})
    else:st.info("No verified items have been added yet.")

init_state();opps=load_opps();apps=load_apps();radar=load_radar()
st.title("🌸 Rukhsar Career + Finnish Assistant");st.caption("Biblical Studies · church/ecumenical career · Finland-only employment · Finnish beginner → A2.2 · funding · research radar")
nav=["📊 Command Centre","🇫🇮 Daily Finnish Trainer","📈 Finnish Progress","⛪ Church & Ecumenical","🎓 Academic Jobs","💶 Funding & Grants","🌍 Conferences & Schools","📋 My Applications","📊 Career Progress","📚 Research Radar","🧬 Rukhsar's Profile"]
section=st.sidebar.radio("Navigation",nav);st.sidebar.markdown("---");st.sidebar.markdown("**Rukhsar Zakria**");st.sidebar.write("PhD · Biblical Studies · UEF");st.sidebar.caption("Employment: Finland only · Finnish goal: A2.2")

if section=="📊 Command Centre":
    daily=round(sum(st.session_state.scores.values())/6);applied=sum(r.get("stage")!="Not applied" for r in st.session_state.pipeline.values())+len(apps);c=st.columns(6);c[0].metric("Finnish level",level(daily));c[1].metric("Today's Finnish",f"{daily}/100");c[2].metric("Applications",applied);c[3].metric("Church",len(opps.get("church",[])));c[4].metric("Academic",len(opps.get("academic",[])));c[5].metric("Funding",len(opps.get("funding",[])));st.markdown("<div class='note'><b>Career rule:</b> jobs and employment are searched only in Finland. International conferences, workshops, summer/winter schools, short training, research visits and mobility are welcome.</div>",unsafe_allow_html=True);st.subheader("📚 Biblical Studies Research Radar")
    for x in radar.get("items",[])[:3]:
        with st.container(border=True):st.caption(f"{x.get('date','')} · {x.get('category','Research')}");st.markdown(f"**{x.get('headline','Untitled')}**");st.write(x.get("why_it_matters") or x.get("summary",""))
    if not radar.get("items"):st.info("Research Radar is ready for verified daily items tailored to Rukhsar's doctoral work.")

elif section=="🇫🇮 Daily Finnish Trainer":
    st.header("🇫🇮 Adaptive Daily Finnish Trainer · Beginner → A2.2")
    stage=training_band();st.markdown(f"<div class='level-chip'>Current training stage: {stage}</div>",unsafe_allow_html=True)
    st.markdown("<div class='capacity-note'><b>Study at your own capacity.</b> Rukhsar starts from complete beginner level. Choose a suggested workload, then complete as many rounds as you want. Tasks gradually become harder only as her results and practice increase, moving from Beginner → A1.1 → A1.2 → A1.3 → A2.1 → A2.2.</div>",unsafe_allow_html=True)
    capacity_map={"Light · 1 round per skill":1,"Standard · 2 rounds per skill":2,"Focused · 3 rounds per skill":3,"Intensive · 5 rounds per skill":5}
    labels=list(capacity_map);current=st.session_state.get("daily_capacity",labels[1]);capacity_label=st.selectbox("Today's study capacity",labels,index=labels.index(current) if current in labels else 1);st.session_state.daily_capacity=capacity_label;target_rounds=capacity_map[capacity_label];completed=sum(st.session_state.attempts.values());target_total=target_rounds*6
    a,b,c=st.columns(3);a.metric("Tasks completed today",completed);b.metric("Suggested target",target_total);c.metric("Completion",f"{min(100,round(100*completed/max(1,target_total)))}%");st.progress(min(1.0,completed/max(1,target_total)))

    beginner_read=[("Minä olen Rukhsar.","Kuka minä olen?",["Rukhsar","Minna","Anna"],"Rukhsar"),("Tämä on kirja.","Mikä tämä on?",["Kirja","Auto","Talo"],"Kirja"),("Minä asun Helsingissä.","Missä minä asun?",["Turussa","Helsingissä","Oulussa"],"Helsingissä"),("Tänään on maanantai.","Mikä päivä tänään on?",["Tiistai","Maanantai","Perjantai"],"Maanantai"),("Minulla on kahvi.","Mitä minulla on?",["Kahvi","Bussi","Kirja"],"Kahvi"),("Hän on opettaja.","Mikä hänen ammatti on?",["Opettaja","Lääkäri","Pappi"],"Opettaja")]
    a1_read=[("Minna asuu Helsingissä. Hän menee aamulla bussilla kouluun.","Miten Minna menee kouluun?",["Junalla","Bussilla","Autolla"],"Bussilla"),("Anna opiskelee suomea maanantaina ja keskiviikkona.","Milloin Anna opiskelee suomea?",["Maanantaina ja keskiviikkona","Tiistaina","Perjantaina"],"Maanantaina ja keskiviikkona"),("Rukhsar menee aamulla kouluun. Tunti alkaa kello yhdeksän.","Mihin aikaan tunti alkaa?",["Kahdeksalta","Yhdeksältä","Kymmeneltä"],"Yhdeksältä"),("Pekalla on vaimo ja yksi lapsi. He asuvat Espoossa.","Missä perhe asuu?",["Helsingissä","Espoossa","Vantaalla"],"Espoossa"),("Sara menee ensin kirkkoon ja sitten kahvilaan.","Minne Sara menee ensin?",["Kahvilaan","Kirkkoon","Kauppaan"],"Kirkkoon"),("Illalla Liisa tekee ruokaa ja katsoo televisiota.","Mitä Liisa tekee illalla?",["Tekee ruokaa","Menee töihin","Ui"],"Tekee ruokaa")]
    a2_read=[("Maria matkustaa perjantaina Tampereelle junalla ja palaa Helsinkiin sunnuntai-iltana.","Milloin Maria palaa Helsinkiin?",["Perjantaina","Lauantaina","Sunnuntai-iltana"],"Sunnuntai-iltana"),("Antti työskentelee sairaalassa. Lounaan jälkeen hän soittaa ystävälleen ja illalla menee kuntosalille.","Missä Antti työskentelee?",["Koulussa","Sairaalassa","Kaupassa"],"Sairaalassa"),("Koska bussit kulkevat harvoin sunnuntaina, Laura lähtee tapaamiseen aikaisemmin.","Miksi Laura lähtee aikaisemmin?",["Koska bussit kulkevat harvoin","Koska hän on väsynyt","Koska sataa"],"Koska bussit kulkevat harvoin"),("Veera on opiskellut suomea vuoden. Hän ymmärtää jo paljon, mutta puhuminen on vielä vaikeaa.","Mikä on Veeralle vielä vaikeaa?",["Lukeminen","Puhuminen","Kuunteleminen"],"Puhuminen"),("Jos sää on hyvä huomenna, menemme puistoon lasten kanssa.","Millä ehdolla he menevät puistoon?",["Jos sää on hyvä","Jos sataa","Jos on maanantai"],"Jos sää on hyvä"),("Opettaja pyysi opiskelijoita palauttamaan tehtävän ennen perjantaita.","Mitä opiskelijoiden pitää tehdä?",["Palauttaa tehtävä","Ostaa kirja","Soittaa opettajalle"],"Palauttaa tehtävä")]

    beginner_listen=[("Hei! Minä olen Anna.","Mikä nimi kuulet?",["Anna","Laura","Minna"],"Anna"),("Minulla on kaksi kirjaa.","Kuinka monta kirjaa?",["Yksi","Kaksi","Kolme"],"Kaksi"),("Kello on seitsemän.","Mitä kello on?",["Seitsemän","Kahdeksan","Yhdeksän"],"Seitsemän"),("Tämä on minun koti.","Mikä paikka?",["Koti","Koulu","Kauppa"],"Koti"),("Minä juon vettä.","Mitä juon?",["Vettä","Maitoa","Kahvia"],"Vettä"),("Huomenna on tiistai.","Mikä päivä on huomenna?",["Tiistai","Torstai","Sunnuntai"],"Tiistai")]
    a1_listen=[("Tänään menen kauppaan ja ostan maitoa, leipää ja omenoita.","Mitä henkilö ostaa?",["Maitoa, leipää ja omenoita","Kahvia ja teetä","Vaatteita"],"Maitoa, leipää ja omenoita"),("Huomenna aamulla menen lääkärille. Sen jälkeen menen kouluun bussilla.","Minne henkilö menee ensin?",["Kouluun","Lääkärille","Kauppaan"],"Lääkärille"),("Sunnuntaina tapaamme ystäviä kahvilassa kello kaksi.","Missä he tapaavat?",["Kirkossa","Kahvilassa","Asemalla"],"Kahvilassa"),("Bussi lähtee kello kahdeksan ja saapuu keskustaan puoli yhdeksältä.","Mihin bussi saapuu?",["Kouluun","Keskustaan","Lentokentälle"],"Keskustaan"),("Illalla teen ruokaa, luen kirjaa ja menen nukkumaan kello yksitoista.","Mitä henkilö tekee illalla?",["Tekee ruokaa","Menee töihin","Matkustaa"],"Tekee ruokaa"),("Kurssi alkaa syyskuussa ja loppuu joulukuussa.","Milloin kurssi loppuu?",["Lokakuussa","Joulukuussa","Tammikuussa"],"Joulukuussa")]
    a2_listen=[("Jos ehdin töistä ajoissa, tulen mukaan kokoukseen illalla.","Millä ehdolla henkilö tulee kokoukseen?",["Jos hän ehtii ajoissa","Jos sataa","Jos bussi myöhästyy"],"Jos hän ehtii ajoissa"),("Olen asunut Suomessa kaksi vuotta, mutta aloitin suomen opiskelun vasta viime kuussa.","Milloin henkilö aloitti suomen opiskelun?",["Kaksi vuotta sitten","Viime kuussa","Eilen"],"Viime kuussa"),("Lääkäri suositteli, että lepään pari päivää ja juon paljon vettä.","Mitä lääkäri suositteli?",["Lepo ja vesi","Matka","Urheilu"],"Lepo ja vesi"),("Seminaari alkaa torstaina aamulla ja jatkuu perjantaihin asti.","Kuinka kauan seminaari kestää?",["Torstaista perjantaihin","Yhden tunnin","Koko viikon"],"Torstaista perjantaihin"),("Vaikka sää oli kylmä, menimme kävelylle meren rannalle.","Mitä he tekivät?",["Menivät kävelylle","Jäivät kotiin","Menivät töihin"],"Menivät kävelylle"),("Hän ei päässyt tapaamiseen, koska juna oli myöhässä.","Miksi hän ei päässyt tapaamiseen?",["Juna oli myöhässä","Hän unohti","Hän oli lomalla"],"Juna oli myöhässä")]

    beginner_grammar=[(["Minä olen Rukhsar.","Minä on Rukhsar."],"Minä olen Rukhsar."),(["Sinä olet opiskelija.","Sinä olen opiskelija."],"Sinä olet opiskelija."),(["Hän on opettaja.","Hän olet opettaja."],"Hän on opettaja."),(["Minulla on kirja.","Minulla olen kirja."],"Minulla on kirja."),(["En ole kotona.","Ei olen kotona."],"En ole kotona."),(["Tämä on auto.","Tämä ovat auto."],"Tämä on auto.")]
    a1_grammar=[(["Minulla ei ole auto.","Minulla ei ole autoa.","Minulla ei ole auton."],"Minulla ei ole autoa."),(["Minä juon kahvi.","Minä juon kahvia.","Minä juon kahvin."],"Minä juon kahvia."),(["Syön kaksi omenaa.","Syön kaksi omenat.","Syön kaksi omenan."],"Syön kaksi omenaa."),(["Menen kauppaan.","Menen kaupassa.","Menen kaupasta."],"Menen kauppaan."),(["Olen Helsingissä.","Olen Helsinkiin.","Olen Helsingistä."],"Olen Helsingissä."),(["Hän ei puhu suomea.","Hän ei puhu suomi.","Hän ei puhu suomen."],"Hän ei puhu suomea.")]
    a2_grammar=[(["Olen asunut Suomessa kaksi vuotta.","Olen asua Suomessa kaksi vuotta."],"Olen asunut Suomessa kaksi vuotta."),(["Jos sataa, jään kotiin.","Jos sataa, jäin kotiin."],"Jos sataa, jään kotiin."),(["Hän sanoi, että tulee huomenna.","Hän sanoi, että tulen huomenna."],"Hän sanoi, että tulee huomenna."),(["Menin kauppaan ostamaan ruokaa.","Menin kauppaan ostaa ruokaa."],"Menin kauppaan ostamaan ruokaa."),(["Vaikka olin väsynyt, opiskelin vielä tunnin.","Vaikka olin väsynyt, opiskelen eilen tunnin."],"Vaikka olin väsynyt, opiskelin vielä tunnin."),(["Minun täytyy lähteä nyt.","Minun täytyy lähden nyt."],"Minun täytyy lähteä nyt.")]

    beginner_vocab=[(["hei","kiitos","juna","moi"],{"hei","kiitos","moi"},"Select greetings/basic words:"),(["yksi","kaksi","omena","kolme"],{"yksi","kaksi","kolme"},"Select numbers:"),(["äiti","isä","bussi","sisko"],{"äiti","isä","sisko"},"Select family words:"),(["punainen","sininen","kirja","vihreä"],{"punainen","sininen","vihreä"},"Select colours:"),(["maanantai","tiistai","kahvi","keskiviikko"],{"maanantai","tiistai","keskiviikko"},"Select weekdays:"),(["minä","sinä","hän","talo"],{"minä","sinä","hän"},"Select pronouns:")]
    a1_vocab=[(["maito","juna","leipä","kahvi","opettaja","omena"],{"maito","leipä","kahvi","omena"},"Select food/drink words:"),(["bussi","juna","omena","metro","kirja","pyörä"],{"bussi","juna","metro","pyörä"},"Select transport words:"),(["aamu","ilta","kauppa","yö","päivä","auto"],{"aamu","ilta","yö","päivä"},"Select time-of-day words:"),(["opettaja","lääkäri","banaani","tutkija","pappi","metro"],{"opettaja","lääkäri","tutkija","pappi"},"Select professions:"),(["keittiö","makuuhuone","juna","olohuone","kylpyhuone","kahvi"],{"keittiö","makuuhuone","olohuone","kylpyhuone"},"Select rooms/home words:"),(["halpa","kallis","nopea","maito","hidas"],{"halpa","kallis","nopea","hidas"},"Select adjectives:")]
    a2_vocab=[(["hakemus","apuraha","kokous","banaani","määräaika"],{"hakemus","apuraha","kokous","määräaika"},"Select study/work words:"),(["sairaus","oire","resepti","juna","lääke"],{"sairaus","oire","resepti","lääke"},"Select health words:"),(["säästää","maksaa","vuokra","raha","omena"],{"säästää","maksaa","vuokra","raha"},"Select money/housing words:"),(["mielestäni","koska","vaikka","mutta","kahvi"],{"mielestäni","koska","vaikka","mutta"},"Select linking/opinion words:"),(["haastattelu","työhakemus","kokemus","juna","osaaminen"],{"haastattelu","työhakemus","kokemus","osaaminen"},"Select job-search words:"),(["seurakunta","jumalanpalvelus","seminaari","apuraha","bussi"],{"seurakunta","jumalanpalvelus","seminaari","apuraha"},"Select church/academic words:")]

    beginner_write=["Write 1–2 very simple Finnish sentences: your name and where you live.","Write 2 simple sentences using Minä olen / Minä asun.","Write the Finnish words for three family members and make one sentence.","Write 2 sentences about today: Tänään on... / Tänään minä...","Write 2 simple sentences about what you have: Minulla on...","Write a 2-line greeting message in Finnish."]
    a1_write=["Write 3–4 simple Finnish sentences about yourself.","Write 3–5 sentences about your family.","Write 4 sentences about your Finnish class day.","Write 4–5 sentences about what you do in the morning.","Write a short Finnish message to a friend: suggest meeting tomorrow.","Describe your home in 4–5 simple sentences."]
    a2_write=["Write 5–7 Finnish sentences about your studies and weekly routine.","Write a short message explaining why you cannot attend a meeting and suggest another time.","Write 6–8 sentences about living in Finland: what is easy and what is difficult.","Write a short application-style paragraph about your teaching experience.","Write 6–8 sentences giving your opinion about learning Finnish and explain why.","Write a short email asking for information about a seminar or course."]

    beginner_speak=["Sano: Minä olen Rukhsar. Minä asun Helsingissä.","Kerro nimesi ja missä asut.","Sano kolme sanaa perheestäsi.","Kerro mikä päivä tänään on.","Kerro kaksi asiaa, jotka sinulla on.","Kerro mitä juot tai syöt tänään."]
    a1_speak=["Kerro itsestäsi: kuka olet, missä asut ja mitä opiskelet?","Kerro perheestäsi.","Kerro tavallisesta aamustasi.","Kerro mitä teet tänään.","Kerro suomen kurssistasi.","Kerro viikonlopustasi."]
    a2_speak=["Kerro opinnoistasi ja miksi aihe kiinnostaa sinua.","Kerro yhdestä tavallisesta viikosta Suomessa.","Selitä, miksi haluat oppia suomea ja missä tarvitset sitä.","Kerro kokemuksestasi opettajana.","Kerro mielipiteesi yhdestä arkisesta aiheesta ja perustele se.","Kerro seminaarista tai tapahtumasta, johon haluaisit osallistua."]

    if stage=="Beginner":
        reading_bank,listen_bank,grammar_bank,vocab_sets=beginner_read,beginner_listen,beginner_grammar,beginner_vocab
        writing_prompts,speaking_prompts=beginner_write,beginner_speak
    elif stage in ["A1.1","A1.2","A1.3"]:
        reading_bank,listen_bank,grammar_bank,vocab_sets=a1_read,a1_listen,a1_grammar,a1_vocab
        writing_prompts,speaking_prompts=a1_write,a1_speak
    else:
        reading_bank,listen_bank,grammar_bank,vocab_sets=a2_read,a2_listen,a2_grammar,a2_vocab
        writing_prompts,speaking_prompts=a2_write,a2_speak

    tabs=st.tabs(["📖 Reading","✍️ Writing","🎧 Listening","🎙️ Speaking","🧩 Grammar","🧠 Vocabulary"]);seed=date.today().toordinal()
    with tabs[0]:
        r=st.session_state.attempts["Reading"]+1;item=reading_bank[(seed+r-1)%len(reading_bank)];st.caption(f"Round {r} · {stage} task · Continue as long as you want today.");st.write("**Teksti:** "+item[0]);ans=st.radio(item[1],item[2],index=None,key=f"read_{date.today()}_{r}")
        if st.button("Submit reading round",key=f"read_btn_{r}"):save_score("Reading",100 if ans==item[3] else 0);st.rerun()
    with tabs[1]:
        r=st.session_state.attempts["Writing"]+1;st.caption(f"Round {r} · {stage} task");txt=st.text_area(writing_prompts[(seed+r-1)%len(writing_prompts)],key=f"write_{r}")
        if st.button("Submit writing round",key=f"write_btn_{r}"):words=len(txt.split());sentences=txt.count(".")+txt.count("!")+txt.count("?");save_score("Writing",min(100,words*4+sentences*8));st.rerun()
    with tabs[2]:
        r=st.session_state.attempts["Listening"]+1;item=listen_bank[(seed+r-1)%len(listen_bank)];st.caption(f"Round {r} · {stage} task");sentence=item[0].replace("'","\\'");components.html(f'''<button onclick="speechSynthesis.cancel();let u=new SpeechSynthesisUtterance('{sentence}');u.lang='fi-FI';u.rate=.78;speechSynthesis.speak(u);">▶ Play Finnish</button>''',height=45);ans=st.radio(item[1],item[2],index=None,key=f"listen_{r}")
        if st.button("Submit listening round",key=f"listen_btn_{r}"):save_score("Listening",100 if ans==item[3] else 0);st.rerun()
    with tabs[3]:
        r=st.session_state.attempts["Speaking"]+1;st.caption(f"Round {r} · {stage} task");st.write("Speak in Finnish: **"+speaking_prompts[(seed+r-1)%len(speaking_prompts)]+"**");spoken=speech_to_text(language="fi",start_prompt="🎙️ Start speaking Finnish",stop_prompt="⏹️ Stop & transcribe",just_once=False,key=f"rukhsar_asr_{r}")
        if spoken:
            score=speaking_score(spoken);st.success(spoken);st.metric("Round speaking score",f"{score}/100")
            if st.button("Save speaking round",key=f"speak_btn_{r}"):save_score("Speaking",score);st.rerun()
    with tabs[4]:
        r=st.session_state.attempts["Grammar"]+1;item=grammar_bank[(seed+r-1)%len(grammar_bank)];st.caption(f"Round {r} · {stage} task");ans=st.radio("Choose the correct sentence:",item[0],index=None,key=f"gram_{r}")
        if st.button("Submit grammar round",key=f"gram_btn_{r}"):save_score("Grammar",100 if ans==item[1] else 0);st.success(f"Correct answer: {item[1]}");st.rerun()
    with tabs[5]:
        r=st.session_state.attempts["Vocabulary"]+1;item=vocab_sets[(seed+r-1)%len(vocab_sets)];st.caption(f"Round {r} · {stage} task");chosen=set(st.multiselect(item[2],item[0],key=f"vocab_{r}"))
        if st.button("Submit vocabulary round",key=f"vocab_btn_{r}"):raw=max(0,len(chosen&item[1])-len(chosen-item[1]));save_score("Vocabulary",round(100*raw/len(item[1])));st.rerun()
    st.markdown("---");cols=st.columns(6)
    for i,s in enumerate(SKILLS):cols[i].metric(s,f"{st.session_state.scores[s]}/100",f"{st.session_state.attempts[s]} rounds")
    overall=round(sum(st.session_state.scores.values())/6);st.subheader(f"Today's overall score: {overall}/100");st.progress(overall)

elif section=="📈 Finnish Progress":
    st.header("📈 Finnish Progress · Beginner → A2.2");h=st.session_state.finnish_history;rows=[{"Date":pd.to_datetime(d),"Overall":x.get("overall",0),**x.get("scores",{})} for d,x in sorted(h.items())];df=pd.DataFrame(rows);overall=round(sum(st.session_state.scores.values())/6);c=st.columns(4);c[0].metric("Current estimate",level(overall));c[1].metric("Target","A2.2");c[2].metric("Practice days",len(h));c[3].metric("Exercises",sum(x.get("tasks_completed",0) for x in h.values()));
    if not df.empty:st.line_chart(df.set_index("Date"),height=300)
    else:st.info("Complete Finnish exercises to start the progress history.")
elif section=="⛪ Church & Ecumenical":st.header("⛪ Church & Ecumenical Opportunities · Finland");st.caption("English-speaking church, parish, ecumenical, Christian education, community, integration and project roles in Finland only.");items=opps.get("church",[]);table("church",items);tracker("church",items)
elif section=="🎓 Academic Jobs":st.header("🎓 Academic & Teaching Jobs · Finland only");st.caption("Biblical Studies/theology plus suitable English-medium school teaching, educational support and tutoring roles in Finland.");items=opps.get("academic",[]);table("academic",items);tracker("academic",items)
elif section=="💶 Funding & Grants":st.header("💶 Funding & Grants");st.caption("Doctoral funding, working grants, Finnish/theological foundations, UEF opportunities, and eligible travel/conference/mobility funding.");items=opps.get("funding",[]);table("funding",items);tracker("funding",items)
elif section=="🌍 Conferences & Schools":st.header("🌍 Conferences, Workshops & Summer/Winter Schools");st.caption("International short academic development is welcome — conferences, doctoral seminars, workshops, summer/winter schools, training, research visits and mobility; no foreign employment.");items=opps.get("other",[]);table("other",items);tracker("other",items)
elif section=="📋 My Applications":
    st.header("📋 My Applications");rows=[]
    for a in apps:rows.append({"Position / Grant":a.get("position") or a.get("title"),"Organisation":a.get("institution") or a.get("organisation"),"Country":a.get("country"),"Deadline":a.get("deadline"),"Stage":a.get("status"),"History":a.get("result"),"Official Link":a.get("link")})
    for r in st.session_state.pipeline.values():
        if r.get("stage")!="Not applied":rows.append({"Position / Grant":r.get("title"),"Organisation":r.get("organisation"),"Country":r.get("country"),"Deadline":r.get("deadline"),"Stage":r.get("stage"),"History":r.get("note"),"Official Link":r.get("link")})
    if rows:st.dataframe(rows,use_container_width=True,hide_index=True,column_config={"Official Link":st.column_config.LinkColumn("Official Link",display_text="Open")})
    else:st.info("No applications tracked yet.")
elif section=="📊 Career Progress":
    pipe=list(st.session_state.pipeline.values());tracked=len(pipe)+len(apps);applied_count=sum(x.get("stage")=="Applied" for x in pipe);replies=sum(x.get("stage")=="Email reply received" for x in pipe);interviews=sum(x.get("stage")=="Interview" for x in pipe);shortlisted=sum(x.get("stage")=="Shortlisted" for x in pipe);accepted=sum(x.get("stage")=="Accepted / Selected" for x in pipe);rejected=sum(x.get("stage")=="Rejected / Not selected" for x in pipe);church_n=len(opps.get("church",[]));academic_n=len(opps.get("academic",[]));funding_n=len(opps.get("funding",[]));other_n=len(opps.get("other",[]));st.markdown("<div class='career-hero'><div class='eyebrow'>Career analytics</div><div class='headline'>📊 Career Progress</div><div class='subline'>Applications, responses and opportunity mix for Rukhsar's Finland-focused career path.</div></div>",unsafe_allow_html=True);c=st.columns(5);c[0].metric("Tracked",tracked);c[1].metric("Applied",applied_count);c[2].metric("Replies",replies);c[3].metric("Interviews",interviews);c[4].metric("Accepted",accepted);left,right=st.columns([1.35,1])
    with left:
        maxo=max(1,church_n,academic_n,funding_n,other_n);bars=[("⛪ Church & Ecumenical",church_n),("🎓 Academic / Teaching",academic_n),("💶 Funding & Grants",funding_n),("🌍 Academic Development",other_n)];html="".join(f"<div class='career-bar-row'><div class='career-bar-label'>{lab}</div><div class='career-track'><div class='career-fill' style='width:{round(100*v/maxo) if v else 0}%'></div></div><div class='career-count'>{v}</div></div>" for lab,v in bars);st.markdown(f"<div class='career-panel'><div class='career-panel-title'>Opportunity Mix</div><div class='career-panel-sub'>Current verified opportunities by category</div>{html}</div>",unsafe_allow_html=True)
    with right:st.markdown(f"<div class='career-panel'><div class='career-panel-title'>Application Pipeline</div><div class='career-panel-sub'>Movement from application to final decision</div><div class='pipeline-grid'><div class='pipeline-card'><div class='num'>{applied_count}</div><div class='lbl'>✅ Applied</div></div><div class='pipeline-card'><div class='num'>{replies}</div><div class='lbl'>📧 Replies</div></div><div class='pipeline-card'><div class='num'>{interviews}</div><div class='lbl'>🎤 Interviews</div></div><div class='pipeline-card'><div class='num'>{shortlisted}</div><div class='lbl'>🟢 Shortlisted</div></div><div class='pipeline-card'><div class='num'>{accepted}</div><div class='lbl'>🏆 Accepted</div></div><div class='pipeline-card'><div class='num'>{rejected}</div><div class='lbl'>🔴 Not selected</div></div></div></div>",unsafe_allow_html=True)
elif section=="📚 Research Radar":
    st.header("📚 Biblical Studies Research Radar");st.caption("Old Testament/Hebrew Bible · Hosea/prophets · suffering · gender · contextual interpretation · Pakistani Christianity · Finnish theology · conferences and methods");st.caption(f"Updated: {radar.get('updated','Not listed')}")
    if not radar.get("items"):st.info("No verified research items added yet.")
    for x in radar.get("items",[]):
        with st.container(border=True):st.caption(f"{x.get('date','Not listed')} · {x.get('category','Research')}");st.subheader(x.get("headline","Untitled"));st.write(x.get("summary",""));st.markdown("**Why it matters:** "+x.get("why_it_matters","Needs review"));st.caption("Source: "+x.get("source","Not listed"))
elif section=="🧬 Rukhsar's Profile":
    st.header("🧬 Rukhsar's CV-based Profile")
    for label,key in [("Name","name"),("Current role","role"),("Location","location"),("Education","education"),("Finnish","finnish"),("Finnish course","course"),("Finnish target","target"),("Doctoral research","research"),("Academic focus","academic_focus"),("Church/community focus","church_focus"),("Profile strengths","strengths"),("Opportunity scope","scope")]:st.markdown(f"**{label}:** {PROFILE[key]}")
    st.info("Employment search rule: FINLAND ONLY. Prioritize Helsinki / Espoo / Vantaa, then the rest of Finland. Outside Finland include only conferences, workshops, summer/winter schools, short training, research visits and mobility.")
st.markdown("---");st.caption("Rukhsar's Finnish and application history uses separate rukhsar_* browser-storage keys, so it does not mix with Touqeer's dashboard data.")