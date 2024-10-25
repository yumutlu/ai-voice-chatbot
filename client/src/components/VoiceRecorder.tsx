import React, { useState, useRef, useEffect } from 'react';
import { Box, Button, VStack, useToast } from '@chakra-ui/react';
import WaveSurfer from 'wavesurfer.js';

interface VoiceRecorderProps {
    onRecordingComplete: (audioBlob: Blob) => void;
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onRecordingComplete }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const chunks = useRef<Blob[]>([]);
    const waveformRef = useRef<HTMLDivElement>(null);
    const wavesurfer = useRef<WaveSurfer | null>(null);
    const toast = useToast();

    useEffect(() => {
        if (waveformRef.current) {
            wavesurfer.current = WaveSurfer.create({
                container: waveformRef.current,
                waveColor: '#4A5568',
                progressColor: '#2B6CB0',
                cursorColor: '#2B6CB0',
                barWidth: 2,
                barRadius: 3,
                responsive: true,
                height: 100,
            });
        }

        return () => {
            wavesurfer.current?.destroy();
        };
    }, []);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const recorder = new MediaRecorder(stream);

            recorder.ondataavailable = (e) => {
                chunks.current.push(e.data);
            };

            recorder.onstop = () => {
                const blob = new Blob(chunks.current, { type: 'audio/wav' });
                const url = URL.createObjectURL(blob);
                setAudioUrl(url);
                onRecordingComplete(blob);

                if (wavesurfer.current) {
                    wavesurfer.current.loadBlob(blob);
                }
            };

            chunks.current = [];
            recorder.start();
            setMediaRecorder(recorder);
            setIsRecording(true);
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Could not access microphone',
                status: 'error',
                duration: 3000,
            });
        }
    };

    const stopRecording = () => {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            setIsRecording(false);
        }
    };

    return (
        <VStack spacing={4} w="100%">
            <Box w="100%" h="100px" ref={waveformRef} />
            <Box>
                {!isRecording ? (
                    <Button
                        colorScheme="blue"
                        onClick={startRecording}
                    >
                        Start Recording
                    </Button>
                ) : (
                    <Button
                        colorScheme="red"
                        onClick={stopRecording}
                    >
                        Stop Recording
                    </Button>
                )}
            </Box>
            {audioUrl && (
                <Box w="100%">
                    <audio src={audioUrl} controls />
                </Box>
            )}
        </VStack>
    );
};

export default VoiceRecorder;
