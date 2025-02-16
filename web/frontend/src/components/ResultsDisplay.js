import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const ResultsDisplay = ({ results }) => {
    if (!results) return null;

    const { success, data, parameters } = results;

    if (!success) {
        return (
            <Box sx={{ mt: 3 }}>
                <Typography color="error">
                    Erreur: {results.message}
                </Typography>
            </Box>
        );
    }

    return (
        <Box sx={{ mt: 3 }}>
            <Typography variant="h5" gutterBottom>Résultats</Typography>
            
            <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" gutterBottom>Paramètres d'entrée</Typography>
                <Typography>Modèle: {parameters.model}</Typography>
                <Typography>Type d'échelle: {parameters.scaleType}</Typography>
                <Typography>Fonction MCAP: {parameters.mcapFunction}</Typography>
                <Typography>Matrice MCA: {parameters.mcaFile}</Typography>
                <Typography>Matrice MCP: {parameters.mcpFile}</Typography>
            </Paper>

            {data && (
                <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>Matrice de résultats</Typography>
                    {data.result && (
                        <Box sx={{ overflowX: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr>
                                        <th style={{ padding: '8px', border: '1px solid #ddd' }}>Activity</th>
                                        {data.result.columns.map((col, i) => (
                                            <th key={i} style={{ padding: '8px', border: '1px solid #ddd' }}>{col}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.result.data.map((row, i) => (
                                        <tr key={i}>
                                            <td style={{ padding: '8px', border: '1px solid #ddd' }}>{data.result.index[i]}</td>
                                            {row.map((cell, j) => (
                                                <td key={j} style={{ padding: '8px', border: '1px solid #ddd' }}>
                                                    {Number(cell).toFixed(3)}
                                                </td>
                                            ))}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </Box>
                    )}
                </Paper>
            )}
        </Box>
    );
};

export default ResultsDisplay;