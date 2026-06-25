from core.tool_registry import ToolRegistry

class ArgumentEngine:
    @staticmethod
    def generate_command(tool_id, target, config_dict):
        tool = ToolRegistry.get_tool(tool_id)
        if not tool:
            return ""
            
        cmd = [tool['binary']]
        
        args = ToolRegistry.get_tool_arguments(tool_id)
        for arg in args:
            flag = arg['flag']
            arg_type = arg['type']
            
            val = config_dict.get(flag)
            if val is None:
                continue
                
            if arg_type == "toggle":
                if str(val).lower() == 'true':
                    cmd.append(flag)
            else:
                if str(val).strip() != "":
                    # If flag contains '=' like '--script=', format differently if needed.
                    # For now, separate by space
                    cmd.append(flag)
                    cmd.append(str(val))
                    
        if target and target.strip() != "":
            cmd.append(target.strip())
            
        return " ".join(cmd)
