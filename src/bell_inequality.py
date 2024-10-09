from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from numpy import pi
import matplotlib.pyplot as plt
from qiskit.visualization import circuit_drawer
from qiskit_aer import Aer


def alice_response(qc, b1, qbit, cbit):
    if b1:
        qc.ry(-pi / 4, qbit)  # Rotate by -45 degrees if b1 is True
    else:
        qc.ry(pi / 4, qbit)  # Rotate by 45 degrees if b1 is False
    qc.measure(qbit, cbit)  # Measure the qubit


def bob_response(qc, b2, qbit, cbit):
    if b2:
        qc.ry(-pi / 8, qbit)  # Rotate by -22.5 degrees if b2 is True
    else:
        qc.ry(3 * pi / 8, qbit)  # Rotate by 67.5 degrees if b2 is False
    qc.measure(qbit, cbit)  # Measure the qubit


def create_and_run_circuit(b1, b2):
    qbits = QuantumRegister(2, 'qbit')
    cbits = ClassicalRegister(2, 'z')
    qc = QuantumCircuit(qbits, cbits)

    # Create the Bell state
    qc.h(qbits[0])
    qc.cx(qbits[0], qbits[1])
    qc.barrier()

    # Apply Alice and Bob's responses
    alice_response(qc, b1, qbits[0], cbits[0])
    bob_response(qc, b2, qbits[1], cbits[1])

    # Simulate
    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc, simulator)
    result = simulator.run(circ, shots=1024).result()
    counts = result.get_counts(circ)

    return qc, counts


def calculate_success_probability():
    total_success_count = 0
    for b1 in [True, False]:
        for b2 in [True, False]:
            _, counts = create_and_run_circuit(b1, b2)
            if b1 and b2:
                success_count = counts.get('01', 0) + counts.get('10', 0)
            else:
                success_count = counts.get('00', 0) + counts.get('11', 0)
            total_success_count += success_count

    return total_success_count / (4 * 1024)


if __name__ == "__main__":
    for b1 in [True, False]:
        for b2 in [True, False]:
            print(f"\nCircuit for b1 = {b1} and b2 = {b2}")
            qc, counts = create_and_run_circuit(b1, b2)

            # Display circuit with modified style
            fig, ax = plt.subplots(figsize=(12, 6))
            circuit_drawer(qc, output='mpl', style={'usepiformat': False, 'displaytext': {'ry': 'RY'}}, ax=ax)
            ax.set_title(f"Bell Inequality Circuit (b1={b1}, b2={b2})")
            plt.tight_layout()
            plt.show()

            print("Measurement counts:", counts)

    prob = calculate_success_probability()
    print(f"\nProbability of Alice/Bob Winning is estimated to be: {prob}")