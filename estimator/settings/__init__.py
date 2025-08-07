import os
import environ

# Setup base environment
env = environ.Env()
environ.Env.read_env()

# Default to dev if ENVIRONMENT is not set
ENVIRONMENT = env('ENVIRONMENT', default='dev')

if ENVIRONMENT == 'prod':
    from .prod import *
else:
    from .dev import *
