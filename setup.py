#!/usr/bin/env python3
"""
Setup script for APS Normative Graph System.

This script helps with the initial setup and configuration of the system.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text)
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ is required. You have {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_directories():
    """Create necessary directories."""
    print("Creating directories...")
    directories = [
        'data/processed',
        'data/schemas',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    
    return True


def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True,
            capture_output=True
        )
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def initialize_database():
    """Initialize the database with tables."""
    print("Initializing database...")
    try:
        from src.models import init_database
        db_path = 'data/normas_aps.db'
        engine, Session = init_database(db_path)
        print(f"✓ Database initialized at {db_path}")
        print(f"  Tables: {', '.join(engine.table_names())}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False


def validate_configuration():
    """Validate configuration files."""
    print("Validating configuration...")
    
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✓ config.yaml is valid")
        
        import json
        with open('data/schemas/norm_schema.json', 'r') as f:
            schema = json.load(f)
        print("✓ norm_schema.json is valid")
        
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


def create_sample_data():
    """Create sample data for demonstration."""
    print("Creating sample data...")
    try:
        # Run the example script to create sample database
        result = subprocess.run(
            [sys.executable, 'examples/usage_example.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Sample data created successfully")
            return True
        else:
            print("⚠ Sample data creation skipped (dependencies may be needed)")
            return True
    except Exception as e:
        print(f"⚠ Could not create sample data: {e}")
        return True  # Not critical


def print_next_steps():
    """Print next steps for the user."""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print()
    print("1. Run data collection:")
    print("   python main.py")
    print()
    print("2. Start the web portal:")
    print("   python -m src.portal.app")
    print("   Then open: http://localhost:5000")
    print()
    print("3. Run example script:")
    print("   python examples/usage_example.py")
    print()
    print("4. Explore the data:")
    print("   sqlite3 data/normas_aps.db")
    print()
    print("5. Read the documentation:")
    print("   - README.md (overview)")
    print("   - docs/quick_start.md (getting started)")
    print("   - docs/developer_guide.md (API reference)")
    print()


def main():
    """Run the setup process."""
    print_header("APS Normative Graph System - Setup")
    
    steps = [
        ("Check Python version", check_python_version),
        ("Create directories", create_directories),
        ("Install dependencies", install_dependencies),
        ("Validate configuration", validate_configuration),
        ("Initialize database", initialize_database),
        ("Create sample data", create_sample_data),
    ]
    
    for step_name, step_func in steps:
        print_header(step_name)
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please resolve the issue and run setup again.")
            return 1
    
    print_next_steps()
    return 0


if __name__ == '__main__':
    sys.exit(main())
