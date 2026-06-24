# Database Audit Report

## Models
- User: Handles authentication and relationships to projects.
- Project: Core organizational unit. Relates to Targets, Scans, Reports, Assets.
- Target: The attack surface unit. Relates to Scans and PluginExecutions.
- Scan: Execution wrapper for a specific target. Relates to Findings.
- Finding: Individual vulnerability or observation.
- Asset: Discovered subdomains, IPs, etc.
- Report: Generated artifacts.
- PluginExecution: Raw plugin data.

## Relationships
- User 1:N Project
- Project 1:N Target, Scan, Report, Asset
- Target 1:N Scan, PluginExecution
- Scan 1:N Finding

## Indexes
- Indexes added to foreign keys: owner_id, project_id, 	arget_id, scan_id.
- Indexes added to lookups: username, email, 
ame, plugin_name, severity.

## Constraints
- Unique constraint on username and email.

## Migrations
- Alembic initialized successfully. lembic upgrade head handles schema generation safely.

## Repositories
- Standardized BaseRepository pattern implemented preventing ad-hoc session.query() calls across the codebase.
