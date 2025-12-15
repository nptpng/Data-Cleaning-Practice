# 🧼 Data Cleaning Practice Project (Python & SQL)

This project simulates a student enrollment management system to practice **data cleaning** and **data validation** skills using commonly used data tools in real-world data roles.

---

## 🎯 Project Objective

The goal of this project is to transform **dirty and unreliable raw data** into **clean, structured, and usable data**.  
The project focuses on solving three major data quality issues:

1. **Incorrect or inconsistent formatting**
   - Extra spaces in names
   - Phone numbers containing dashes or special characters

2. **Duplicate records**
   - Users submitting the application multiple times

3. **Anomalous or invalid data**
   - Birth year set in the future
   - Invalid email formats

---

## 🛠️ Tools & Technologies

- **Python**
  - `Pandas` for data manipulation
  - `Faker` for generating mock data
- **Regular Expressions (Regex)**
  - Used for cleaning complex text patterns such as phone numbers
- **SQL (SQLite)**
  - Data validation and deduplication
  - Window functions and conditional logic

---

## 🏗️ Workflow

1. **Mock Data Generation**
   - Generate 300 simulated enrollment records
   - Intentionally inject data errors for testing purposes

2. **Data Cleaning with Python**
   - Trim extra spaces from names
   - Normalize phone numbers to digits-only format using Regex

3. **Data Validation & Deduplication with SQL**
   - Use `ROW_NUMBER()` to keep the latest record per applicant
   - Use `CASE WHEN` to classify records as:
     - **Verified** → valid email and realistic birth year
     - **Unverified** → requires manual review

---

## 📊 Final Output

The final dataset is clean and analysis-ready, with a clear verification status:

- **Verified**
  - Valid email format
  - Birth year within a realistic range

- **Unverified**
  - Contains data issues that require further inspection

---


## 🚀 How to Run the Project

1. Install required libraries:  `pip install pandas faker`
2. Run the script: `python main.py` (personally i run the script in Colab)

---



