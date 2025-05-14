import openai
import os
import json
import numpy as np
from typing import List, Dict, Tuple
import logging
import streamlit as st

logger = logging.getLogger(__name__)

def get_embedding(text: str) -> List[float]:
    """Generates embedding for the given text using OpenAI API."""
    try:
        client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Błąd podczas generowania embeddingu dla '{text}': {e}")
        raise

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculates cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_faq_data() -> Tuple[Dict[str, str], Dict[str, List[float]]]:
    """Loads FAQ data and their embeddings."""
    try:
        with open('data/faq.json', 'r', encoding='utf-8') as f:
            faq_data = json.load(f)
        
        # Generate embeddings for questions
        question_embeddings = {}
        for question in faq_data.keys():
            question_embeddings[question] = get_embedding(question)
        
        return faq_data, question_embeddings
    except Exception as e:
        logging.error(f"Błąd podczas ładowania FAQ lub generowania embeddingów: {e}")
        raise

def get_faq_answer(question: str) -> str:
    """Finds the most similar question in FAQ and returns the answer."""
    try:
        # Load FAQ data and embeddings
        faq_data, question_embeddings = load_faq_data()
        
        # Generate embedding for user's question
        question_embedding = get_embedding(question)
        
        # Find the most similar question
        max_similarity = -1
        most_similar_question = None
        
        for faq_question, faq_embedding in question_embeddings.items():
            similarity = cosine_similarity(question_embedding, faq_embedding)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_question = faq_question
        
        # If similarity is high enough, return the answer
        if max_similarity > 0.7:  # Similarity threshold
            return faq_data[most_similar_question]
        
        # If no sufficiently similar question is found, use GPT to generate the answer
        context = "FAQ:\n"
        for q, a in faq_data.items():
            context += f"P: {q}\nO: {a}\n\n"
        
        client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś asystentem FAQ. Odpowiadaj na pytania na podstawie dostępnych informacji."},
                {"role": "user", "content": f"{context}\nPytanie użytkownika: {question}"}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Błąd w get_faq_answer: {e}")
        raise
