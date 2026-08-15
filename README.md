# Debate Class Dashboard

A colorful Streamlit dashboard for class homework, POI participation, points, and teacher feedback.

## GitHub files

Upload these files to the root of your existing repository:

- `app.py`
- `sample_students.csv`
- `requirements.txt`
- `README.md`

## Updating scores later

Replace `sample_students.csv` and commit it.

The dashboard reads the CSV directly and does not include a student-facing upload control.

## Tie behavior

When multiple students share the top Homework or POI score, all tied names are shown in the champion card.

## Date display

The CSV still stores plain dates such as `2026-08-09`. The dashboard displays them as `Week of Aug 9, 2026`.
