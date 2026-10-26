#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from microface import microface
from m1cr0face.settings import ALLOWED_MAC_ADDRESSES,ALLOWED_HOSTS

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm1cr0face.settings')
    try:
        from django.core.management import execute_from_command_line
        face_result = microface.fetchFaceModel() #fetch all face-model after deploying 
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
