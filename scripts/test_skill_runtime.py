"""Include the portable skill runtime's boundary cases in package CI."""
from pathlib import Path


def load_tests(loader, standard_tests, pattern):
    package = Path(__file__).resolve().parents[1] / 'assets/blueprint/00_System/Skills/skill-maintenance/scripts'
    return loader.discover(str(package), pattern='test_runtime.py', top_level_dir=str(package))
