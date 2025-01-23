from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import zipfile

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow requests from any origin

os.makedirs('static', exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    building_name = data['buildingName']
    template = data['template']
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
    <title>{building_name}</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>
    <header>
        <div class="logo" role="banner">
            <h1>{building_name}</h1>
        </div>
        <nav role="navigation">
            <ul>
                <li><a href="#services">Services</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#testimonials">Testimonials</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <section class="hero2" style="display: banner; direction: column; width: 90%; padding: 50px; position: relative; overflow-x: hidden;">
        <div data-id="33bf44c" data-element_type="container" style="max-width: 100%; display: flex; flex-direction: column; padding: 50px; box-sizing: border-box;">
            <div data-id="955f6aa" data-element_type="container" style="background-image:url('https://websitedemos.net/real-estate-company-04/wp-content/uploads/sites/1484/2023/07/services-bg.jpg'); background-position: 0px; background-repeat: no-repeat; background-size: cover; border-radius: 20px; display: flex; flex-direction: column; width: 100%; padding: 150px 50px; box-sizing: border-box;">
                <div style="width: 100%; max-width: min(100%, 1820px); margin: auto; padding-inline: 0px;">
                    <div style="text-align:center;">
                        <h4 style="color:#fff; margin:0; font-size:20.8px;">Services</h4>
                    </div>
                    <div style="text-align:center;">
                        <h1 style="color:#fff; margin:0; font-size:32px;">We offer a wide Range of Services</h1>
                    </div>
                </div>
            </div>
        </div>
    </section>
    

    <section class="hero">
        <h2>Your Vision, Our Expertise</h2>
        <p>Building the future with quality and precision.</p>
        <p>{description}</p>
        <a href="#contact" class="btn">Get a Quote</a>
    </section>

    <section id="services">
        <h2>Our Services</h2>
        <div class="service-list" style="display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; padding: 20px;">
            <div class="service-item" style="background: #f9f9f9; border: 1px solid #ddd; border-radius: 10px; padding: 20px; width: 250px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center;">
                <img src="https://via.placeholder.com/50" alt="Residential Construction" style="width: 50px; height: 50px; margin-bottom: 10px;">
                <h3 style="font-size: 20px; margin: 10px 0;">Residential Construction</h3>
                <p style="font-size: 14px; color: #555;">We build homes that reflect your style and needs.</p>
            </div>
            <div class="service-item" style="background: #f9f9f9; border: 1px solid #ddd; border-radius: 10px; padding: 20px; width: 250px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center;">
                <img src="https://via.placeholder.com/50" alt="Commercial Construction" style="width: 50px; height: 50px; margin-bottom: 10px;">
                <h3 style="font-size: 20px; margin: 10px 0;">Commercial Construction</h3>
                <p style="font-size: 14px; color: #555;">Expertise in constructing commercial spaces that drive business.</p>
            </div>
            <div class="service-item" style="background: #f9f9f9; border: 1px solid #ddd; border-radius: 10px; padding: 20px; width: 250px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center;">
                <img src="https://via.placeholder.com/50" alt="Renovations" style="width: 50px; height: 50px; margin-bottom: 10px;">
                <h3 style="font-size: 20px; margin: 10px 0;">Renovations</h3>
                <p style="font-size: 14px; color: #555;">Transforming your existing spaces into something extraordinary.</p>
            </div>
        </div>
        
    </section>

    <section id="projects">
        <h2>Our Projects</h2>
        <div class="project-gallery">
            <div class="project-card">
                <img src="project1.jpg" alt="Project 1 - Description of project 1" loading="lazy">
                <div class="card-content">
                    <h3>Project Title 1</h3>
                    <p>A brief description of the project, highlighting key features and accomplishments.</p>
                    <a href="project1-details.html" class="btn">Read More</a>
                </div>
            </div>

            <div class="project-card">
                <img src="project2.jpg" alt="Project 2 - Description of project 2" loading="lazy">
                <div class="card-content">
                    <h3>Project Title 2</h3>
                    <p>A brief description of the project, highlighting key features and accomplishments.</p>
                    <a href="project2-details.html" class="btn">Read More</a>
                </div>
            </div>

            <div class="project-card">
                <img src="project3.jpg" alt="Project 3 - Description of project 3" loading="lazy">
                <div class="card-content">
                    <h3>Project Title 3</h3>
                    <p>A brief description of the project, highlighting key features and accomplishments.</p>
                    <a href="project3-details.html" class="btn">Read More</a>
                </div>
            </div>
        </div>
    </section>

    <section id="testimonials">
        <h2>What Our Clients Say</h2>
        <blockquote cite="https://www.advancedconstruction.com/testimonials">"Advanced Construction turned my dream home into reality!" - Jane Doe</blockquote>
        <blockquote cite="https://www.advancedconstruction.com/testimonials">"Professional and reliable service from start to finish." - John Smith</blockquote>
    </section>

    <footer id="contact">
        <h2>Contact Us</h2>
        <form action="#" method="post">
            <input type="text" placeholder="Your Name" required class="input-field" autocomplete="name">
            <input type="email" placeholder="Your Email" required class="input-field" autocomplete="email">
            <textarea placeholder="Your Message" required></textarea>
            <button type="submit" class="btn">Send Message</button>
        </form>

        <p>&copy; 2025 Advanced Construction. All rights reserved.</p>
        <p><small>Website by <a href="https://www.advancedconstruction.com">Advanced Construction</a></small></p>
    </footer>
</body>
</html>
        """
        
        
        
        )

    with open(f'website/styles.css', 'w') as f:
        f.write("""
body {
    font-family: 'Helvetica', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    box-sizing: border-box;
    line-height: 1.6;
    color: #333;
}

header {
    background-color: #444;
    color: white;
    padding: 20px;
}

header .logo {
    display: inline-block;
}

nav ul {
    list-style: none;
    padding: 0;
}

nav ul li {
    display: inline;
    margin-right: 20px;
}

nav ul li a {
    color: white;
    text-decoration: none;
    transition: color 0.3s ease; /* Added transition */
}

nav ul li a:hover {
    color: #007BFF; /* Change color on hover */
}

.hero {
    background-color: #007BFF; /* Updated color */
    text-align: center;
    padding: 50px 20px;
    color: white; /* Text color for better contrast */
}

.hero2 {
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 50px;
    position: relative;
}

.hero2 > div {
    max-width: 80%;
    display: flex;
    flex-direction: column;
    padding: 50px;
    box-sizing: border-box;
}

.hero2 > div > div {
    background-image: url('https://websitedemos.net/real-estate-company-04/wp-content/uploads/sites/1484/2023/07/services-bg.jpg');
    background-position: 0 -152px;
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 150px 50px;
    box-sizing: border-box;
}

.btn {
    background-color: #28a745; /* Updated button color */
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    transition: background-color 0.3s ease, transform 0.3s ease; /* Added transition */
}

.btn:hover {
    background-color: #218838; /* Darker on hover */
    transform: scale(1.05); /* Slightly enlarge on hover */
}

section {
    padding: 40px 20px;
}

.service-list {
    display: flex;
    justify-content: space-between; /* Improved spacing */
}

.service-item {
    flex: 1;
    margin-right: 20px;
}

.service-item:last-child {
    margin-right: 0;
}

.project-gallery {
   display: flex; 
   flex-wrap: wrap; 
   justify-content: space-between; 
   gap: 20px; /* Space between cards */
}

.project-card {
   background-color: #fff; 
   border-radius: 10px; 
   box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 8px; 
   overflow: hidden; 
   width: calc(33.33% - 20px); /* Adjust width for three cards in a row */
   transition: transform 0.3s ease; /* Transition for hover effect */
}

.project-card:hover {
   transform: translateY(-5px); /* Lift effect on hover */
}

.project-card img {
   width: 100%; /* Responsive image */
   height: auto; 
}

.card-content {
   padding: 15px; 
}

.card-content h3 {
   margin-top: 10px; 
   font-size: 1.5em; 
}

.card-content p {
   font-size: 1em; 
   color: #555; 
}

blockquote {
   font-style: italic;
   margin-bottom: 20px;
   border-left: 4px solid #007BFF;
   padding-left: 10px;
}

footer {
   background-color: #333;
   color: white;
   text-align: center;
   padding: 20px 0;
}

footer form {
   display: flex;
   flex-direction: column;
   max-width: 400px;
   margin: auto;
}

footer input, footer textarea {
   margin-bottom: 10px;
   padding: 10px;
   border-radius: 5px; 
   border: none; 
   transition: border-color 0.3s ease, transform 0.3s ease; /* Added transition */
}

footer input.input-field:hover,
footer input.input-field:focus,
footer textarea:hover,
footer textarea:focus {
   border-color: blue; /* Change border color on focus/hover */
}

/* Responsive Design */
@media (max-width: 768px) {
    .service-list {
        flex-direction: column; /* Stack services vertically on small screens */
    }

    .service-item {
        margin-right: 0; /* Remove right margin */
        margin-bottom: 20px; /* Add bottom margin for spacing */
     }

     .project-card {
         width: calc(100% - 20px); /* Full width on small screens */
     }
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

        """)

#zip file
    zip_filename = 'static/website.zip'  
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk('website'):
            for file in files:
                if file.endswith(".html") or file.endswith(".css"):
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), 'website'))
#download link
    base_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")
    return jsonify({'download_link': f'{base_url}/static/website.zip'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
