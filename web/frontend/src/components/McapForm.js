// ...existing code...

const handleSubmit = async (event) => {
  event.preventDefault();
  
  // Log des paramètres envoyés
  console.log('Sending parameters:', {
    model_function: selectedModel,
    mcap_function: selectedMcap,
    scale_type: selectedScale
  });

  try {
    const response = await fetch('/api/process-mcap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mca_matrix: mcaData,
        mcp_matrix: mcpData,
        model_function: selectedModel,    // Assurez-vous que ces valeurs sont définies
        mcap_function: selectedMcap,      // et correspondent aux sélections de l'utilisateur
        scale_type: selectedScale
      })
    });

    const data = await response.json();
    
    // Log de la réponse
    console.log('Response:', data);

    if (data.status === 'success') {
      // Assurez-vous que la matrice est dans le bon format avant affichage
      const resultMatrix = data.data.result_matrix;
      setResults(resultMatrix);
    } else {
      console.error('Error:', data.message);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

// ...existing code...
