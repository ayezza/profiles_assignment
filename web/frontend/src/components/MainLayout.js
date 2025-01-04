import React from 'react';
import { Box, Container, AppBar, Toolbar, Typography } from '@mui/material';
import MatrixInput from './MatrixInput';
import ResultsDisplay from './ResultsDisplay';

const MainLayout = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Affectation des Profils
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <MatrixInput />
        <ResultsDisplay />
      </Container>
    </Box>
  );
};

export default MainLayout; 