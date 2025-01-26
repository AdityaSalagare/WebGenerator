import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';

const Form = () => {
    const [companyName, setCompanyName]= useState('');
    const [description, setDescription] = useState('');
    const [template, setTemplate] = useState('');
    const [projects, setProjects] = useState([{ title: '', image: null, description: '' }]);
    const [preview, setPreview] = useState('');
    const [notification, setNotification] = useState('');

    // Handle adding a new project
    const handleAddProject = () => {
        setProjects([...projects, { title: '', image: null, description: '' }]);
    };

    // Handle removing a project
    const handleRemoveProject = (index) => {
        setProjects(projects.filter((_, i) => i !== index));
    };

    // Handle project changes (title, image, description)
    const handleProjectChange = (index, key, value) => {
        const updatedProjects = projects.map((project, i) => {
            if (i === index) {
                return { ...project, [key]: value };
            }
            return project;
        });
        setProjects(updatedProjects);
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setNotification('');

        const formData = new FormData();
        formData.append('companyName', companyName);
        formData.append('description', description);
        formData.append('template', template);
        console.log(template);

        // Append project data
        projects.forEach((project, index) => {
            formData.append(`projectTitles`, project.title); // Append title
            if (project.image) {
                formData.append(`projectImages`, project.image); // Append image
            }
            formData.append(`projectDescriptions`, project.description); // Append description
        });

        try {
            const response = await axios.post(
                `${process.env.REACT_APP_BACKEND_URL || "http://localhost:5000"}/generate`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            if (response.data && response.data.download_link) {
                setPreview(response.data.download_link); // Display the download link
            } else {
                setNotification('Error: No download link received.');
            }
        } catch (error) {
            setNotification('Error generating website.');
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <input
                type="text"
                placeholder="Company Name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                required
            />
            <textarea
                placeholder="Abstract about the Company"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
            />

            <h3>Projects</h3>
            <p>Add details about past Company Projects</p>
            {projects.map((project, index) => (
                <div key={index} style={{ marginBottom: '20px' }}>
                    <input
                        type="text"
                        placeholder="Project Title"
                        value={project.title}
                        onChange={(e) =>
                            handleProjectChange(index, 'title', e.target.value)
                        }
                        required
                    />
                    <p style={{ color: 'red' }}>Project Image("Upload image(only) of project to show on website")</p>
                    <input
                        type="file"
                        onChange={(e) =>
                            handleProjectChange(index, 'image', e.target.files[0])
                        }
                        accept="image/*"
                        required
                    />
                    <textarea
                        placeholder="Project Description"
                        value={project.description}
                        onChange={(e) =>
                            handleProjectChange(index, 'description', e.target.value)
                        }
                        required
                    />
                    <button
                        type="button"
                        onClick={() => handleRemoveProject(index)}
                        style={{ marginTop: '10px' }}
                    >
                        Remove
                    </button>
                </div>
            ))}
            <button type="button" onClick={handleAddProject}>
                Add Project
            </button>

            <select
                value={template}
                onChange={(e) => setTemplate(Number(e.target.value))}
                required
            >
                <option value="" disabled>Select a template</option>
                <option value="1">Template 1</option>
                <option value="2">Template 2</option>
            </select>
            <button type="submit">Generate Website</button>
            {preview && (
                <a href={preview} download>
                    Download Website
                </a>
            )}
            {notification && <p>{notification}</p>}
        </form>
    );
};

export default Form;
