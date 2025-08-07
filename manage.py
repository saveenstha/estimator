#!/usr/bin/env python
import os
import sys
import environ


def main():
    """Run administrative tasks."""
    # Load environment from .env
    env = environ.Env()
    environ.Env.read_env()

    # Get ENVIRONMENT value from .env (default to 'dev')
    environment = env('ENVIRONMENT', default='dev')

    # Set correct settings module dynamically
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'estimator.settings.{environment}')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
