class MigrationError(Exception):
    def __init__(self, root_exception):
        self.root_exception = root_exception


class RollbackError(MigrationError):
    pass
