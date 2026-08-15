
# Debate Class Game Dashboard

A simple Streamlit dashboard for tracking:
- Homework
- Homework Champion
- POI participation
- POI Champion
- Class points
- Bonus points
- Overall leaderboard
- Teacher feedback

## CSV format

Your CSV must contain:

- `Date`
- `Student`
- `Homework_Status`
- `Homework_Points`
- `POI_Points`
- `Class_Points`
- `Bonus_Points`
- `Feedback`

Example:

| Date | Student | Homework_Status | Homework_Points | POI_Points | Class_Points | Bonus_Points | Feedback |
|---|---|---|---:|---:|---:|---:|---|
| 2026-08-09 | Alyssa | Complete | 10 | 4 | 6 | 1 | Great improvement... |

Recommended homework statuses:
- Complete
- Late
- Missing
- Excused

Each row represents one student for one class date.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Update the dashboard

1. Keep your records in Excel or Google Sheets.
2. Export the newest version as CSV.
3. Upload it using the sidebar.
4. The app recalculates all leaderboards automatically.

If no file is uploaded, the sample CSV is shown.

## Current game categories

- 📚 Homework Champion = highest Homework_Points
- 🙋 POI Champion = highest POI_Points
- 🏆 Overall Leaderboard = Homework + POI + Class + Bonus points

Important: all feedback in the CSV is visible to anyone who can access the app.
