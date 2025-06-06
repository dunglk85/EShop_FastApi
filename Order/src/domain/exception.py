class DomainException(Exception):
    def __init__(self, message: str):
        super().__init__(f'Domain Exception: "{message}" throws from Domain Layer.')