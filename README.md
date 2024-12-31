# Quantum Computing Implementations

Python implementations of core quantum computing algorithms using Qiskit, focusing on error correction, qubit routing, and QAOA.

## Features

- Quantum Error Correction (QEC) with 3-qubit bit-flip code
- Qubit routing and mapping optimization using SABRE algorithm
- QAOA (Quantum Approximate Optimization Algorithm) for MaxCut problems

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
# Error Correction
from src.circuits.error_correction import QuantumErrorCorrection
qec = QuantumErrorCorrection()
encoder = qec.create_encoder()

# Qubit Routing
from src.circuits.qubit_routing import QubitRouter
router = QubitRouter(basis_gates=['cx', 'u'])
result = router.optimize_layout(your_circuit, coupling_map)

# QAOA
from src.circuits.qaoa import QAOA
qaoa = QAOA(n_qubits=4)
circuit = qaoa.create_qaoa_circuit(graph_edges, gamma=0.5, beta=1.0)
```

## Testing

```bash
python -m unittest discover tests
```

