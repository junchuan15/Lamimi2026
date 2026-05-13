## Introduction

This is the project repository for team **Lamimi** for **UKM Data Challenge 5.0**. Contributing towards **SDG 4: Quality Education** and **SDG 8: Decent Work and Economic Growth**, this project aims to bridge 3Es: **Education**, **Employment** and **Economy** by:

- Investigating on graduate statistics
- Analyzing sectoral absorption of graduates into the workforce
- Evaluate the economic impact of graduate employability 

---

## Data Sources

Data used in this project is collected from two office sources:

1. **Department of Statistics Malaysia (DOSM)**
   - Official statistics on graduates, employment, unemployment, and labor market indicators
   - Link: [open.dosm.gov.my](https://open.dosm.gov.my/)

2. **Malaysia's Official Open Data Portal**
   - National datasets including GDP, population, and macroeconomic indicators
   - Link: [data.gov.my](https://data.gov.my/)

---

## Methodology

### Data Medallion Architecture

The data pipeline adopts a **data medallion architecture** for with **Supabase** as data warehouse and **Apache Airflow** as orchestrator. Data are seperated into 3 layers:

- **Bronze Layer**: Raw data ingested directly from source systems
- **Silver Layer**: Cleaned, processed and transformed data
- **Gold Layer**: Business-ready data

### Dashboard

Power BI dashboard transforms processed gold layer data into actionable insights across four main pages:

1. **Home Page**: Navigation hub and key performance indicators
2. **Education Page**: Multidimensional analysis of graduate statistics
3. **Employment Page**: Graduate supply vs. sectoral demand mapping, gap identification, and underutilization analysis
4. **Economy Page**: Graduate employability's impact on national economic performance

**View Dashboard**: [Power BI Link](https://app.powerbi.com/view?r=eyJrIjoiMjg2ZTgyYzAtYzk4Mi00YThjLTkzZTctZmQzODc4ODc0ODRiIiwidCI6ImE2M2JiMWE5LTQ4YzItNDQ4Yi04NjkzLTMzMTdiMDBjYTdmYiIsImMiOjEwfQ%3D%3D)

---

## Repository Structure

```
Lamimi2026/
├── airflow/                          # Apache Airflow DAG orchestration
│   └── dags/
│       └── pipeline_orchestrator.py  # Main pipeline DAG 
│
├── src/                              # Core data processing pipelines
│   ├── landing/                      # Bronze layer - raw data ingestion notebooks
│   ├── staging/                      # Silver layer - data transformation notebooks
│   ├── ml/                           # Machine learning transformation notebooks
│   ├── powerbi/                      # Gold layer - business-ready data aggregation notebooks
│   │   ├── Dimension/                # Dimension tables for Power BI
│   │   └── Fact/                     # Fact tables for Power BI
│   └── utils/                        # Shared utilities
│       ├── __init__.py
│       ├── db_utils.py               # Supabase connection 
│       └── notebook_runner.py        # Notebook execution 
│
├── data/                             # Raw data
├── requirements.txt                  
├── README.md                         
└── .gitignore                        
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Supabase project initialized
- Apache Airflow installed

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/junchuan15/Lamimi_UKM-Data-Challenge-5.0.git
cd Lamimi_UKM-Data-Challenge-5.0
```

#### 2. Create a Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the `src/` directory with the following credentials obtained from Supabase connector:

```env
host=your_database_host
port=5432
dbname=your_database_name
user=your_database_user
password=your_database_password
```
