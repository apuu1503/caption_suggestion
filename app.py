from flask import Flask, render_template, request
import base64
from io import BytesIO
from PIL import Image
import json

app = Flask(__name__)

# Load captions, music, and view more links from the JSON file
with open('captions_music_links.json', 'r') as file:
    data = json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Read the image file
    image_data = file.read()

    # Convert image data to base64 for embedding in HTML
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    image_src = f'data:image/png;base64,{encoded_image}'

    # Process the image (add your image processing code here)
    image = Image.open(BytesIO(image_data))
    resized_image = image.resize((256, 256))

    # Get captions, music, and view more link based on the image filename
    filename = file.filename
    if filename in data:
        suggestions = data[filename]
    else:
        suggestions = {
            "captions": ["Default Caption 1", "Default Caption 2"],
            "music": ["Default Music 1", "Default Music 2"],
            "view_more_link": "#"
        }

    # Return the result with the image source, structured suggestions, and the View More link
    return render_template('index.html', image_src=image_src, result=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
