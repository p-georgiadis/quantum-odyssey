# src/quantum_teleportation.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import matplotlib.pyplot as plt


def quantum_teleport(qc, b0, b1, cbit):
    """
    Implement the quantum teleportation protocol.

    Parameters:
    - qc (QuantumCircuit): Quantum circuit instance.
    - b0 (int): Index of the qubit holding the state to teleport.
    - b1 (int): Index of the qubit that will receive the teleported state.
    - cbit (int): Index of the classical bit to store measurement result.
    """
    # Step 1: Apply Hadamard gate to b1
    qc.h(b1)

    # Step 2: Apply controlled-X (CNOT) gate with control b1 and target b0
    qc.cx(b1, b0)

    # Step 3: Apply controlled-X (CNOT) gate with control b0 and target b1
    qc.cx(b0, b1)

    # Step 4: Measure b0 into classical bit cbit
    qc.measure(b0, cbit)


def create_teleportation_circuit():
    """
    Create a basic quantum teleportation circuit.

    Returns:
    - QuantumCircuit: A quantum circuit set up for teleportation.
    """
    b = QuantumRegister(2, 'b')
    c = ClassicalRegister(1, 'z')
    qc = QuantumCircuit(b, c)
    quantum_teleport(qc, b[0], b[1], c[0])
    return qc


if __name__ == "__main__":
    circuit = create_teleportation_circuit()
    fig = circuit.draw('mpl', style='iqp')
    plt.show()