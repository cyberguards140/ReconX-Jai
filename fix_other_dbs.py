import os
import glob
import re

for root, _, files in os.walk('product/src/reconx'):
    for f in files:
        if f.endswith('.py'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r') as fp:
                content = fp.read()
            
            new_content = re.sub(
                r"os\.path\.join\(os\.path\.dirname\(os\.path\.dirname\(__file__\)\), 'workspace',",
                r"os.path.join(os.path.dirname(__file__), '..', '..', '..', 'workspace',",
                content
            )
            
            if new_content != content:
                with open(filepath, 'w') as fp:
                    fp.write(new_content)
                print(f"Fixed {filepath}")
