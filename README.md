# pyeasycmdline

A powerful YAML-driven command-line interface framework for Python applications.

## Features

- Define command structure using YAML configuration
- Support for nested subcommands
- Command and handler separation for clean architecture
- Automatic argument parsing based on YAML definitions
- Extensible command registry
- Class-based API for programmatic usage

## Installation

Using pip:

```bash
pip install pyeasycmdline
```

## Quick Start

Now you can easily implement complex command line interfaces without having to write argument parsing code, allowing you to focus on your actual command implementation.

### 1. Define your commands in YAML

```yaml
# my_config.yml
commands:
  convert:
    description: "Convert files between formats"
    command_class: "myapp.commands.ConvertCommand"
    handler_class: "myapp.handlers.ConvertHandler"  # Optional: handlers can be omitted
    arguments:
      - name: "--input"
        required: true
        help: "Input file path"
      - name: "--output"
        required: true
        help: "Output file path"
      - name: "--format"
        choices: ["json", "yaml", "xml"]
        default: "json"
        help: "Output format"
      - name: "--pretty"
        action: "store_true"
        help: "Pretty-print the output"
```

### 2. Implement your command class

```python
# myapp/commands.py
from easycmdline.core.base import BaseCommand

class ConvertCommand(BaseCommand):
    """
    Command to convert files between different formats.
    """
    
    def __init__(self, args, handler=None):
        super().__init__(args, handler)
        # You can perform additional initialization here if needed
        
    def run(self):
        """Execute the command logic or delegate to the handler"""
        print(f"Convert command received:")
        print(f"  Input file: {self.args.input}")
        print(f"  Output file: {self.args.output}")
        print(f"  Format: {self.args.format}")
        print(f"  Pretty: {self.args.pretty}")
        
        # If a handler is provided, delegate the actual work to it
        if self.handler:
            return self.handler.run(self.args)
        else:
            # Implement your command logic directly here if no handler is used
            print("Performing conversion...")
            # Your conversion logic here
            print("Conversion complete!")
```

### 3. (Optional) Implement a handler class for separation of concerns

Handlers are optional but recommended for complex commands to separate command parsing from execution logic:

```python
# myapp/handlers.py
from easycmdline.core.base import BaseHandler

class ConvertHandler(BaseHandler):
    def __init__(self, args):
        super().__init__(args)
        self.input_file = args.input
        self.output_file = args.output
        self.output_format = args.format
        self.pretty = args.pretty
    
    def run(self, args):
        print(f"Converting {self.input_file} to {self.output_format}")
        print(f"Writing to {self.output_file}")
        print(f"Pretty print: {'enabled' if self.pretty else 'disabled'}")
        
        # Your actual conversion logic here
        # ...
```

### 4. Create a simple entry point script

```python
# mycli.py
#!/usr/bin/env python
from easycmdline.cli import run

if __name__ == "__main__":
    # Pass the path to your YAML config file
    run("my_config.yml")
```

That's it! You now have a full-featured CLI application with:
- Argument validation
- Help text generation
- Command structure
- Separation of concerns

Run your application:
```bash
python mycli.py convert --input data.csv --output result.json --pretty
```

## Handler-Free Usage

For simpler commands, you can omit the handler class entirely:

```yaml
commands:
  simple:
    description: "A simple command without a handler"
    command_class: "myapp.commands.SimpleCommand"
    arguments:
      - name: "--message"
        default: "Hello world"
        help: "Message to display"
```

Then implement all your logic directly in the command class:

```python
class SimpleCommand(BaseCommand):
    def run(self):
        print(f"Message: {self.args.message}")
        # All your command logic here
```

## Creating Complex Commands

You can create nested command structures using subcommands:

```yaml
commands:
  remote:
    description: "Manage remote repositories."
    subcommands:
      origin:
        description: "Manage origin remotes."
        subcommands:
          add:
            description: "Add an origin remote."
            command_class: "myapp.commands.OriginAddCommand"
            handler_class: "myapp.handlers.OriginAddHandler"
            arguments:
              - name: "--url"
                required: true
                help: "Remote URL."
```

To invoke subcommands:

```bash
python mycli.py remote origin add --url https://github.com/user/repo.git
```

## Programmatic Usage

You can also use pyeasycmdline programmatically in your own applications:

```python
from easycmdline.cli import EasyCmdLine

# Initialize with a configuration file
cli = EasyCmdLine("my_config.yml")

# Execute a command with arguments
result = cli.execute(["convert", "--input", "data.csv", "--output", "result.json"])
```

## Configuration

You can set the configuration file using an environment variable:

```bash
export EASYCMDLINE_CONFIG=/path/to/config.yml
python mycli.py convert --input data.csv --output result.json
```

Enable debug logging with:

```bash
export EASYCMDLINE_DEBUG=1
python mycli.py convert --input data.csv --output result.json
```

## Command-Specific Logging

You can configure logging levels for specific commands in your YAML configuration:

```yaml
logging:
  default_level: "WARNING"
  format: "%(asctime)s - %(name)s - %(levelname)s - [%(command_path)s] %(message)s"

commands:
  convert:
    description: "Convert files between formats"
    command_class: "myapp.commands.ConvertCommand"
    logging_level: "DEBUG"  # This command will log at DEBUG level
    # ...
```

## Development and Contribution

### Git Workflow and CI/CD

This project uses GitHub Actions with semantic-release for automated versioning and releases. For detailed information about our Git workflow, release process, and CI/CD pipeline, please refer to [GitHubActions.md](./GitHubActions.md).

Key features of our workflow:
- Automated semantic versioning based on commit messages
- Release candidate (RC) creation on release branches
- Production releases when merging to main
- Hotfix process for addressing bugs in production
- Proper branch management and protection

## License

MIT License
