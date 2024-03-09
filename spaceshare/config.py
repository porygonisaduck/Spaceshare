"""Spaceshare development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY_FIRST = b'\x89\xad\xf8\xd1\x9e\xe7}\xd7'
SECRET_KEY_LAST = b'#\x8ci\x14\xc5\xfcx"[z\xac\x14x\x87\x12\xc9'
SECRET_KEY = f"{SECRET_KEY_FIRST}{SECRET_KEY_LAST}"
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SPACESHARE_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SPACESHARE_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/spaceshare.sqlite3
DATABASE_FILENAME = SPACESHARE_ROOT/'var'/'spaceshare.sqlite3'
