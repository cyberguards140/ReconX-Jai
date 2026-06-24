import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

def validate_registry(loader):
    logging.info("Validating registry...")
    tool_ids = set()
    category_ids = {c['id'] for c in loader.categories}
    
    for tool in loader.tools:
        tid = tool.get('id')
        if not tid:
            logging.error("Found tool with missing ID")
            continue
            
        if tid in tool_ids:
            logging.error(f"Duplicate tool ID found: {tid}")
        tool_ids.add(tid)
        
        if tool.get('category') not in category_ids:
            logging.error(f"Invalid category for tool {tid}: {tool.get('category')}")
            
        if not tool.get('binary'):
            logging.error(f"Missing binary for tool {tid}")
            
    # Check metadata
    metadata_ids = {m['id'] for m in loader.metadata}
    for tid in tool_ids:
        if tid not in metadata_ids:
            logging.error(f"Missing metadata for tool {tid}")
            
    logging.info("Validation complete.")
