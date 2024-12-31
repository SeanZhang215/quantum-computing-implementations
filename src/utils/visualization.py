# src/utils/visualization.py

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Any
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

class CircuitVisualizer:
    """Utility class for visualizing quantum circuits and their results."""
    
    @staticmethod
    def plot_circuit_comparison(original: QuantumCircuit, 
                              transformed: QuantumCircuit, 
                              title: str = "Circuit Comparison") -> None:
        """
        Plot original and transformed circuits side by side.
        
        Args:
            original: Original quantum circuit
            transformed: Transformed quantum circuit
            title: Title for the comparison plot
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        original.draw(output='mpl', ax=ax1)
        transformed.draw(output='mpl', ax=ax2)
        
        ax1.set_title("Original Circuit")
        ax2.set_title("Transformed Circuit")
        fig.suptitle(title)
        plt.tight_layout()
        
    @staticmethod
    def plot_measurement_results(counts: Dict[str, int], 
                               title: str = "Measurement Results") -> None:
        """
        Plot histogram of measurement results.
        
        Args:
            counts: Dictionary of measurement results and their counts
            title: Title for the histogram
        """
        plot_histogram(counts)
        plt.title(title)
        
    @staticmethod
    def plot_coupling_map(coupling_map: List[Tuple[int, int]], 
                         node_colors: List[str] = None) -> None:
        """
        Visualize a coupling map as a graph.
        
        Args:
            coupling_map: List of tuples representing qubit connections
            node_colors: Optional list of colors for nodes
        """
        G = nx.Graph()
        G.add_edges_from(coupling_map)
        
        if node_colors is None:
            node_colors = ['lightblue'] * len(G.nodes())
            
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, 
                node_color=node_colors,
                with_labels=True, 
                node_size=500,
                font_size=16,
                font_weight='bold')
        plt.title("Qubit Coupling Map")
        
    @staticmethod
    def plot_qaoa_landscape(gammas: np.ndarray, 
                          betas: np.ndarray, 
                          expectations: np.ndarray) -> None:
        """
        Plot QAOA optimization landscape.
        
        Args:
            gammas: Array of gamma values
            betas: Array of beta values
            expectations: 2D array of expectation values
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        gamma_mesh, beta_mesh = np.meshgrid(gammas, betas)
        
        surf = ax.plot_surface(gamma_mesh, beta_mesh, expectations,
                             cmap='viridis',
                             edgecolor='none')
        
        ax.set_xlabel('Gamma')
        ax.set_ylabel('Beta')
        ax.set_zlabel('Expectation Value')
        plt.colorbar(surf)
        plt.title('QAOA Parameter Landscape')
