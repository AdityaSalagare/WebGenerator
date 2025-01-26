from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import zipfile
import shutil

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow requests from any origin

os.makedirs('static', exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate():
    company_name = request.form['companyName']
    description = request.form['description']
    template = int(request.form['template'])  # Convert template to an integer
    
    project_titles = request.form.getlist('projectTitles')
    project_images = request.files.getlist('projectImages')  # Get uploaded images and descriptions
    project_descriptions = request.form.getlist('projectDescriptions')
    
    
    # Generate website files
    shutil.rmtree('website', ignore_errors=True)
    os.makedirs('website', exist_ok=True)
    os.makedirs('website/images', exist_ok=True)
    os.makedirs('website/icons', exist_ok=True)
    
    
    projects = []
    for idx, file in enumerate(project_images):
        filename = f"project{idx + 1}.jpg"
        filepath = os.path.join('website/images', filename)
        file.save(filepath)

        title = project_titles[idx] if idx < len(project_titles) else f"Project {idx + 1}"
        description = project_descriptions[idx] if idx < len(project_descriptions) else ""
        projects.append({"title": title, "image": filename, "description": description})
        
        
    source_icon_dir = 'iconAssets'
    target_icon_dir = 'website/icons'
    if os.path.exists(source_icon_dir):
        for icon in os.listdir(source_icon_dir):
            icon_path = os.path.join(source_icon_dir, icon)
            if os.path.isfile(icon_path):  # Ensure it's a file
                shutil.copy(icon_path, target_icon_dir)
    
    if template == 1:
        rendered_html = render_template('index_template1.html', company_name=company_name,description=description, projects=projects)
    else:
        rendered_html = render_template('index_template2.html', company_name=company_name, description=description, projects=projects)
    
    with open('website/index.html', 'w') as f:
        f.write(rendered_html)
#zip file
    zip_filename = 'static/website.zip'
    if os.path.exists('static/website.zip'):
        os.remove('static/website.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk('website'):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), 'website'))
    shutil.rmtree('website')            
                
#download link
    base_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")
    return jsonify({'download_link': f'{base_url}/static/website.zip'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
