# tests/test_qaoa.py

import unittest
import numpy as np
from src.circuits.qaoa import QAOA

class TestQAOA(unittest.TestCase):
    """Test cases for QAOA implementation."""
    
    def setUp(self):
        """Set up test cases."""
        self.n_qubits = 4
        self.qaoa = QAOA(self.n_qubits)
        self.test_edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
        
    def test_circuit_creation(self):
        """Test QAOA circuit creation."""
        gamma = 0.5
        beta = 1.0
        
        circuit = self.qaoa.create_qaoa_circuit(self.test_edges, gamma, beta)
        
        self.assertEqual(circuit.num_qubits, self.n_qubits)
        self.assertEqual(circuit.num_clbits, self.n_qubits)
        
    def test_circuit_execution(self):
        """Test QAOA circuit execution."""
        circuit = self.qaoa.create_qaoa_circuit(self.test_edges, 0.5, 1.0)
        counts = self.qaoa.execute_circuit(circuit, shots=1000)
        
        # Check if we get valid measurement results
        self.assertEqual(sum(counts.values()), 1000)
        for bitstring in counts:
            self.assertEqual(len(bitstring), self.n_qubits)
            
    def test_expectation_computation(self):
        """Test expectation value computation."""
        # Mock measurement results
        counts = {'0000': 500, '1111': 500}
        
        expectation = self.qaoa.compute_expectation(counts, self.test_edges)
        self.assertIsInstance(expectation, float)

if __name__ == '__main__':
    unittest.main()