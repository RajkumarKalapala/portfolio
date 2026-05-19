import MobileStepper from '@mui/material/MobileStepper';
import { Box, useTheme } from '@mui/material';
import { useState, useEffect, useRef } from 'react';

export const ProductBanner = ({images}) => {
    const theme = useTheme()
    const [activeStep, setActiveStep] = useState(0);
    const maxSteps = images.length;
    const timerRef = useRef(null);

    // Auto-play
    useEffect(() => {
        timerRef.current = setInterval(() => {
            setActiveStep(prev => (prev + 1) % maxSteps);
        }, 3000);
        return () => clearInterval(timerRef.current);
    }, [maxSteps]);

    return (
        <>
            <Box sx={{ width: '100%', overflow: 'hidden', position: 'relative' }}>
                <Box
                    sx={{
                        display: 'flex',
                        transition: 'transform 0.5s ease',
                        transform: `translateX(-${activeStep * 100}%)`,
                        width: '100%',
                    }}
                >
                    {images.map((image, index) => (
                        <Box
                            key={index}
                            component="img"
                            src={image}
                            alt={`Banner ${index + 1}`}
                            sx={{
                                minWidth: '100%',
                                width: '100%',
                                objectFit: 'contain',
                            }}
                        />
                    ))}
                </Box>
            </Box>
            <div style={{ alignSelf: 'center' }}>
                <MobileStepper
                    steps={maxSteps}
                    position="static"
                    activeStep={activeStep}
                />
            </div>
        </>
    );
};
