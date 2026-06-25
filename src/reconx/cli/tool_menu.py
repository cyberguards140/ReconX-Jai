import questionary
from cli.ui import console
from core.tool_registry import ToolRegistry

def manage_tools():
    while True:
        console.clear()
        console.print("[bold cyan]Tool Manager[/bold cyan]\n")
        
        tools = ToolRegistry.get_tools()
        if not tools:
            console.print("[-] No tools found in registry.", style="red")
            questionary.press_any_key_to_continue("Press any key to return...").ask()
            return
            
        console.print("Installed Tools\n")
        for t in tools:
            mark = "[✓]" if t['status'] == "installed" else "[✗]"
            color = "green" if t['status'] == "installed" else "red"
            console.print(f"[{color}]{mark} {t['name']}[/{color}]")
        
        console.print("\n═══════════════════════════════════════\n", style="dim")
        
        choice = questionary.select(
            "Select an action:",
            choices=[
                questionary.Choice(title="[1] View Details", value="1"),
                questionary.Choice(title="[2] Enable Tool", value="2"),
                questionary.Choice(title="[3] Disable Tool", value="3"),
                questionary.Choice(title="[4] Back", value="4"),
            ],
            qmark="?"
        ).ask()
        
        if choice == "1":
            _view_details(tools)
        elif choice == "2":
            _set_tool_state(tools, True)
        elif choice == "3":
            _set_tool_state(tools, False)
        elif choice == "4":
            break

def _select_tool(tools, action_msg):
    choices = [questionary.Choice(title=t['name'], value=t['id']) for t in tools]
    choices.append(questionary.Choice(title="Cancel", value=None))
    return questionary.select(action_msg, choices=choices).ask()

def _view_details(tools):
    tool_id = _select_tool(tools, "Select tool to view details:")
    if not tool_id: return
    
    details = ToolRegistry.get_tool(tool_id)
    if details:
        console.print(f"\n[bold yellow]Tool:[/bold yellow] {details['name']}")
        console.print(f"[bold yellow]Category:[/bold yellow] {details['category']}")
        console.print(f"[bold yellow]Status:[/bold yellow] {'Enabled' if details['enabled'] else 'Disabled'}")
        console.print(f"[bold yellow]Binary:[/bold yellow] {details['binary']}")
        
        if details.get('arguments'):
            console.print("\n[bold yellow]Arguments:[/bold yellow]")
            for arg in details['arguments']:
                console.print(f"  {arg['flag']} ({arg['type']})")
                
        if details.get('dependencies'):
            console.print("\n[bold yellow]Dependencies:[/bold yellow]")
            for dep in details['dependencies']:
                console.print(f"  {dep['name']} ({dep['type']})")
    else:
        console.print("[-] Could not retrieve details.", style="red")
        
    questionary.press_any_key_to_continue("\nPress any key to continue...").ask()

def _set_tool_state(tools, state):
    action = "Enable" if state else "Disable"
    tool_id = _select_tool(tools, f"Select tool to {action}:")
    if not tool_id: return
    
    ToolRegistry.set_tool_status(tool_id, state)
    console.print(f"[+] Tool {action}d successfully.", style="green")
    questionary.press_any_key_to_continue("Press any key to continue...").ask()
