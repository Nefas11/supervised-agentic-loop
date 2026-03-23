"""Load SAL environment configuration from .env.sal"""
import os
from pathlib import Path

def load_sal_env():
    """Load .env.sal configuration file if it exists."""
    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env.sal"
    
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    os.environ[key] = val
        
        # Create log directories
        for key in ['MONITOR_STATE_DIR', 'SAL_LEARNINGS_DIR']:
            if key in os.environ:
                Path(os.environ[key]).mkdir(parents=True, exist_ok=True)

# Auto-load when imported
load_sal_env()
