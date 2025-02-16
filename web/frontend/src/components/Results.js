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
    console.log('Results props:', { results, loading });

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <CircularProgress />
            </Box>
        );
    }

    if (!results || !results.data) {
        console.log('No results to display');
        return (
            <Box sx={{ mt: 2 }}>
                <Typography color="error">No results available</Typography>
            </Box>
        );
    }

    const { ranking_matrix, result_matrix, ranking_results, parameters_used } = results.data;

    const renderParameters = () => {
        if (!parameters_used) return null;

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
        if (!ranking_matrix) return null;

        const activities = Object.keys(ranking_matrix);
        
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
        if (!result_matrix) return null;

        const activities = Object.keys(result_matrix);
        if (!activities.length) return null;

        const profiles = Object.keys(result_matrix[activities[0]] || {});
        if (!profiles.length) return null;

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

    return (
        <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                MCAP Analysis Results
            </Typography>
            
            {renderParameters()}
            
            <Box sx={{ mb: 4 }}>
                <Typography variant="h5" gutterBottom>Profile Rankings by Activity</Typography>
                {renderRankingMatrix()}
            </Box>
            
            <Box sx={{ mb: 4 }}>
                <Typography variant="h5" gutterBottom>Detailed Results Matrix</Typography>
                {renderResultMatrix()}
            </Box>
            
            {ranking_results && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h5" gutterBottom>Detailed Results</Typography>
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