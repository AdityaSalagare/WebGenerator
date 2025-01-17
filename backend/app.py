from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import zipfile

app = Flask(__name__)
CORS(app)

os.makedirs('static', exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    building_name = data['buildingName']
    description = data['description']
    features = data['features'].split(',')
    images = data['images']
# Create html+css
    os.makedirs('website', exist_ok=True)
    with open(f'website/index.html', 'w') as f:
        f.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="styles.css">
            <title>{building_name}</title>
        </head>
        <body>
            <h1>{building_name}</h1>
            <p>{description}</p>
            <h2>Features</h2>
            <ul>
                {''.join(f'<li>{feature.strip()}</li>' for feature in features)}
            </ul>
            <h2>Gallery</h2>
            <div class="gallery">
                <div class="slider">
                    {''.join(f'<div class="slide"><img src="{img.strip()}" alt="Gallery Image" /></div>' for img in images)}
                </div>
                <button class="prev" onclick="prevSlide()">&#10094 ;</button>
                <button class="next" onclick="nextSlide()">&#10095;</button>
            </div>
            <script>
                var currentIndex = 0;
                var slides = document.querySelectorAll('.slide');
                var totalSlides = slides.length;

                function showSlide(index) {{
                    for (var i = 0; i < totalSlides; i++) {{
                        slides[i].style.display = (i === index) ? 'block' : 'none';
                    }}
                }}

                function nextSlide() {{
                    currentIndex = (currentIndex + 1) % totalSlides;
                    showSlide(currentIndex);
                }}

                function prevSlide() {{
                    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
                    showSlide(currentIndex);
                }}

                showSlide(currentIndex);
                setInterval(nextSlide, 3000); // Change slide every 3 seconds
            </script>
        </body>
        </html>
        """)

    with open(f'website/styles.css', 'w') as f:
        f.write("""
body {
    width: 80%;
    margin: 0 auto;
    font-family: 'Arial', sans-serif;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}

h1, h2 {
    color: #2c3e50;
    text-align: center;
}

h1 {
    margin-top: 20px;
    font-size: 2.5em;
}

h2 {
    margin-top: 30px;
    font-size: 2em;
}

/* Container Styles */
.container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
    padding: 20px;
    background: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

/* List Styles */
ul {
    list-style-type: none;
    padding: 0;
}

li {
    text-align: center;
    background: #e7f1ff;
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
}

/* Gallery Styles */
.gallery {
    position: relative;
    max-width: 800px;
    margin: 20px auto;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.slider {
    display: flex;
    transition: transform 0.5s ease;
}

.slide {
    min-width: 100%;
    box-sizing: border-box;
}

.slide img {
    width: 100%;
    height: auto;
    border-radius: 8px;
}

/* Navigation Buttons (if you want to add them) */
.prev, .next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    padding: 10px;
    cursor: pointer;
    border-radius: 50%;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.prev {
    left: 10px;
}

.next {
    right: 10px;
}

/* Responsive Styles */
@media (max-width: 768px) {
    h1 {
        font-size: 2em;
    }

    h2 {
        font-size: 1.5em;
    }

    .container {
        padding: 10px;
    }

    .prev, .next {
        padding: 8px;
    }
}
        """)

#zip file
    zip_filename = 'static/website.zip'  
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk('website'):
            for file in files:
                if file.endswith(".html") or file.endswith(".css"):
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), 'website'))
#download link
    return jsonify({'download_link': f'http://localhost:5000/{zip_filename}'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
