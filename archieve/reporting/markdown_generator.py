class MarkdownGenerator:
    @staticmethod
    def generate(data, output_path):
        content = f"""# {data['project_name']}
## {data['report_type']} Report

**Date:** {data['date']}

---

### Risk Overview
- **Critical:** {data['stats']['critical']}
- **High:** {data['stats']['high']}
- **Medium:** {data['stats']['medium']}
- **Low:** {data['stats']['low']}
- **Info:** {data['stats']['info']}

### Asset Statistics
- **Domains:** {data['stats']['domains']}
- **Cloud Exposures:** {data['stats']['cloud_exposures']}

---

### Key Findings
"""
        for f in data['findings']:
            content += f"- **[{f['severity']}]** {f['title']} ({f['asset']})\n"

        with open(output_path, 'w') as f:
            f.write(content)
        return output_path
