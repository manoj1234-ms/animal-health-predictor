"""
Knowledge Graph Builder
Visualizes relationships between species, diseases, and categories using NetworkX
"""
import networkx as nx
import json
import matplotlib.pyplot as plt
import os
import joblib

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.load_data()
        
    def load_data(self):
        # Load encoders to get all known species and diseases
        try:
            category_encoder = joblib.load('models/category_encoder.pkl')
            species_encoder = joblib.load('models/species_encoder.pkl')
            disease_encoders = joblib.load('models/disease_encoders.pkl')
            
            self.categories = category_encoder.classes_
            self.species = species_encoder.classes_
            self.disease_map = {}
            for cat, enc in disease_encoders.items():
                self.disease_map[cat] = enc.classes_
                
        except Exception as e:
            print(f"Error loading model artifacts: {e}")
            self.categories = []
            self.species = []
            self.disease_map = {}

    def build_graph(self):
        print("Building Knowledge Graph...")
        
        # Add Categories (Hubs)
        for cat in self.categories:
            self.graph.add_node(cat, type="category", color="red", size=20)
            
            # Add Diseases linked to Categories
            if cat in self.disease_map:
                for disease in self.disease_map[cat]:
                    self.graph.add_node(disease, type="disease", color="blue", size=10)
                    self.graph.add_edge(cat, disease, weight=1)
                    
        # Add Species (This is harder because we don't have direct Dis->Spec mapping in artifacts)
        # We can infer from the `biological_validation.py` dict if we import it, 
        # or just visualize Category->Disease structure for now.
        
        # Let's import the compatibility matrix
        from src.biological_validation import ANIMAL_DISEASE_COMPATIBILITY
        
        for animal, cats in ANIMAL_DISEASE_COMPATIBILITY.items():
            self.graph.add_node(animal, type="animal", color="green", size=15)
            
            for cat, diseases in cats.items():
                # Link Animal -> Category (weak link)
                # self.graph.add_edge(animal, cat, weight=0.5) 
                
                # Link Animal -> Disease (strong link)
                for disease in diseases:
                    if self.graph.has_node(disease):
                        self.graph.add_edge(animal, disease, weight=2)

    def export_graph_json(self, path='data/knowledge_graph.json'):
        data = nx.node_link_data(self.graph)
        os.makedirs('data', exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f)
        print(f"✅ Knowledge Graph exported to {path}")

    def get_stats(self):
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges()
        }

if __name__ == "__main__":
    kg = KnowledgeGraph()
    kg.build_graph()
    kg.export_graph_json()
    print(kg.get_stats())
