from typing import Optional
import argparse
from easycmdline.core.base import BaseHandler


class GreeterHandler(BaseHandler):
    def __init__(self, args: argparse.Namespace):
        super().__init__(args)
        self.name: str = args.name

    def run(self, args: Optional[argparse.Namespace] = None) -> None:
        print(f"Hello {self.name}!")
        # Here you would typically run the command to greet
        # For example, using subprocess to run a greeting command
        # subprocess.run(['echo', f'Hello {self.name}!'])
