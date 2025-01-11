import stanza
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from ..logger import setup_logger

logger = setup_logger("summarizer", "logs/summarizer.log")

class TextSummarizer:
    def __init__(self):
        self.nlp = stanza.Pipeline('tr')
        
    def stanza_sentence_split(self, text):
        doc = self.nlp(text)
        return [sentence.text for sentence in doc.sentences]
    
    def compute_tfidf_weights(self, sentences):
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences)
        return X.sum(axis=1).A1
    
    def compute_graph_weights(self, sentences):
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        for i, sent1 in enumerate(sentences):
            for j, sent2 in enumerate(sentences):
                if i != j:
                    similarity_matrix[i][j] = len(set(sent1.split()) & set(sent2.split()))
        graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(graph)
        return [scores[i] for i in range(len(sentences))]
    
    def select_sentences(self, sentences, weights, threshold=0.25):
        sorted_indices = np.argsort(weights)[::-1]
        top_indices = sorted_indices[:int(len(sentences) * threshold)]
        return [sentences[i] for i in top_indices]
    
    def create_summary(self, set1, set2, sentences, summary_size=0.175):
        summary = []
        set1_indices = [sentences.index(sent) for sent in set1]
        set2_indices = [sentences.index(sent) for sent in set2]
        common_indices = set(set1_indices) & set(set2_indices)

        for idx in common_indices:
            if len(summary) / len(sentences) < summary_size:
                summary.append(sentences[idx])

        for idx in set1_indices + set2_indices:
            if len(summary) / len(sentences) < summary_size and sentences[idx] not in summary:
                summary.append(sentences[idx])

        return sorted(summary, key=sentences.index)
    
    def summarize_with_tfidf(self, text):
        try:
            sentences = self.stanza_sentence_split(text)
            if len(sentences) <= 3:
                return text

            tfidf_weights = self.compute_tfidf_weights(sentences)
            graph_weights = self.compute_graph_weights(sentences)

            top_tfidf_sentences = self.select_sentences(sentences, tfidf_weights)
            top_graph_sentences = self.select_sentences(sentences, graph_weights)

            summary = self.create_summary(top_tfidf_sentences, top_graph_sentences, sentences)
            return ' '.join(summary)
        except Exception as e:
            logger.error(f"Error in TF-IDF summarization: {e}", exc_info=True)
            raise 