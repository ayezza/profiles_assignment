import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

const MatrixDisplay = ({ matrix, title }) => {
  if (!matrix || Object.keys(matrix).length === 0) return null;

  // Convert the matrix object to array format
  const rows = Object.keys(matrix);
  const columns = Object.keys(matrix[rows[0]]);

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              {columns.map((col) => (
                <TableCell key={col}>{col}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row}>
                <TableCell component="th" scope="row">
                  {row}
                </TableCell>
                {columns.map((col) => (
                  <TableCell key={`${row}-${col}`}>
                    {typeof matrix[row][col] === 'number' 
                      ? matrix[row][col].toFixed(3) 
                      : matrix[row][col]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

const ResultsDisplay = ({ results }) => {
  const [key, setKey] = useState(0);

  useEffect(() => {
    // Force re-render when results change
    setKey(prev => prev + 1);
  }, [results]);

  return (
    <Box sx={{ mt: 4 }} key={key}>
      <Typography variant="h5" gutterBottom>
        Résultats
      </Typography>

      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>Paramètres d'entrée</Typography>
        <Typography>Modèle: {results.model}</Typography>
        <Typography>Type d'échelle: {results.scaleType}</Typography>
        <Typography>Fonction MCAP: {results.mcapFunction}</Typography>
        <Typography>Matrice MCA: {results.mcaFile || 'Aucun fichier chargé'}</Typography>
        <Typography>Matrice MCP: {results.mcpFile || 'Aucun fichier chargé'}</Typography>
      </Paper>

      {results.message && (
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>Message:</Typography>
          <Typography>{results.message}</Typography>
        </Paper>
      )}

      {results.ranking_matrix && (
        <MatrixDisplay 
          matrix={results.ranking_matrix} 
          title="Matrice de classement"
        />
      )}

      {results.result_matrix && (
        <MatrixDisplay 
          matrix={results.result_matrix} 
          title="Matrice de résultats"
        />
      )}

      {results.figures && Object.keys(results.figures).length > 0 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>Visualisations</Typography>
          {Object.entries(results.figures).map(([name, base64Data]) => (
            <Box key={name} sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>{name}</Typography>
              <img 
                src={`data:image/png;base64,${base64Data}`}
                alt={name}
                style={{ maxWidth: '100%', height: 'auto' }}
              />
            </Box>
          ))}
        </Paper>
      )}
    </Box>
  );
};

export default ResultsDisplay;