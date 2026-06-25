# ReconX Archive Manifest
*Generated during Repository Cleanup - Phase 21*

This manifest documents the exact relocation of 70+ directories into the safe `archive/` structure. **No files were permanently deleted.**

## 1. Experimental AI & Features (Moved to `archive/experimental/`)
**Reason:** These 52 directories represented highly conceptual, prototype, or abandoned ideas regarding AI swarms, cognitive modeling, and enterprise grid operations. They were not integrated into the core spine.
- `ai`, `analyst_tools`, `automation`, `autonomy`, `behavioral`, `cognition`, `collaboration`, `coordination`, `digital_twin`, `distributed`, `distributed_cognition`, `enterprise_ops`, `evolution`, `federation`, `global_ops`, `governance`, `grid`, `guided_ops`, `hyperscale`, `integrations`, `intelligence`, `intelligence_exchange`, `knowledge`, `knowledge_evolution`, `knowledge_management`, `learning`, `learning_engine`, `lifecycle`, `marketplace`, `mesh_intelligence`, `missions`, `monitoring`, `observability`, `operations`, `optimization`, `pccc`, `performance`, `policies`, `predictive`, `profiles`, `recovery`, `research`, `research_ai`, `resilience`, `runtimes`, `sdk`, `security`, `simulation`, `strategic`, `swarm`, `threat_intelligence`, `upgrade`

## 2. Duplicate & Merged Modules (Moved to `archive/duplicate_modules/`)
**Reason:** These directories were refactored and absorbed into the `core/` directory or unified under `plugins/` during the enterprise architecture phase.
- `adapters` (Merged into `plugins/`)
- `configs` (Merged into `config.yaml` and `core/config.py`)
- `console` (Replaced by `reconx.py` CLI)
- `correlation` (Merged into `core/correlation_engine.py`)
- `dashboards` (Duplicate of `dashboard/`)
- `events` (Merged into `core/events.py`)
- `execution` (Merged into `core/execution_manager.py`)
- `logging` (Merged into `core/logger.py`)
- `normalization` (Handled by correlation engine)
- `orchestration` (Merged into `core/orchestrator.py`)
- `reporting` (Merged into `core/report_generator.py`)
- `security_hardening` (Not implemented)
- `storage` (Merged into `core/database.py` and `core/result_store.py`)
- `testing` (Replaced by standard `tests/` folder)
- `ui` (Duplicate of `dashboard/`)
- `workspaces` (Handled by SQLite `projects/` architecture)

## 3. Legacy Documentation (Moved to `archive/legacy_docs/`)
**Reason:** Outdated schemas, draft texts, and old setup files replaced by the `docs/` suite.
- `audit`
- `dependency_maps`
- `release`
- `schemas`
- `templates`
- `reconx setup.txt`

## 4. Migration Artifacts (Moved to `archive/migration_artifacts/`)
**Reason:** Temporary files used during workflow conversions and deployments.
- `deployment` (Replaced by `scripts/install.sh`)
- `golden_workflow.yaml` (Replaced by `workflows/basic.yaml`, `medium.yaml`, `deep.yaml`)
- `wf_crash.yaml` (Test artifact)
- `wf_hang.yaml` (Test artifact)

## 5. Unnecessary Files (Moved to `archive/unnecessary/`)
**Reason:** Empty or arbitrary scratch folders.
- `allfiles`
- `files`
- `files (1)`
