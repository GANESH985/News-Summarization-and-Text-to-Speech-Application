import requests
import torch
from transformers import pipeline
from gtts import gTTS
import os

def fetch_news(company):
    """Fetches news articles related to a company from an API"""
    API_URL = f"https://newsapi.org/v2/everything?q={company}&apiKey=YOUR_NEWS_API_KEY"
    response = requests.get(API_URL)
    data = response.json()
    
    articles = []
    for article in data["articles"][:5]:
        articles.append({
            "title": article["title"],
            "content": article["description"] or "",
            "topics": ["Stock Market", "Technology"] 
        })
    return articles

def summarize_text(text):
    """Summarizes text using Hugging Face transformers"""
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]["summary_text"]

def analyze_sentiment(text):
    """Analyzes sentiment using Hugging Face transformers"""
    classifier = pipeline("sentiment-analysis")
    result = classifier(text)
    return result[0]["label"]

def generate_tts(text):
    """Generates Hindi speech from text"""
    tts = gTTS(text=text, lang="hi")
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path
