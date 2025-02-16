# ...existing code...

def main(args):
    try:
        # ...existing code...
        
        # Créer le processeur avec les paramètres explicites
        processor = McapProcessor(
            logger=logger,
            mca_matrix=mca_matrix,
            mcp_matrix=mcp_matrix,
            model_function=model_function,
            mcap_function=args.mcap,    # Assurez-vous que ce paramètre est passé
            scale_type=args.scale,      # Assurez-vous que ce paramètre est passé
            normalize=True,
            norm='l2',
            axis=1
        )

        # Traiter et obtenir les résultats
        results = processor.process()
        
        # Ne pas transposer la matrice, elle doit rester en Activities x Profiles
        result_matrix = results['result_matrix']
        
        # Afficher la matrice dans le bon format
        print("\nMatrice MCAP (Activités x Profiles):")
        print("=================================")
        print(result_matrix.to_string(float_format=lambda x: '{:.3f}'.format(x)))
        
        return 0

# ...existing code...
