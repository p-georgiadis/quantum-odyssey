# src/ghz_state.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def create_ghz_circuit(qc):
    """
    Create a GHZ state circuit.

    Args:
    qc (QuantumCircuit): A quantum circuit with at least 3 qubits.

    Returns:
    None: The function modifies the input circuit in-place.
    """
    # Apply a Hadamard gate to the first qubit
    qc.h(0)

    # Apply CNOT gates to entangle the first qubit with the second and third qubits
    qc.cx(0, 1)
    qc.cx(0, 2)


def run_ghz_experiment(shots=1024):
    """
    Run the GHZ state experiment.

    Args:
    shots (int): Number of times to run the circuit.

    Returns:
    dict: Counts of measurement results.
    """
    # Create a quantum circuit with 3 qubits and 3 classical bits for measurement
    qc = QuantumCircuit(3, 3)

    # Create the GHZ state circuit
    create_ghz_circuit(qc)

    # Measure all the qubits into their corresponding classical bits
    qc.measure([0, 1, 2], [0, 1, 2])

    # Use the AerSimulator for the experiment
    simulator = AerSimulator()

    # Transpile and run the circuit
    transpiled_qc = transpile(qc, simulator)
    job = simulator.run(transpiled_qc, shots=shots)

    # Retrieve the result counts
    result = job.result()
    counts = result.get_counts(transpiled_qc)

    return counts


if __name__ == "__main__":
    # Create the GHZ circuit
    qc = QuantumCircuit(3, 3)
    create_ghz_circuit(qc)
    qc.measure_all()

    # Display the circuit
    print("GHZ Circuit:")
    print(qc.draw('text'))

    # Draw the circuit using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    qc.draw('mpl', ax=ax, style='iqp')
    ax.set_title("GHZ State Quantum Circuit", fontsize=16)
    plt.tight_layout()
    plt.show()

    # Run the experiment
    counts = run_ghz_experiment()

    # Print the results
    print(f"\nResult counts from 1024 simulations: {counts}")

    # Plot the histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_histogram(counts, ax=ax, title='GHZ State Measurement Results')
    ax.set_title("GHZ State Measurement Results (1024 simulations)", fontsize=16)
    plt.tight_layout()
    plt.show()