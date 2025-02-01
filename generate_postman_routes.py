import subprocess
import json
import re

def get_django_urls():
    result = subprocess.run(['python', 'manage.py', 'show_urls'], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Error running show_urls: {result.stderr.decode('utf-8')}")
    return result.stdout.decode('utf-8')

def parse_urls(show_urls_output):
    # Regex to split: URL, View, Name (if available)
    route_pattern = re.compile(r'^(\S+)\s+(\S+)(?:\s+(\S+))?$')
    
    routes = []
    for line in show_urls_output.splitlines():
        match = route_pattern.match(line.strip())
        if match:
            url = match.group(1)
            view = match.group(2)
            name = match.group(3) if match.group(3) else ""
            
            # Infer HTTP method from view/route name/url
            method = infer_http_method(view, name, url)
            
            # Exclude admin routes and empty URLs
            if "/admin/" not in url and url.strip():
                routes.append((method, url))
    
    return routes

def infer_http_method(view, name, url):
    view_lower = view.lower()
    name_lower = name.lower()
    url_lower = url.lower()
    
    if any(keyword in view_lower or keyword in name_lower or keyword in url_lower for keyword in ["get", "list", "retrieve", "detail"]):
        return "GET"
    elif any(keyword in view_lower or keyword in name_lower or keyword in url_lower for keyword in ["create", "add", "post"]):
        return "POST"
    elif any(keyword in view_lower or keyword in name_lower or keyword in url_lower for keyword in ["update", "edit", "put", "patch"]):
        return "PUT"
    elif any(keyword in view_lower or keyword in name_lower or keyword in url_lower for keyword in ["delete", "remove", "destroy"]):
        return "DELETE"
    else:
        return "GET"  # Default to GET if method can't be inferred

def generate_postman_collection(routes):
    collection = {
        "info": {
            "name": "Django API",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for method, url in routes:
        postman_request = {
            "name": f"{method} {url}",
            "request": {
                "method": method.upper(),
                "url": {
                    "raw": f"{{base_url}}{url}",
                    "host": ["{{base_url}}"],
                    "path": url.strip('/').split('/')
                },
                "header": [{
                    "key": "Content-Type",
                    "value": "application/json"
                }]
            }
        }
        collection['item'].append(postman_request)
    
    return collection

def save_postman_collection(collection, filename="postman_collection.json"):
    with open(filename, 'w') as f:
        json.dump(collection, f, indent=4)

if __name__ == "__main__":
    try:
        urls_output = get_django_urls()
        routes = parse_urls(urls_output)
        collection = generate_postman_collection(routes)
        save_postman_collection(collection)
        print(f"Postman collection generated successfully with {len(routes)} routes!")
    except Exception as e:
        print(f"Error: {e}")
