from easycmdline.core.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class SimpleCommand(BaseCommand):
    def __init__(self, args, handler=None):
        """
        Initialize the command with arguments and an optional handler.
        :param args: Arguments for the command.
        :param handler: Optional handler to process the command.
        """

        """ Technicaly we don't really need to call the super constructor here,
        but it's a good practice to do so, because the BaseCommand class might
        have some initialization logic that we want to inherit. 

        This is a basic command class that doesn't do much, but it serves as a
        template for more complex commands.

        If needed we could also add some command specific arguments here, but
        we don't need to do that for now.

        """

        super().__init__(args, handler)
        logging.debug(f"SimpleCommand initialized with args: {args}")

    def run(self):
        """
        Run the command:

        The handler also has by default the same args as this command. It is passed
        by the run method of the cli.py module when it instantiates the command.
        """
        print(f"Message:  {self.args.message}")

        # The handler is optional, so we check if it's provided before calling it.
        # If it's not provided, we just print a message.
        #
        # In a real command, you would typically run some logic here,
        # such as executing a command or processing data, or just completely
        # leave the logic to the handler.

        # We could for example implement run_async instead of run and run the command
        # in a separate thread or process, but for now we just run it in the main thread.
        # This is a simple command that just prints a message.
        if self.handler:
            self.handler.run(self.args)
        else:
            print("No handler provided.")
