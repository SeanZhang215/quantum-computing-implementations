# tests/test_qubit_routing.py

import unittest
from qiskit import QuantumCircuit
from src.circuits.qubit_routing import QubitRouter

class TestQubitRouter(unittest.TestCase):
    """Test cases for qubit routing implementations."""
    
    def setUp(self):
        """Set up test cases."""
        self.router = QubitRouter(basis_gates=['cx', 'u'])
        
    def test_basic_decomposition(self):
        """Test basic circuit decomposition."""
        # Create test circuit
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        
        decomposed = self.router.decompose_circuit(circuit)
        self.assertIsInstance(decomposed, QuantumCircuit)
        
        # Check if only basis gates are used
        for gate in decomposed.data:
            self.assertIn(gate[0].name, ['cx', 'u'])
            
    def test_layout_optimization(self):
        """Test layout optimization with coupling map."""
        # Create test circuit
        circuit = QuantumCircuit(3)
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        
        # Define linear coupling map
        coupling_map = [(0, 1), (1, 2)]
        
        result = self.router.optimize_layout(circuit, coupling_map)
        
        self.assertIn('circuit', result)
        self.assertIn('depth', result)
        self.assertIn('size', result)
        self.assertIn('gate_counts', result)
