import unittest
from src.grover_search import run_grover_search


class TestGroverSearch(unittest.TestCase):
    def test_marked_states_amplification(self):
        _, counts = run_grover_search()
        marked_states_count = counts.get('0011', 0) + counts.get('1010', 0) + counts.get('1100', 0)

        self.assertGreaterEqual(
            marked_states_count,
            500,
            "The marked states should account for more than 50% of the counts. Are you implementing the Marking circuit correctly?"
        )

    def test_unmarked_states_suppression(self):
        _, counts = run_grover_search()

        for state in ['0000', '0001', '0010', '0100', '0101', '0110', '0111', '1000', '1001', '1011', '1101', '1110',
                      '1111']:
            self.assertLess(
                counts.get(state, 0),
                100,
                f"Unmarked state {state} has unexpectedly high count. The Grover diffusion operator might not be working correctly."
            )


if __name__ == '__main__':
    unittest.main()