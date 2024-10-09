# tests/test_quantum_teleportation.py
import unittest

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
import numpy as np
from src.quantum_teleportation import quantum_teleport


class TestQuantumTeleportation(unittest.TestCase):

    def test_basic_teleportation(self):
        b = QuantumRegister(2, 'b')
        c = ClassicalRegister(1, 'z')
        qc = QuantumCircuit(b, c)
        quantum_teleport(qc, b[0], b[1], c[0])

        self.assertEqual(qc.num_qubits, 2)
        self.assertEqual(qc.num_clbits, 1)

    def test_teleportation_state_transfer(self):
        b = QuantumRegister(2, 'b')
        c = ClassicalRegister(2, 'z')
        qc = QuantumCircuit(b, c)

        # Prepare initial state
        qc.rx(np.pi / 4, b[0])

        # Teleport
        quantum_teleport(qc, b[0], b[1], c[1])

        # Measure teleported state
        qc.measure(b[1], c[0])

        # Simulate
        simulator = Aer.get_backend('aer_simulator')
        job = simulator.run(transpile(qc, simulator), shots=1024)
        result = job.result()
        counts = result.get_counts(qc)

        # Check results
        self.assertIn('00', counts)
        self.assertIn('01', counts)
        self.assertTrue(0.75 * 1024 <= counts['00'] + counts['10'] <= 0.95 * 1024)

    def test_bell_state_teleportation(self):
        b = QuantumRegister(3, 'b')
        c = ClassicalRegister(3, 'z')
        qc = QuantumCircuit(b, c)

        # Create Bell state
        qc.h(b[0])
        qc.cx(b[0], b[1])

        # Teleport
        quantum_teleport(qc, b[0], b[2], c[2])

        # Measure
        qc.measure(b[2], c[0])
        qc.measure(b[1], c[1])

        # Simulate
        simulator = Aer.get_backend('aer_simulator')
        job = simulator.run(transpile(qc, simulator), shots=1024)
        result = job.result()
        counts = result.get_counts(qc)

        # Check results
        self.assertNotIn('001', counts)
        self.assertNotIn('010', counts)
        self.assertNotIn('101', counts)
        self.assertNotIn('110', counts)
        for state in ['000', '011', '100', '111']:
            self.assertTrue(0.2 * 1024 <= counts[state] <= 0.3 * 1024)


if __name__ == '__main__':
    unittest.main()