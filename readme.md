# 📑 BBC Dari Web Crawler  
*A Python-based crawler for building a structured Dari text dataset*  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)  
![BeautifulSoup](https://img.shields.io/badge/Library-BeautifulSoup4-brightgreen?style=flat-square)  
![Pandas](https://img.shields.io/badge/Library-Pandas-yellow?style=flat-square)  

---

## 📘 Project Overview  
This project is a **Python web crawler** that extracts and organizes news articles from **BBC Dari** into a structured dataset.  
The crawler systematically collects **headlines, publication dates, authors, article bodies, and URLs**, and saves them into a **CSV file (`dari_dataset.csv`)** encoded in UTF-8.  

The dataset is intended for **academic and research use**, particularly in **Natural Language Processing (NLP)**, **machine learning**, and **linguistic studies** involving the Dari language.  

---

## 🎯 Objectives  
- ✅ Build a clean and reliable **Dari-language dataset**.  
- ✅ Facilitate **NLP tasks** such as classification, sentiment analysis, and summarization.  
- ✅ Provide resources for **machine learning models** trained on low-resource languages.  
- ✅ Contribute to **linguistic research** in Dari.  

---

## 🔑 Features  
- 🌐 Crawls multiple BBC Dari categories (Politics, Economy, Culture, World, etc.).  
- 📝 Extracts clean, UTF-8 encoded text suitable for NLP tasks.  
- 💾 Stores structured data in a **CSV format**.  
- 🔄 Designed to be **extendable** to other Dari-language news sources.  

---

## 📂 Dataset Format (`dari_dataset.csv`)  
| Column   | Description |  
|----------|-------------|  
| `title`  | Headline of the article |  
| `date`   | Publication date (ISO format) |  
| `author` | Author name (if available, else `null`) |  
| `content`| Full article text |  
| `url`    | Original source link |  

---

## 🛠️ Installation & Usage  

### Prerequisites  
- Python 3.9+  
- Install dependencies:  
```bash
pip install requests beautifulsoup4 pandas
