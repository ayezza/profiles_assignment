import React from 'react';
import { Box, Paper, Typography, Grid } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';

const Results = ({ results }) => {
    if (!results) return null;

    const { ranking_matrix, ranking_results, figures } = results;

    // Conversion de la matrice de classement en format DataGrid
    const rows = Object.entries(ranking_matrix).map(([activity, profiles], index) => ({
        id: index,
        activity,
        ...profiles
    }));

    const columns = [
        { field: 'activity', headerName: 'Activité', width: 150 },
        ...Object.keys(ranking_matrix[Object.keys(ranking_matrix)[0]] || {}).map(profile => ({
            field: profile,
            headerName: profile,
            width: 130,
            type: 'number'
        }))
    ];

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
                Résultats
            </Typography>

            <Grid container spacing={3}>
                {/* Matrice de classement */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Matrice de classement
                        </Typography>
                        <div style={{ height: 400, width: '100%' }}>
                            <DataGrid
                                rows={rows}
                                columns={columns}
                                pageSize={5}
                                rowsPerPageOptions={[5]}
                                disableSelectionOnClick
                            />
                        </div>
                    </Paper>
                </Grid>

                {/* Résultats détaillés */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Résultats détaillés
                        </Typography>
                        <Typography component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                            {ranking_results}
                        </Typography>
                    </Paper>
                </Grid>

                {/* Graphiques */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                            Visualisations
                        </Typography>
                        <Grid container spacing={2}>
                            {Object.entries(figures).map(([name, data]) => (
                                <Grid item xs={12} md={6} key={name}>
                                    <Typography variant="subtitle1" gutterBottom>
                                        {name}
                                    </Typography>
                                    <img
                                        src={`data:image/png;base64,${data}`}
                                        alt={name}
                                        style={{
                                            maxWidth: '100%',
                                            height: 'auto'
                                        }}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Results; 