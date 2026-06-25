import os
import subprocess

# Things to keep in root
product_items = {
    '.git', '.github', '.gitignore', '.dockerignore', '.env', '.env.example',
    'Dockerfile', 'docker-compose.yml', 'requirements.txt',
    'pyproject.toml', 'pytest.ini', 'mypy.ini', 'ruff.toml', 'alembic.ini',
    'README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
    'SECURITY.md', 'MAINTAINERS.md', 'ROADMAP.md', 'USAGE.md', 'ARCHIVE_MANIFEST.md', 'VERSION',
    'src', 'tests', 'docs', 'config', 'scripts', 'reconx-env.sh',
    'archive', 'archives', 'plugins', 'requirements', 'move_to_archieve.py',
    'mkdocs.yml', 'migrations'
}

archieve_dir = 'archieve'
os.makedirs(archieve_dir, exist_ok=True)

# List all items in the root directory
all_items = os.listdir('.')
for item in all_items:
    if item in product_items or item == archieve_dir:
        continue

    # Move the item
    print(f"Moving {item} to {archieve_dir}...")
    
    # Check if tracked by git
    res = subprocess.run(['git', 'ls-files', '--error-unmatch', item], capture_output=True)
    if res.returncode == 0:
        # It's tracked, use git mv
        subprocess.run(['git', 'mv', item, archieve_dir + '/'])
    else:
        # Not tracked, use mv
        subprocess.run(['mv', item, archieve_dir + '/'])

# Also stage the new archieve_dir
subprocess.run(['git', 'add', archieve_dir])
print("Move complete.")
