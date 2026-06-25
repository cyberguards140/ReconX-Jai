from reconx.database.models import PluginExecution
from reconx.database.repositories.base import BaseRepository


class PluginExecutionRepository(BaseRepository[PluginExecution]):
    pass


plugin_execution_repo = PluginExecutionRepository(PluginExecution)
