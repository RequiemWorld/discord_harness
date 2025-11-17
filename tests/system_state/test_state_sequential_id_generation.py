import unittest
from discord_harness.backend import SystemState


class TestSystemStateId(unittest.TestCase):
    def setUp(self):
        self._state = SystemState()

    def test_should_get_1_on_first_call_to_next_id(self):
        self.assertEqual(1, self._state.next_id())

    def test_should_go_up_by_one_one_each_call_to_next_id(self):
        self.assertEqual(1, self._state.next_id())
        self.assertEqual(2, self._state.next_id())
        self.assertEqual(3, self._state.next_id())
