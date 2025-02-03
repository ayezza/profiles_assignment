import React, { useState, useEffect } from 'react';
import { Box, Button, FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

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

    useEffect(() => {
        console.log('Models received:', models);
        console.log('Scale types received:', scaleTypes);
        console.log('MCAP functions received:', mcapFunctions);
    }, [models, scaleTypes, mcapFunctions]);

    const handleFileChange = (type) => (event) => {
        const file = event.target.files[0];
        setSelectedFiles(prev => ({
            ...prev,
            [type]: file
        }));
        
        if (file) {
            const newFiles = {
                ...selectedFiles,
                [type]: file
            };
            console.log('Sending files to parent:', newFiles);
            onFileSelect({
                files: newFiles,
                model,
                scaleType,
                mcapFunction
            });
        }
    };

    const handleModelChange = (event) => {
        const newModel = event.target.value;
        console.log('Model changed to:', newModel);
        setModel(newModel);
        onFileSelect({
            files: selectedFiles,
            model: newModel,
            scaleType,
            mcapFunction
        });
    };

    const handleScaleTypeChange = (event) => {
        const newScaleType = event.target.value;
        console.log('Scale type changed to:', newScaleType);
        setScaleType(newScaleType);
        onFileSelect({
            files: selectedFiles,
            model,
            scaleType: newScaleType,
            mcapFunction
        });
    };

    const handleMcapFunctionChange = (event) => {
        const newMcapFunction = event.target.value;
        console.log('MCAP function changed to:', newMcapFunction);
        setMcapFunction(newMcapFunction);
        onFileSelect({
            files: selectedFiles,
            model,
            scaleType,
            mcapFunction: newMcapFunction
        });
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
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
        </Box>
    );
};

export default FileUpload; 