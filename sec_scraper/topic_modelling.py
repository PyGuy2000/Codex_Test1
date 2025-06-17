from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from search_module import docs_2020, docs_2024  # Assuming you have the documents loaded

# Prepare document texts for topic modeling
texts_2020 = [doc.get('content', '') for doc in docs_2020]
texts_2024 = [doc.get('content', '') for doc in docs_2024]

# Function to perform topic modeling
def perform_topic_modeling(texts, n_topics=5):
    # Create vectorizer
    vectorizer = CountVectorizer(
        max_df=0.95, min_df=2, 
        stop_words='english', 
        max_features=1000
    )
    
    # Fit and transform texts
    X = vectorizer.fit_transform(texts)
    
    # Create and fit LDA model
    lda = LatentDirichletAllocation(
        n_components=n_topics, 
        random_state=42,
        learning_method='online'
    )
    
    lda.fit(X)
    
    # Extract top words for each topic
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[:-10-1:-1]
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append({
            'topic_id': topic_idx,
            'top_words': top_words
        })
    
    return topics, lda, vectorizer

# Perform topic modeling for both periods
topics_2020, lda_2020, vectorizer_2020 = perform_topic_modeling(texts_2020)
topics_2024, lda_2024, vectorizer_2024 = perform_topic_modeling(texts_2024)

# Output topics
print("2020 Topics:")
for topic in topics_2020:
    print(f"Topic {topic['topic_id']}: {', '.join(topic['top_words'])}")

print("\n2024 Topics:")
for topic in topics_2024:
    print(f"Topic {topic['topic_id']}: {', '.join(topic['top_words'])}")
