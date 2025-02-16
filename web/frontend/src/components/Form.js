const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const form = e.target;
    
    // Get form values
    const mcaFile = form.querySelector('input[name="mca"]').files[0];
    const mcpFile = form.querySelector('input[name="mcp"]').files[0];
    const model = form.querySelector('select[name="model"]').value;
    const scale = form.querySelector('select[name="scale"]').value;
    const mcapFunction = form.querySelector('select[name="mcap"]').value;

    // Log for debugging
    console.log('Sending parameters:', {
        model,
        scale_type: scale,
        mcap_function: mcapFunction
    });

    // Append form data
    formData.append('mca_file', mcaFile);
    formData.append('mcp_file', mcpFile);
    formData.append('model', model);
    formData.append('scale_type', scale);
    formData.append('mcap_function', mcapFunction);

    try {
        const response = await fetch('http://localhost:3001/process', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        console.log('Server response:', data);
        
        if (!data.status || data.status !== 'success' || !data.data) {
            throw new Error(data.error || 'Invalid server response');
        }
        
        const { ranking, result } = data.data;
        if (!ranking || !result || !result.data || !result.columns) {
            throw new Error('Missing data in server response');
        }
        
        // Transform result matrix for display
        const transformedMatrix = result.data.map((row, i) => {
            const obj = { activity: result.index[i] };
            result.columns.forEach((col, j) => {
                obj[col] = row[j];
            });
            return obj;
        });
        
        setResults(transformedMatrix);
        setMatrixShape([result.data.length, result.columns.length]);
        
    } catch (error) {
        console.error('Error:', error);
        setError(error.message || 'Failed to process request');
    }
};
