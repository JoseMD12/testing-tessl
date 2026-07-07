#!/usr/bin/env python3
import sys
import json
import os
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def send_response(response):
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def handle_initialize(request_id):
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mcp-sdd-validator", "version": "1.0.0"}
        }
    })

def handle_tools_list(request_id):
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "validate_sdd_spec",
                    "description": "Validates if an SDD spec Markdown file satisfies the frontmatter and BDD scenario guidelines.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "specPath": {
                                "type": "string",
                                "description": "Path to the spec markdown file (relative to workspace or absolute)."
                            }
                        },
                        "required": ["specPath"]
                    }
                }
            ]
        }
    })

def validate_sdd_spec(spec_path):
    if not os.path.isabs(spec_path):
        spec_path = os.path.join(WORKSPACE_ROOT, spec_path)
        
    if not os.path.exists(spec_path):
        return {"valid": False, "errors": [f"Spec file does not exist at path: {spec_path}"]}
        
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"valid": False, "errors": [f"Failed to read file: {str(e)}"]}
        
    errors = []
    metadata = {}
    
    # 1. Check YAML frontmatter
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not fm_match:
        errors.append("Missing or invalid YAML frontmatter (needs starting/ending '---').")
    else:
        fm_text = fm_match.group(1)
        required_keys = ["id", "feature", "pod", "priority", "iteration"]
        for line in fm_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                metadata[k.strip()] = v.strip()
        
        for rk in required_keys:
            if rk not in metadata:
                errors.append(f"Frontmatter is missing required key: '{rk}'.")
                
    # 2. Check BDD scenarios syntax
    bdd_patterns = [
        r"\bDado\b", r"\bQuando\b", r"\bEntão\b",
        r"\bGiven\b", r"\bWhen\b", r"\bThen\b"
    ]
    bdd_found = False
    for pat in bdd_patterns:
        if re.search(pat, content, re.IGNORECASE):
            bdd_found = True
            break
            
    if not bdd_found:
        errors.append("Spec does not seem to contain BDD scenarios (needs Given/When/Then or Dado/Quando/Então syntax).")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "metadata": metadata
    }

def handle_tools_call(request_id, name, arguments):
    if name == "validate_sdd_spec":
        spec_path = arguments.get("specPath")
        res = validate_sdd_spec(spec_path)
        send_response({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        })
    else:
        send_response({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {name}"}
        })

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            request = json.loads(line)
            req_id = request.get("id")
            method = request.get("method")
            
            if method == "initialize":
                handle_initialize(req_id)
            elif method == "notifications/initialized":
                pass
            elif method == "tools/list":
                handle_tools_list(req_id)
            elif method == "tools/call":
                params = request.get("params", {})
                name = params.get("name")
                arguments = params.get("arguments", {})
                handle_tools_call(req_id, name, arguments)
        except Exception as e:
            sys.stderr.write(f"Error in MCP main loop: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
