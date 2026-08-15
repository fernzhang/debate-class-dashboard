
import streamlit as st
import pandas as pd
from html import escape

st.set_page_config(
    page_title="Debate Class Dashboard",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="collapsed"
)

REQUIRED = [
    "Date", "Student", "Homework_Status", "Homework_Points",
    "POI_Points", "Class_Points", "Bonus_Points", "Feedback"
]

STATUS = {
    "Complete": ("Complete", "status-complete"),
    "Late": ("Late", "status-late"),
    "Missing": ("Missing", "status-missing"),
    "Excused": ("Excused", "status-excused"),
}

# Do NOT cache this read. The CSV is intentionally replaceable through GitHub.
def load_default_data():
    return pd.read_csv("sample_students.csv")

st.markdown("""
<style>
:root {
  --bg:#FFF9F2;
  --paper:#FFFFFF;
  --ink:#22213A;
  --muted:#716F83;
  --line:#E8E1D8;
  --violet:#7458E8;
  --violet-soft:#EEE9FF;
  --coral:#FF6F61;
  --coral-soft:#FFE9E5;
  --aqua:#35C8C3;
  --aqua-soft:#DFF8F6;
  --yellow:#F7C94B;
  --yellow-soft:#FFF3C9;
  --blue:#4D8CF7;
  --blue-soft:#E8F0FF;
  --green:#39A87A;
  --green-soft:#E5F6EF;
  --red:#D85959;
  --red-soft:#FCE8E8;
}
html, body, [class*="css"] {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.stApp { background:var(--bg); color:var(--ink); }
.block-container { max-width:1180px; padding-top:1.25rem; padding-bottom:4rem; }
#MainMenu, footer, header { visibility:hidden; }
::selection { background:#DAD0FF; color:var(--ink); }

.topbar {
  display:flex; align-items:center; justify-content:space-between;
  padding:8px 0 17px; border-bottom:1px solid var(--line); margin-bottom:22px;
}
.brand { display:flex; align-items:center; gap:12px; }
.brand-mark {
  width:42px; height:42px; border-radius:13px;
  background:var(--violet); color:white; display:grid; place-items:center;
  box-shadow:0 6px 0 #DCD3FF;
}
.brand-mark svg { width:24px; height:24px; }
.brand-title { font-size:1.34rem; font-weight:800; letter-spacing:-.025em; }
.brand-sub { color:var(--muted); font-size:.82rem; margin-top:2px; }
.top-date { color:var(--muted); font-size:.82rem; }

.hero {
  position:relative; overflow:hidden;
  display:grid; grid-template-columns:1.15fr .85fr;
  background:var(--violet-soft);
  border:1px solid #DED4FF;
  border-radius:22px;
  min-height:260px;
  margin:0 0 22px;
}
.hero-copy { padding:34px 36px; position:relative; z-index:2; }
.hero h1 {
  margin:0; max-width:620px; font-size:3rem; line-height:.98;
  letter-spacing:-.05em;
}
.hero p { margin:15px 0 0; color:#5F587E; line-height:1.55; max-width:52ch; }
.hero-art { position:relative; min-height:250px; }
.hero-art svg { position:absolute; right:20px; bottom:0; width:min(420px,100%); height:auto; }

.filter-shell {
  display:grid; grid-template-columns:1.15fr .85fr; gap:18px;
  margin:0 0 22px;
}
div[data-baseweb="select"] > div,
section[data-testid="stFileUploaderDropzone"] {
  background:white !important;
  border:1px solid var(--line) !important;
  border-radius:12px !important;
  box-shadow:none !important;
}

.champ-grid {
  display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:18px;
}
.champ-card {
  border-radius:18px; padding:22px 24px; position:relative; overflow:hidden;
  min-height:182px;
}
.champ-card.homework { background:var(--yellow-soft); border:1px solid #F0D878; }
.champ-card.poi { background:var(--aqua-soft); border:1px solid #A8E6E1; }
.champ-top { display:flex; justify-content:space-between; gap:16px; align-items:center; }
.champ-label { font-size:.85rem; font-weight:750; }
.champ-period { font-size:.76rem; color:var(--muted); }
.champ-name { font-size:2.05rem; line-height:1; font-weight:850; letter-spacing:-.04em; margin-top:33px; }
.champ-score { color:var(--muted); margin-top:7px; font-size:.86rem; }
.champ-icon { position:absolute; right:18px; bottom:14px; width:96px; height:96px; opacity:.95; }
.champ-icon svg { width:100%; height:100%; }

.stats {
  display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:25px;
}
.stat {
  min-height:108px; background:var(--paper); border:1px solid var(--line);
  border-radius:16px; padding:17px 18px;
}
.stat:nth-child(1) { box-shadow:inset 0 4px 0 var(--coral); }
.stat:nth-child(2) { box-shadow:inset 0 4px 0 var(--violet); }
.stat:nth-child(3) { box-shadow:inset 0 4px 0 var(--aqua); }
.stat:nth-child(4) { box-shadow:inset 0 4px 0 var(--yellow); }
.stat-value { font-size:1.65rem; font-weight:850; letter-spacing:-.035em; }
.stat-label { color:var(--muted); font-size:.78rem; margin-top:5px; }

button[data-baseweb="tab"] {
  font-weight:700 !important; color:var(--muted) !important;
  padding-left:1rem !important; padding-right:1rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] { color:var(--ink) !important; }
div[data-baseweb="tab-highlight"] { background:var(--violet) !important; height:3px !important; }

.section-head {
  display:flex; justify-content:space-between; align-items:end;
  margin:23px 0 11px; gap:18px;
}
.section-head h2 { margin:0; font-size:1.42rem; letter-spacing:-.03em; }
.section-head p { margin:0; color:var(--muted); font-size:.8rem; }

.board { background:white; border:1px solid var(--line); border-radius:16px; overflow:hidden; }
.board-row {
  display:grid; grid-template-columns:54px 1.15fr 2fr 88px;
  gap:16px; align-items:center; min-height:66px; padding:0 18px;
  border-bottom:1px solid var(--line);
}
.board-row:last-child { border-bottom:none; }
.board-row.top { min-height:78px; }
.rank {
  width:34px; height:34px; border-radius:10px; display:grid; place-items:center;
  background:#F5F2EE; color:var(--muted); font-weight:800;
}
.board-row:nth-child(1) .rank { background:var(--yellow-soft); color:#916D05; }
.board-row:nth-child(2) .rank { background:var(--violet-soft); color:var(--violet); }
.board-row:nth-child(3) .rank { background:var(--coral-soft); color:var(--coral); }
.student { font-weight:750; }
.track { height:9px; background:#F0ECE7; border-radius:999px; overflow:hidden; }
.fill { height:100%; border-radius:999px; min-width:5px; background:linear-gradient(90deg,var(--violet),var(--blue)); }
.points { text-align:right; font-weight:800; font-variant-numeric:tabular-nums; }
.points small { color:var(--muted); font-weight:500; }

.table-wrap {
  background:white; border:1px solid var(--line); border-radius:16px; overflow-x:auto;
}
.data-table { width:100%; border-collapse:collapse; min-width:680px; }
.data-table th {
  text-align:left; color:var(--muted); font-size:.75rem; font-weight:700;
  padding:12px 14px; background:#FFFCF8; border-bottom:1px solid var(--line);
}
.data-table td { padding:14px; border-bottom:1px solid var(--line); font-size:.9rem; }
.data-table tr:last-child td { border-bottom:none; }
.data-table td:last-child, .data-table th:last-child { text-align:right; }
.pill {
  display:inline-flex; align-items:center; padding:5px 10px;
  border-radius:999px; font-size:.75rem; font-weight:700;
}
.status-complete { color:var(--green); background:var(--green-soft); }
.status-late { color:#956B10; background:var(--yellow-soft); }
.status-missing { color:var(--red); background:var(--red-soft); }
.status-excused { color:var(--muted); background:#F0ECE7; }

.feedback-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
.feedback-card {
  background:white; border:1px solid var(--line); border-radius:16px;
  padding:18px 19px; position:relative; min-height:155px;
}
.feedback-card:nth-child(3n+1) { box-shadow:inset 4px 0 0 var(--violet); }
.feedback-card:nth-child(3n+2) { box-shadow:inset 4px 0 0 var(--coral); }
.feedback-card:nth-child(3n+3) { box-shadow:inset 4px 0 0 var(--aqua); }
.feedback-top { display:flex; justify-content:space-between; gap:15px; }
.feedback-name { font-weight:800; }
.feedback-date { color:var(--muted); font-size:.75rem; }
.feedback-copy { margin-top:19px; line-height:1.48; color:#4B485D; }
.feedback-meta { margin-top:12px; color:var(--muted); font-size:.73rem; }

.fun-note {
  margin-top:16px; background:var(--blue-soft); border:1px solid #CADCFF;
  border-radius:14px; padding:13px 15px; color:#4A5D8A; font-size:.82rem;
}

@media(max-width:820px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .hero { grid-template-columns:1fr; }
  .hero h1 { font-size:2.35rem; }
  .hero-art { min-height:180px; }
  .filter-shell { grid-template-columns:1fr; }
  .champ-grid { grid-template-columns:1fr; }
  .stats { grid-template-columns:1fr 1fr; }
  .board-row { grid-template-columns:42px 1fr 80px; padding:0 12px; gap:10px; }
  .track { display:none; }
  .feedback-grid { grid-template-columns:1fr; }
}
</style>
""", unsafe_allow_html=True)

# Custom SVG illustrations drawn in code — no emoji.
brand_svg = """
<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">
  <path d="M6 7.5C6 5.57 7.57 4 9.5 4h13C24.43 4 26 5.57 26 7.5v8C26 17.43 24.43 19 22.5 19H16l-5.5 5v-5h-1C7.57 19 6 17.43 6 15.5v-8Z" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
  <path d="M11 10h10M11 14h6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
</svg>
"""

hero_svg = """
<svg viewBox="0 0 430 250" fill="none" aria-hidden="true">
  <path d="M57 204c25-36 40-49 74-52 35-3 53 20 84 11 34-10 44-44 79-48 30-4 53 15 76 45" stroke="#7458E8" stroke-width="6" stroke-linecap="round"/>
  <rect x="54" y="52" width="126" height="82" rx="22" fill="#FFFFFF"/>
  <path d="M86 134 75 154l27-20" fill="#FFFFFF"/>
  <path d="M78 78h78M78 98h53" stroke="#FF6F61" stroke-width="7" stroke-linecap="round"/>
  <rect x="238" y="35" width="132" height="92" rx="24" fill="#35C8C3"/>
  <path d="m335 127 20 20-7-25" fill="#35C8C3"/>
  <path d="M265 66h76M265 87h48" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <circle cx="203" cy="92" r="26" fill="#F7C94B"/>
  <path d="M194 92h18M203 83v18" stroke="#22213A" stroke-width="5" stroke-linecap="round"/>
  <path d="M129 196h54v-33h42v33h54" stroke="#22213A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="156" cy="180" r="7" fill="#FF6F61"/>
  <circle cx="252" cy="180" r="7" fill="#7458E8"/>
</svg>
"""

book_svg = """
<svg viewBox="0 0 110 110" fill="none" aria-hidden="true">
  <rect x="20" y="19" width="68" height="78" rx="13" fill="#FFFFFF" stroke="#22213A" stroke-width="4"/>
  <path d="M36 38h36M36 53h27M36 68h32" stroke="#7458E8" stroke-width="5" stroke-linecap="round"/>
  <path d="m75 79 8 8 14-19" stroke="#35C8C3" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

poi_svg = """
<svg viewBox="0 0 110 110" fill="none" aria-hidden="true">
  <path d="M22 28c0-8 6-14 14-14h44c8 0 14 6 14 14v30c0 8-6 14-14 14H59L40 91V72h-4c-8 0-14-6-14-14V28Z" fill="#FFFFFF" stroke="#22213A" stroke-width="4"/>
  <path d="M42 41h33M42 55h22" stroke="#FF6F61" stroke-width="5" stroke-linecap="round"/>
</svg>
"""

st.markdown(f"""
<div class="topbar">
  <div class="brand">
    <div class="brand-mark">{brand_svg}</div>
    <div>
      <div class="brand-title">Debate Class Dashboard</div>
      <div class="brand-sub">Homework, participation, and progress</div>
    </div>
  </div>
  <div class="top-date">Student view</div>
</div>

<div class="hero">
  <div class="hero-copy">
    <h1>Show up prepared. Speak up. Level up.</h1>
    <p>A colorful snapshot of homework progress, class participation, and the ideas that move our debates forward.</p>
  </div>
  <div class="hero-art">{hero_svg}</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.15, .85])
with c1:
    uploaded = st.file_uploader(
        "Upload updated class CSV",
        type=["csv"],
        help="Optional: upload a CSV here to preview data before replacing sample_students.csv on GitHub."
    )

if uploaded is not None:
    df = pd.read_csv(uploaded)
    source = uploaded.name
else:
    df = load_default_data()
    source = "sample_students.csv"

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()

for c in ["Homework_Points","POI_Points","Class_Points","Bonus_Points"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"]).copy()
df["Student"] = df["Student"].fillna("").astype(str)
df["Homework_Status"] = df["Homework_Status"].fillna("").astype(str)
df["Feedback"] = df["Feedback"].fillna("").astype(str)
df["Total_Points"] = df[["Homework_Points","POI_Points","Class_Points","Bonus_Points"]].sum(axis=1)
df["Date_Label"] = df["Date"].dt.strftime("%b %d, %Y")

dates = (
    df[["Date","Date_Label"]].drop_duplicates()
    .sort_values("Date", ascending=False)["Date_Label"].tolist()
)
with c2:
    selected_date = st.selectbox("View class date", ["All dates"] + dates)

view = df.copy() if selected_date == "All dates" else df[df["Date_Label"] == selected_date].copy()
view_title = "All classes" if selected_date == "All dates" else selected_date

def board_for(column):
    return (
        view.groupby("Student", as_index=False)[column].sum()
        .sort_values([column,"Student"], ascending=[False,True])
        .reset_index(drop=True)
    )

homework_board = board_for("Homework_Points")
poi_board = board_for("POI_Points")
overall_board = board_for("Total_Points")

hw = homework_board.iloc[0] if not homework_board.empty else None
poi = poi_board.iloc[0] if not poi_board.empty else None

complete_count = (view["Homework_Status"].str.lower() == "complete").sum()
completion_rate = complete_count / len(view) * 100 if len(view) else 0

if hw is not None and poi is not None:
    st.markdown(f"""
    <div class="champ-grid">
      <div class="champ-card homework">
        <div class="champ-top">
          <div class="champ-label">Homework Champion</div>
          <div class="champ-period">{escape(view_title)}</div>
        </div>
        <div class="champ-name">{escape(str(hw["Student"]))}</div>
        <div class="champ-score">{hw["Homework_Points"]:.0f} homework points</div>
        <div class="champ-icon">{book_svg}</div>
      </div>
      <div class="champ-card poi">
        <div class="champ-top">
          <div class="champ-label">POI Champion</div>
          <div class="champ-period">{escape(view_title)}</div>
        </div>
        <div class="champ-name">{escape(str(poi["Student"]))}</div>
        <div class="champ-score">{poi["POI_Points"]:.0f} POI points</div>
        <div class="champ-icon">{poi_svg}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="stats">
  <div class="stat"><div class="stat-value">{view["Student"].nunique()}</div><div class="stat-label">Students</div></div>
  <div class="stat"><div class="stat-value">{completion_rate:.0f}%</div><div class="stat-label">Homework complete</div></div>
  <div class="stat"><div class="stat-value">{view["POI_Points"].sum():.0f}</div><div class="stat-label">POI points</div></div>
  <div class="stat"><div class="stat-value">{view["Total_Points"].sum():.0f}</div><div class="stat-label">Total points</div></div>
</div>
""", unsafe_allow_html=True)

def leaderboard(board, column):
    if board.empty:
        return "<div>No scores yet.</div>"
    max_value = max(float(board[column].max()), 1)
    rows = []
    for i, row in board.iterrows():
        pct = max(3, float(row[column]) / max_value * 100)
        rows.append(
            f'<div class="board-row {"top" if i < 3 else ""}">'
            f'<div class="rank">{i+1}</div>'
            f'<div class="student">{escape(str(row["Student"]))}</div>'
            f'<div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div>'
            f'<div class="points">{row[column]:.0f} <small>pts</small></div>'
            f'</div>'
        )
    return '<div class="board">' + "".join(rows) + "</div>"

tab1, tab2, tab3, tab4 = st.tabs(["Overall", "Homework", "POI Champion", "Feedback"])

with tab1:
    st.markdown(
        f'<div class="section-head"><h2>Overall standings</h2>'
        f'<p>{escape(view_title)} · homework + POI + class + bonus</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(leaderboard(overall_board, "Total_Points"), unsafe_allow_html=True)

with tab2:
    st.markdown(
        f'<div class="section-head"><h2>Homework standings</h2>'
        f'<p>{escape(view_title)}</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(leaderboard(homework_board, "Homework_Points"), unsafe_allow_html=True)

    status_rows = []
    for _, row in view.sort_values(["Date","Student"], ascending=[False,True]).iterrows():
        label, cls = STATUS.get(
            row["Homework_Status"],
            (row["Homework_Status"] or "Not set", "status-excused")
        )
        status_rows.append(
            f'<tr><td>{escape(str(row["Student"]))}</td>'
            f'<td>{escape(str(row["Date_Label"]))}</td>'
            f'<td><span class="pill {cls}">{escape(label)}</span></td>'
            f'<td>{row["Homework_Points"]:.0f}</td></tr>'
        )

    st.markdown(
        '<div class="section-head"><h2>Homework status</h2>'
        '<p>By class date</p></div>'
        '<div class="table-wrap"><table class="data-table">'
        '<thead><tr><th>Student</th><th>Date</th><th>Status</th><th>Points</th></tr></thead>'
        '<tbody>' + "".join(status_rows) + '</tbody></table></div>',
        unsafe_allow_html=True
    )

with tab3:
    st.markdown(
        f'<div class="section-head"><h2>POI standings</h2>'
        f'<p>{escape(view_title)}</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(leaderboard(poi_board, "POI_Points"), unsafe_allow_html=True)
    st.markdown(
        '<div class="fun-note">POI points recognize active debate participation. '
        'Use the same scoring rule consistently from class to class.</div>',
        unsafe_allow_html=True
    )

with tab4:
    st.markdown(
        f'<div class="section-head"><h2>Teacher feedback</h2>'
        f'<p>{escape(view_title)}</p></div>',
        unsafe_allow_html=True
    )
    cards = []
    for _, row in view.sort_values(["Date","Student"], ascending=[False,True]).iterrows():
        feedback = row["Feedback"].strip() or "No written feedback for this class."
        cards.append(
            f'<div class="feedback-card">'
            f'<div class="feedback-top"><div class="feedback-name">{escape(str(row["Student"]))}</div>'
            f'<div class="feedback-date">{escape(str(row["Date_Label"]))}</div></div>'
            f'<div class="feedback-copy">{escape(feedback)}</div>'
            f'<div class="feedback-meta">Homework {row["Homework_Points"]:.0f} · '
            f'POI {row["POI_Points"]:.0f} · Class {row["Class_Points"]:.0f} · '
            f'Bonus {row["Bonus_Points"]:.0f}</div></div>'
        )
    st.markdown('<div class="feedback-grid">' + "".join(cards) + "</div>", unsafe_allow_html=True)
    st.caption("Feedback shown here is visible to anyone who can access the dashboard.")

st.markdown(
    f'<div style="margin-top:26px;color:#8B8799;font-size:.74rem;">'
    f'Data source: {escape(source)}</div>',
    unsafe_allow_html=True
)
