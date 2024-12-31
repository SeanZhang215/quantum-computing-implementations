# src/circuits/error_correction.py

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from typing import Tuple, Optional

class QuantumErrorCorrection:
    """
    Implementation of quantum error correction circuits including bit-flip error correction.
    
    This class provides methods to create quantum circuits for encoding and decoding
    quantum states with error correction capabilities.
    """
    
    def __init__(self):
        """Initialize the quantum error correction module."""
        pass
        
    def create_encoder(self) -> QuantumCircuit:
        """
        Create a 3-qubit bit-flip QEC encoder circuit.
        
        The encoder creates the following state:
        |ψ⟩ = |q₂⟩⊗|q₁⟩⊗|q₀⟩ = |0⟩⊗|0⟩⊗(α|0⟩+β|1⟩)
        
        Returns:
            QuantumCircuit: Encoder circuit for 3-qubit bit-flip code
        """
        qr = QuantumRegister(3)
        qc = QuantumCircuit(qr, name='encoder')
        
        # Encode logical qubit into 3-qubit state
        qc.cx(qr[0], qr[1])  # CNOT from control q₀ to target q₁
        qc.cx(qr[0], qr[2])  # CNOT from control q₀ to target q₂
        
        return qc
    
    def create_single_error_decoder(self) -> QuantumCircuit:
        """
        Create a decoder circuit that can correct a single bit-flip error.
        
        The decoder identifies and corrects up to one bit-flip error by using
        majority voting implemented with Toffoli (CCX) gates.
        
        Returns:
            QuantumCircuit: Decoder circuit for single bit-flip error correction
        """
        qr = QuantumRegister(3)
        qc = QuantumCircuit(qr, name='single_error_decoder')
        
        # Syndrome measurement using CNOTs
        qc.cx(qr[0], qr[1])
        qc.cx(qr[0], qr[2])
        
        # Error correction using CCX (Toffoli) gates
        qc.ccx(qr[1], qr[2], qr[0])  # Correct error on q₀
        qc.ccx(qr[2], qr[0], qr[1])  # Correct error on q₁
        qc.ccx(qr[0], qr[1], qr[2])  # Correct error on q₂
        
        return qc
    
    def create_double_error_decoder(self) -> QuantumCircuit:
        """
        Create a decoder circuit that can correct up to two bit-flip errors.
        
        This implementation uses a more complex syndrome measurement scheme
        to handle multiple errors.
        
        Returns:
            QuantumCircuit: Decoder circuit for double bit-flip error correction
        """
        qr = QuantumRegister(9)
        qc = QuantumCircuit(qr, name='double_error_decoder')
        
        # Syndrome measurement
        qc.cx(qr[0], qr[5])
        qc.cx(qr[1], qr[5])
        qc.cx(qr[1], qr[6])
        qc.cx(qr[2], qr[6])
        qc.cx(qr[2], qr[7])
        qc.cx(qr[3], qr[7])
        qc.cx(qr[3], qr[8])
        qc.cx(qr[4], qr[8])
        
        # Error correction logic
        qc.ccx(qr[5], qr[7], qr[1])
        qc.ccx(qr[6], qr[8], qr[3])
        qc.ccx(qr[5], qr[6], qr[0])
        qc.ccx(qr[6], qr[7], qr[2])
        qc.ccx(qr[7], qr[8], qr[4])
        
        return qc
