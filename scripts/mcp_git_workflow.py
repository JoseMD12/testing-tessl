#!/usr/bin/env python3
import sys
import json
import subprocess
import re
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
            "serverInfo": {"name": "mcp-git-workflow", "version": "1.0.0"}
        }
    })

def handle_tools_list(request_id):
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "git_create_branch",
                    "description": "Validates and creates a git branch from develop following the strict naming policy.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "opType": {
                                "type": "string",
                                "enum": ["feat", "fix", "refac", "doc", "test", "chore"],
                                "description": "The operation prefix type."
                            },
                            "ticketId": {
                                "type": "string",
                                "description": "The ticket/issue identifier (e.g. MR-123)."
                            },
                            "description": {
                                "type": "string",
                                "description": "A brief description of the branch scope."
                            }
                        },
                        "required": ["opType", "ticketId", "description"]
                    }
                },
                {
                    "name": "git_commit_changes",
                    "description": "Enforces git hygiene rules and commits modifications.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Commit message (e.g. feat: create return request)."
                            }
                        },
                        "required": ["message"]
                    }
                }
            ]
        }
    })

def git_create_branch(op_type, ticket_id, description):
    ticket_id = ticket_id.upper().strip()
    if not re.match(r"^[A-Z0-9\-]+$", ticket_id):
        return {"success": False, "error": f"Invalid ticket ID format: {ticket_id}"}
        
    clean_desc = re.sub(r"[^a-zA-Z0-9]+", "-", description).lower().strip("-")
    branch_name = f"{op_type}/{ticket_id}-{clean_desc}"
    
    try:
        subprocess.run(["git", "checkout", "develop"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORKSPACE_ROOT)
        subprocess.run(["git", "pull", "origin", "develop"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORKSPACE_ROOT)
        res = subprocess.run(["git", "checkout", "-b", branch_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
        return {
            "success": True,
            "branchName": branch_name,
            "stdout": res.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Git command failed: {e.stderr.decode('utf-8', errors='ignore').strip()}"
        }

def git_commit_changes(message):
    try:
        status_res = subprocess.run(["git", "status", "--porcelain"], check=True, stdout=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
        status_lines = status_res.stdout.splitlines()
        
        forbidden_patterns = ["bin/", "obj/", ".vs/", "tasks/.active"]
        forbidden_found = []
        
        for line in status_lines:
            file_path = line[3:].strip()
            for pattern in forbidden_patterns:
                if pattern in file_path or file_path.startswith(pattern):
                    forbidden_found.append(file_path)
                    
        if forbidden_found:
            return {
                "success": False,
                "error": f"Commit blocked due to Git Hygiene violations. The following files/directories should not be versioned: {', '.join(forbidden_found)}. Please check gitignore."
            }
            
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORKSPACE_ROOT)
        res = subprocess.run(["git", "commit", "-m", message], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
        return {
            "success": True,
            "stdout": res.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Git commit failed: {e.stderr.decode('utf-8', errors='ignore').strip()}"
        }

def handle_tools_call(request_id, name, arguments):
    if name == "git_create_branch":
        op_type = arguments.get("opType")
        ticket_id = arguments.get("ticketId")
        description = arguments.get("description")
        res = git_create_branch(op_type, ticket_id, description)
    elif name == "git_commit_changes":
        msg = arguments.get("message")
        res = git_commit_changes(msg)
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
