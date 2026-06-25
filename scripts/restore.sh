#!/bin/bash
set -e

# ReconX Restore Script
BACKUP_DIR=${1:-"./backups"}
TIMESTAMP=$2

if [ -z "$TIMESTAMP" ]; then
    echo "Usage: $0 <backup_dir> <timestamp>"
    echo "Example: $0 ./backups 20260617_120000"
    exit 1
fi

echo "Restoring ReconX from $BACKUP_DIR for timestamp $TIMESTAMP..."

if [ -f "$BACKUP_DIR/reconx_$TIMESTAMP.database" ]; then
    cp "$BACKUP_DIR/reconx_$TIMESTAMP.database" reconx.database
    echo "Restored SQLite database."
fi

if [ -f "$BACKUP_DIR/workflows_$TIMESTAMP.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/workflows_$TIMESTAMP.tar.gz"
    echo "Restored workflows."
fi

if [ -f "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz"
    echo "Restored configurations."
fi

echo "Restore completed successfully!"
