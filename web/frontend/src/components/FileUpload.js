import React, { useState } from 'react';
import { Box, Button, FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import ResultsDisplay from './ResultsDisplay';
import mcapService from '../services/mcapService';

const Input = styled('input')({
    display: 'none',
});

const FileUpload = ({ onFileSelect, models, scaleTypes, mcapFunctions }) => {
    const [selectedFiles, setSelectedFiles] = useState({
        mca: null,
        mcp: null
    });
    const [model, setModel] = useState('model2');
    const [scaleType, setScaleType] = useState('0-1');
    const [mcapFunction, setMcapFunction] = useState('sum');
    const [results, setResults] = useState(null);
    const [showFileUpload, setShowFileUpload] = useState(true);

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
        setResults(null); // Clear previous results
        console.log('Submitting with parameters:', { model, scaleType, mcapFunction });

        if (!selectedFiles.mca || !selectedFiles.mcp) {
            setResults({
                message: "Les fichiers MCA et MCP doivent être sélectionnés",
                resultMatrix: [],
            });
            return;
        }

        // Create fresh FormData for each submission
        const formData = new FormData();
        formData.append('mca_file', selectedFiles.mca);
        formData.append('mcp_file', selectedFiles.mcp);
        formData.append('model_name', model);  // Make sure this matches backend parameter name
        formData.append('scale_type', scaleType);  // Make sure this matches backend parameter name
        formData.append('mcap_function', mcapFunction);  // Make sure this matches backend parameter name
        formData.append('request_id', Date.now().toString());

        try {
            const response = await mcapService.processMcap(formData);
            
            if (!response.success) {
                throw new Error(response.error || 'Processing failed');
            }

            // Create new results object with current parameters
            const newResults = {
                ...response,
                model,
                scaleType,
                mcapFunction,
                mcaFile: selectedFiles.mca.name,
                mcpFile: selectedFiles.mcp.name,
                timestamp: Date.now()
            };

            console.log('Calculation results:', newResults);
            setResults(newResults);

        } catch (error) {
            console.error('Calculation error:', error);
            setResults({
                message: error.message || "Une erreur est survenue lors du traitement",
                resultMatrix: [],
                model,
                scaleType,
                mcapFunction,
                timestamp: Date.now()
            });
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

            {results && (
                <ResultsDisplay 
                    results={results} 
                />
            )}
        </Box>
    );
};

export default FileUpload;