#!/usr/bin/env python
import sys, os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from django.core.management import execute_manager

try:
    import littlepony.settings as settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't import littlepony.settings. Are you running manage.py from one directory higher than littlepony, or are there any syntax errors?'")
    sys.exit(1)

if __name__ == "__main__":
    import os
    execute_manager(settings)
    