from easycmdline.core.base import BaseHandler
import logging 

logger = logging.getLogger(__name__)


class OriginAddHandler(BaseHandler):

    def __init__(self, args):
        super().__init__(args)
        logger.debug("Initializing OriginAddHandler with args: %s", args)
        self.url = args.url
        

    def run(self):

        logger.debug("Running OriginAddHandler with URL: %s", self.url)
        # Here you would typically run the command to add the remote
        # For example, using subprocess to run a git command
        # subprocess.run(['git', 'remote', 'add', self.url])
        print(f"Adding remote with URL: {self.url}")
        # Simulate adding remote
