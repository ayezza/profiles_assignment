import React, { useState, useEffect } from 'react';
import { Box, Button, FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import ResultsDisplay from './ResultsDisplay';

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
    const [results, setResults] = useState(null); // État pour stocker les résultats

    useEffect(() => {
        onFileSelect({
            files: selectedFiles,
            model,
            scaleType,
            mcapFunction
        });
    }, [selectedFiles, model, scaleType, mcapFunction]);

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
        // Créer une constante pour les paramètres d'entrée
        const params = {
            model,
            scaleType,
            mcapFunction,
            mcaFile: selectedFiles.mca,
            mcpFile: selectedFiles.mcp
        };

        // Effectuer le calcul de la matrice MCAP ici
        const calculatedResults = await calculateMcapMatrix(selectedFiles, model, scaleType, mcapFunction);
        
        // Mettre à jour l'état avec les résultats
        setResults(calculatedResults);
    };

    

    // Fonction fictive pour le calcul de la matrice MCAP
    const calculateMcapMatrix = async (files, model, scaleType, mcapFunction) => {
        // Logique de calcul ici
        // Par exemple, vous pouvez lire les fichiers et effectuer des calculs
        // Retournez les résultats sous forme d'objet ou de tableau
        return {
            message: "Calcul effectué avec succès",
            // Ajoutez d'autres données de résultats ici
        };
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Configuration
            </Typography>
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

            {/* Affichage des résultats */}
            {results && (
                <ResultsDisplay 
                    results={{
                        message: results.message,
                        model,
                        scaleType,
                        mcapFunction,
                        mcaFile: selectedFiles.mca,
                        mcpFile: selectedFiles.mcp
                    }} 
                />
            )}
        </Box>
    );
};

export default FileUpload;