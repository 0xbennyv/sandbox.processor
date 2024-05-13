import json

def build_process_tree(processes):
    tree = {}
    for proc in processes:
        tree[proc['process_id']] = {
            'name': proc['name'],
            'process_id': proc['process_id'],
            'path': proc['path'],
            'hash': proc['hash'],
            'children': []
        }
    for proc in processes:
        parent_id = proc['parent_process_id']
        if parent_id in tree:
            tree[parent_id]['children'].append(tree[proc['process_id']])
    return tree

def render_html_tree(node):
    if not node['children']:
        return f"<li>{node['name']} ({node['process_id']}) - {node['path']} {node['hash']}</li>"
    else:
        children_html = "".join(render_html_tree(child) for child in node['children'])
        return f"<li>{node['name']} ({node['process_id']}) - {node['path']} {node['hash']}<ul>{children_html}</ul></li>"

def main():
    with open('process_log.json', 'r') as file:
        data = json.load(file)
        
    # Identify root processes (those without a parent in the list)
    process_ids = {proc['process_id'] for proc in data}
    root_processes = [proc for proc in data if proc['parent_process_id'] not in process_ids]
    
    # Build the process tree starting from the roots
    full_tree = [build_process_tree(data)[proc['process_id']] for proc in root_processes]
    
    # Render the full tree in HTML
    html_content = "<ul>" + "".join(render_html_tree(node) for node in full_tree) + "</ul>"
    
    # Output to HTML file
    with open('process_tree.html', 'w') as html_file:
        html_file.write(html_content)
    print("HTML file created successfully!")

if __name__ == "__main__":
    main()
