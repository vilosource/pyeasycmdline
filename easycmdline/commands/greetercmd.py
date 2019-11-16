from easycmdline.core.base import BaseCommand


class GreeterCommand(BaseCommand):
    def __init__(self, args, handler=None):
        super().__init__(args, handler)
        self.name = args.name

    def run(self):
        print(f"Hello {self.name}!")
        if self.handler:
            # Call the handler's run method if provided
            # We don't pass args to the handler here, because
            # the handler should already have the necessary data
            # hwhen it was passed to this class during initialization
            # This is a design choice; you could also pass args if needed
            self.handler.run()
        else:
            print("No handler provided.")
