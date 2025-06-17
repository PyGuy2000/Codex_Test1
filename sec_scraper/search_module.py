import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import json
# Download NLTK resources
nltk.download('vader_lexicon')

# Define ESG keyword categories
esg_keywords = {
    'environmental': [
        'climate change', 'carbon', 'emissions', 'greenhouse gas', 'ghg', 'renewable', 
        'sustainability', 'sustainable', 'green', 'environmental', 'energy efficiency',
        'carbon neutral', 'net zero', 'pollution', 'clean energy', 'solar', 'wind power'
    ],
    'social': [
        'diversity', 'inclusion', 'equity', 'dei', 'community', 'human rights', 'labor', 
        'health and safety', 'employee', 'social responsibility', 'gender', 'racial', 
        'indigenous', 'stakeholder', 'supply chain', 'customer safety'
    ],
    'governance': [
        'board diversity', 'executive compensation', 'ethics', 'compliance', 'transparency',
        'accountability', 'risk management', 'audit', 'shareholder', 'corporate governance',
        'bribery', 'corruption', 'whistleblower', 'disclosure', 'voting rights'
    ]
}

# Load processed documents
with open("edgar_data/all_processed_docs.json", 'r', encoding='utf-8') as f:
    docs = json.load(f)

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Group documents by year
docs_2020 = [doc for doc in docs if doc['metadata']['year'] == '2020']
docs_2024 = [doc for doc in docs if doc['metadata']['year'] == '2024']

# Function to analyze ESG keywords in documents
def analyze_esg_keywords(documents):
    results = {
        'environmental': [],
        'social': [],
        'governance': [],
        'overall': []
    }
    
    for doc in documents:
        text = doc.get('content', '')  # Adjust based on your parser's output structure
        
        # Count ESG keywords
        e_count = sum(text.lower().count(kw) for kw in esg_keywords['environmental'])
        s_count = sum(text.lower().count(kw) for kw in esg_keywords['social'])
        g_count = sum(text.lower().count(kw) for kw in esg_keywords['governance'])
        total_count = e_count + s_count + g_count
        
        # Calculate document length for normalization
        doc_length = len(text.split())
        
        # Normalize counts (per 1000 words)
        if doc_length > 0:
            e_normalized = (e_count / doc_length) * 1000
            s_normalized = (s_count / doc_length) * 1000
            g_normalized = (g_count / doc_length) * 1000
            total_normalized = (total_count / doc_length) * 1000
        else:
            e_normalized = s_normalized = g_normalized = total_normalized = 0
        
        # Find sentences containing ESG terms
        all_esg_terms = esg_keywords['environmental'] + esg_keywords['social'] + esg_keywords['governance']
        esg_sentences = []
        
        for sentence in re.split(r'[.!?]', text):
            if any(kw in sentence.lower() for kw in all_esg_terms):
                esg_sentences.append(sentence.strip())
        
        # Calculate sentiment for ESG sentences
        sentiments = [sia.polarity_scores(sentence)['compound'] for sentence in esg_sentences]
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        
        # Store results
        doc_result = {
            'ticker': doc['metadata']['ticker'],
            'filing_type': doc['metadata']['filing_type'],
            'date': doc['metadata']['date'],
            'e_count': e_count,
            'e_normalized': e_normalized,
            's_count': s_count,
            's_normalized': s_normalized,
            'g_count': g_count,
            'g_normalized': g_normalized,
            'total_count': total_count,
            'total_normalized': total_normalized,
            'esg_sentences': len(esg_sentences),
            'avg_sentiment': avg_sentiment
        }
        
        results['environmental'].append(e_normalized)
        results['social'].append(s_normalized)
        results['governance'].append(g_normalized)
        results['overall'].append(total_normalized)
    
    return results

# Analyze both time periods
results_2020 = analyze_esg_keywords(docs_2020)
results_2024 = analyze_esg_keywords(docs_2024)

# Visualize the results
plt.figure(figsize=(12, 8))

# ESG category comparison between years
categories = ['Environmental', 'Social', 'Governance', 'Overall']
avg_2020 = [np.mean(results_2020['environmental']), np.mean(results_2020['social']), 
            np.mean(results_2020['governance']), np.mean(results_2020['overall'])]
avg_2024 = [np.mean(results_2024['environmental']), np.mean(results_2024['social']), 
            np.mean(results_2024['governance']), np.mean(results_2024['overall'])]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, avg_2020, width, label='2020')
rects2 = ax.bar(x + width/2, avg_2024, width, label='2024')

ax.set_title('ESG Keyword Frequency in Energy Sector SEC Filings')
ax.set_ylabel('Frequency per 1000 words')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

plt.tight_layout()
plt.savefig("esg_comparison.png")
plt.show()
