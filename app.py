from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
summarizer = pipeline("summarization")

@app.route('/summarize', methods=['POST'])
def summarize_article():
    try:
        # Get the URL of the article from the request
        article_url = request.json.get('url')

        # Fetch the content of the article (you might need to use libraries like requests or urllib)
        # For simplicity, let's assume you have a function called fetch_article_content
        article_content = fetch_article_content(article_url)

        # Chunk the article content into smaller parts
        chunk_size = 1000  # Adjust the chunk size as needed
        chunks = [article_content[i:i + chunk_size] for i in range(0, len(article_content), chunk_size)]

        # Summarize each chunk and concatenate the summaries
        summarized_text = ""
        for chunk in chunks:
            chunk_summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            summarized_text += chunk_summary + "\n"

        return jsonify({'summary': summarized_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def fetch_article_content(url):
    try:
        # Fetch the HTML content of the article
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            # Extract the main text content from the article (you may need to adjust this based on the structure of the website)
            article_content = ""
            for paragraph in soup.find_all('p'):
                article_content += paragraph.get_text() + "\n"
            return article_content
        else:
            return "Failed to fetch article content"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)