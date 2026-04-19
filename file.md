I am building a project titled:

"Space Debris Density Analysis and Monitoring Portal"

using Django, Pandas, NumPy, Chart.js, and MongoDB (basic integration).

--------------------------------------
PROJECT REQUIREMENTS
--------------------------------------

The system should:
- Analyze space debris dataset (CSV/Excel)
- Provide insights:
  - Country-wise contribution
  - Object type distribution
  - Altitude-based density
  - Orbit grouping (if available)
- Focus only on data analysis (no ML)

--------------------------------------
CURRENT STATUS (VERY IMPORTANT)
--------------------------------------

I have ALREADY started the project:

- Django project created: debris_analysis
- App created: managespace
- Dataset already in project folder
- manage.py, settings.py, views.py already exist

👉 DO NOT recreate the project
👉 DO NOT change folder structure

--------------------------------------
WHAT I WANT YOU TO DO
--------------------------------------

Continue building from my existing project step-by-step.

--------------------------------------
TASKS
--------------------------------------

1. Add 'managespace' to INSTALLED_APPS

2. Setup URLs:
- Create managespace/urls.py
- Connect it in main urls.py

3. Create views:
- dashboard (summary)
- analysis (detailed + upload)

4. Data handling:
- Use Pandas to read dataset
- If uploaded → use that
- Else → use default dataset

5. Global data sync:
- Use Django session
- Ensure BOTH dashboard and analysis use SAME data

6. Analysis logic:
- total objects
- object type count
- country-wise count
- altitude grouping
- mean altitude using NumPy

7. Frontend:
- Create:
  - base.html
  - dashboard.html
  - analysis.html
- Add navbar:
  Dashboard | Analysis

8. UI Design:
- Dark theme (space style)
- Add:
  - summary cards
  - charts (Chart.js)
  - glow + hover effects

9. Charts:
- Bar chart → country
- Pie chart → object types (small + centered)

10. Upload feature:
- Add at top of analysis page
- File input + "Upload & Analyze"
- Show message:
  "Dataset uploaded successfully. Analysis updated."

11. Error handling:
- Invalid CSV
- Missing columns

12. Simple MongoDB (for syllabus only):
- Connect using pymongo
- Create DB: space_debris_db
- Collection: objects
- Perform basic CRUD:
  - Insert
  - Read
  - Update
  - Delete
- Keep MongoDB separate from main logic

--------------------------------------
IMPORTANT RULES
--------------------------------------

- Do NOT recreate project
- Work with existing files only
- Give code step-by-step
- Ensure code runs without errors

--------------------------------------

Start with:
1. settings.py
2. urls.py
3. managespace/urls.py
Then continue step-by-step.