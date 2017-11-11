""""
FILE: Manage.py
DESCRIPTION: Used to start and stop the application
"""

import os, sys

# Creates a pointer to the project/parent folder
# Tells python where to start and find other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from web import app
from web import timechange

manager = Manager(app)

# Starts the server with the following settings
manager.add_command("runserver", Server(
    use_debugger = True,
    # Automatically reloads code
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000))
    )
)

# This runs the manager which runs the app
if __name__ == "__main__":
    manager.run()
