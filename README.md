\# Job \& Internship Analytics Dashboard



An interactive dashboard for analyzing job and internship opportunities using live job listing data.



\## Project Overview



This project collects job listings from the Adzuna API, processes and organizes the data using n8n, stores the updated data in Google Sheets, and displays the results through an interactive Streamlit dashboard.



\## Workflow



\*\*Adzuna API → n8n → Google Sheets → Streamlit\*\*



\## Features



\- Live job and internship data

\- Location-based filtering

\- Category filtering

\- Company filtering

\- Job type filtering

\- Total jobs KPI

\- Companies hiring KPI

\- Location count

\- Salary availability

\- Jobs by location

\- Jobs by category

\- Top hiring companies

\- Job freshness analysis

\- Most in-demand skills

\- Job posting trends

\- Job opportunity table with application links



\## Technologies Used



\- Python

\- Streamlit

\- Pandas

\- Plotly

\- n8n

\- Adzuna API

\- Google Sheets



\## Dashboard



The Streamlit dashboard provides an interactive view of job opportunities and allows users to filter the data based on different criteria.



\## Data Pipeline



1\. Adzuna API provides job listing data.

2\. n8n retrieves and processes the job data.

3\. Processed data is stored in Google Sheets.

4\. Streamlit reads the Google Sheet.

5\. The dashboard visualizes the latest available data.



\## Data Processing



The n8n workflow processes job listings by:



\- Cleaning job descriptions

\- Handling missing salary information

\- Calculating job age

\- Categorizing job freshness

\- Extracting relevant technical skills

\- Updating existing jobs using Job ID

\- Storing processed data in Google Sheets



\## Project Structure



```text

Job Dashboard/

├── job\_dashboard.py

├── requirements.txt

├── README.md

├── .gitignore

└── Job Tracker Data - Sheet1 (2).csv

