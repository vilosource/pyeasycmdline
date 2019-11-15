from easycmdline.core.base import BaseCommand


class OriginAddCommand(BaseCommand):
    """
    Command to add a remote origin to a Git repository.
    """

    def __init__(self, args, handler=None):
        super().__init__(args, handler)

    def run(self, args=None):
        if self.handler:
            self.handler.run()
        else:
            raise ValueError("No handler provided.")

