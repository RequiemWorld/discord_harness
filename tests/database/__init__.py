import unittest
from discord_harness.database import SystemState
from discord_harness.database import UserOperationsService


class DatabaseTestFixture(unittest.TestCase):

    def setUp(self):
        self._state = SystemState()
        self._user_operations = UserOperationsService(self._state)

    def override_system_state_next_id_indefinitely(self, new_id: int):
        self._state.next_id = lambda: new_id
