import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { List, ListItem, ListItemText, Typography, Button, Box } from '@mui/material';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const ProfilesList = () => {
  const { data: profiles, isLoading, error } = useQuery({
    queryKey: ['profiles'],
    queryFn: async () => {
      const { data } = await axios.get(`${API_URL}/profiles/`);
      return data;
    },
  });

  if (isLoading) return <Typography>Chargement des profils...</Typography>;
  if (error) return <Typography color="error">Erreur: {error.message}</Typography>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Profils</Typography>
        <Button variant="contained" color="primary">
          Ajouter un profil
        </Button>
      </Box>
      
      <List>
        {profiles?.map((profile) => (
          <ListItem key={profile.id} divider>
            <ListItemText
              primary={profile.name}
              secondary={profile.description}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default ProfilesList; 