# tests/test_error_correction.py

import unittest
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import state_fidelity
from src.circuits.error_correction import QuantumErrorCorrection

class TestQuantumErrorCorrection(unittest.TestCase):
    """Test cases for quantum error correction implementations."""
    
    def setUp(self):
        """Set up test cases."""
        self.qec = QuantumErrorCorrection()
        self.simulator = Aer.get_backend('statevector_simulator')
    
    def test_encoder_circuit_creation(self):
        """Test if encoder circuit is created correctly."""
        encoder = self.qec.create_encoder()
        self.assertIsInstance(encoder, QuantumCircuit)
        self.assertEqual(encoder.num_qubits, 3)
        
    def test_single_error_decoder_creation(self):
        """Test if single error decoder circuit is created correctly."""
        decoder = self.qec.create_single_error_decoder()
        self.assertIsInstance(decoder, QuantumCircuit)
        self.assertEqual(decoder.num_qubits, 3)
        
    def test_error_correction_single_error(self):
        """Test if single bit-flip error is corrected."""
        # Create test state |0⟩ + |1⟩
        initial_state = QuantumCircuit(1)
        initial_state.h(0)
        
        # Encode
        encoder = self.qec.create_encoder()
        encoded_circuit = initial_state.compose(encoder)
        
        # Add error (X gate) to first qubit
        encoded_circuit.x(0)
        
        # Decode
        decoder = self.qec.create_single_error_decoder()
        final_circuit = encoded_circuit.compose(decoder)
        
        # Simulate
        result = execute(final_circuit, self.simulator).result()
        final_state = result.get_statevector()
        
        # Check if state is recovered
        expected_state = execute(initial_state, self.simulator).result().get_statevector()
        fidelity = state_fidelity(final_state, expected_state)
        self.assertGreater(fidelity, 0.99)


