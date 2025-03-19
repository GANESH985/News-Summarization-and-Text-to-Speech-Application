from flask import Flask, request, jsonify, send_file
import os
from gtts import gTTS
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")

def fetch_news(company_name):
    """Mock function to simulate fetching news articles."""
    articles = [
        {"title": "Tesla's New Model Breaks Sales Records", "content": "Tesla's latest EV sees record sales in Q3..."},
        {"title": "Regulatory Scrutiny on Tesla's Self-Driving Tech", "content": "Regulators have raised concerns over Tesla’s self-driving software..."},
        {"title": "Tesla's Stock Price Continues to Rise", "content": "Tesla's shares surge as investors remain bullish on EV market..."},
        {"title": "Tesla's New Model Breaks Sales Records", "content": "Tesla's latest EV sees record sales in Q3..."},
        {"title": "Regulatory Scrutiny on Tesla's Self-Driving Tech", "content": "Regulators have raised concerns over Tesla’s self-driving software..."},
        {"title": "Tesla's Stock Price Continues to Rise", "content": "Tesla's shares surge as investors remain bullish on EV market..."}
    ]
    return articles

def analyze_sentiment(text):
    """Performs sentiment analysis on text."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def extract_topics(text):
    """Extracts key topics from text."""
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(filtered_words)
    return [word for word, _ in word_freq.most_common(5)]

def generate_comparative_analysis(articles):
    """Creates a comparative sentiment and topic analysis."""
    positive_count = sum(1 for a in articles if a.get("Sentiment") == "Positive")
    negative_count = sum(1 for a in articles if a.get("Sentiment") == "Negative")
    neutral_count = sum(1 for a in articles if a.get("Sentiment") == "Neutral")
    
    topic_sets = [set(a.get("Topics", [])) for a in articles]
    common_topics = set.intersection(*topic_sets) if len(topic_sets) > 1 else set()
    unique_topics = [list(t - common_topics) for t in topic_sets]
    
    return {
        "Sentiment Distribution": {"Positive": positive_count, "Negative": negative_count, "Neutral": neutral_count},
        "Coverage Differences": [
            {"Comparison": "Article 1 highlights Tesla's strong sales, while Article 2 discusses regulatory issues.",
             "Impact": "The first article boosts confidence in Tesla's market growth, while the second raises concerns about future regulatory hurdles."},
            {"Comparison": "Article 1 is focused on financial success and innovation, whereas Article 2 is about legal challenges and risks.",
             "Impact": "Investors may react positively to growth news but stay cautious due to regulatory scrutiny."}
        ],
        "Topic Overlap": {
            "Common Topics": list(common_topics),
            "Unique Topics in Article 1": unique_topics[0] if unique_topics else [],
            "Unique Topics in Article 2": unique_topics[1] if len(unique_topics) > 1 else []
        }
    }

def generate_hindi_speech(text, filename="output.mp3"):
    """Generates Hindi TTS speech from text."""
    tts = gTTS(text=text, lang="hi")
    file_path = os.path.join("static", filename)
    tts.save(file_path)
    return file_path

@app.route('/get_news', methods=['GET'])
def get_news():
    company = request.args.get('company', '').strip()
    if not company:
        return jsonify({"error": "Missing company name."}), 400
    
    articles = fetch_news(company)
    processed_articles = []
    
    for article in articles:
        sentiment = analyze_sentiment(article["content"])
        topics = extract_topics(article["content"])
        processed_articles.append({
            "Title": article["title"],
            "Summary": article["content"],
            "Sentiment": sentiment,
            "Topics": topics
        })
    
    comparative_analysis = generate_comparative_analysis(processed_articles)
    final_sentiment = f"{company} की नवीनतम समाचार कवरेज ज्यादातर सकारात्मक है। संभावित स्टॉक वृद्धि की उम्मीद है।"
    
    audio_path = generate_hindi_speech(final_sentiment)

    return jsonify({
        "Company": company,
        "Articles": processed_articles,
        "Comparative Sentiment Score": comparative_analysis,
        "Final Sentiment Analysis": final_sentiment,
        "Audio": request.host_url + audio_path
    })

@app.route('/play_audio', methods=['GET'])
def play_audio():
    """Returns the generated audio file."""
    file_path = os.path.join("static", "output.mp3")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="audio/mp3")
    return jsonify({"error": "Audio file not found"}), 404

@app.route("/generate_tts", methods=["POST"])
def generate_tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        tts = gTTS(text, lang="hi")
        audio_path = "tts_output.mp3"
        tts.save(audio_path)

        return jsonify({"audio": audio_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
