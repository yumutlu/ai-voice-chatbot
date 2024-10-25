import React from 'react';
import { Box, Container } from '@chakra-ui/react';
import VoiceRecorder from '../components/VoiceRecorder';

const Chat: React.FC = () => {
    const handleRecordingComplete = async (audioBlob: Blob) => {
        // Will implement audio processing in the next PR
        console.log('Recording completed:', audioBlob);
    };

    return (
        <Container maxW="container.md" py={8}>
            <Box>
                <VoiceRecorder onRecordingComplete={handleRecordingComplete} />
            </Box>
        </Container>
    );
};

export default Chat;