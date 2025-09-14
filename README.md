
# data-engineering-pipeline for AI Model Training


Youtube Video Link for its demonstartion (My Youtube Channel): https://youtu.be/KnMcTJ7cG20

## 📋 Project Overview
**Task**: Build a complete data engineering pipeline for recruitment-specific AI models  
**Domain Selected**: **Software Engineering**  
**Submission**: Complete end-to-end pipeline with real-world data collected from multiple sources  

---

## 🎯 Executive Summary

This project demonstrates **real execution** of a production-ready data engineering pipeline that collects, cleans, and annotates software engineering job market data. The solution simulates the exact workflow needed for training recruitment AI models at Parikshak.ai.

**Key Achievements:**
- ✅ Collected **106 real-world entries** from 4 legitimate data sources
- ✅ Built robust data cleaning with deduplication and normalization  
- ✅ Implemented comprehensive annotation system with 3 primary labels + 4 additional features
- ✅ Created production-ready, runnable pipeline with error handling
- ✅ Generated ML-ready datasets in both JSON and CSV formats

---

## 🏗️ Project Architecture

### Directory Structure
```
data-engineering-pipeline/
├── scraper/
│   └── job_scraper.py             # Data collection script  
│               
├── processing/
│   ├── data_cleaner.py             # Data cleaning script
│   └── data_annotator.py           # Data annotation script
├── data/                           # Generated datasets directory
│   ├── raw_jobs.json              # Raw scraped data (106 entries)
│   ├── raw_jobs.csv               # Raw data in CSV format
│   ├── cleaned_jobs.json          # Cleaned dataset (79 entries)
│   ├── cleaned_jobs.csv           # Cleaned data in CSV format
│   ├── annotated_jobs.json        # Final annotated dataset (79 entries)
│   ├── annotated_jobs.csv         # Annotated data in CSV format
├── main.py                        # Complete pipeline runner
├── requirements.txt               # Python dependencies
└── README.md                      # This documentation
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
# Clone/download the project files
cd software-engineering-pipeline

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Complete Pipeline
```bash
# Execute all three steps in sequence
python main.py
```

**Expected Output:**
```
🚀 Starting Data Engineering Pipeline for Job Data
📥 STEP 1: DATA SCRAPING - ✅ 106 entries collected
🧹 STEP 2: DATA CLEANING - ✅ 79 entries cleaned  
🏷️ STEP 3: DATA ANNOTATION - ✅ 79 entries annotated
🎉 Pipeline completed successfully!
```

---

## 📊 Step 1: Data Scraping & Collection

### **Approach: Multi-Source API Strategy**

Implemented a robust **API-based collection system** using 4 legitimate sources:

### **Data Sources Used:**

| Source | API Used | Content Type | Relevance |
|--------|----------|--------------|-----------|
| **GitHub API** | REST API v3 | Job repositories, career guides | High |
| **StackOverflow API** | StackExchange API | Career & interview questions | High |
| **Reddit API** | JSON API | Job discussions, career advice | High |
| **HackerNews API** | Firebase API | Tech job posts, hiring threads | Very High |

### **Content Types Collected:**
- ✅ **Job Descriptions**
- ✅ **Interview Questions**
- ✅ **Career Blogs / Advice**
- ✅ **Resume & Career Templates**

### **Technical Implementation:**
```python
class JobScraper:
    def scrape_all(self, total_count=60):
        # Multi-source collection with error handling
        self.scrape_github_jobs(count=15)      # Job-related repositories
        self.scrape_stackoverflow_jobs(count=15)  # Interview questions
        self.scrape_reddit_jobs(count=15)      # Career discussions  
        self.scrape_hackernews_jobs(count=15)  # Tech job posts
```

### **Smart Features:**
- **Rate Limiting**: 2-3 second delays between requests
- **User-Agent Rotation**: Prevents blocking
- **Error Resilience**: Continues collection even if one source fails

### **Output Files:**
- `data/raw_jobs.json` - Structured JSON with all scraped data
- `data/raw_jobs.csv` - CSV format for easy inspection

---

## 🧹 Step 2: Data Cleaning

### **Comprehensive Cleaning Process:**

#### **Text Normalization:**
```python
def clean_text(self, text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\/]', '', text)
```

#### **Data Standardization:**
- **Job Titles**: Normalized "Sr." → "Senior", "Jr." → "Junior"
- **Company Names**: Removed suffixes like "Inc.", "LLC", "Corp."
- **Consistent Formatting**: Title case, trimmed whitespace

#### **Quality Control:**
- **Duplicate Removal**: Based on title + company combination
- **Entry Validation**: Minimum content requirements (10+ char descriptions)
- **Empty Row Filtering**: Removes entries with insufficient data

#### **Statistics:**
- **Input**: 106 raw entries
- **After Validation**: 80 entries
- **After Deduplication**: 79 unique entries

### **Output Files:**
- `data/cleaned_jobs.json` - Clean, normalized dataset
- `data/cleaned_jobs.csv` - CSV format for analysis

---

## 🏷️ Step 3: Data Annotation

### **Annotation Strategy: 3 Primary Labels + 4 Additional Features**

#### **Primary Labels:**
1. **🔧 Skill Tags** - Technical skills extracted
2. **📈 Experience Level** - Entry, Mid, Senior, or Management
3. **📝 Content Type** - Job Description, Interview Question, Career Advice, Technical Discussion, Company Info

#### **Additional Features:**
4. **🎯 Relevance Score** (0-1)
5. **🏠 Remote Work**: Boolean
6. **🏢 Company Size**: Startup/Medium/Large
7. **📊 Content Analysis**: Text length, requirements presence

### **Output Files:**
- `data/annotated_jobs.json` - Complete annotated dataset (79 entries)
- `data/annotated_jobs.csv` - CSV format with annotations

---

## 📂 Complete Deliverables

### **1. Code Scripts** ✅

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `scraper/job_scraper.py` | Data collection | Multi-API integration, error handling |
| `processing/data_cleaner.py` | Data cleaning | Text normalization, deduplication |
| `processing/data_annotator.py` | Data annotation | ML-ready labeling system |
| `main.py` | Pipeline orchestration | End-to-end automation |

### **2. Data Files** ✅

| File | Description | Entry Count | Use Case |
|------|-------------|-------------|----------|
| `raw_jobs.json/.csv` | Raw scraped data | 106 entries | Initial collection results |
| `cleaned_jobs.json/.csv` | Cleaned dataset | 79 entries | Post-cleaning analysis |
| `annotated_jobs.json/.csv` | Final ML dataset | 79 entries | AI model training |

---

## 🛠️ Tools & Technologies Used

- **Python Libraries**: `requests`, `beautifulsoup4`, `pandas`
- **Data Formats**: JSON and CSV
- **APIs**: GitHub, StackExchange, Reddit, Firebase (HackerNews)
- **Processing Techniques**: Regex cleaning, text normalization, deduplication
- **Operational Features**: Rate limiting, error handling, modular pipeline

---

## 💡 Approach & Problem-Solving

- **Multi-source API collection** for legal, reliable data
- **Dynamic field normalization** for consistency
- **Deduplication & validation** for high-quality dataset
- **Annotation** with multi-layered labels for AI training

---

## 📊 Results & Metrics

- **Raw Entries**: 106
- **After Cleaning**: 79
- **After Annotation**: 79

**Content Types:**
- Job Descriptions
- Interview Questions
- Career Blogs/Advice
- Resume/Template content

**Annotation Accuracy**:
- Experience Level: Pattern-based
- Content Type: Multi-source validation

---

## 🚀 Production Readiness

- Modular, runnable pipeline
- JSON + CSV outputs
- Error-handling and rate-limiting implemented
- Fully ML-ready annotated dataset

---

**This pipeline demonstrates a production-ready, end-to-end approach for software engineering recruitment AI.** 🚀
