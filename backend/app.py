from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import zipfile

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow requests from any origin

os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)  # Folder for storing multiple templates

# Create a folder structure for multiple templates
TEMPLATE_DIR = 'templates'

# Predefined templates
TEMPLATES = {
    "default": {
        "html": "default/index.html",
        "css": "default/styles.css",
    },
    "modern": {
        "html": "modern/index.html",
        "css": "modern/styles.css",
    },
}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    building_name = data['buildingName']
    template_name = data['template']
    description = data['description']
    features = data['features'].split(',')
    images = data['images']

    # Validate the template name
    if template_name not in TEMPLATES:
        return jsonify({"error": "Invalid template name"}), 400

    # Paths to the selected template's files
    html_template_path = os.path.join(TEMPLATE_DIR, TEMPLATES[template_name]["html"])
    css_template_path = os.path.join(TEMPLATE_DIR, TEMPLATES[template_name]["css"])

    # Read and customize the selected HTML template
    with open(html_template_path, 'r') as html_file:
        html_template = html_file.read()

    customized_html = html_template.format(
        building_name=building_name,
        description=description,
        features=''.join([f"<li>{feature}</li>" for feature in features])
    )

    # Prepare the website folder
    os.makedirs('website', exist_ok=True)
    with open('website/index.html', 'w') as html_file:
        html_file.write(customized_html)

    # Copy the CSS template to the website folder
    with open(css_template_path, 'r') as css_file:
        css_content = css_file.read()

    with open('website/styles.css', 'w') as css_file:
        css_file.write(css_content)

    # Generate a zip file for the website
    zip_filename = 'static/website.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk('website'):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), 'website'))

    # Return the download link
    base_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")
    return jsonify({'download_link': f'{base_url}/static/website.zip'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
