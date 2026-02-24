import sys
from pathlib import Path

# Ensure the project root is on sys.path so `from api import ...` resolves
# regardless of the working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
