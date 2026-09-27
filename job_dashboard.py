import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Job & Internship Analytics",
    page_icon="💼",
    layout="wide"
)


# ==========================================================
# PROFESSIONAL COLOR PALETTE
# ==========================================================

NAVY = "#17324D"
BLUE = "#2F6B9A"
LIGHT_BLUE = "#5B8DB8"
SOFT_BLUE = "#8FB3CF"
PALE_BLUE = "#C8D8E6"

BACKGROUND = "#F5F7FA"
WHITE = "#FFFFFF"
BORDER = "#E4E7EC"
MUTED = "#667085"


# ==========================================================
# PROFESSIONAL CSS
# ==========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {BACKGROUND};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    .main-title {{
        font-size: 36px;
        font-weight: 750;
        color: {NAVY};
        margin-bottom: 3px;
    }}

    .subtitle {{
        color: {MUTED};
        font-size: 16px;
        margin-bottom: 18px;
    }}

    .section-title {{
        color: {NAVY};
        font-size: 21px;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 10px;
    }}

    /* KPI CARDS */

    .kpi-card {{
        background-color: {WHITE};
        padding: 20px 22px;
        border-radius: 12px;
        border: 1px solid {BORDER};
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
        min-height: 105px;
    }}

    .kpi-title {{
        color: {MUTED};
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}

    .kpi-value {{
        color: {NAVY};
        font-size: 30px;
        font-weight: 750;
        margin-top: 5px;
    }}

    /* BUTTON */

    .stButton > button {{
        background-color: {NAVY};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 650;
    }}

    .stButton > button:hover {{
        background-color: {BLUE};
        color: white;
    }}

    /* DATA TABLE */

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# GOOGLE SHEETS CONNECTION
# ==========================================================

conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)

df = conn.read(ttl=0)


# ==========================================================
# CLEAN DATA
# ==========================================================

df.columns = df.columns.str.strip()

for column in df.columns:

    if df[column].dtype == "object":

        df[column] = df[column].fillna(
            "Not specified"
        )


# ==========================================================
# SALARY AVAILABILITY
# ==========================================================

if "Salary" in df.columns:

    salary_text = (
        df["Salary"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["Salary_Available"] = ~salary_text.isin(
        [
            "",
            "not specified",
            "nan",
            "none",
            "null",
            "undefined"
        ]
    )

else:

    df["Salary_Available"] = False


# ==========================================================
# DATE CONVERSION
# ==========================================================

if "Posted_Date" in df.columns:

    df["Posted_Date"] = pd.to_datetime(
        df["Posted_Date"],
        errors="coerce"
    )


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">💼 Job & Internship Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Live job market overview powered by Google Sheets'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# REFRESH BUTTON
# ==========================================================

col_refresh, col_status = st.columns([1, 4])

with col_refresh:

    if st.button("🔄 Refresh Data"):

        st.rerun()


with col_status:

    st.caption(
        "Refresh to load the latest data from Google Sheets."
    )


# ==========================================================
# FILTERS
# ==========================================================

st.markdown(
    '<div class="section-title">🔎 Filters</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


# ----------------------------------------------------------
# LOCATION
# ----------------------------------------------------------

with col1:

    locations = ["All"] + sorted(
        df["Location"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_location = st.selectbox(
        "Location",
        locations
    )


# ----------------------------------------------------------
# CATEGORY
# ----------------------------------------------------------

with col2:

    categories = ["All"] + sorted(
        df["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )


# ----------------------------------------------------------
# COMPANY
# ----------------------------------------------------------

with col3:

    companies = ["All"] + sorted(
        df["Company"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_company = st.selectbox(
        "Company",
        companies
    )


# ----------------------------------------------------------
# JOB TYPE
# ----------------------------------------------------------

with col4:

    job_types = ["All"] + sorted(
        df["Job_Type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_job_type = st.selectbox(
        "Job Type",
        job_types
    )


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df.copy()


if selected_location != "All":

    filtered_df = filtered_df[
        filtered_df["Location"] == selected_location
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


if selected_company != "All":

    filtered_df = filtered_df[
        filtered_df["Company"] == selected_company
    ]


if selected_job_type != "All":

    filtered_df = filtered_df[
        filtered_df["Job_Type"] == selected_job_type
    ]


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_jobs = len(filtered_df)

companies_hiring = filtered_df["Company"].nunique()

locations_count = filtered_df["Location"].nunique()

salary_jobs = int(
    filtered_df["Salary_Available"].sum()
)


# ==========================================================
# KEY METRICS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Key Metrics</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)


# ----------------------------------------------------------
# TOTAL JOBS
# ----------------------------------------------------------

with k1:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">TOTAL JOBS</div>'
        f'<div class="kpi-value">{total_jobs:,}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# COMPANIES
# ----------------------------------------------------------

with k2:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">COMPANIES HIRING</div>'
        f'<div class="kpi-value">{companies_hiring:,}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# LOCATIONS
# ----------------------------------------------------------

with k3:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">LOCATIONS</div>'
        f'<div class="kpi-value">{locations_count:,}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# SALARY LISTED
# ----------------------------------------------------------

with k4:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">SALARY LISTED</div>'
        f'<div class="kpi-value">{salary_jobs:,}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ==========================================================
# CHART TEMPLATE
# ==========================================================

chart_template = "plotly_white"


# ==========================================================
# JOB DISTRIBUTION
# ==========================================================

st.markdown(
    '<div class="section-title">📍 Job Distribution</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)


# ==========================================================
# JOBS BY LOCATION
# ==========================================================

with c1:

    location_data = (
        filtered_df["Location"]
        .value_counts()
        .reset_index()
    )

    location_data.columns = [
        "Location",
        "Jobs"
    ]

    fig_location = px.bar(
        location_data.head(10),
        x="Jobs",
        y="Location",
        orientation="h",
        title="Jobs by Location",
        template=chart_template
    )

    fig_location.update_traces(
        marker_color=BLUE,
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Jobs: %{x}"
            "<extra></extra>"
        )
    )

    fig_location.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        showlegend=False,
        height=400,
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_location,
        use_container_width=True
    )


# ==========================================================
# JOBS BY CATEGORY
# ==========================================================

with c2:

    category_data = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [
        "Category",
        "Jobs"
    ]

    fig_category = px.pie(
        category_data,
        names="Category",
        values="Jobs",
        hole=0.48,
        title="Jobs by Category",
        template=chart_template
    )

    category_colors = [
        NAVY,
        BLUE,
        LIGHT_BLUE,
        SOFT_BLUE,
        PALE_BLUE
    ]

    fig_category.update_traces(
        marker=dict(
            colors=category_colors[
                :len(category_data)
            ]
        ),
        textposition="inside",
        textinfo="percent+label"
    )

    fig_category.update_layout(
        height=400,
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ==========================================================
# HIRING & FRESHNESS
# ==========================================================

st.markdown(
    '<div class="section-title">🏢 Hiring & Freshness</div>',
    unsafe_allow_html=True
)

c3, c4 = st.columns(2)


# ==========================================================
# TOP HIRING COMPANIES
# ==========================================================

with c3:

    company_data = (
        filtered_df["Company"]
        .value_counts()
        .reset_index()
    )

    company_data.columns = [
        "Company",
        "Jobs"
    ]

    fig_company = px.bar(
        company_data.head(10),
        x="Jobs",
        y="Company",
        orientation="h",
        title="Top Hiring Companies",
        template=chart_template
    )

    fig_company.update_traces(
        marker_color=LIGHT_BLUE,
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Jobs: %{x}"
            "<extra></extra>"
        )
    )

    fig_company.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        showlegend=False,
        height=400,
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_company,
        use_container_width=True
    )


# ==========================================================
# JOB FRESHNESS
# ==========================================================

with c4:

    if "Job_Status" in filtered_df.columns:

        status_data = (
            filtered_df["Job_Status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "Status",
            "Jobs"
        ]

        # SAME COLOR THEME AS THE REST OF THE DASHBOARD

        freshness_colors = [
            NAVY,
            BLUE,
            LIGHT_BLUE,
            SOFT_BLUE,
            PALE_BLUE
        ]

        fig_status = px.pie(
            status_data,
            names="Status",
            values="Jobs",
            hole=0.48,
            title="Job Freshness",
            template=chart_template
        )

        fig_status.update_traces(
            marker=dict(
                colors=freshness_colors[
                    :len(status_data)
                ]
            ),
            textposition="inside",
            textinfo="percent+label"
        )

        fig_status.update_layout(
            height=400,
            margin=dict(
                l=10,
                r=10,
                t=55,
                b=10
            )
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )


# ==========================================================
# MOST IN-DEMAND SKILLS
# ==========================================================

st.markdown(
    '<div class="section-title">🧠 Most In-Demand Skills</div>',
    unsafe_allow_html=True
)

skill_series = (
    filtered_df["Skills"]
    .astype(str)
    .str.split(", ")
    .explode()
)

skill_data = (
    skill_series
    .value_counts()
    .reset_index()
)

skill_data.columns = [
    "Skill",
    "Jobs"
]

skill_data = skill_data[
    skill_data["Skill"]
    .str.lower()
    != "not specified"
]


if not skill_data.empty:

    fig_skills = px.bar(
        skill_data.head(15),
        x="Jobs",
        y="Skill",
        orientation="h",
        title="Most Frequently Mentioned Skills",
        template=chart_template
    )

    fig_skills.update_traces(
        marker_color=BLUE,
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Jobs: %{x}"
            "<extra></extra>"
        )
    )

    fig_skills.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        showlegend=False,
        height=500,
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_skills,
        use_container_width=True
    )

else:

    st.info(
        "No extracted skills are currently available."
    )


# ==========================================================
# JOB POSTING TREND
# ==========================================================

st.markdown(
    '<div class="section-title">📈 Job Posting Trend</div>',
    unsafe_allow_html=True
)

if "Posted_Date" in filtered_df.columns:

    trend_data = (
        filtered_df
        .dropna(subset=["Posted_Date"])
        .copy()
    )

    if not trend_data.empty:

        trend_data["Month"] = (
            trend_data["Posted_Date"]
            .dt.to_period("M")
            .astype(str)
        )

        trend_data = (
            trend_data["Month"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        trend_data.columns = [
            "Month",
            "Jobs"
        ]

        fig_trend = px.line(
            trend_data,
            x="Month",
            y="Jobs",
            markers=True,
            title="Jobs Posted Over Time",
            template=chart_template
        )

        fig_trend.update_traces(
            line=dict(
                color=NAVY,
                width=3
            ),
            marker=dict(
                color=BLUE,
                size=7
            ),
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Jobs: %{y}"
                "<extra></extra>"
            )
        )

        fig_trend.update_layout(
            height=400,
            margin=dict(
                l=10,
                r=10,
                t=55,
                b=10
            )
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

    else:

        st.info(
            "No valid posting dates are available."
        )


# ==========================================================
# JOB OPPORTUNITIES
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Job Opportunities</div>',
    unsafe_allow_html=True
)

display_columns = [
    "Job_Title",
    "Company",
    "Location",
    "Job_Type",
    "Category",
    "Salary",
    "Posted_Date",
    "Skills",
    "Job_Status",
    "Application_URL"
]

available_columns = [
    column
    for column in display_columns
    if column in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Data source: Adzuna API → n8n → Google Sheets | "
    "Dashboard: Streamlit"
)