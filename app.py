import streamlit as st
import pandas as pd
from html import escape

st.set_page_config(page_title="Debate Arena", page_icon="•", layout="wide", initial_sidebar_state="collapsed")

REQUIRED = ["Date", "Student", "Homework_Status", "Homework_Points", "POI_Points", "Class_Points", "Bonus_Points", "Feedback"]
STATUS = {
    "Complete": ("Complete", "status-complete"),
    "Late": ("Late", "status-late"),
    "Missing": ("Missing", "status-missing"),
    "Excused": ("Excused", "status-excused"),
}

@st.cache_data
def load_example():
    return pd.read_csv("sample_students.csv")

st.markdown(r"""
<style>
:root {
  --bg: #F5F2EA; --surface: #FCFBF7; --surface-2: #EFECE4;
  --ink: #172033; --muted: #687083; --line: #D9D5CB;
  --accent: #3157D5; --success: #26735F; --success-soft: #E5F1EC;
  --warning: #9A641C; --warning-soft: #F7ECD8;
  --danger: #A34646; --danger-soft: #F6E7E5;
  --shadow: 0 10px 28px rgba(23, 32, 51, 0.08);
}
html, body, [class*="css"] { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.stApp { background: var(--bg); color: var(--ink); }
.block-container { max-width: 1180px; padding-top: 1.6rem; padding-bottom: 4rem; }
#MainMenu, footer, header { visibility: hidden; }
::selection { background: #C9D4FF; color: var(--ink); }
div[data-baseweb="select"] > div, section[data-testid="stFileUploaderDropzone"] { background: var(--surface) !important; border-color: var(--line) !important; border-radius: 10px !important; box-shadow: none !important; }
button[kind="secondary"], button[kind="primary"] { border-radius: 9px !important; }
:focus-visible { outline: 3px solid rgba(49,87,213,.28) !important; outline-offset: 2px !important; }
button[data-baseweb="tab"] { font-weight: 650 !important; color: var(--muted) !important; padding-left: .9rem !important; padding-right: .9rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--ink) !important; }
div[data-baseweb="tab-highlight"] { background: var(--accent) !important; }
.app-header { display:flex; align-items:flex-end; justify-content:space-between; gap:24px; border-bottom:1px solid var(--line); padding:8px 0 22px; margin-bottom:22px; }
.brand-lockup { display:flex; align-items:center; gap:12px; }
.brand-mark { width:38px; height:38px; border-radius:10px; background:var(--ink); color:white; display:grid; place-items:center; }
.brand-mark svg { width:21px; height:21px; }
.brand-title { font-size:1.42rem; font-weight:780; letter-spacing:-.025em; }
.brand-sub { color:var(--muted); font-size:.88rem; margin-top:2px; }
.period-label { color:var(--muted); font-size:.86rem; font-variant-numeric:tabular-nums; }
.intro { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(250px,.65fr); gap:32px; align-items:end; margin:8px 0 26px; }
.intro h1 { font-size:3rem; line-height:.98; letter-spacing:-.045em; margin:0; max-width:760px; }
.intro p { color:var(--muted); margin:0; line-height:1.55; max-width:42ch; }
.champions { display:grid; grid-template-columns:1fr 1fr; border:1px solid var(--line); border-radius:14px; overflow:hidden; background:var(--surface); box-shadow:var(--shadow); margin:10px 0 24px; }
.champion { padding:24px 26px 22px; min-height:190px; position:relative; }
.champion + .champion { border-left:1px solid var(--line); }
.champion-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:32px; }
.champion-type { display:flex; align-items:center; gap:9px; font-weight:700; font-size:.9rem; }
.icon-box { width:30px; height:30px; border-radius:8px; display:grid; place-items:center; background:var(--surface-2); color:var(--ink); }
.icon-box svg { width:17px; height:17px; stroke-width:1.8; }
.champion-rank { color:var(--muted); font-size:.78rem; }
.champion-name { font-size:2.05rem; font-weight:780; letter-spacing:-.035em; line-height:1.05; }
.champion-score { color:var(--muted); margin-top:7px; font-variant-numeric:tabular-nums; }
.champion-accent { position:absolute; left:0; bottom:0; height:4px; background:var(--accent); }
.poi .champion-accent { background:var(--ink); }
.stat-strip { display:grid; grid-template-columns:repeat(4,1fr); border-top:1px solid var(--line); border-bottom:1px solid var(--line); margin:4px 0 28px; }
.stat { padding:16px 18px 15px 0; }
.stat + .stat { border-left:1px solid var(--line); padding-left:18px; }
.stat-value { font-size:1.45rem; font-weight:760; letter-spacing:-.02em; font-variant-numeric:tabular-nums; }
.stat-label { color:var(--muted); font-size:.8rem; margin-top:2px; }
.section-head { display:flex; align-items:end; justify-content:space-between; gap:20px; margin:22px 0 12px; }
.section-head h2 { font-size:1.45rem; margin:0; letter-spacing:-.025em; }
.section-head p { margin:0; color:var(--muted); font-size:.84rem; }
.board { border-top:1px solid var(--line); }
.board-row { display:grid; grid-template-columns:56px minmax(150px,1.2fr) minmax(180px,2fr) 90px; align-items:center; gap:16px; min-height:66px; border-bottom:1px solid var(--line); }
.board-row.top { min-height:76px; }
.rank { color:var(--muted); font-size:.9rem; font-variant-numeric:tabular-nums; }
.rank strong { color:var(--ink); font-size:1.2rem; }
.student { font-weight:700; }
.top .student { font-size:1.08rem; }
.track { height:7px; background:#E2DED4; border-radius:999px; overflow:hidden; }
.fill { height:100%; background:var(--accent); border-radius:999px; min-width:4px; }
.points { text-align:right; font-weight:730; font-variant-numeric:tabular-nums; }
.points small { color:var(--muted); font-weight:500; }
.table-wrap { overflow-x:auto; border-top:1px solid var(--line); }
.data-table { width:100%; border-collapse:collapse; min-width:720px; }
.data-table th { text-align:left; color:var(--muted); font-size:.76rem; font-weight:650; padding:11px 10px; border-bottom:1px solid var(--line); }
.data-table td { padding:14px 10px; border-bottom:1px solid var(--line); font-size:.9rem; }
.data-table td:last-child, .data-table th:last-child { text-align:right; font-variant-numeric:tabular-nums; }
.pill { display:inline-flex; align-items:center; gap:7px; padding:5px 9px; border-radius:999px; font-size:.76rem; font-weight:650; }
.pill:before { content:""; width:6px; height:6px; border-radius:50%; background:currentColor; }
.status-complete { color:var(--success); background:var(--success-soft); }
.status-late { color:var(--warning); background:var(--warning-soft); }
.status-missing { color:var(--danger); background:var(--danger-soft); }
.status-excused { color:var(--muted); background:var(--surface-2); }
.feedback-list { border-top:1px solid var(--line); }
.feedback-item { display:grid; grid-template-columns:minmax(130px,.6fr) minmax(0,2fr); gap:30px; padding:21px 0; border-bottom:1px solid var(--line); }
.feedback-name { font-weight:720; }
.feedback-date { color:var(--muted); font-size:.78rem; margin-top:3px; }
.feedback-copy { line-height:1.55; color:#3A4253; max-width:75ch; }
.feedback-meta { margin-top:8px; color:var(--muted); font-size:.76rem; font-variant-numeric:tabular-nums; }
.note { padding:14px 16px; border:1px solid var(--line); background:var(--surface); border-radius:10px; color:var(--muted); }
@media (max-width:800px) {
  .block-container { padding-left:1rem; padding-right:1rem; padding-top:1rem; }
  .app-header { align-items:flex-start; }
  .intro { grid-template-columns:1fr; gap:12px; }
  .intro h1 { font-size:2.35rem; }
  .champions { grid-template-columns:1fr; }
  .champion + .champion { border-left:none; border-top:1px solid var(--line); }
  .stat-strip { grid-template-columns:1fr 1fr; }
  .stat:nth-child(3) { border-left:none; }
  .stat:nth-child(n+3) { border-top:1px solid var(--line); }
  .board-row { grid-template-columns:40px minmax(110px,1fr) 90px; gap:10px; }
  .board-row .track { display:none; }
  .feedback-item { grid-template-columns:1fr; gap:8px; }
}
</style>
""", unsafe_allow_html=True)

book_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'
mic_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/></svg>'
mark_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18 18 6"/><path d="M8 6h10v10"/></svg>'

st.markdown(f'<div class="app-header"><div class="brand-lockup"><div class="brand-mark">{mark_icon}</div><div><div class="brand-title">Debate Arena</div><div class="brand-sub">Class progress & participation</div></div></div><div class="period-label">Student dashboard</div></div>', unsafe_allow_html=True)

control_a, control_b = st.columns([1.15, .85])
with control_a:
    uploaded = st.file_uploader("Update class data", type=["csv"], help="Upload your latest CSV. Sample data is shown until you upload one.")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    source = uploaded.name
else:
    df = load_example()
    source = "Sample data"

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()

for c in ["Homework_Points", "POI_Points", "Class_Points", "Bonus_Points"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"]).copy()
df["Student"] = df["Student"].fillna("Unknown student").astype(str)
df["Homework_Status"] = df["Homework_Status"].fillna("").astype(str)
df["Feedback"] = df["Feedback"].fillna("").astype(str)
df["Total_Points"] = df[["Homework_Points", "POI_Points", "Class_Points", "Bonus_Points"]].sum(axis=1)
df["Date_Label"] = df["Date"].dt.strftime("%b %d, %Y")
labels = df[["Date", "Date_Label"]].drop_duplicates().sort_values("Date", ascending=False)["Date_Label"].tolist()
with control_b:
    selected_date = st.selectbox("Class date", ["All dates"] + labels)
view = df.copy() if selected_date == "All dates" else df[df["Date_Label"] == selected_date].copy()
view_title = "Season to date" if selected_date == "All dates" else selected_date

def board_for(column):
    return view.groupby("Student", as_index=False)[column].sum().sort_values([column, "Student"], ascending=[False, True]).reset_index(drop=True)

homework_board = board_for("Homework_Points")
poi_board = board_for("POI_Points")
overall_board = board_for("Total_Points")
hw_champ = homework_board.iloc[0] if len(homework_board) else None
poi_champ = poi_board.iloc[0] if len(poi_board) else None
complete_count = (view["Homework_Status"].str.lower() == "complete").sum()
completion_rate = (complete_count / len(view) * 100) if len(view) else 0

st.markdown('<div class="intro"><h1>Every class leaves a mark.</h1><p>Track preparation, reward sharp participation, and make progress visible without turning the class into a spreadsheet.</p></div>', unsafe_allow_html=True)

if hw_champ is not None and poi_champ is not None:
    hw_max = max(float(homework_board["Homework_Points"].max()), 1)
    poi_max = max(float(poi_board["POI_Points"].max()), 1)
    champions_html = f'''
    <div class="champions">
      <div class="champion homework">
        <div class="champion-top"><div class="champion-type"><span class="icon-box">{book_icon}</span>Homework Champion</div><div class="champion-rank">{escape(view_title)}</div></div>
        <div class="champion-name">{escape(str(hw_champ['Student']))}</div>
        <div class="champion-score">{hw_champ['Homework_Points']:.0f} homework points</div>
        <div class="champion-accent" style="width:{min(100, hw_champ['Homework_Points']/hw_max*100):.0f}%"></div>
      </div>
      <div class="champion poi">
        <div class="champion-top"><div class="champion-type"><span class="icon-box">{mic_icon}</span>POI Champion</div><div class="champion-rank">{escape(view_title)}</div></div>
        <div class="champion-name">{escape(str(poi_champ['Student']))}</div>
        <div class="champion-score">{poi_champ['POI_Points']:.0f} POI points</div>
        <div class="champion-accent" style="width:{min(100, poi_champ['POI_Points']/poi_max*100):.0f}%"></div>
      </div>
    </div>
    '''
    st.markdown(champions_html, unsafe_allow_html=True)

stats_html = f'''
<div class="stat-strip">
  <div class="stat"><div class="stat-value">{view['Student'].nunique()}</div><div class="stat-label">students</div></div>
  <div class="stat"><div class="stat-value">{completion_rate:.0f}%</div><div class="stat-label">homework complete</div></div>
  <div class="stat"><div class="stat-value">{view['POI_Points'].sum():.0f}</div><div class="stat-label">POI points</div></div>
  <div class="stat"><div class="stat-value">{view['Total_Points'].sum():.0f}</div><div class="stat-label">points awarded</div></div>
</div>
'''
st.markdown(stats_html, unsafe_allow_html=True)

tab_overall, tab_hw, tab_poi, tab_feedback = st.tabs(["Overall", "Homework", "POI Champion", "Feedback"])

def leaderboard_html(board, value_col, label):
    if board.empty:
        return '<div class="note">No results for this date yet.</div>'
    max_val = max(float(board[value_col].max()), 1)
    rows = []
    for i, row in board.iterrows():
        rank = i + 1
        pct = max(2, float(row[value_col]) / max_val * 100)
        top_class = "top" if rank <= 3 else ""
        rows.append(f'<div class="board-row {top_class}"><div class="rank"><strong>{rank}</strong></div><div class="student">{escape(str(row["Student"]))}</div><div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div><div class="points">{row[value_col]:.0f} <small>{label}</small></div></div>')
    return '<div class="board">' + ''.join(rows) + '</div>'

with tab_overall:
    st.markdown(f'<div class="section-head"><h2>Overall standings</h2><p>{escape(view_title)} · homework + POI + class + bonus</p></div>', unsafe_allow_html=True)
    st.markdown(leaderboard_html(overall_board, "Total_Points", "pts"), unsafe_allow_html=True)

with tab_hw:
    st.markdown(f'<div class="section-head"><h2>Homework standings</h2><p>Preparation points · {escape(view_title)}</p></div>', unsafe_allow_html=True)
    st.markdown(leaderboard_html(homework_board, "Homework_Points", "pts"), unsafe_allow_html=True)
    st.markdown('<div class="section-head"><h2>Submission status</h2><p>Most recent records in this view</p></div>', unsafe_allow_html=True)
    rows = []
    for _, row in view.sort_values(["Date", "Student"], ascending=[False, True]).iterrows():
        label, cls = STATUS.get(row["Homework_Status"], (row["Homework_Status"] or "Not set", "status-excused"))
        rows.append(f'<tr><td>{escape(str(row["Student"]))}</td><td>{escape(str(row["Date_Label"]))}</td><td><span class="pill {cls}">{escape(str(label))}</span></td><td>{row["Homework_Points"]:.0f}</td></tr>')
    table = '<div class="table-wrap"><table class="data-table"><thead><tr><th>Student</th><th>Date</th><th>Status</th><th>Points</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
    st.markdown(table, unsafe_allow_html=True)

with tab_poi:
    st.markdown(f'<div class="section-head"><h2>POI standings</h2><p>Questions, challenges, and engagement · {escape(view_title)}</p></div>', unsafe_allow_html=True)
    st.markdown(leaderboard_html(poi_board, "POI_Points", "pts"), unsafe_allow_html=True)
    st.markdown('<div class="note" style="margin-top:18px">POI points can reward offering a strong POI, answering one well, or both. Keep the rule consistent across the class.</div>', unsafe_allow_html=True)

with tab_feedback:
    st.markdown(f'<div class="section-head"><h2>Teacher feedback</h2><p>{escape(view_title)}</p></div>', unsafe_allow_html=True)
    feedback_rows = []
    for _, row in view.sort_values(["Date", "Student"], ascending=[False, True]).iterrows():
        copy = row["Feedback"].strip() or "No written feedback for this class."
        feedback_rows.append(f'<div class="feedback-item"><div><div class="feedback-name">{escape(str(row["Student"]))}</div><div class="feedback-date">{escape(str(row["Date_Label"]))}</div></div><div><div class="feedback-copy">{escape(copy)}</div><div class="feedback-meta">Homework {row["Homework_Points"]:.0f} · POI {row["POI_Points"]:.0f} · Class {row["Class_Points"]:.0f} · Bonus {row["Bonus_Points"]:.0f}</div></div></div>')
    st.markdown('<div class="feedback-list">' + ''.join(feedback_rows) + '</div>', unsafe_allow_html=True)
    st.caption("Feedback is visible to anyone who can access this app. Use a private version if you want individual feedback hidden from classmates.")

st.markdown(f'<div style="margin-top:28px;color:#7A8090;font-size:.75rem">Data source: {escape(source)}</div>', unsafe_allow_html=True)
