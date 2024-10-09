import unittest
from src.bell_inequality import create_and_run_circuit, calculate_success_probability

class TestBellInequality(unittest.TestCase):

    def test_circuit_outcomes(self):
        for b1 in [True, False]:
            for b2 in [True, False]:
                with self.subTest(b1=b1, b2=b2):
                    _, counts = create_and_run_circuit(b1, b2)
                    self.assertIn('00', counts, f'Result for b1={b1} and b2={b2} must have non-zero amplitude for |00>')
                    self.assertIn('11', counts, f'Result for b1={b1} and b2={b2} must have non-zero amplitude for |11>')
                    self.assertIn('01', counts, f'Result for b1={b1} and b2={b2} must have non-zero amplitude for |01>')
                    self.assertIn('10', counts, f'Result for b1={b1} and b2={b2} must have non-zero amplitude for |10>')

    def test_success_probability(self):
        prob = calculate_success_probability()
        self.assertGreater(prob, 0.45, "Success probability should be greater than 45%")
        self.assertLess(prob, 0.55, "Success probability should be less than 55%")
        print(f"Calculated success probability: {prob}")

if __name__ == '__main__':
    unittest.main()