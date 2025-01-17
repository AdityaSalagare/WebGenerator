import React, { useState } from 'react';
import axios from 'axios';
import './Form.css'; 

const Form = () => {
    const [buildingName, setBuildingName] = useState(''); 
    const [description, setDescription] = useState('');
    const [features, setFeatures] = useState('');
    const [images, setImages] = useState('');
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
                    images: images.split(',')
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
                placeholder="Building Name"
                value={buildingName}
                onChange={(e) => setBuildingName(e.target.value)}
                required
            />
            <textarea
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
            />
            <input
                type="text"
                placeholder="Features (comma separated)"
                value={features}
                onChange={(e) => setFeatures(e.target.value)}
                required
            />
            <input
                type="text"
                placeholder="Image URLs (comma separated)"
                value={images}
                onChange={(e) => setImages(e.target.value)}
                required
            />
            <button type="submit">Generate Website</button>
            {preview && <a href={preview} download>Download Website</a>}
            {notification && <p>{notification}</p>}
        </form>
    );
};

export default Form;
