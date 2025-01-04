import React, { useState } from 'react';
import { 
  Box, Paper, Grid, TextField, Button, 
  FormControl, InputLabel, Select, MenuItem 
} from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import { processMatrices } from '../services/api';

const MatrixInput = () => {
  const [dimensions, setDimensions] = useState({
    activities: 3,
    competencies: 3,
    profiles: 3
  });

  const [matrices, setMatrices] = useState({
    mca: {},
    mcp: {}
  });

  const [config, setConfig] = useState({
    model: 'model1',
    scale_type: 'free'
  });

  const mutation = useMutation({
    mutationFn: processMatrices,
    onSuccess: (data) => {
      console.log('Résultats:', data);
      // Mettre à jour l'affichage des résultats
    }
  });

  const handleProcess = () => {
    mutation.mutate({
      mca: matrices.mca,
      mcp: matrices.mcp,
      ...config
    });
  };

  return (
    <Paper sx={{ p: 2, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Configuration */}
        <Grid item xs={12} md={4}>
          <FormControl fullWidth>
            <InputLabel>Modèle</InputLabel>
            <Select
              value={config.model}
              onChange={(e) => setConfig({ ...config, model: e.target.value })}
            >
              {[1, 2, 3, 4, 5].map(num => (
                <MenuItem key={num} value={`model${num}`}>
                  Modèle {num}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={4}>
          <FormControl fullWidth>
            <InputLabel>Type d'échelle</InputLabel>
            <Select
              value={config.scale_type}
              onChange={(e) => setConfig({ ...config, scale_type: e.target.value })}
            >
              <MenuItem value="free">Free</MenuItem>
              <MenuItem value="0-1">0-1</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Matrices */}
        <Grid item xs={12}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6">Matrice MCA</Typography>
            {/* Matrice MCA dynamique */}
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6">Matrice MCP</Typography>
            {/* Matrice MCP dynamique */}
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Button 
            variant="contained" 
            onClick={handleProcess}
            disabled={mutation.isLoading}
          >
            Lancer le traitement
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default MatrixInput; 