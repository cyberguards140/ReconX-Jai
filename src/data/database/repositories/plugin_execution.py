from data.database.models import PluginExecution
from data.database.repositories.base import BaseRepository


class PluginExecutionRepository(BaseRepository[PluginExecution]):
    pass


plugin_execution_repo = PluginExecutionRepository(PluginExecution)
