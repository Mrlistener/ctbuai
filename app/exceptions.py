# @auth: Lizx
# @date: 2024-10-24 14:00

class ModelLoadingError(Exception):
    """Exception raised when there is an error loading the model."""

    def __init__(self, message="Error occurred while loading the model."):
        self.message = message
        super().__init__(self.message)


class ResponseGenerationError(Exception):
    """Exception raised when there is an error generating the response."""

    def __init__(self, message="Error occurred while generating the response."):
        self.message = message
        super().__init__(self.message)
