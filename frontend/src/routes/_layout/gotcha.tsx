import React from 'react';
import VideoStreamer from '../components/VideoStreamer'; // Adjust the import path as necessary

const GotchaPage: React.FC = () => {
    return (
        <div>
            <h1>Video Verification</h1>
            <VideoStreamer />
        </div>
    );
};

export default GotchaPage;