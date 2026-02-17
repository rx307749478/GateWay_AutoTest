"""
Configuration loading module for GateWay AutoTest framework.
Supports YAML configuration files with environment variable overrides.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


class Config:
    """Configuration manager for the test framework."""

    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls) -> 'Config':
        """Singleton pattern to ensure single configuration instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """Load configuration from YAML files and environment variables."""
        # Load .env file if exists
        load_dotenv()

        # Get config directory
        config_dir = Path(__file__).parent

        # Load device configuration
        devices_file = config_dir / 'devices.yaml'
        if devices_file.exists():
            with open(devices_file, 'r', encoding='utf-8') as f:
                self._config['devices'] = yaml.safe_load(f) or {}
        else:
            self._config['devices'] = {}

        # Load test cases configuration
        test_cases_file = config_dir / 'test_cases.yaml'
        if test_cases_file.exists():
            with open(test_cases_file, 'r', encoding='utf-8') as f:
                self._config['test_cases'] = yaml.safe_load(f) or {}
        else:
            self._config['test_cases'] = {}

        # Override with environment variables
        self._load_env_overrides()

    def _load_env_overrides(self) -> None:
        """Load configuration overrides from environment variables."""
        # Device overrides
        if os.getenv('DEVICE_HOST'):
            if 'default' not in self._config['devices']:
                self._config['devices']['default'] = {}
            self._config['devices']['default']['host'] = os.getenv('DEVICE_HOST')

        if os.getenv('DEVICE_PORT'):
            if 'default' not in self._config['devices']:
                self._config['devices']['default'] = {}
            self._config['devices']['default']['port'] = int(os.getenv('DEVICE_PORT', 22))

        if os.getenv('DEVICE_USER'):
            if 'default' not in self._config['devices']:
                self._config['devices']['default'] = {}
            self._config['devices']['default']['username'] = os.getenv('DEVICE_USER')

        if os.getenv('DEVICE_PASSWORD'):
            if 'default' not in self._config['devices']:
                self._config['devices']['default'] = {}
            self._config['devices']['default']['password'] = os.getenv('DEVICE_PASSWORD')

        # Web UI overrides
        if os.getenv('WEB_URL'):
            if 'web' not in self._config['devices']:
                self._config['devices']['web'] = {}
            self._config['devices']['web']['url'] = os.getenv('WEB_URL')

    @property
    def devices(self) -> Dict[str, Any]:
        """Get device configurations."""
        return self._config.get('devices', {})

    @property
    def test_cases(self) -> Dict[str, Any]:
        """Get test case configurations."""
        return self._config.get('test_cases', {})

    def get_device(self, device_name: str = 'default') -> Dict[str, Any]:
        """
        Get configuration for a specific device.

        Args:
            device_name: Name of the device configuration

        Returns:
            Device configuration dictionary
        """
        return self._config.get('devices', {}).get(device_name, {})

    def get_test_case(self, test_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific test case.

        Args:
            test_name: Name of the test case

        Returns:
            Test case configuration dictionary
        """
        return self._config.get('test_cases', {}).get(test_name, {})

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def reload(self) -> None:
        """Reload configuration from files."""
        self._config = {}
        self._load_config()


def get_config() -> Config:
    """
    Get the singleton Config instance.

    Returns:
        Config instance
    """
    return Config()
