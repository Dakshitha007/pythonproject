# Space Debris Analysis Portal

A Django-based web application for analyzing and visualizing orbital space debris data. This application provides comprehensive analytics, data visualization, and MongoDB integration for tracking and managing space debris objects across multiple dimensions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Installation & Setup](#installation--setup)
- [Dependencies](#dependencies)
- [Usage Guide](#usage-guide)
- [API Routes](#api-routes)
- [Data Requirements](#data-requirements)
- [Database](#database)
- [File Uploads](#file-uploads)
- [Troubleshooting](#troubleshooting)

---

## 📡 Overview

The **Space Debris Analysis Portal** is a comprehensive web application designed to track, analyze, and visualize orbital space debris. With over 1200+ tracked objects in the default dataset, this application provides real-time analytics and insights into debris patterns, distribution by country, altitude analysis, and object classification.

The application supports:
- Dashboard with live statistics and analytics
- Advanced data filtering and analysis
- Multiple data visualization charts
- CSV file uploads for custom datasets
- MongoDB integration for data storage
- Multi-filter analysis across country, object type, altitude, and orbit type

---

## ✨ Features

### Dashboard
- **Real-time Statistics**: Total objects, payloads, debris count
- **Dynamic Insights**: AI-generated insights about debris patterns
- **Visual Analytics**: Doughnut charts showing payload vs debris distribution
- **Trend Analysis**: Line charts tracking debris growth over time
- **Country Distribution**: Top countries contributing to debris
- **Altitude Analysis**: Mean altitude and altitude-based distributions

### Analysis Page
- **Data Upload**: Upload custom CSV datasets for analysis
- **Advanced Filtering**: Filter by:
  - Country of origin
  - Object type (Payload, Debris, Rocket Body)
  - Orbit type
  - Altitude range (min/max)
- **Multiple Chart Types**:
  - Object type distribution (Pie/Doughnut charts)
  - Geographic distribution (Top 10 countries)
  - Altitude distribution (8-bin histogram)
  - Temporal trends (Year-wise growth)
- **Data Validation**: Automatic validation of required columns
- **Real-time Updates**: Charts update instantly based on selected filters

### MongoDB Integration
- Sample MongoDB CRUD operations demonstration
- Insert, Read, Update, Delete (CRUD) capabilities
- Direct database connectivity for advanced data management
- Sample data for reference objects

### About Page
- Application information and version details
- Project overview

---

## 🏗️ Project Structure

```
pythonprojectofficial/
├── debris_analysis/                 # Main Django project
│   ├── manage.py                    # Django management script
│   ├── db.sqlite3                   # SQLite database
│   ├── debris_analysis/             # Project configuration
│   │   ├── __init__.py
│   │   ├── asgi.py                  # ASGI configuration
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # Project-level URL routing
│   │   └── wsgi.py                  # WSGI configuration
│   │
│   └── managespace/                 # Django app for debris management
│       ├── __init__.py
│       ├── admin.py                 # Django admin configuration
│       ├── apps.py                  # App configuration
│       ├── models.py                # Database models
│       ├── tests.py                 # Unit tests
│       ├── urls.py                  # App-level URL routing
│       ├── views.py                 # View handlers and business logic
│       ├── migrations/              # Database migrations
│       ├── templates/               # HTML templates
│       │   ├── base.html            # Base template
│       │   ├── about.html           # About page
│       │   ├── analysis.html        # Analysis page
│       │   ├── dashboard.html       # Dashboard page
│       │   ├── mongodb.html         # MongoDB demo page
│       │   └── managespace/         # App-specific templates
│       │       ├── analysis.html
│       │       ├── base.html
│       │       ├── dashboard.html
│       │       └── mongodb.html
│       └── media/
│           └── uploads/             # Uploaded CSV files
│
├── debris.csv                       # Default debris dataset
├── Space_Debris_Dataset_1200.csv    # Full 1200-object dataset
├── Space_Debris_Dataset_Missing_Required.csv  # Test dataset with missing columns
├── file.md                          # Project notes
└── README.md                        # This file
```

---

## 🛠️ Technologies

### Backend
- **Django 6.0.3** - Web framework
- **Python 3.x** - Programming language
- **SQLite** - Default database

### Data Processing
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript** - Interactive features
- **Chart.js** - Data visualization (implied by chart contexts)

### Database
- **SQLite** - Development database
- **MongoDB** - Optional data storage (when available)
- **PyMongo** - MongoDB Python driver

### File Handling
- **Django FileSystemStorage** - File upload management

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
cd c:\Users\ASUS\OneDrive\Documents\pythonprojectofficial
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
cd debris_analysis
python manage.py migrate
```

### Step 5: Start Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

---

## 📦 Dependencies

The project requires the following Python packages:

```
Django==6.0.3
pandas>=1.3.0
numpy>=1.21.0
pymongo>=3.12.0
```

### Installation
```bash
pip install Django pandas numpy pymongo
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

---

## 📖 Usage Guide

### Accessing the Application

1. **Dashboard** (`/`)
   - View comprehensive statistics about orbital objects
   - See dynamic insights about debris patterns
   - Monitor payload vs debris distribution
   - Track debris growth over time

2. **Analysis** (`/analysis/`)
   - Upload custom CSV datasets
   - Filter data by multiple dimensions
   - Generate detailed charts and visualizations
   - Export filtered analysis results

3. **MongoDB Demo** (`/mongodb/`)
   - View MongoDB CRUD operations
   - See sample data insertions
   - Observe update and delete operations

4. **About** (`/about/`)
   - Application information
   - Version details

### Uploading Data

1. Navigate to the Analysis page
2. Click "Upload Dataset"
3. Select a CSV file with required columns:
   - `object_type` - Type of object (PAYLOAD, DEBRIS, ROCKET BODY)
   - `country` - Country of origin
   - `altitude_km` - Orbital altitude in kilometers
4. Click "Upload"
5. The application validates the file and updates all charts automatically

### Filtering Data

1. Select filters from the available dropdown menus:
   - **Country**: Choose a specific country or "All"
   - **Object Type**: Filter by payload, debris, or rocket body
   - **Orbit Type**: Select specific orbit types (if available)
   - **Altitude Range**: Set minimum and maximum altitude values
2. Filters apply in real-time, updating all visualizations
3. Use "Reset Filters" to return to the unfiltered view

### Interpreting Charts

- **Object Type Distribution**: Shows percentage breakdown of debris types
- **Country Distribution**: Lists top 10 countries by debris contribution
- **Altitude Distribution**: Visualizes debris across 8 altitude ranges
- **Temporal Trends**: Shows debris accumulation over time

---

## 🔗 API Routes

### URL Patterns

```
/                           - Dashboard (GET)
/analysis/                  - Analysis page (GET, POST for file upload)
/about/                     - About page (GET)
/mongodb/                   - MongoDB demo (GET)
```

### Route Details

#### Dashboard (`/`)
- **Method**: GET
- **Response**: HTML with dashboard statistics and charts
- **Context Variables**:
  - `total_objects` - Count of all objects
  - `total_payloads` - Count of active payloads
  - `total_debris` - Count of debris objects
  - `primary_debris_type` - Most common debris type
  - `insights` - List of generated insights
  - `chart_labels` - JSON formatted chart labels
  - `chart_data` - JSON formatted chart data
  - `line_labels` - Timeline labels
  - `line_data` - Timeline data values

#### Analysis (`/analysis/`)
- **Method**: GET, POST
- **POST Parameters**: 
  - `file` - CSV file upload
  - `country` - Filter by country (GET)
  - `object_type` - Filter by object type (GET)
  - `orbit_type` - Filter by orbit type (GET)
  - `min_altitude` - Minimum altitude filter (GET)
  - `max_altitude` - Maximum altitude filter (GET)
- **Response**: HTML with analysis charts and filters
- **Context Variables**:
  - `countries` - List of available countries
  - `object_types` - List of object types
  - `orbit_types` - List of orbit types
  - `has_data` - Boolean indicating data availability
  - `message` - Upload status message
  - `message_type` - 'success' or 'error'

#### MongoDB (`/mongodb/`)
- **Method**: GET
- **Response**: HTML demonstrating CRUD operations
- **Context Variables**:
  - `insert_ids` - IDs of inserted documents
  - `objects_before` - Original data
  - `objects_after` - Data after CRUD operations

#### About (`/about/`)
- **Method**: GET
- **Response**: HTML with application info
- **Context Variables**:
  - `app_version` - Application version
  - `app_name` - Application name

---

## 📊 Data Requirements

### Required Columns

All datasets must include these three columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `object_type` | String | Type of orbital object | PAYLOAD, DEBRIS, ROCKET BODY |
| `country` | String | Country of origin | US, RUS, CHN, etc. |
| `altitude_km` | Float | Orbital altitude in kilometers | 400.5, 800.2, 36000.0 |

### Optional Columns

These columns enhance the analysis but are not required:

| Column | Type | Description |
|--------|------|-------------|
| `launch_year_estimate` | Integer | Estimated launch year |
| `launch_year` | Integer | Actual launch year |
| `orbit_type` | String | Type of orbit (LEO, MEO, GEO, etc.) |
| `norad_id` | Integer | NORAD catalog number |
| `name` | String | Object name/designation |

### Data Validation

The application automatically validates:
- ✓ All required columns are present
- ✓ CSV file format is valid
- ✓ No data type mismatches
- ✗ Files with missing columns are rejected with detailed error messages

### Sample Data

Three sample datasets are included:

1. **debris.csv** - Default dataset for quick testing
2. **Space_Debris_Dataset_1200.csv** - Full comprehensive dataset with 1200+ objects
3. **Space_Debris_Dataset_Missing_Required.csv** - Test dataset to validate error handling

---

## 🗄️ Database

### SQLite (Default)

- **Location**: `debris_analysis/db.sqlite3`
- **Purpose**: Django ORM and session storage
- **Note**: Currently no models are defined; database is primarily for Django infrastructure

### MongoDB (Optional)

- **Purpose**: Alternative data storage for debris objects
- **Connection**: `mongodb://localhost:27017/`
- **Database**: `space_debris_db`
- **Collection**: `objects`
- **Status**: Demonstration only in current version

#### MongoDB Document Schema
```json
{
  "norad_id": 900,
  "name": "CALSPHERE 1",
  "object_type": "PAYLOAD",
  "country": "US",
  "altitude_km": 976.14
}
```

---

## 📤 File Uploads

### Upload Location
- **Directory**: `debris_analysis/media/uploads/`
- **File Type**: CSV only
- **Size Limit**: Django default (typically 2.5 MB)

### Upload Process
1. File is received and saved to media/uploads/
2. File is read and validated for required columns
3. If valid: file path is stored in session for future use
4. If invalid: file is deleted and error message is shown

### Session Storage
- Uploaded file paths are stored in `request.session['data_file']`
- Session data persists across page reloads
- Uploading a new file replaces the previous session data

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Default dataset not found" Error
**Problem**: `debris.csv` is missing from the project root
**Solution**: 
- Ensure `debris.csv` exists in the main directory
- Use `Space_Debris_Dataset_1200.csv` as replacement by renaming it to `debris.csv`

#### 2. MongoDB Connection Error
**Problem**: MongoDB is not running or not accessible
**Solution**:
- Install MongoDB locally or use MongoDB Atlas
- Ensure MongoDB service is running: `mongod`
- Update connection string in `mongodb_demo()` view

#### 3. Missing Required Columns Error
**Problem**: Uploaded CSV lacks required columns
**Solution**:
- Verify your CSV contains: `object_type`, `country`, `altitude_km`
- Use the provided sample datasets as reference
- Use `Space_Debris_Dataset_Missing_Required.csv` to see expected error format

#### 4. Permission Denied on File Upload
**Problem**: Cannot save files to media/uploads directory
**Solution**:
- Ensure `media/uploads/` directory exists and has write permissions
- Create directory: `mkdir -p debris_analysis/media/uploads`

#### 5. Charts Not Loading
**Problem**: Charts appear empty on dashboard/analysis pages
**Solution**:
- Verify CSV file is properly formatted
- Check browser console for JavaScript errors
- Ensure all required data columns are present
- Try resetting filters to default state

### Debug Mode

The application runs with `DEBUG = True` in settings.py. For troubleshooting:

1. Check Django error pages for detailed traceback
2. Verify file paths in your environment
3. Use `python manage.py shell` to test data loading
4. Check `manage.py` logs for request/response errors

---

## 🚀 Future Enhancements

- [ ] User authentication and authorization
- [ ] Database models for persistent storage
- [ ] Advanced search and filtering capabilities
- [ ] Real-time debris tracking integration
- [ ] Export functionality (PDF, Excel)
- [ ] API endpoints for programmatic access
- [ ] Machine learning predictions for debris collision risks
- [ ] Interactive 3D orbital visualization
- [ ] Historical data archival
- [ ] Performance optimizations for large datasets

---

## 📝 Configuration

### Django Settings Highlights

- **SECRET_KEY**: Change in production
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Configure for your domain
- **INSTALLED_APPS**: Contains `managespace` app
- **MIDDLEWARE**: Standard Django middleware stack
- **STATIC_FILES**: CSS, JS, images configuration
- **MEDIA_ROOT**: File upload directory path

### Recommendations for Production

1. Set `DEBUG = False`
2. Update `SECRET_KEY` with a secure value
3. Add allowed hosts: `ALLOWED_HOSTS = ['yourdomain.com']`
4. Use environment variables for sensitive data
5. Configure proper database (PostgreSQL recommended)
6. Set up static file serving (WhiteNoise or Nginx)
7. Enable HTTPS and security headers
8. Use MongoDB Atlas for cloud database

---

## 📞 Support

For issues or questions:
- Review the Troubleshooting section above
- Check Django documentation: https://docs.djangoproject.com/
- Refer to Pandas documentation: https://pandas.pydata.org/docs/
- MongoDB docs: https://docs.mongodb.com/

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Django Version**: 6.0.3  
**Python Version**: 3.x+.