# src/utils/benchmarks.py

import time
import glob
import os
from typing import Dict, List, Tuple, Any
from qiskit import QuantumCircuit
import numpy as np

class CircuitBenchmarker:
    """Utility class for benchmarking quantum circuits and algorithms."""
    
    def __init__(self):
        self.benchmarks = {}
        self.results = {}
        
    def load_qasm_benchmarks(self, path: str) -> Dict[str, QuantumCircuit]:
        """
        Load QASM benchmark circuits from a directory.
        
        Args:
            path: Directory containing QASM files
            
        Returns:
            Dictionary mapping benchmark names to circuits
        """
        qasm_files = glob.glob(os.path.join(path, '*.qasm'))
        benchmarks = {}
        
        for qasm_file in qasm_files:
            name = os.path.basename(qasm_file).split('.')[0]
            circuit = QuantumCircuit.from_qasm_file(qasm_file)
            circuit.name = name
            benchmarks[name] = circuit
            
        self.benchmarks = benchmarks
        return benchmarks
    
    def analyze_circuit_metrics(self, circuit: QuantumCircuit) -> Dict[str, Any]:
        """
        Analyze various metrics of a quantum circuit.
        
        Args:
            circuit: Quantum circuit to analyze
            
        Returns:
            Dictionary containing circuit metrics
        """
        return {
            'depth': circuit.depth(),
            'width': circuit.width(),
            'size': circuit.size(),
            'num_qubits': circuit.num_qubits,
            'num_clbits': circuit.num_clbits,
            'gate_counts': circuit.count_ops(),
            'nonlocal_gates': sum(1 for inst in circuit.data if len(inst[1]) > 1)
        }
    
    def benchmark_execution_time(self, 
                               circuit: QuantumCircuit, 
                               num_runs: int = 5) -> Dict[str, float]:
        """
        Benchmark circuit execution time.
        
        Args:
            circuit: Circuit to benchmark
            num_runs: Number of runs for averaging
            
        Returns:
            Dictionary containing timing metrics
        """
        times = []
        
        for _ in range(num_runs):
            start_time = time.time()
            # Execute circuit (placeholder for actual execution)
            _ = circuit.depth()  # Simple operation for demonstration
            end_time = time.time()
            times.append(end_time - start_time)
            
        return {
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'min_time': np.min(times),
            'max_time': np.max(times)
        }
    
    def compare_circuits(self, 
                        circuit1: QuantumCircuit, 
                        circuit2: QuantumCircuit) -> Dict[str, Any]:
        """
        Compare metrics between two circuits.
        
        Args:
            circuit1: First circuit
            circuit2: Second circuit
            
        Returns:
            Dictionary containing comparison metrics
        """
        metrics1 = self.analyze_circuit_metrics(circuit1)
        metrics2 = self.analyze_circuit_metrics(circuit2)
        
        comparison = {}
        for key in metrics1.keys():
            if isinstance(metrics1[key], (int, float)):
                comparison[f'{key}_diff'] = metrics2[key] - metrics1[key]
                comparison[f'{key}_ratio'] = metrics2[key] / metrics1[key] if metrics1[key] != 0 else float('inf')
                
        return comparison

class QAOABenchmarker:
    """Utility class specifically for benchmarking QAOA performance."""
    
    @staticmethod
    def generate_random_graph(n_nodes: int, 
                            edge_probability: float = 0.3) -> List[Tuple[int, int, float]]:
        """
        Generate random graph for QAOA testing.
        
        Args:
            n_nodes: Number of nodes in the graph
            edge_probability: Probability of edge between any two nodes
            
        Returns:
            List of (node1, node2, weight) tuples
        """
        edges = []
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                if np.random.random() < edge_probability:
                    weight = np.random.uniform(0.5, 1.5)
                    edges.append((i, j, weight))
        return edges
    
    @staticmethod
    def compute_classical_maxcut(edges: List[Tuple[int, int, float]], 
                               n_nodes: int) -> Tuple[float, str]:
        """
        Compute classical MaxCut solution for comparison.
        
        Args:
            edges: List of (node1, node2, weight) tuples
            n_nodes: Number of nodes in the graph
            
        Returns:
            Tuple of (maximum cut value, bit string of cut)
        """
        max_cut = 0
        best_cut = None
        
        for i in range(2**n_nodes):
            cut = format(i, f'0{n_nodes}b')
            cut_value = 0
            
            for u, v, weight in edges:
                if cut[u] != cut[v]:
                    cut_value += weight
                    
            if cut_value > max_cut:
                max_cut = cut_value
                best_cut = cut
                
        return max_cut, best_cut
    
    @staticmethod
    def analyze_qaoa_accuracy(quantum_solution: Dict[str, int],
                            classical_solution: Tuple[float, str],
                            edges: List[Tuple[int, int, float]]) -> Dict[str, float]:
        """
        Analyze QAOA solution quality compared to classical solution.
        
        Args:
            quantum_solution: QAOA measurement results
            classical_solution: Classical MaxCut solution
            edges: Graph edges with weights
            
        Returns:
            Dictionary containing accuracy metrics
        """
        classical_max, _ = classical_solution
        
        # Calculate the cut value for each measured state
        quantum_cuts = {}
        for state, count in quantum_solution.items():
            cut_value = sum(weight for i, j, weight in edges 
                          if state[i] != state[j])
            quantum_cuts[state] = cut_value
            
        best_quantum_cut = max(quantum_cuts.values())
        
        return {
            'approximation_ratio': best_quantum_cut / classical_max,
            'average_cut_ratio': np.mean(list(quantum_cuts.values())) / classical_max,
            'success_probability': sum(count for state, count in quantum_solution.items() 
                                    if quantum_cuts[state] == best_quantum_cut) / sum(quantum_solution.values())
        }