import React from 'react';
import VideoStreamer from '../../components/Gotcha/VerifyCameraStream';
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute("/_layout/gotcha")({
    component: Gotcha,
  })

function Gotcha() {
    return (
        <div>
            <h1>Video Verification</h1>
            <VideoStreamer />
        </div>
    );
};
