import React from 'react';
import { Box, Container, AppBar, Toolbar, Typography, Paper } from '@mui/material';
import ProfilesList from './ProfilesList';
import CompetenciesList from './CompetenciesList';

const MainLayout = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MCAP Profiles Manager
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 4 }}>
          <Paper sx={{ p: 2 }}>
            <ProfilesList />
          </Paper>
          <Paper sx={{ p: 2 }}>
            <CompetenciesList />
          </Paper>
        </Box>
      </Container>
    </Box>
  );
};

export default MainLayout; 