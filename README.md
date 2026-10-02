# 🍽️ DineSight — AI-Powered Restaurant Review Analyzer

DineSight is an end-to-end **restaurant review analytics platform** that converts raw customer reviews into structured, actionable insights.

It combines **data cleaning, exploratory analysis, statistical testing, outlier detection, rule-based NLP, theme extraction, hierarchical qualitative analysis, and relevance scoring** to help restaurant stakeholders understand what customers like, what they dislike, and why.

---

## 🚀 What Does DineSight Do?

Restaurant reviews contain a lot of useful information, but simply calculating an average rating does not explain **why** customers are satisfied or dissatisfied.

DineSight addresses this by analyzing reviews from two perspectives:

### 📊 Quantitative Analysis

It analyzes the numerical and structured information in reviews, including:

- Overall ratings
- Review counts
- Likes / engagement
- City-wise performance
- Cuisine-wise performance
- Restaurant-wise performance
- Rating distributions
- Temporal trends
- Statistical outliers
- Correlations
- Statistical significance

### 💬 Qualitative Analysis

It analyzes the actual review text to identify:

- Customer sentiment/polarity
- Recurring themes
- Sub-themes
- Food quality issues
- Service-related issues
- Specific customer complaints
- Dish-level problems
- Relevant customer quotes

The two analysis layers are combined to produce a more complete picture of restaurant performance.

---

# ✨ Key Features

## 1. 📥 Flexible Data Ingestion

DineSight accepts restaurant review data in:

- CSV
- XLS
- XLSX

The ingestion pipeline automatically:

- Detects the header row
- Normalizes column names
- Maps different column names to a common schema
- Handles duplicate columns
- Fills missing fields with sensible defaults
- Converts ratings into numeric values
- Generates missing review text from ratings when necessary

This allows datasets with different column naming conventions to be analyzed using the same pipeline.

---

## 2. 🧹 Data Standardization

Raw review datasets are transformed into a consistent schema containing fields such as:

```text
created_at
reviewer_name
review_text
rating_overall
like_count
restaurant_name
city
primary_cuisine
```

The pipeline also generates additional features such as:

```text
date
year_month
day_of_week
hour_of_day
restaurant_review_count
restaurant_overall_rating
```

This standardized dataset becomes the foundation for the downstream analysis pipeline.

---

# 📊 Quantitative Analytics

DineSight performs multiple statistical analyses using **Pandas, NumPy and SciPy**.

### Descriptive Statistics

The system calculates:

- Mean
- Median
- Standard deviation
- Coefficient of variation
- Rating range
- Review counts
- Average likes
- Restaurant-level statistics
- City-level statistics
- Cuisine-level statistics

It can automatically determine whether the dataset represents:

- A single restaurant
- Multiple restaurants in one city
- Multiple cities

---

## 🧪 Statistical Testing

DineSight goes beyond descriptive statistics by testing whether observed differences are statistically meaningful.

### ANOVA

Used to compare rating distributions across:

- Cities
- Cuisines

The system reports:

- F-statistic
- p-value
- η² (eta-squared)
- Effect size
- Statistical significance

### Independent T-Test

Ratings are compared between:

- Reviews with likes
- Reviews without likes

The system reports:

- t-statistic
- p-value
- Cohen's d
- Effect size
- Mean difference

### Pearson Correlation

The relationship between:

```text
Rating ↔ Likes
```

is analyzed using Pearson correlation.

The system reports:

- Correlation coefficient
- p-value
- Correlation strength
- Statistical significance

---

# 🔎 Outlier & Anomaly Detection

DineSight uses multiple approaches to identify unusual review behavior.

### Statistical Outliers

It uses:

- IQR method
- Z-score method

for variables such as:

- Ratings
- Likes
- Restaurant ratings

### Behavioral Anomalies

The system also identifies unusual patterns such as:

- Reviews with unusually high engagement
- Low-rated reviews receiving unusually high engagement
- Reviews whose rating differs substantially from the restaurant's overall rating

This allows the system to distinguish ordinary statistical variation from potentially interesting review behavior.

---

# 🧠 NLP-Based Theme Extraction

DineSight uses a lightweight, interpretable **rule-based NLP pipeline** for extracting meaningful themes from review text.

Instead of relying entirely on black-box predictions, the system uses domain-specific keywords and phrases.

The pipeline performs:

```text
Review
   ↓
Text Normalization
   ↓
Tokenization
   ↓
Stopword Filtering
   ↓
Phrase Matching
   ↓
Token Matching
   ↓
Theme + Sub-theme + Polarity
```

For example, a review mentioning:

> "The food was cold and the portion was too small."

can be associated with concepts such as:

```text
Theme: Food
Sub-theme: Temperature
Polarity: Negative

Theme: Food
Sub-theme: Portion Size
Polarity: Negative
```

Phrase matching is prioritized for higher precision, while token matching provides a fallback mechanism.

---

# 🔬 Multi-Tier Qualitative Analysis

One of the core components of DineSight is its hierarchical analysis pipeline.

Instead of treating every complaint as simply "negative sentiment", the system progressively investigates **what went wrong and why**.

## Tier 1 — Problem Domain

Reviews are classified into broad issue domains such as:

```text
FOOD_PROBLEM
SERVICE_PROBLEM
...
```

The system calculates the distribution of identified issue categories.

---

## Tier 2 — Food Quality Diagnostics

Food-related negative reviews are further analyzed using dimensions such as:

- Texture
- Freshness
- Temperature
- Spice level
- Salt/sweet balance
- Portion size

This transforms a generic complaint like:

> "The food was bad."

into a more useful diagnosis such as:

```text
Food Problem
    ↓
Food Quality
    ↓
Temperature
```

---

## Tier 3 — Dish-Level Root Cause Analysis

The system goes one level deeper by connecting food complaints to specific dishes.

Examples of potential root causes include:

- Overcooked
- Undercooked
- Burnt
- Cold
- Soggy
- Dry
- Rubbery
- Stale
- Too salty
- Too spicy
- Oily
- Overpriced

The system identifies the most frequently occurring negative phrases and associates them with dishes mentioned in the reviews.

This helps answer:

> **"Which dishes are causing which customer complaints?"**

---

# ⭐ Relevant Quote Ranking

DineSight also ranks representative customer feedback.

Instead of simply displaying random negative reviews, it calculates a relevance score using multiple signals:

```text
Relevance Score
      =
Severity
× Theme Weight
× Sub-theme Weight
× Phrase Weight
× Specificity
```

The ranking considers:

- Review severity
- Importance of the issue domain
- Frequency of the sub-theme
- Root-cause frequency
- Specificity of the complaint

Generic phrases such as "bad" receive lower specificity scores than more informative complaints such as "served cold" or "too salty".

This produces a smaller set of representative signals that can be used for decision-making.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   CSV / Excel Data  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Ingestion &    │
                    │ Standardization     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Cleaned & Enriched  │
                    │ Review Dataset      │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
      ┌──────────────────┐          ┌──────────────────┐
      │ Quantitative     │          │ Qualitative/NLP  │
      │ Analysis         │          │ Analysis         │
      └────────┬─────────┘          └────────┬─────────┘
               │                             │
               ▼                             ▼
      ┌──────────────────┐          ┌──────────────────┐
      │ Statistics       │          │ Theme Extraction │
      │ ANOVA            │          │ Multi-tier NLP   │
      │ T-Test           │          │ Root Cause       │
      │ Correlation      │          │ Quote Ranking    │
      │ Outliers         │          └────────┬─────────┘
      └────────┬─────────┘                   │
               │                             │
               └──────────────┬──────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ Structured Insights │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   DineSight Web UI  │
                    └─────────────────────┘
```

---

# 🛠️ Tech Stack

### Backend

- **Python**
- **Flask**

### Data & Statistics

- **Pandas**
- **NumPy**
- **SciPy**

### NLP

- Rule-based text normalization
- Keyword and phrase matching
- Theme extraction
- Hierarchical qualitative analysis
- Domain-specific ontology

### Frontend

- HTML
- Tailwind CSS
- JavaScript
- Material Symbols
- Inter UI font

The repository's dependency configuration includes Flask, Gunicorn, python-dotenv, Pandas, NumPy, SciPy, and LangChain/Google Generative AI packages.

---

# 📁 Project Structure

```text
DineSight/
│
├── app.py
├── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── upload.html
│   ├── about.html
│   ├── quant.html
│   └── qual.html
│
├── scripts/
│   ├── runnner.py
│   ├── excel_ingestion.py
│   ├── quantitative_analysis.py
│   ├── theme_extraction.py
│   ├── multilayer_verbatim_analysis.py
│   ├── quote_relevance_scoring.py
│   ├── rule_keywords.json
│   └── food_domain_ontology.json
│
└── uploads/
```

The central runner orchestrates standardization, quantitative analysis, theme extraction, multi-layer qualitative analysis, and quote relevance scoring as a single pipeline.

---

# ⚙️ How the Pipeline Works

The complete analysis can be summarized as:

```text
1. Upload Dataset
        ↓
2. Detect & Standardize Schema
        ↓
3. Clean Reviews
        ↓
4. Generate Time & Restaurant Features
        ↓
5. Descriptive Statistics
        ↓
6. Statistical Testing
        ↓
7. Outlier Detection
        ↓
8. Theme Extraction
        ↓
9. Multi-Tier Qualitative Analysis
        ↓
10. Dish-Level Root Cause Analysis
        ↓
11. Quote Relevance Scoring
        ↓
12. Display Insights
```

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

- Python 3.9+
- pip
- Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/Tanmay140906/DineSight.git
cd DineSight
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

The Flask application will start locally.

Open:

```text
http://127.0.0.1:5000
```

---

# 📄 Input Data

DineSight can process CSV and Excel files containing restaurant review information.

The ingestion layer attempts to map different column names to a standardized schema.

For example:

| Possible Input | Standardized Field |
|---|---|
| `review`, `comment`, `feedback` | `review_text` |
| `rating`, `stars`, `score` | `rating_overall` |
| `restaurant`, `cafe`, `business` | `restaurant_name` |
| `city`, `location`, `town` | `city` |
| `cuisine`, `food_type` | `primary_cuisine` |
| `likes`, `upvotes` | `like_count` |

This makes the analysis pipeline less dependent on a particular dataset format.

---

# 📈 Example Insights

DineSight is designed to answer questions such as:

### Restaurant Performance

- What is the average restaurant rating?
- Which restaurants receive the most reviews?
- How consistent are ratings?
- Which cities or cuisines show different rating patterns?

### Customer Experience

- What are customers complaining about most?
- Are complaints related to food, service, or value?
- Which food-quality dimensions generate the most negative feedback?

### Root Causes

- Which dishes receive the most complaints?
- Are customers complaining about temperature, texture, freshness, quantity, or taste?
- Which specific phrases repeatedly appear in low-rated reviews?

### Engagement

- Do highly-rated reviews receive more likes?
- Are unusually negative reviews attracting unusually high engagement?

---

# 🎯 Why DineSight?

Traditional restaurant analytics often reduces customer feedback to:

```text
Average Rating = 4.1 ⭐
```

DineSight attempts to answer the more useful question:

```text
Why is the rating 4.1?
What do customers like?
What are they unhappy about?
What specific problems keep appearing?
Which dishes are involved?
```

By combining statistical analysis with structured review-text analysis, the system turns unstructured customer feedback into more interpretable insights.

---

# 🔮 Future Improvements

Potential extensions include:

- Transformer-based sentiment classification
- Aspect-based sentiment analysis
- Multilingual review support
- Embedding-based semantic similarity
- Automated theme discovery
- Interactive dashboards
- Database-backed storage
- Authentication and multi-user support
- Deployment using Docker
- LLM-generated natural-language executive summaries
- Real-time review ingestion

---

# 👨‍💻 Author

**Tanmay Gupta**

GitHub: [@Tanmay140906](https://github.com/Tanmay140906)

---

# 📜 License

Add the appropriate license for your project here.

---

## ⭐ Project Summary

**DineSight is an end-to-end restaurant review analytics platform that combines statistical analysis and rule-based NLP to transform raw customer reviews into structured insights, recurring themes, and dish-level root causes.**
