import streamlit as st
import requests

st.title("📰 News Summarization & Sentiment Analysis")

company_name = st.text_input("Enter a company name:", "")

if st.button("Analyze News"):
    if company_name:
        with st.spinner("Fetching news..."):
            response = requests.get(f"http://127.0.0.1:5001/get_news?company={company_name}")
            if response.status_code == 200:
                articles = response.json()
                
                st.subheader("📌 Extracted Articles")
                for i, article in enumerate(articles):
                    st.write(f"**{i+1}. {article['title']}**")
                    st.write(f"[Read More]({article['link']})")

                with st.spinner("Performing sentiment analysis..."):
                    analysis_response = requests.post("http://127.0.0.1:5001/analyze_news", json={"articles": articles})
                    if analysis_response.status_code == 200:
                        results = analysis_response.json()

                        st.subheader("📊 Sentiment Analysis")
                        for result in results:
                            st.write(f"🔹 **Title:** {result['title']}")
                            st.write(f"📌 **Summary:** {result['summary']}")
                            st.write(f"🔺 **Sentiment:** {result['sentiment']}")
                            st.write("---")

                        with st.spinner("Generating Hindi Speech..."):
                            text_summary = " ".join([res["summary"] for res in results])
                            tts_response = requests.post("http://127.0.0.1:5001/generate_tts", json={"text": text_summary})
                            
                            if tts_response.status_code == 200:
                                audio_file = tts_response.json()["audio_file"]
                                st.audio(audio_file)
                            else:
                                st.error("Error generating TTS")
                    else:
                        st.error("Error analyzing news")
            else:
                st.error("Error fetching news")
    else:
        st.warning("Please enter a company name")
        
def get_tts(text):
    print("Sending text to TTS:", text) 
    response = requests.post("http://127.0.0.1:5001/generate_tts", json={"text": text})
    print("TTS Response:", response.text)
    return response.json()