from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text).sentiment.polarity
    if analysis > 0:
        return "Positive"
    elif analysis < 0:
        return "Negative"
    else:
        return "Neutral"