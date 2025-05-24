class ResponseParsingError(Exception):
    """
    Custom exception for errors during LLM response parsing.
    https://ai.google.dev/gemini-api/docs/structured-output#configuring-a-schema
    """

    pass


class ClientInitializationError(Exception):
    """
    Custom exception for errors during client initialization.
    """

    pass


class APIKeyError(Exception):
    """
    Custom exception for errors when API key.
    """


class MissingAPIKeyError(APIKeyError):
    """
    Custom exception for errors when API key is missing.
    """

    pass


class InvalidAPIKeyError(APIKeyError):
    """
    Custom exception for errors when API key is invalid.
    """

    pass