class TrillerLoginException(Exception):
    def __init__(
        self,
        message="Triller login failed",
    ):
        self.message = message
        super().__init__(self.message)


class TrillerAPIException(Exception):
    def __init__(self, message="Triller API Failure"):
        self.message = message
        super().__init__(self.message)
