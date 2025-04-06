from flask import Flask, render_template, jsonify, request
import os
import json
from wiki_category_analysis import get_category_members, get_page_content, analyze_text, download_nltk_data
from nltk.corpus import stopwords
import base64
from wordcloud import WordCloud
import io
from templates.colour_palette import get_all_colour_palettes
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

app = Flask(__name__)

# Initialize NLTK data
download_nltk_data()
stop_words = set(stopwords.words('english'))

def get_palette_colors(palette_name):
    palettes = {p.__class__.__name__: p for p in get_all_colour_palettes()}
    if palette_name not in palettes:
        return []
    return palettes[palette_name].get_colours()

def generate_word_cloud(word_freq, color_palette=None):
    # Create and generate a word cloud image
    wordcloud_params = {
        'width': 600,
        'height': 400,
        'background_color': 'white'
    }
    
    if color_palette:
        colors = get_palette_colors(color_palette)
        if colors:
            # Create a matplotlib colormap from our colors
            colors_float = [tuple(int(h.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4)) for h in colors]
            n_bins = 100  # Number of color gradients
            color_map = LinearSegmentedColormap.from_list('custom', colors_float, N=n_bins)
            wordcloud_params['colormap'] = color_map
    
    wordcloud = WordCloud(**wordcloud_params).generate_from_frequencies(word_freq)
    
    # Convert the image to a data URL
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_palette_colors', methods=['POST'])
def get_palette_preview():
    palette_name = request.json.get('palette')
    colors = get_palette_colors(palette_name)
    return jsonify(colors)

@app.route('/analyze', methods=['POST'])
def analyze():
    category = request.json.get('category')
    color_palette = request.json.get('colorPalette')
    if not category:
        return jsonify({'error': 'Category is required'}), 400

    try:
        # Get all pages in the category
        pages = get_category_members(category)
        if not pages:
            return jsonify({'error': 'No pages found in the category'}), 404

        # Analyze each page
        total_word_freq = {}
        for page_title in pages:
            content = get_page_content(page_title)
            word_freq = analyze_text(content, stop_words)
            for word, freq in word_freq.items():
                total_word_freq[word] = total_word_freq.get(word, 0) + freq

        # Generate word cloud
        word_cloud_img = generate_word_cloud(total_word_freq, color_palette)
        
        # Get top words
        sorted_words = sorted(total_word_freq.items(), key=lambda x: x[1], reverse=True)
        top_words = dict(sorted_words[:20])

        # Get colors for the palette
        colors = get_palette_colors(color_palette) if color_palette else []

        return jsonify({
            'wordCloudImage': word_cloud_img,
            'topWords': top_words,
            'colors': colors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)
