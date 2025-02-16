import React from 'react';
import { 
    Box, 
    Paper, 
    Typography, 
    Table, 
    TableBody, 
    TableCell, 
    TableContainer, 
    TableHead, 
    TableRow,
    CircularProgress
} from '@mui/material';

const Results = ({ results, loading }) => {
    // Add entry point logging
    console.log('Results component entry:', { 
        results, 
        loading,
        hasData: results?.data,
        dataKeys: results?.data ? Object.keys(results.data) : []
    });

    // Add detailed logging
    console.log('Results component state:', {
        isLoading: loading,
        hasResults: !!results,
        resultsType: results ? typeof results : 'none',
        dataKeys: results?.data ? Object.keys(results.data) : []
    });

    console.log('Results component received:', { results, loading });

    // Deep log of the actual data
    console.log('Full results object:', JSON.stringify(results, null, 2));

    if (loading) {
        console.log('Showing loading state');
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <CircularProgress />
            </Box>
        );
    }

    if (!results || !results.data) {
        console.log('No results to display:', results);
        return (
            <Box sx={{ mt: 2 }}>
                <Typography color="error">No results available</Typography>
            </Box>
        );
    }

    const { ranking_matrix, result_matrix, ranking_results, parameters_used, figures } = results.data;
    
    // Log each data piece
    console.log('Parsed data details:', {
        rankingMatrixKeys: ranking_matrix ? Object.keys(ranking_matrix) : [],
        resultMatrixKeys: result_matrix ? Object.keys(result_matrix) : [],
        hasRankingResults: !!ranking_results,
        parametersUsed: parameters_used || 'none',
        figureCount: figures ? Object.keys(figures).length : 0
    });

    console.log('Data received:', {
        hasRankingMatrix: !!ranking_matrix,
        hasResultMatrix: !!result_matrix,
        hasRankingResults: !!ranking_results,
        hasParameters: !!parameters_used,
        hasFigures: !!figures,
        figureKeys: figures ? Object.keys(figures) : []
    });

    // Add debug logging right before each render call
    const debugRender = (data, name) => {
        console.log(`Rendering ${name}:`, {
            hasData: !!data,
            type: typeof data,
            isObject: typeof data === 'object',
            keys: data ? Object.keys(data) : []
        });
        return true;
    };

    const renderParameters = () => {
        debugRender(parameters_used, 'parameters');
        if (!parameters_used) {
            console.log('No parameters to display');
            return null;
        }

        // Force render parameters even if other sections fail
        return (
            <Box sx={{ mb: 4 }}>
                <Typography variant="h6">Parameters Used</Typography>
                <Paper sx={{ p: 2 }}>
                    <Typography>Model: {parameters_used.model_name}</Typography>
                    <Typography>Scale Type: {parameters_used.scale_type}</Typography>
                    <Typography>MCAP Function: {parameters_used.mcap_function}</Typography>
                </Paper>
            </Box>
        );
    };

    const renderRankingMatrix = () => {
        debugRender(ranking_matrix, 'ranking_matrix');
        if (!ranking_matrix) {
            console.log('No ranking matrix to display');
            return null;
        }

        const activities = Object.keys(ranking_matrix);
        if (!activities.length) {
            console.log('No activities in ranking matrix');
            return null;
        }

        console.log('Ranking matrix data:', ranking_matrix);
        
        return (
            <TableContainer component={Paper} sx={{ mb: 4 }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Activity</TableCell>
                            <TableCell>Top 1</TableCell>
                            <TableCell>Top 2</TableCell>
                            <TableCell>Top 3</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {activities.map(activity => (
                            <TableRow key={activity}>
                                <TableCell>{activity}</TableCell>
                                <TableCell>{ranking_matrix[activity].Top1}</TableCell>
                                <TableCell>{ranking_matrix[activity].Top2}</TableCell>
                                <TableCell>{ranking_matrix[activity].Top3}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        );
    };

    const renderResultMatrix = () => {
        debugRender(result_matrix, 'result_matrix');
        if (!result_matrix) {
            console.log('No result matrix to display');
            return null;
        }

        console.log('Result matrix data:', result_matrix);

        const activities = Object.keys(result_matrix);
        if (!activities.length) {
            console.log('No activities in result matrix');
            return null;
        }

        const profiles = Object.keys(result_matrix[activities[0]] || {});
        if (!profiles.length) {
            console.log('No profiles in result matrix');
            return null;
        }

        console.log('Rendering matrix with:', {
            activities: activities.length,
            profiles: profiles.length
        });

        return (
            <TableContainer component={Paper} sx={{ mb: 4 }}>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Activity</TableCell>
                            {profiles.map(profile => (
                                <TableCell key={profile}>{profile}</TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {activities.map(activity => (
                            <TableRow key={activity}>
                                <TableCell>{activity}</TableCell>
                                {profiles.map(profile => (
                                    <TableCell key={`${activity}-${profile}`}>
                                        {Number(result_matrix[activity][profile]).toFixed(3)}
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        );
    };

    const renderFigures = () => {
        if (!figures) {
            console.log('No figures available');
            return null;
        }

        return (
            <Box sx={{ mb: 4 }}>
                <Typography variant="h5" gutterBottom>Graphiques</Typography>
                
                {/* Bar plot section */}
                {figures.bar_plot && (
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" gutterBottom>Distribution des poids</Typography>
                        <Box sx={{ maxWidth: '100%', overflow: 'auto' }}>
                            <img 
                                src={figures.bar_plot} 
                                alt="Bar Plot"
                                style={{ 
                                    maxWidth: 'none', 
                                    height: 'auto',
                                    minWidth: '800px'
                                }}
                                onError={(e) => {
                                    console.error('Error loading bar plot');
                                    e.target.style.display = 'none';
                                }}
                            />
                        </Box>
                    </Box>
                )}

                {/* Radar plots section - Modified for 2 columns */}
                <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>Graphiques radar par activité</Typography>
                    <Box sx={{ 
                        display: 'grid',
                        gridTemplateColumns: 'repeat(2, 1fr)', // Changed to 2 columns
                        gap: 2,
                        '& img': {
                            maxWidth: '100%',
                            height: 'auto'
                        }
                    }}>
                        {Object.entries(figures)
                            .filter(([key]) => key.startsWith('radar_plot_'))
                            .map(([key, value]) => (
                                <Box key={key} sx={{ 
                                    p: 1,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center'
                                }}>
                                    <Typography variant="subtitle1" gutterBottom align="center">
                                        {key.replace('radar_plot_', 'Activité ')}
                                    </Typography>
                                    <img 
                                        src={value} 
                                        alt={`Radar plot for ${key}`}
                                        style={{ width: '100%', maxWidth: '450px' }} // Added maxWidth
                                        onError={(e) => {
                                            console.error(`Error loading radar plot ${key}`);
                                            e.target.style.display = 'none';
                                        }}
                                    />
                                </Box>
                            ))}
                    </Box>
                </Box>
            </Box>
        );
    };

    // Add debug logging before final render
    console.log('Final render check:', {
        hasParameters: !!parameters_used,
        hasRankingMatrix: !!ranking_matrix,
        hasResultMatrix: !!result_matrix,
        hasRankingResults: !!ranking_results,
        hasFigures: !!figures
    });

    return (
        <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Résultats de l'analyse MCAP
            </Typography>
            
            {/* Force render each section separately */}
            <Box>{renderParameters()}</Box>
            
            <Box>{renderFigures()}</Box>
            
            <Box sx={{ mb: 4 }}>
                <Typography variant="h5" gutterBottom>
                    Classement des profils par activité
                </Typography>
                {renderRankingMatrix()}
            </Box>
            
            <Box sx={{ mb: 4 }}>
                <Typography variant="h5" gutterBottom>
                    Matrice des résultats détaillée
                </Typography>
                {renderResultMatrix()}
            </Box>
            
            {ranking_results && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h5" gutterBottom>
                        Resulats détaillés
                    </Typography>
                    <Paper sx={{ p: 2 }}>
                        <pre style={{ whiteSpace: 'pre-wrap', overflow: 'auto' }}>
                            {ranking_results}
                        </pre>
                    </Paper>
                </Box>
            )}
        </Box>
    );
};

export default Results;