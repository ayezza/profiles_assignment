import React, { useState, useEffect } from 'react';
import { Container, CssBaseline, AppBar, Toolbar, Typography, Box, CircularProgress, Alert } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import mcapService from './services/mcapService';

const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
    },
});

function App() {
    const [models, setModels] = useState([]);
    const [scaleTypes, setScaleTypes] = useState([]);
    const [mcapFunctions, setMcapFunctions] = useState([]);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                console.log('Fetching initial data...');

                // Appel séquentiel pour mieux gérer les erreurs
                const modelsData = await mcapService.getModels();
                console.log('Models data:', modelsData);
                setModels(modelsData);

                const scaleTypesData = await mcapService.getScaleTypes();
                console.log('Scale types data:', scaleTypesData);
                setScaleTypes(scaleTypesData);

                const mcapFunctionsData = await mcapService.getMcapFunctions();
                console.log('MCAP functions data:', mcapFunctionsData);
                setMcapFunctions(mcapFunctionsData);

            } catch (error) {
                console.error('Error fetching initial data:', error);
                setError("Erreur lors du chargement des données initiales: " + error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleFileSelect = async (data) => {
        const { files, model, scaleType, mcapFunction } = data;
        
        if (!files.mca || !files.mcp) return;

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('mca_file', files.mca);
            formData.append('mcp_file', files.mcp);
            formData.append('model_name', model);
            formData.append('scale_type', scaleType);
            formData.append('mcap_function', mcapFunction);

            const response = await mcapService.processMcap(formData);
            setResults(response);
        } catch (error) {
            setError(error.message || "Une erreur est survenue lors du traitement");
            console.error('Error processing files:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <Container>
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                        <CircularProgress />
                    </Box>
                </Container>
            </ThemeProvider>
        );
    }

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6">
                        Affectation des Profils
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container maxWidth="lg">
                <Box sx={{ mt: 4 }}>
                    {error && (
                        <Alert severity="error" sx={{ mb: 2 }}>
                            {error}
                        </Alert>
                    )}

                    <FileUpload
                        onFileSelect={handleFileSelect}
                        models={models}
                        scaleTypes={scaleTypes}
                        mcapFunctions={mcapFunctions}
                    />

                    {results && !loading && (
                        <Results results={results} />
                    )}
                </Box>
            </Container>
        </ThemeProvider>
    );
}

export default App; 