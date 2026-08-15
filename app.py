
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Debate Class Game Dashboard",
    page_icon="🏆",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #f8fafc, #eef2ff);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.25rem;
    }
    .hero p {
        margin: .45rem 0 0 0;
        color: #475569;
        font-size: 1rem;
    }
    .champion-card {
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1.2rem 1.3rem;
        background: white;
        min-height: 150px;
    }
    .champion-label {
        color: #64748b;
        font-size: .85rem;
        text-transform: uppercase;
        letter-spacing: .05em;
        margin-bottom: .35rem;
    }
    .champion-name {
        font-size: 1.5rem;
        font-weight: 750;
        margin-bottom: .25rem;
    }
    .champion-score {
        font-size: 1.05rem;
        color: #334155;
    }
    .student-card {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: .8rem;
        background: white;
    }
    .student-name {
        font-size: 1.2rem;
        font-weight: 700;
    }
    .feedback {
        color: #475569;
        margin-top: .4rem;
    }
    .small-label {
        font-size: .78rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: .04em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏆 Debate Class Game Dashboard</h1>
    <p>Homework progress, POI participation, class points, champions, and teacher feedback.</p>
</div>
""", unsafe_allow_html=True)

REQUIRED = [
    "Date", "Student", "Homework_Status",
    "Homework_Points", "POI_Points",
    "Class_Points", "Bonus_Points", "Feedback"
]

STATUS_ICONS = {
    "Complete": "✅",
    "Late": "🟡",
    "Missing": "❌",
    "Excused": "➖"
}

@st.cache_data
def load_example():
    return pd.read_csv("sample_students.csv")

uploaded = st.sidebar.file_uploader("Upload class CSV", type=["csv"])
st.sidebar.caption("Upload a new CSV whenever you want to refresh the dashboard.")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    source = uploaded.name
else:
    df = load_example()
    source = "sample_students.csv"

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error("Your CSV is missing these columns: " + ", ".join(missing))
    st.stop()

for c in ["Homework_Points", "POI_Points", "Class_Points", "Bonus_Points"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"]).copy()

df["Student"] = df["Student"].astype(str)
df["Homework_Status"] = df["Homework_Status"].fillna("").astype(str)
df["Feedback"] = df["Feedback"].fillna("").astype(str)

df["Total_Points"] = (
    df["Homework_Points"]
    + df["POI_Points"]
    + df["Class_Points"]
    + df["Bonus_Points"]
)

df["Date_Label"] = df["Date"].dt.strftime("%b %d, %Y")

date_options = (
    df[["Date", "Date_Label"]]
    .drop_duplicates()
    .sort_values("Date", ascending=False)
)

labels = date_options["Date_Label"].tolist()

selected_date = st.sidebar.selectbox(
    "View date",
    ["All Dates"] + labels
)

st.sidebar.caption(f"Data source: {source}")

if selected_date == "All Dates":
    view = df.copy()
    view_title = "All Dates"
else:
    view = df[df["Date_Label"] == selected_date].copy()
    view_title = selected_date

# ----- Champion calculations -----
homework_board = (
    view.groupby("Student", as_index=False)["Homework_Points"]
        .sum()
        .sort_values(["Homework_Points", "Student"], ascending=[False, True])
        .reset_index(drop=True)
)

poi_board = (
    view.groupby("Student", as_index=False)["POI_Points"]
        .sum()
        .sort_values(["POI_Points", "Student"], ascending=[False, True])
        .reset_index(drop=True)
)

overall_board = (
    view.groupby("Student", as_index=False)["Total_Points"]
        .sum()
        .sort_values(["Total_Points", "Student"], ascending=[False, True])
        .reset_index(drop=True)
)

homework_champion = homework_board.iloc[0] if len(homework_board) else None
poi_champion = poi_board.iloc[0] if len(poi_board) else None

# ----- Featured Champions -----
st.subheader(f"🌟 Champions · {view_title}")

left, right = st.columns(2)

with left:
    if homework_champion is not None:
        st.markdown(
            f"""
            <div class="champion-card">
                <div class="champion-label">📚 Homework Champion</div>
                <div class="champion-name">👑 {homework_champion['Student']}</div>
                <div class="champion-score">{homework_champion['Homework_Points']:.0f} homework points</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with right:
    if poi_champion is not None:
        st.markdown(
            f"""
            <div class="champion-card">
                <div class="champion-label">🙋 POI Champion</div>
                <div class="champion-name">👑 {poi_champion['Student']}</div>
                <div class="champion-score">{poi_champion['POI_Points']:.0f} POI points</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

complete_count = (view["Homework_Status"].str.lower() == "complete").sum()
total_records = len(view)
completion_rate = (complete_count / total_records * 100) if total_records else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Students", view["Student"].nunique())
m2.metric("Homework completed", f"{completion_rate:.0f}%")
m3.metric("POI points", f"{view['POI_Points'].sum():.0f}")
m4.metric("Total class points", f"{view['Total_Points'].sum():.0f}")

tabs = st.tabs([
    "🏆 Overall",
    "📚 Homework",
    "🙋 POI",
    "💬 Feedback"
])

# ----- Overall -----
with tabs[0]:
    st.subheader(f"Overall Leaderboard · {view_title}")

    board = overall_board.copy()
    board["Rank"] = board.index + 1
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    board["Place"] = board["Rank"].map(medals).fillna(
        board["Rank"].astype(str) + "."
    )

    if len(board):
        cols = st.columns(min(3, len(board)))
        for i in range(min(3, len(board))):
            row = board.iloc[i]
            with cols[i]:
                st.metric(
                    f"{medals.get(i + 1, '')} {row['Student']}",
                    f"{row['Total_Points']:.0f} pts"
                )

    st.bar_chart(
        board.set_index("Student")["Total_Points"],
        horizontal=True
    )

    st.dataframe(
        board[["Place", "Student", "Total_Points"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Place": "Rank",
            "Student": "Student",
            "Total_Points": st.column_config.NumberColumn("Total Points", format="%.0f")
        }
    )

# ----- Homework -----
with tabs[1]:
    st.subheader(f"📚 Homework Champion Board · {view_title}")

    hw = homework_board.copy()
    hw["Rank"] = hw.index + 1
    hw["Place"] = hw["Rank"].map({1:"🥇",2:"🥈",3:"🥉"}).fillna(
        hw["Rank"].astype(str) + "."
    )

    st.bar_chart(
        hw.set_index("Student")["Homework_Points"],
        horizontal=True
    )

    st.dataframe(
        hw[["Place", "Student", "Homework_Points"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Place": "Rank",
            "Homework_Points": st.column_config.NumberColumn(
                "Homework Points", format="%.0f"
            )
        }
    )

    st.markdown("#### Homework Status")

    tracker = view[[
        "Student", "Date", "Date_Label",
        "Homework_Status", "Homework_Points"
    ]].copy()

    tracker["Status"] = tracker["Homework_Status"].apply(
        lambda x: f"{STATUS_ICONS.get(x, '•')} {x}"
    )

    if selected_date == "All Dates":
        display = (
            tracker.pivot_table(
                index="Student",
                columns="Date_Label",
                values="Status",
                aggfunc="first",
                fill_value=""
            )
            .reset_index()
        )
        st.dataframe(display, hide_index=True, use_container_width=True)
    else:
        tracker = tracker.sort_values("Student")
        st.dataframe(
            tracker[["Student", "Status", "Homework_Points"]],
            hide_index=True,
            use_container_width=True,
            column_config={
                "Homework_Points": st.column_config.NumberColumn(
                    "Homework Points", format="%.0f"
                )
            }
        )

    st.caption("✅ Complete   ·   🟡 Late   ·   ❌ Missing   ·   ➖ Excused")

# ----- POI -----
with tabs[2]:
    st.subheader(f"🙋 POI Champion Board · {view_title}")

    poi = poi_board.copy()
    poi["Rank"] = poi.index + 1
    poi["Place"] = poi["Rank"].map({1:"🥇",2:"🥈",3:"🥉"}).fillna(
        poi["Rank"].astype(str) + "."
    )

    st.bar_chart(
        poi.set_index("Student")["POI_Points"],
        horizontal=True
    )

    st.dataframe(
        poi[["Place", "Student", "POI_Points"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Place": "Rank",
            "POI_Points": st.column_config.NumberColumn(
                "POI Points", format="%.0f"
            )
        }
    )

    st.caption("Use POI points however you like — for example, +1 for offering a strong POI and +1 for answering one well.")

# ----- Feedback -----
with tabs[3]:
    st.subheader(f"💬 Teacher Feedback · {view_title}")
    st.caption("Anything written here is visible to anyone who can access the app.")

    feedback_view = (
        view.sort_values(["Date", "Student"], ascending=[False, True])
            [[
                "Student", "Date_Label", "Homework_Status",
                "Homework_Points", "POI_Points",
                "Class_Points", "Bonus_Points",
                "Total_Points", "Feedback"
            ]]
    )

    for _, row in feedback_view.iterrows():
        icon = STATUS_ICONS.get(row["Homework_Status"], "•")
        st.markdown(
            f"""
            <div class="student-card">
                <div class="student-name">
                    {row['Student']}
                    <span style="font-size:.9rem;">· {row['Date_Label']}</span>
                </div>
                <div class="small-label">
                    {icon} {row['Homework_Status']}
                    &nbsp; | &nbsp; Homework {row['Homework_Points']:.0f}
                    &nbsp; | &nbsp; POI {row['POI_Points']:.0f}
                    &nbsp; | &nbsp; Class {row['Class_Points']:.0f}
                    &nbsp; | &nbsp; Bonus {row['Bonus_Points']:.0f}
                    &nbsp; | &nbsp; <b>Total {row['Total_Points']:.0f}</b>
                </div>
                <div class="feedback">
                    {row['Feedback'] or 'No feedback for this class.'}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()
st.caption(
    "Teacher workflow: update your master spreadsheet → export CSV → upload the newest file here."
)
