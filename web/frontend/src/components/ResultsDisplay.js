import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

const ResultsDisplay = ({ results }) => {
  if (!results) return null;

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Résultats
      </Typography>
      
      {/* Tableau des résultats */}
      {results.matrix && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6">Matrice des résultats</Typography>
          {/* Affichage du tableau */}
        </Box>
      )}

      {/* Détails textuels */}
      {results.details && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6">Détails</Typography>
          <pre>{results.details}</pre>
        </Box>
      )}

      {/* Graphiques */}
      {results.figures && (
        <Box>
          <Typography variant="h6">Visualisations</Typography>
          {/* Affichage des graphiques */}
        </Box>
      )}
    </Paper>
  );
};

export default ResultsDisplay; 