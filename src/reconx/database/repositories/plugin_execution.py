from reconx.database.repositories.base import BaseRepository
from reconx.database.models import PluginExecution

class PluginExecutionRepository(BaseRepository[PluginExecution]):
    pass

plugin_execution_repo = PluginExecutionRepository(PluginExecution)
