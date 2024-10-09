# tests/test_ghz_state.py
import unittest
from qiskit import QuantumCircuit
from src.ghz_state import create_ghz_circuit, run_ghz_experiment

class TestGHZState(unittest.TestCase):
    def test_ghz_circuit_creation(self):
        """
        Test that the GHZ circuit is correctly created with the expected gates.
        """
        # Create a new quantum circuit with 3 qubits
        qc = QuantumCircuit(3)

        # Create the GHZ state circuit
        create_ghz_circuit(qc)

        # Check that the correct number of Hadamard and CNOT gates were applied
        self.assertEqual(qc.count_ops()['h'], 1)  # One Hadamard gate
        self.assertEqual(qc.count_ops()['cx'], 2)  # Two CNOT gates

    def test_ghz_experiment_results(self):
        """
        Test that the GHZ state experiment produces the expected results.
        """
        # Run the GHZ state experiment and get the measurement counts
        counts = run_ghz_experiment(shots=1024)

        # Check that the counts for '000' and '111' are present in the results
        self.assertIn('000', counts)
        self.assertIn('111', counts)

        # Check that the counts for '000' and '111' are roughly equal (allowing some noise)
        self.assertGreater(counts['000'] + counts['111'], 900)

        # Ensure that no other states are present in the results
        for state in ['001', '010', '011', '100', '101', '110']:
            self.assertNotIn(state, counts)

if __name__ == '__main__':
    unittest.main()
