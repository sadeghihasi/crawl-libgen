import os
from pathlib import Path

# DJANGO SETTINGS
DATABASE = {
    'NAME': 'p1',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': 'localhost',
    'PORT': '5432',
}

base_dir = Path(__file__).resolve().parent
MEDIA_ROOT = os.path.join(base_dir, "uploads")
