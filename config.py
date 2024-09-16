import json

class Config:
    _config_data = {}
    _config_file_path = "config.json"

    @classmethod
    def load_config(cls, file_path=_config_file_path):
        """Load the configuration from a JSON file."""
        with open(file_path, "r") as f:
            cls._config_data = json.load(f)

    @classmethod
    def get(cls, key, parent=None):
        """Get a configuration value."""
        if parent != None:
            return cls._config_data[parent][key]
        else:
            return cls._config_data[key]
    
    @classmethod
    def set(cls, key, value, parent=None):
        """Set a configuration value"""
        if parent != None:
            cls._config_data[parent][key] = value
        else:
            cls._config_data[key] = value
        cls._save_config(cls)

    def _save_config(cls):
        """Persist the current configuration to the JSON file"""
        with open(cls._config_file_path, "w") as f:
            json.dump(cls._config_data, f, indent=2)
        print(f"Configuration saved to {cls._config_file_path}")
        cls.reload()

    @classmethod
    def reload(cls, file_path=_config_file_path):
        """Reload the configuration from the file."""
        cls.load_config(file_path)
        print(f"Configuration reloaded from {file_path}")

# Initial loading of configuration
Config.load_config()