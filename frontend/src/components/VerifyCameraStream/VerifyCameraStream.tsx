import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

const VideoStreamer: React.FC = () => {
    const webcamRef = useRef<Webcam>(null);
    const [messages, setMessages] = useState<string[]>([]);
    const [verificationRequestId, setVerificationRequestId] = useState<number | null>(null);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        if (verificationRequestId && !ws.current) {
            ws.current = new WebSocket(`ws://localhost:8000/api/ws/${verificationRequestId}`);
            ws.current.onmessage = (event) => {
                setMessages(prev => [...prev, event.data]);
            };
            ws.current.onclose = () => console.log('WebSocket closed');
            ws.current.onerror = (error) => console.log('WebSocket error:', error);
        }

        return () => {
            ws.current?.close();
        };
    }, [verificationRequestId]);

    const handleStart = async () => {
        const videoBlob = webcamRef.current?.getScreenshot();
        if (videoBlob) {
            try {
                const response = await axios.post('http://localhost:8000/api/video/{verification_request_id}', videoBlob, {
                    headers: {
                        'Content-Type': 'application/octet-stream',
                    },
                });
                setVerificationRequestId(response.data.id);
            } catch (error) {
                console.error('Error sending video:', error);
            }
        }
    };

    return (
        <div>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
            />
            <button onClick={handleStart}>Start Verification</button>
            <div>
                {messages.map((msg, index) => (
                    <div key={index}>{msg}</div>
                ))}
            </div>
        </div>
    );
};

export default VideoStreamer;