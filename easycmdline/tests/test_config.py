import pytest
from easycmdline.core.config import load_config


def test_load_config(tmp_path):
    config_content = """
commands:
  greet:
    command_class: "commands.GreetCommand"
    handler_class: "handlers.GreetHandler"
    description: "Greet a user."
    arguments:
      - name: "--name"
        default: "World"
        help: "Name of the user."
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = load_config(str(config_file))
    assert "greet" in config["commands"]
    assert config["commands"]["greet"]["command_class"] == "commands.GreetCommand"
