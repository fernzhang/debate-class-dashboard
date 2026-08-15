
import streamlit as st
import pandas as pd
from html import escape

st.set_page_config(
    page_title="Debate Arena",
    page_icon="🏆",
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

@st.cache_data
def load_example():
    return pd.read_csv("sample_students.csv")

st.markdown("""
<style>
:root {
  --bg:#F5F2EA;
  --surface:#FCFBF7;
  --surface-2:#ECE8DE;
  --ink:#182033;
  --muted:#6B7280;
  --line:#D8D3C8;
  --accent:#3157D5;
  --accent-soft:#E7ECFF;
  --success:#276A58;
  --success-soft:#E4F1EB;
  --warning:#9A641C;
  --warning-soft:#F6ECD8;
  --danger:#9F4545;
  --danger-soft:#F5E6E4;
}
html, body, [class*="css"] {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.stApp { background:var(--bg); color:var(--ink); }
.block-container { max-width:1160px; padding-top:1.5rem; padding-bottom:4rem; }
#MainMenu, footer, header { visibility:hidden; }

.app-header {
  display:flex; justify-content:space-between; align-items:center;
  border-bottom:1px solid var(--line); padding:4px 0 18px; margin-bottom:24px;
}
.brand { display:flex; gap:12px; align-items:center; }
.brand-mark {
  width:40px; height:40px; border-radius:10px; background:var(--ink); color:white;
  display:grid; place-items:center; font-weight:800; font-size:18px;
}
.brand-title { font-size:1.45rem; font-weight:800; letter-spacing:-.025em; }
.brand-sub { color:var(--muted); font-size:.86rem; margin-top:2px; }
.period { color:var(--muted); font-size:.84rem; }

.intro {
  display:grid; grid-template-columns:1.5fr .7fr; gap:30px; align-items:end;
  margin:6px 0 28px;
}
.intro h1 {
  font-size:3rem; line-height:1; letter-spacing:-.045em; margin:0; max-width:720px;
}
.intro p { color:var(--muted); line-height:1.55; margin:0; max-width:40ch; }

.controls {
  border:1px solid var(--line); background:var(--surface); border-radius:12px;
  padding:16px 18px; margin-bottom:22px;
}

.champions {
  display:grid; grid-template-columns:1fr 1fr;
  border:1px solid var(--line); background:var(--surface);
  border-radius:14px; overflow:hidden; margin-bottom:22px;
  box-shadow:0 10px 28px rgba(24,32,51,.07);
}
.champion { padding:24px 26px 22px; min-height:170px; position:relative; }
.champion + .champion { border-left:1px solid var(--line); }
.champion-label { font-size:.84rem; font-weight:700; color:var(--muted); }
.champion-name { font-size:2rem; font-weight:800; letter-spacing:-.035em; margin-top:34px; }
.champion-score { color:var(--muted); margin-top:6px; }
.champion-bar { position:absolute; left:0; bottom:0; height:4px; background:var(--accent); }
.poi .champion-bar { background:var(--ink); }

.stat-strip {
  display:grid; grid-template-columns:repeat(4,1fr);
  border-top:1px solid var(--line); border-bottom:1px solid var(--line);
  margin:0 0 28px;
}
.stat { padding:15px 18px 14px 0; }
.stat + .stat { border-left:1px solid var(--line); padding-left:18px; }
.stat-value { font-size:1.45rem; font-weight:780; font-variant-numeric:tabular-nums; }
.stat-label { color:var(--muted); font-size:.78rem; margin-top:2px; }

.section-head {
  display:flex; justify-content:space-between; align-items:end;
  margin:22px 0 10px; gap:18px;
}
.section-head h2 { margin:0; font-size:1.4rem; letter-spacing:-.025em; }
.section-head p { margin:0; color:var(--muted); font-size:.82rem; }

.board { border-top:1px solid var(--line); }
.board-row {
  display:grid; grid-template-columns:54px 1.2fr 2fr 90px;
  gap:16px; align-items:center; min-height:64px; border-bottom:1px solid var(--line);
}
.board-row.top { min-height:74px; }
.rank { color:var(--muted); font-variant-numeric:tabular-nums; }
.rank strong { color:var(--ink); font-size:1.2rem; }
.student { font-weight:700; }
.track { height:7px; background:#E2DED4; border-radius:999px; overflow:hidden; }
.fill { height:100%; background:var(--accent); border-radius:999px; min-width:4px; }
.points { text-align:right; font-weight:730; font-variant-numeric:tabular-nums; }
.points small { color:var(--muted); font-weight:500; }

.table-wrap { overflow-x:auto; border-top:1px solid var(--line); }
.data-table { width:100%; border-collapse:collapse; min-width:680px; }
.data-table th {
  text-align:left; color:var(--muted); font-size:.76rem; padding:10px;
  border-bottom:1px solid var(--line);
}
.data-table td { padding:14px 10px; border-bottom:1px solid var(--line); font-size:.9rem; }
.data-table td:last-child, .data-table th:last-child { text-align:right; }

.pill {
  display:inline-flex; align-items:center; gap:6px; padding:5px 9px;
  border-radius:999px; font-size:.76rem; font-weight:650;
}
.pill:before { content:""; width:6px; height:6px; border-radius:50%; background:currentColor; }
.status-complete { color:var(--success); background:var(--success-soft); }
.status-late { color:var(--warning); background:var(--warning-soft); }
.status-missing { color:var(--danger); background:var(--danger-soft); }
.status-excused { color:var(--muted); background:var(--surface-2); }

.feedback-list { border-top:1px solid var(--line); }
.feedback-item {
  display:grid; grid-template-columns:minmax(140px,.6fr) minmax(0,2fr);
  gap:26px; padding:20px 0; border-bottom:1px solid var(--line);
}
.feedback-name { font-weight:720; }
.feedback-date { color:var(--muted); font-size:.78rem; margin-top:3px; }
.feedback-copy { color:#3A4253; line-height:1.55; max-width:72ch; }
.feedback-meta { margin-top:8px; color:var(--muted); font-size:.75rem; }

button[data-baseweb="tab"] { font-weight:650 !important; color:var(--muted) !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:var(--ink) !important; }
div[data-baseweb="tab-highlight"] { background:var(--accent) !important; }

@media (max-width:800px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .intro { grid-template-columns:1fr; gap:10px; }
  .intro h1 { font-size:2.35rem; }
  .champions { grid-template-columns:1fr; }
  .champion + .champion { border-left:none; border-top:1px solid var(--line); }
  .stat-strip { grid-template-columns:1fr 1fr; }
  .stat:nth-child(3) { border-left:none; }
  .stat:nth-child(n+3) { border-top:1px solid var(--line); }
  .board-row { grid-template-columns:40px 1fr 80px; gap:10px; }
  .board-row .track { display:none; }
  .feedback-item { grid-template-columns:1fr; gap:8px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
  <div class="brand">
    <div class="brand-mark">D</div>
    <div>
      <div class="brand-title">Debate Arena</div>
      <div class="brand-sub">Class progress & participation</div>
    </div>
  </div>
  <div class="period">Student dashboard</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro">
  <h1>Every class leaves a mark.</h1>
  <p>Track preparation, reward sharp participation, and make progress visible without turning the class into a spreadsheet.</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.15, .85])
with c1:
    uploaded = st.file_uploader(
        "Update class data",
        type=["csv"],
        help="Upload the latest class CSV. Sample data is shown until you upload one."
    )

if uploaded is not None:
    df = pd.read_csv(uploaded)
    source = uploaded.name
else:
    df = load_example()
    source = "sample_students.csv"

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()

for col in ["Homework_Points", "POI_Points", "Class_Points", "Bonus_Points"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"]).copy()
df["Student"] = df["Student"].fillna("").astype(str)
df["Homework_Status"] = df["Homework_Status"].fillna("").astype(str)
df["Feedback"] = df["Feedback"].fillna("").astype(str)
df["Total_Points"] = df[[
    "Homework_Points","POI_Points","Class_Points","Bonus_Points"
]].sum(axis=1)
df["Date_Label"] = df["Date"].dt.strftime("%b %d, %Y")

date_labels = (
    df[["Date","Date_Label"]]
    .drop_duplicates()
    .sort_values("Date", ascending=False)["Date_Label"]
    .tolist()
)

with c2:
    selected_date = st.selectbox("Class date", ["All dates"] + date_labels)

view = df.copy() if selected_date == "All dates" else df[df["Date_Label"] == selected_date].copy()
view_title = "Season to date" if selected_date == "All dates" else selected_date

def make_board(column):
    return (
        view.groupby("Student", as_index=False)[column]
        .sum()
        .sort_values([column, "Student"], ascending=[False, True])
        .reset_index(drop=True)
    )

homework_board = make_board("Homework_Points")
poi_board = make_board("POI_Points")
overall_board = make_board("Total_Points")

hw_champ = homework_board.iloc[0] if not homework_board.empty else None
poi_champ = poi_board.iloc[0] if not poi_board.empty else None

complete_count = (view["Homework_Status"].str.lower() == "complete").sum()
completion_rate = (complete_count / len(view) * 100) if len(view) else 0

if hw_champ is not None and poi_champ is not None:
    hw_max = max(float(homework_board["Homework_Points"].max()), 1)
    poi_max = max(float(poi_board["POI_Points"].max()), 1)

    st.markdown(f"""
    <div class="champions">
      <div class="champion">
        <div class="champion-label">Homework Champion · {escape(view_title)}</div>
        <div class="champion-name">{escape(str(hw_champ["Student"]))}</div>
        <div class="champion-score">{hw_champ["Homework_Points"]:.0f} homework points</div>
        <div class="champion-bar" style="width:{min(100, hw_champ['Homework_Points']/hw_max*100):.0f}%"></div>
      </div>
      <div class="champion poi">
        <div class="champion-label">POI Champion · {escape(view_title)}</div>
        <div class="champion-name">{escape(str(poi_champ["Student"]))}</div>
        <div class="champion-score">{poi_champ["POI_Points"]:.0f} POI points</div>
        <div class="champion-bar" style="width:{min(100, poi_champ['POI_Points']/poi_max*100):.0f}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="stat-strip">
  <div class="stat"><div class="stat-value">{view["Student"].nunique()}</div><div class="stat-label">students</div></div>
  <div class="stat"><div class="stat-value">{completion_rate:.0f}%</div><div class="stat-label">homework complete</div></div>
  <div class="stat"><div class="stat-value">{view["POI_Points"].sum():.0f}</div><div class="stat-label">POI points</div></div>
  <div class="stat"><div class="stat-value">{view["Total_Points"].sum():.0f}</div><div class="stat-label">points awarded</div></div>
</div>
""", unsafe_allow_html=True)

def leaderboard_html(board, value_col, unit="pts"):
    if board.empty:
        return '<div>No results yet.</div>'
    max_val = max(float(board[value_col].max()), 1)
    rows = []
    for i, row in board.iterrows():
        rank = i + 1
        pct = max(2, float(row[value_col]) / max_val * 100)
        top_class = "top" if rank <= 3 else ""
        rows.append(
            f'<div class="board-row {top_class}">'
            f'<div class="rank"><strong>{rank}</strong></div>'
            f'<div class="student">{escape(str(row["Student"]))}</div>'
            f'<div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div>'
            f'<div class="points">{row[value_col]:.0f} <small>{unit}</small></div>'
            f'</div>'
        )
    return '<div class="board">' + ''.join(rows) + '</div>'

tab1, tab2, tab3, tab4 = st.tabs(["Overall", "Homework", "POI Champion", "Feedback"])

with tab1:
    st.markdown(
        f'<div class="section-head"><h2>Overall standings</h2>'
        f'<p>{escape(view_title)} · homework + POI + class + bonus</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(leaderboard_html(overall_board, "Total_Points"), unsafe_allow_html=True)

with tab2:
    st.markdown(
        f'<div class="section-head"><h2>Homework standings</h2>'
        f'<p>Preparation points · {escape(view_title)}</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(leaderboard_html(homework_board, "Homework_Points"), unsafe_allow_html=True)

    rows = []
    for _, row in view.sort_values(["Date","Student"], ascending=[False,True]).iterrows():
        label, cls = STATUS.get(
            row["Homework_Status"],
            (row["Homework_Status"] or "Not set", "status-excused")
        )
        rows.append(
            f'<tr>'
            f'<td>{escape(str(row["Student"]))}</td>'
            f'<td>{escape(str(row["Date_Label"]))}</td>'
            f'<td><span class="pill {cls}">{escape(label)}</span></td>'
            f'<td>{row["Homework_Points"]:.0f}</td>'
            f'</tr>'
        )

    st.markdown(
        '<div class="section-head"><h2>Submission status</h2>'
        '<p>Records in this view</p></div>'
        '<div class="table-wrap"><table class="data-table">'
        '<thead><tr><th>Student</th><th>Date</th><th>Status</th><th>Points</th></tr></thead>'
        '<tbody>' + ''.join(rows) + '</tbody></table></div>',
        unsafe_allow_html=True
    )

with tab3:
    st.markdown(
        f'<div class="section-head"><h2>POI standings</h2>'
        f'<p>Questions, challenges, and engagement · {escape(view_title)}</p></div>',
        unsafe_allow_html=True
    )
    st.markdown(leaderboard_html(poi_board, "POI_Points"), unsafe_allow_html=True)

with tab4:
    st.markdown(
        f'<div class="section-head"><h2>Teacher feedback</h2>'
        f'<p>{escape(view_title)}</p></div>',
        unsafe_allow_html=True
    )

    items = []
    for _, row in view.sort_values(["Date","Student"], ascending=[False,True]).iterrows():
        feedback = row["Feedback"].strip() or "No written feedback for this class."
        items.append(
            f'<div class="feedback-item">'
            f'<div><div class="feedback-name">{escape(str(row["Student"]))}</div>'
            f'<div class="feedback-date">{escape(str(row["Date_Label"]))}</div></div>'
            f'<div><div class="feedback-copy">{escape(feedback)}</div>'
            f'<div class="feedback-meta">'
            f'Homework {row["Homework_Points"]:.0f} · '
            f'POI {row["POI_Points"]:.0f} · '
            f'Class {row["Class_Points"]:.0f} · '
            f'Bonus {row["Bonus_Points"]:.0f}'
            f'</div></div></div>'
        )

    st.markdown('<div class="feedback-list">' + ''.join(items) + '</div>', unsafe_allow_html=True)
    st.caption("Feedback is visible to anyone who can access this app.")

st.markdown(
    f'<div style="margin-top:28px;color:#7A8090;font-size:.75rem">'
    f'Data source: {escape(source)}</div>',
    unsafe_allow_html=True
)
