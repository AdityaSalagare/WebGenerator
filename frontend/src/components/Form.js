import React, { useState } from 'react';
import axios from 'axios';
import './Form.css'; 

const Form = () => {
    const [buildingName, setBuildingName] = useState(''); 
    const [description, setDescription] = useState('');
    const [features, setFeatures] = useState(''); // Added for features input
    const [images, setImages] = useState(''); // Added for images input
    const [template, setTemplate] = useState('template1'); // Default template
    const [preview, setPreview] = useState('');
    const [notification, setNotification] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setNotification(''); // Clear previous notifications
    
        try {
            const response = await axios.post(
                `${process.env.REACT_APP_BACKEND_URL}/generate`, // Use the backend URL from environment variables
                {
                    buildingName,
                    description,
                    features,
                    images: images.split(','),
                    template // Include selected template in the request
                }
            );
    
            if (response.data && response.data.download_link) {
                setPreview(response.data.download_link);
            } else {
                setNotification('No download link received. Please try again.');
            }
        } catch (error) {
            console.error('Error generating the website:', error);
            setNotification('An error occurred while generating the website. Please try again.');
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Company Name"
                value={buildingName}
                onChange={(e) => setBuildingName(e.target.value)}
                required
            />
            <textarea
                placeholder="Abstract description about the company"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
            />
           
           
            <select value={template} onChange={(e) => setTemplate(e.target.value)} required>
                <option value="default">Default Template</option>
                <option value="modern">Modern Template</option>
            </select>
            <button type="submit">Generate Website</button>
            {preview && <a href={preview} download>Download Website</a>}
            {notification && <p>{notification}</p>}
        </form>
    );
};

export default Form;