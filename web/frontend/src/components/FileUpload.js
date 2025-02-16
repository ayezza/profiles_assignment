import React, { useState, useEffect } from 'react';
import { Box, Button, FormControl, InputLabel, MenuItem, Select, Typography, CircularProgress, Alert } from '@mui/material';
import { styled } from '@mui/material/styles';
import Results from './Results';
import mcapService from '../services/mcapService';

const Input = styled('input')({
    display: 'none',
});

const FileUpload = () => {
    const [selectedFiles, setSelectedFiles] = useState({
        mca: null,
        mcp: null
    });
    const [model, setModel] = useState('model2');
    const [scaleType, setScaleType] = useState('0-1');
    const [mcapFunction, setMcapFunction] = useState('sum');
    const [results, setResults] = useState(null);
    const [showFileUpload, setShowFileUpload] = useState(true);
    const [models, setModels] = useState([]);
    const [scaleTypes, setScaleTypes] = useState([]);
    const [mcapFunctions, setMcapFunctions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadInitialData = async () => {
            try {
                const [
                    modelsData,
                    scaleTypesData,
                    mcapFunctionsData
                ] = await Promise.all([
                    mcapService.getModels(),
                    mcapService.getScaleTypes(),
                    mcapService.getMcapFunctions()
                ]);

                setModels(modelsData);
                setScaleTypes(scaleTypesData);
                setMcapFunctions(mcapFunctionsData);
                setLoading(false);
            } catch (error) {
                console.error('Error loading initial data:', error);
                setError('Error loading initial data: ' + error.message);
                setLoading(false);
            }
        };

        loadInitialData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    const handleFileChange = (type) => (event) => {
        const file = event.target.files[0];
        setSelectedFiles(prev => ({
            ...prev,
            [type]: file
        }));
    };

    const handleModelChange = (event) => {
        const newModel = event.target.value;
        setModel(newModel);
    };

    const handleScaleTypeChange = (event) => {
        const newScaleType = event.target.value;
        setScaleType(newScaleType);
    };

    const handleMcapFunctionChange = (event) => {
        const newMcapFunction = event.target.value;
        setMcapFunction(newMcapFunction);
    };

    const handleSubmit = async () => {
        setResults(null);
        setError(null);
        setLoading(true);
        
        try {
            if (!selectedFiles.mca || !selectedFiles.mcp) {
                throw new Error("Please select both MCA and MCP files");
            }

            const formData = new FormData();
            formData.append('mca_file', selectedFiles.mca);
            formData.append('mcp_file', selectedFiles.mcp);
            formData.append('model_name', model);
            formData.append('scale_type', scaleType);
            formData.append('mcap_function', mcapFunction);

            console.log('Submitting with parameters:', {
                model_name: model,
                scale_type: scaleType,
                mcap_function: mcapFunction
            });

            const response = await mcapService.processMcap(formData);
            
            if (response.status === 'error') {
                throw new Error(response.error || 'Processing failed');
            }

            console.log('Received response:', response);
            setResults(response);

        } catch (error) {
            console.error('Error processing files:', error);
            setError(`Error: ${error.message}`);
            setResults(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Configuration
            </Typography>
            {showFileUpload && (
                <>
                    <Box sx={{ mb: 3 }}>
                        <label htmlFor="mca-file">
                            <Input
                                accept=".csv"
                                id="mca-file"
                                type="file"
                                onChange={handleFileChange('mca')}
                            />
                            <Button variant="contained" component="span" fullWidth>
                                {selectedFiles.mca ? selectedFiles.mca.name : 'Charger le fichier MCA'}
                            </Button>
                        </label>
                    </Box>
                    <Box sx={{ mb: 3 }}>
                        <label htmlFor="mcp-file">
                            <Input
                                accept=".csv"
                                id="mcp-file"
                                type="file"
                                onChange={handleFileChange('mcp')}
                            />
                            <Button variant="contained" component="span" fullWidth>
                                {selectedFiles.mcp ? selectedFiles.mcp.name : 'Charger le fichier MCP'}
                            </Button>
                        </label>
                    </Box>
                </>
            )}
            <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Modèle</InputLabel>
                <Select
                    value={model}
                    label="Modèle"
                    onChange={handleModelChange}
                >
                    {Array.isArray(models) && models.map((model) => (
                        <MenuItem key={model.id} value={model.id}>
                            {model.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Type d'échelle</InputLabel>
                <Select
                    value={scaleType}
                    label="Type d'échelle"
                    onChange={handleScaleTypeChange}
                >
                    {Array.isArray(scaleTypes) && scaleTypes.map((type) => (
                        <MenuItem key={type.id} value={type.id}>
                            {type.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Fonction MCAP</InputLabel>
                <Select
                    value={mcapFunction}
                    label="Fonction MCAP"
                    onChange={handleMcapFunctionChange}
                >
                    {Array.isArray(mcapFunctions) && mcapFunctions.map((func) => (
                        <MenuItem key={func.id} value={func.id}>
                            {func.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <Button variant="contained" onClick={handleSubmit}>
                Calculer la matrice MCAP
            </Button>

            {loading && <CircularProgress />}
            
            {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                </Alert>
            )}

            {results && !loading && (
                <Results results={results} loading={loading} />
            )}
        </Box>
    );
};

export default FileUpload;