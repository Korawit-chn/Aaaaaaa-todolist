"""Pytest configuration file."""

import sys
from pathlib import Path

# Add the workspace root to the path so imports work correctly
workspace_root = Path(__file__).parent
sys.path.insert(0, str(workspace_root))
