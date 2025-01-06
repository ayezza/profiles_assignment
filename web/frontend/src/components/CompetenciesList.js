import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { List, ListItem, ListItemText, Typography, Button, Box, Chip } from '@mui/material';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const CompetenciesList = () => {
  const { data: competencies, isLoading, error } = useQuery({
    queryKey: ['competencies'],
    queryFn: async () => {
      const { data } = await axios.get(`${API_URL}/competencies/`);
      return data;
    },
  });

  if (isLoading) return <Typography>Chargement des compétences...</Typography>;
  if (error) return <Typography color="error">Erreur: {error.message}</Typography>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Compétences</Typography>
        <Button variant="contained" color="primary">
          Ajouter une compétence
        </Button>
      </Box>
      
      <List>
        {competencies?.map((competency) => (
          <ListItem key={competency.id} divider>
            <ListItemText
              primary={competency.name}
              secondary={competency.description}
            />
            <Chip 
              label={`Niveau ${competency.level}`}
              color="primary"
              variant="outlined"
              sx={{ ml: 2 }}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default CompetenciesList; 