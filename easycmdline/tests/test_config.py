import pytest
from easycmdline.core.config import load_config


def test_load_config(tmp_path):
    """Test loading configuration from a YAML file"""
    config_content = """
    logging:
      default_level: "INFO"
    commands:
      greet:
        command_class: "commands.GreetCommand"
        handler_class: "handlers.GreetHandler"
        description: "Greet a user by name."
        arguments:
          - name: "--name"
            default: "World"
            help: "Name to greet."
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = load_config(str(config_file))

    assert "commands" in config
    assert "greet" in config["commands"]
    assert config["commands"]["greet"]["command_class"] == "commands.GreetCommand"
    assert config["commands"]["greet"]["handler_class"] == "handlers.GreetHandler"
    assert "logging" in config
    assert config["logging"]["default_level"] == "INFO"


def test_load_config_with_subcommands(tmp_path):
    """Test loading configuration with subcommands"""
    config_content = """
    commands:
      remote:
        description: "Manage remote repositories."
        subcommands:
          origin:
            description: "Manage origin remotes."
            subcommands:
              add:
                description: "Add an origin remote."
                command_class: "commands.OriginAddCommand"
                handler_class: "handlers.OriginAddHandler"
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = load_config(str(config_file))

    assert "commands" in config
    assert "remote" in config["commands"]
    assert "subcommands" in config["commands"]["remote"]
    assert "origin" in config["commands"]["remote"]["subcommands"]
    assert "add" in config["commands"]["remote"]["subcommands"]["origin"]["subcommands"]
    assert (
        config["commands"]["remote"]["subcommands"]["origin"]["subcommands"]["add"][
            "command_class"
        ]
        == "commands.OriginAddCommand"
    )


def test_load_config_file_not_found():
    """Test that loading a non-existent config file raises an error"""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_file.yaml")
