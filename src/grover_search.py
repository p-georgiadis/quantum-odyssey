from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import MCPhaseGate
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np


def mark_pure_states(qc, b0, b1, b2, b3):
    mcphase = MCPhaseGate(np.pi, 3)

    # Mark |0011>
    qc.x(b0)
    qc.x(b1)
    qc.append(mcphase, [b0, b1, b2, b3])
    qc.x(b0)
    qc.x(b1)

    # Mark |1100>
    qc.x(b2)
    qc.x(b3)
    qc.append(mcphase, [b0, b1, b2, b3])
    qc.x(b2)
    qc.x(b3)

    # Mark |0101>
    qc.x(b0)
    qc.x(b2)
    qc.append(mcphase, [b0, b1, b2, b3])
    qc.x(b0)
    qc.x(b2)


def Uf(qc, b):
    mark_pure_states(qc, b[0], b[1], b[2], b[3])


def apply_reflection_about_uniform_state(qc, input_registers):
    for i in input_registers:
        qc.h(i)
        qc.x(i)
    n = len(input_registers)
    qc.mcp(np.pi, input_registers[0:n - 1], input_registers[n - 1])
    for i in input_registers:
        qc.x(i)
        qc.h(i)


def Grover_diffuse(qc, inputs):
    Uf(qc, inputs)
    apply_reflection_about_uniform_state(qc, inputs)
    qc.barrier()


def create_quantum_circuit_for_grover(n_iters):
    inputs = QuantumRegister(4, 'b')
    cbit = ClassicalRegister(4, 'z')
    qc = QuantumCircuit(inputs, cbit)
    for i in inputs:
        qc.h(i)
    qc.barrier()
    for i in range(n_iters):
        Grover_diffuse(qc, inputs)
    qc.measure(inputs, cbit)
    return qc


def run_grover_search(n_iters=4):
    qc = create_quantum_circuit_for_grover(n_iters)
    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc, simulator)
    result = simulator.run(circ, shots=1024).result()
    counts = result.get_counts(circ)
    return qc, counts


if __name__ == "__main__":
    qc, counts = run_grover_search()

    print('Grover Search After Four Iterations')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

    qc.draw('mpl', ax=ax1)
    ax1.set_title("Grover's Search Circuit")

    plot_histogram(counts, ax=ax2, title='Result Counts (1024 simulations)')

    plt.tight_layout()
    plt.show()

    print(f"Measurement counts: {counts}")
    marked_states_count = counts.get('0011', 0) + counts.get('1010', 0) + counts.get('1100', 0)
    print(f"Total count for marked states: {marked_states_count}")