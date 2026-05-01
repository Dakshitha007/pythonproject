from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import io
import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pymongo import MongoClient
,
def get_data(request):
    default_csv = os.path.join(settings.BASE_DIR, '..', 'debris.csv')
    default_csv = os.path.normpath(default_csv)
    if 'data_file' in request.session:
        file_path = request.session['data_file']
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
    if os.path.exists(default_csv):
        return pd.read_csv(default_csv)
    raise FileNotFoundError(f"Default dataset not found: {default_csv}")

# Chart rendering helpers using Matplotlib
DARK_GRID_COLOR = (1.0, 1.0, 1.0, 0.08)
SPINE_COLOR = (71 / 255, 85 / 255, 105 / 255, 0.8)
TICK_COLOR = '#94a3b8'
LINE_COLOR = (0 / 255, 229 / 255, 255 / 255, 1.0)
LINE_FILL_COLOR = (0 / 255, 229 / 255, 255 / 255, 0.22)
ALTITUDE_BAR_COLOR = (139 / 255, 92 / 255, 246 / 255, 0.7)
CHART_COLORS = [
    (0 / 255, 229 / 255, 255 / 255, 0.8),
    (236 / 255, 72 / 255, 153 / 255, 0.8),
    (251 / 255, 191 / 255, 36 / 255, 0.8),
    (34 / 255, 197 / 255, 94 / 255, 0.8),
    (139 / 255, 92 / 255, 246 / 255, 0.8),
    (59 / 255, 130 / 255, 246 / 255, 0.8),
]

COLOR_CYAN = (0 / 255, 229 / 255, 255 / 255, 0.7)

def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', transparent=True, dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('ascii')
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"


def _configure_axis(ax):
    ax.set_facecolor('none')
    ax.grid(False)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    ax.tick_params(colors=TICK_COLOR, labelcolor=TICK_COLOR)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    return ax


def create_doughnut_chart(labels, values, colors):
    if not labels or sum(values) == 0:
        return None

    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors[: len(labels)],
        startangle=140,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.2),
        autopct=lambda pct: f'{pct:.1f}%' if pct > 0 else '',
        pctdistance=0.78,
        textprops=dict(color='white', fontsize=10, weight='bold'),
    )

    ax.axis('equal')
    ax.legend(
        wedges,
        labels,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=min(3, len(labels)),
        frameon=False,
        prop={'size': 9},
        labelcolor='white',
    )
    fig.tight_layout(pad=0.8)
    return fig_to_base64(fig)


def create_line_chart(labels, values):
    if not labels or not values or len(labels) != len(values):
        return None

    fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    x = range(len(labels))
    ax.plot(x, values, color=LINE_COLOR, linewidth=3, zorder=4)
    ax.fill_between(x, values, color=LINE_FILL_COLOR)
    ax.scatter(x, values, color=LINE_COLOR, edgecolors='white', linewidths=1.5, s=60, zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', color=TICK_COLOR, fontsize=9)
    ax.set_ylim(bottom=0)
    _configure_axis(ax)
    fig.tight_layout(pad=0.8)
    return fig_to_base64(fig)


def create_bar_chart(labels, values, bar_color, rotate_xticks=False):
    if not labels or not values:
        return None

    fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    x = range(len(labels))
    bars = ax.bar(x, values, color=bar_color, edgecolor=bar_color, width=0.7, zorder=3)

    for rect in bars:
        height = rect.get_height()
        if height >= 0:
            offset = max(values) * 0.02 if max(values) else 0.1
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                height + offset,
                str(int(height)),
                ha='center',
                va='bottom',
                color='white',
                fontsize=9,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45 if rotate_xticks else 0, ha='right' if rotate_xticks else 'center', color=TICK_COLOR, fontsize=9)
    ax.set_ylim(bottom=0)
    _configure_axis(ax)
    fig.tight_layout(pad=0.8)
    return fig_to_base64(fig)


def dashboard(request):
    df = get_data(request)
    required_columns = ['object_type', 'country', 'altitude_km', 'launch_year_estimate']
    missing_columns = [col for col in required_columns if col not in df.columns]

    # Analysis logic
    total_objects = len(df)
    object_type_count = df['object_type'].value_counts().to_dict() if 'object_type' in df.columns else {}
    country_count = df['country'].value_counts().to_dict() if 'country' in df.columns else {}
    altitude_groups = df.groupby(pd.cut(df['altitude_km'], bins=5)).size().to_dict() if 'altitude_km' in df.columns else {}
    mean_altitude = np.mean(df['altitude_km']) if 'altitude_km' in df.columns else 0

    # New metrics
    total_payloads = df[df['object_type'] == 'PAYLOAD'].shape[0] if 'object_type' in df.columns else 0
    rocket_unknown_count = df[df['object_type'].str.contains('ROCKET|UNKNOWN', case=False, na=False)].shape[0] if 'object_type' in df.columns else 0
    total_debris = max(total_objects - total_payloads - rocket_unknown_count, 0)
    non_payload_types = {k: v for k, v in object_type_count.items() if k != 'PAYLOAD'}
    primary_debris_type = max(non_payload_types, key=non_payload_types.get) if non_payload_types else 'N/A'

    # Line chart data for debris growth over time
    debris_over_time = {}
    if 'launch_year_estimate' in df.columns:
        debris_over_time = df[df['object_type'] != 'PAYLOAD']['launch_year_estimate'].dropna().astype(int).value_counts().sort_index().to_dict()
        line_labels = [str(year) for year in sorted(debris_over_time.keys())] if debris_over_time else []
        line_data = [debris_over_time[int(year)] for year in sorted(debris_over_time.keys())] if debris_over_time else []
    else:
        line_labels = []
        line_data = []

    # Generate dynamic insights - ALWAYS generate, never show "not enough data"
    insights = []
    if total_objects > 0:
        if total_objects > 1000:
            insights.append("📊 Dataset contains a comprehensive collection of 1000+ orbital objects")
        elif total_objects > 100:
            insights.append(f"📊 Dataset contains {total_objects} tracked orbital objects")
        else:
            insights.append(f"📊 Currently monitoring {total_objects} orbital objects in the dataset")

        if object_type_count:
            dominant_type = max(object_type_count, key=object_type_count.get)
            dominant_pct = (object_type_count[dominant_type] / total_objects) * 100
            insights.append(f"🎯 {dominant_type.title()} objects dominate the dataset ({dominant_pct:.0f}%)")

        if total_payloads > 0 or total_debris > 0:
            if total_payloads > total_debris:
                insights.append(f"🛰️ Payloads ({total_payloads}) outnumber debris, indicating active satellite presence")
            elif total_debris > total_payloads:
                insights.append(f"⚠️ Debris ({total_debris}) exceeds payloads, highlighting collision risk concern")
            else:
                insights.append(f"⚖️ Balanced distribution: {total_payloads} payloads vs {total_debris} debris objects")

        if len(debris_over_time) >= 2:
            years = sorted(debris_over_time.keys())
            recent_years = years[-3:] if len(years) >= 3 else years
            recent_counts = [debris_over_time[y] for y in recent_years]
            if len(recent_counts) >= 2:
                trend = "increasing" if recent_counts[-1] > recent_counts[0] else "decreasing" if recent_counts[-1] < recent_counts[0] else "stable"
                insights.append(f"📈 Debris shows a {trend} trend over time ({int(years[0])} to {int(years[-1])})")
        elif len(debris_over_time) == 1:
            year_val = int(list(debris_over_time.keys())[0])
            insights.append(f"📅 Data available for year {year_val}")
        else:
            insights.append(f"📈 Debris data patterns available for analysis")

        if 'country' in df.columns and len(df) > 0:
            top_country = df['country'].value_counts().index[0] if len(df['country'].value_counts()) > 0 else None
            if top_country:
                top_pct = (df[df['country'] == top_country].shape[0] / total_objects) * 100
                insights.append(f"🌍 {top_country} leads in debris contribution ({top_pct:.0f}%)")

        if 'altitude_km' in df.columns and len(df) > 0:
            alt_data = df['altitude_km'].dropna()
            if len(alt_data) > 0:
                mean_alt = alt_data.mean()
                insights.append(f"📍 Average orbital altitude: {mean_alt:,.0f} km")

    if not insights:
        insights.append("📊 Ready to analyze orbital debris data. Upload a dataset to begin.")

    chart_labels = ['Payload', 'Debris', 'Rocket Body / Unknown']
    chart_data = [total_payloads, total_debris, rocket_unknown_count]

    type_chart = None
    line_chart = None
    if not missing_columns:
        type_chart = create_doughnut_chart(chart_labels, chart_data, CHART_COLORS[:3])
        line_chart = create_line_chart(line_labels, line_data)

    dashboard_error = "Required column is missing" if missing_columns else None

    context = {
        'total_objects': total_objects,
        'total_payloads': total_payloads,
        'total_debris': total_debris,
        'primary_debris_type': primary_debris_type,
        'insights': insights,
        'type_chart': type_chart,
        'line_chart': line_chart,
        'dashboard_error': dashboard_error,
    }
    return render(request, 'dashboard.html', context)

def get_filter_data(request, df):
    """Apply filters to the dataframe and return filtered data"""
    filtered_df = df.copy()
    
    # Get filter parameters from request
    selected_country = request.GET.get('country', '')
    selected_object_type = request.GET.get('object_type', '')
    start_year = request.GET.get('start_year', '')
    end_year = request.GET.get('end_year', '')
    selected_status = request.GET.get('status', '')
    
    print(f"[DEBUG] Filter params - Country: {selected_country}, Type: {selected_object_type}, Years: {start_year}-{end_year}, Status: {selected_status}")
    
    # Apply country filter
    if selected_country and selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
        print(f"[DEBUG] After country filter: {len(filtered_df)} rows")
    
    # Apply object type filter
    if selected_object_type and selected_object_type != 'all':
        filtered_df = filtered_df[filtered_df['object_type'] == selected_object_type]
        print(f"[DEBUG] After object_type filter: {len(filtered_df)} rows")
    
    # Apply year range filter (using launch_year_estimate)
    if 'launch_year_estimate' in filtered_df.columns:
        try:
            year_mask = pd.Series([True] * len(filtered_df), index=filtered_df.index)
            
            if start_year:
                try:
                    start_val = int(start_year)
                    year_mask = year_mask & (filtered_df['launch_year_estimate'] >= start_val)
                    print(f"[DEBUG] Applied start year filter: >= {start_val}")
                except (ValueError, TypeError):
                    print(f"[DEBUG] Invalid start_year value: {start_year}")
            
            if end_year:
                try:
                    end_val = int(end_year)
                    year_mask = year_mask & (filtered_df['launch_year_estimate'] <= end_val)
                    print(f"[DEBUG] Applied end year filter: <= {end_val}")
                except (ValueError, TypeError):
                    print(f"[DEBUG] Invalid end_year value: {end_year}")
            
            filtered_df = filtered_df[year_mask]
            print(f"[DEBUG] After year filter: {len(filtered_df)} rows")
        except Exception as e:
            print(f"[DEBUG] Error in year filtering: {str(e)}")
    
    # Apply status filter (if status column exists)
    if selected_status and selected_status != 'All' and 'status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['status'] == selected_status]
        print(f"[DEBUG] After status filter: {len(filtered_df)} rows")
    
    print(f"[DEBUG] Final filtered data: {len(filtered_df)} rows")
    return filtered_df

def get_chart_data(filtered_df):
    """Generate chart data from filtered dataframe"""
    total_objects = len(filtered_df)

    object_labels = []
    object_values = []
    if 'object_type' in filtered_df.columns and len(filtered_df) > 0:
        object_type_count = filtered_df['object_type'].value_counts().to_dict()
        object_labels = list(object_type_count.keys())
        object_values = list(object_type_count.values())

    country_labels = []
    country_values = []
    if 'country' in filtered_df.columns and len(filtered_df) > 0:
        country_count = filtered_df['country'].value_counts().head(10).to_dict()
        country_labels = list(country_count.keys())
        country_values = list(country_count.values())

    line_labels = []
    line_data = []
    if len(filtered_df) > 0:
        if 'launch_year_estimate' in filtered_df.columns:
            debris_trend = filtered_df['launch_year_estimate'].dropna().astype(int).value_counts().sort_index().to_dict()
            if debris_trend:
                line_labels = [str(year) for year in debris_trend.keys()]
                line_data = list(debris_trend.values())
        elif 'launch_year' in filtered_df.columns:
            debris_trend = filtered_df['launch_year'].dropna().astype(int).value_counts().sort_index().to_dict()
            if debris_trend:
                line_labels = [str(year) for year in debris_trend.keys()]
                line_data = list(debris_trend.values())
        elif 'country' in filtered_df.columns and len(country_labels) > 0:
            line_labels = country_labels[:10]
            line_data = country_values[:10]
        else:
            line_labels = ['2020', '2021', '2022', '2023', '2024']
            line_data = [total_objects // 5 * i for i in range(1, 6)]

    altitude_labels = []
    altitude_values = []
    if 'altitude_km' in filtered_df.columns and len(filtered_df) > 0:
        try:
            alt_data = filtered_df['altitude_km'].dropna()
            if len(alt_data) > 0:
                altitude_bins = pd.cut(alt_data, bins=8, duplicates='drop')
                altitude_dist = altitude_bins.value_counts().sort_index()
                for interval, count in altitude_dist.items():
                    altitude_labels.append(f"{int(interval.left)}-{int(interval.right)}")
                    altitude_values.append(int(count))
        except Exception:
            pass

    if not altitude_labels and 'altitude_km' in filtered_df.columns:
        altitude_ranges = [
            ('0-500', (filtered_df['altitude_km'] >= 0) & (filtered_df['altitude_km'] < 500)),
            ('500-1000', (filtered_df['altitude_km'] >= 500) & (filtered_df['altitude_km'] < 1000)),
            ('1000-1500', (filtered_df['altitude_km'] >= 1000) & (filtered_df['altitude_km'] < 1500)),
            ('1500-2000', (filtered_df['altitude_km'] >= 1500) & (filtered_df['altitude_km'] < 2000)),
            ('2000+', (filtered_df['altitude_km'] >= 2000)),
        ]
        altitude_labels = [label for label, _ in altitude_ranges]
        altitude_values = [int(filtered_df[mask].shape[0]) for _, mask in altitude_ranges]

    mean_altitude = filtered_df['altitude_km'].mean() if 'altitude_km' in filtered_df.columns and len(filtered_df) > 0 else 0

    return {
        'total_objects': total_objects,
        'object_labels': object_labels,
        'object_values': object_values,
        'country_labels': country_labels,
        'country_values': country_values,
        'line_labels': line_labels,
        'line_data': line_data,
        'altitude_labels': altitude_labels,
        'altitude_values': altitude_values,
        'mean_altitude': round(mean_altitude, 2),
    }

def analysis(request):
    message = None
    message_type = None
    required_columns = ['object_type', 'country', 'altitude_km', 'launch_year_estimate']

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        try:
            df_test = pd.read_csv(file_path)
            missing_cols = [col for col in required_columns if col not in df_test.columns]
            if not missing_cols:
                request.session['data_file'] = file_path
                message = "✓ Dataset uploaded successfully! All required columns detected. Analysis updated."
                message_type = 'success'
            else:
                message = "Required column is missing"
                message_type = 'error'
                os.remove(file_path)
        except Exception as e:
            message = f"✗ Error reading CSV file: {str(e)}\n\nPlease ensure the file is a valid CSV format."
            message_type = 'error'
            if os.path.exists(file_path):
                os.remove(file_path)

    try:
        df = get_data(request)
    except FileNotFoundError:
        df = pd.DataFrame()

    missing_columns = [col for col in required_columns if col not in df.columns] if len(df) > 0 else required_columns
    has_valid_data = len(df) > 0 and not missing_columns
    has_filters = any(request.GET.get(param) for param in ['country', 'object_type', 'start_year', 'end_year', 'status'])

    if has_valid_data and has_filters:
        filtered_df = get_filter_data(request, df)
    elif has_valid_data:
        filtered_df = df
    else:
        filtered_df = pd.DataFrame()

    chart_images = {
        'object_chart': None,
        'country_chart': None,
        'line_chart': None,
        'altitude_chart': None,
    }
    if has_valid_data and len(filtered_df) > 0:
        chart_data = get_chart_data(filtered_df)
        chart_images['object_chart'] = create_doughnut_chart(chart_data['object_labels'], chart_data['object_values'], CHART_COLORS)
        chart_images['country_chart'] = create_bar_chart(chart_data['country_labels'], chart_data['country_values'], COLOR_CYAN, rotate_xticks=True)
        chart_images['line_chart'] = create_line_chart(chart_data['line_labels'], chart_data['line_data'])
        chart_images['altitude_chart'] = create_bar_chart(chart_data['altitude_labels'], chart_data['altitude_values'], ALTITUDE_BAR_COLOR, rotate_xticks=True)
        mean_altitude = chart_data['mean_altitude']
        total_objects = chart_data['total_objects']
    else:
        mean_altitude = 0
        total_objects = 0

    filter_message = None
    if has_filters and has_valid_data and len(filtered_df) == 0:
        filter_message = 'No data available'
    elif not has_valid_data and len(df) > 0:
        filter_message = 'Required column is missing'

    countries = sorted(df['country'].dropna().unique().tolist()) if 'country' in df.columns and len(df) > 0 else []
    object_types = sorted(df['object_type'].dropna().unique().tolist()) if 'object_type' in df.columns and len(df) > 0 else []
    min_year = int(df['launch_year_estimate'].min()) if 'launch_year_estimate' in df.columns and len(df) > 0 else 1900
    max_year = int(df['launch_year_estimate'].max()) if 'launch_year_estimate' in df.columns and len(df) > 0 else 2030
    statuses = sorted(df['status'].dropna().unique().tolist()) if 'status' in df.columns and len(df) > 0 else []

    context = {
        'message': message,
        'message_type': message_type,
        'countries': countries,
        'object_types': object_types,
        'statuses': statuses,
        'min_year_range': min_year,
        'max_year_range': max_year,
        'has_data': len(df) > 0,
        'has_valid_data': has_valid_data,
        'has_filters': has_filters,
        'has_filtered_results': has_valid_data and len(filtered_df) > 0,
        'filter_message': filter_message,
        'total_objects': total_objects,
        'mean_altitude': mean_altitude,
        **chart_images,
    }
    return render(request, 'analysis.html', context)

def mongodb_demo(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['space_debris_db']
    collection = db['objects']

    # Sample data
    sample_data = [
        {'norad_id': 900, 'name': 'CALSPHERE 1', 'object_type': 'PAYLOAD', 'country': 'US', 'altitude_km': 976.14},
        {'norad_id': 902, 'name': 'CALSPHERE 2', 'object_type': 'PAYLOAD', 'country': 'US', 'altitude_km': 1061.63},
    ]

    # Insert
    insert_result = collection.insert_many(sample_data)

    # Read
    objects = list(collection.find())

    # Update
    collection.update_one({'norad_id': 900}, {'$set': {'altitude_km': 980.0}})

    # Delete
    collection.delete_one({'norad_id': 902})

    # Read again
    objects_after = list(collection.find())

    context = {
        'insert_ids': insert_result.inserted_ids,
        'objects_before': objects,
        'objects_after': objects_after,
    }
    return render(request, 'mongodb.html', context)

def about(request):
    """About page for Space Debris Portal"""
    context = {
        'app_version': '1.0.0',
        'app_name': 'Space Debris Portal',
    }
    return render(request, 'about.html', context)
