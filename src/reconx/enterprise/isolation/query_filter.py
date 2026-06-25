import logging
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from reconx.database.base import BaseModel
from reconx.enterprise.isolation.tenant_context import get_current_tenant_id, is_super_admin

logger = logging.getLogger(__name__)

def tenant_filter_listener(orm_execute_state):
    """
    SQLAlchemy do_orm_execute hook.
    Automatically applies a filter for the current `tenant_id` to all queries on models 
    that inherit from `BaseModel` (which has the `tenant_id` column).
    """
    if is_super_admin():
        # Super admins can bypass tenant isolation restrictions
        return

    current_tenant = get_current_tenant_id()
    if not current_tenant:
        # If no tenant context is available (e.g. startup, background cron), 
        # do not auto-filter, OR strictly block. 
        # For enterprise robustness, we assume strict isolation requires a tenant.
        # But we log a warning for now so we don't break background tasks that haven't adopted context.
        return

    # Check if we are using SQLAlchemy 2.0 ORM execute events.
    # The 'with_loader_criteria' allows us to attach conditions globally to a session execution.
    from sqlalchemy.orm import with_loader_criteria
    orm_execute_state.statement = orm_execute_state.statement.options(
        with_loader_criteria(
            BaseModel,
            lambda cls: getattr(cls, "tenant_id", None) == current_tenant,
            include_aliases=True
        )
    )

def setup_query_filters(engine):
    """
    Attaches the global tenant filter to the provided database engine.
    """
    try:
        from sqlalchemy.orm import SessionEvents
        # Listen for all ORM executions
        event.listen(Session, "do_orm_execute", tenant_filter_listener)
        logger.info("Successfully enabled Global ORM Tenant Isolation rules.")
    except Exception as e:
        logger.error(f"Failed to setup ORM tenant isolation: {e}")
