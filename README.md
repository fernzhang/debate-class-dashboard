# Debate Class Dashboard

A colorful Streamlit dashboard for class homework, POI participation, points, and teacher feedback.

## GitHub files

Upload these four files to the root of your existing repository:

- `app.py`
- `sample_students.csv`
- `requirements.txt`
- `README.md`

When the filenames already exist, upload the new versions and commit the changes.

## Updating scores later

For score/feedback-only changes, replace `sample_students.csv` and commit it.

The app intentionally does **not** cache the default CSV, so updated GitHub data will be loaded after the Streamlit app redeploys/restarts.

## CSV columns

`Date, Student, Homework_Status, Homework_Points, POI_Points, Class_Points, Bonus_Points, Feedback`
