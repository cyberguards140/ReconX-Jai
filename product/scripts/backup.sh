#!/bin/bash
set -e

# ReconX Backup Script
BACKUP_DIR=${1:-"./backups"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "$BACKUP_DIR"

echo "Starting ReconX backup to $BACKUP_DIR..."

# Backup SQLite Database if running locally
if [ -f "reconx.database" ]; then
    echo "Backing up SQLite database..."
    cp reconx.database "$BACKUP_DIR/reconx_$TIMESTAMP.database"
fi

# Backup workflows
if [ -d "src/reconx/workflows" ]; then
    echo "Backing up workflows..."
    tar -czf "$BACKUP_DIR/workflows_$TIMESTAMP.tar.gz" src/reconx/workflows/
fi

# Backup configuration
if [ -d "config" ]; then
    echo "Backing up configurations..."
    tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" config/
fi

echo "Backup completed successfully!"
