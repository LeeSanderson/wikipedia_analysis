import sys
import os
import json
import requests
import nltk
from collections import Counter
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Create cache directory
CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

def download_nltk_data():
    nltk.download('punkt')
    nltk.download('stopwords')

def get_cache_path(category=None, title=None):
    if category:
        return os.path.join(CACHE_DIR, f"{category}_members.json")
    return os.path.join(CACHE_DIR, f"{title.replace('/', '_')}.json")

def get_category_members(category):
    cache_path = get_cache_path(category=category)
    
    # Try to load from cache first
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "500"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    pages = [page['title'] for page in data['query']['categorymembers'] if page['ns'] == 0]
    
    # Save to cache
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(pages, f)
    
    return pages

def get_page_content(title):
    cache_path = get_cache_path(title=title)
    
    # Try to load from cache first
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "explaintext": True
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    content = pages[page_id].get('extract', '')
    
    # Save to cache
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(content, f)
    
    return content

def analyze_text(text, stop_words):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return Counter(words)

def main():
    if len(sys.argv) != 2:
        print("Usage: python wiki_category_analysis.py <category_name>")
        sys.exit(1)
    
    category = sys.argv[1]
    print(f"Analyzing category: {category}")
    
    # Download required NLTK data
    download_nltk_data()
    stop_words = set(stopwords.words('english'))
    
    # Get all pages in the category
    print("Fetching category members...")
    pages = get_category_members(category)
    
    if not pages:
        print("No pages found in the category.")
        return
    
    # Analyze each page
    total_word_freq = Counter()
    print("\nAnalyzing pages...")
    for page_title in tqdm(pages):
        content = get_page_content(page_title)
        word_freq = analyze_text(content, stop_words)
        total_word_freq.update(word_freq)
    
    # Print results
    print("\nMost common non-common words and their frequencies:")
    for word, freq in total_word_freq.most_common(20):
        print(f"{word}: {freq}")

if __name__ == "__main__":
    main()
