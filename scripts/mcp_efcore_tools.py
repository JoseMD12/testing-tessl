#!/usr/bin/env python3
import sys
import json
import subprocess
import os

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
            "serverInfo": {"name": "mcp-efcore-tools", "version": "1.0.0"}
        }
    })

def handle_tools_list(request_id):
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "ef_add_migration",
                    "description": "Creates a new EF Core database migration in the Infra project.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the migration to create."
                            }
                        },
                        "required": ["name"]
                    }
                },
                {
                    "name": "ef_database_update",
                    "description": "Applies EF Core migrations to the local database.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }
    })

def ef_add_migration(name):
    cmd = ["dotnet", "ef", "migrations", "add", name, "--project", "src/MachineReturn.Infra", "--startup-project", "src/MachineReturn.API"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

def ef_database_update():
    cmd = ["dotnet", "ef", "database", "update", "--project", "src/MachineReturn.Infra", "--startup-project", "src/MachineReturn.API"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

def handle_tools_call(request_id, name, arguments):
    if name == "ef_add_migration":
        name_arg = arguments.get("name")
        res = ef_add_migration(name_arg)
    elif name == "ef_database_update":
        res = ef_database_update()
    else:
        send_response({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {name}"}
        })
        return
        
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
        }
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
