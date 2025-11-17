

class SystemState:
    def __init__(self):
        self._id_to_increment_from = 0

    def next_id(self):
        next_id = self._id_to_increment_from + 1
        self._id_to_increment_from = next_id
        return next_id