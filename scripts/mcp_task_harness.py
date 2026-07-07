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
            "serverInfo": {"name": "mcp-task-harness", "version": "1.0.0"}
        }
    })

def handle_tools_list(request_id):
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "harness_init_task",
                    "description": "Initializes a new task in the harness.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task to initialize."
                            }
                        },
                        "required": ["title"]
                    }
                },
                {
                    "name": "harness_get_status",
                    "description": "Queries the active task status and returns it as structured JSON.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "harness_approve_phase",
                    "description": "Approves and advances the current phase in the active task.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }
    })

def harness_init_task(title):
    cmd = ["bash", "scripts/task.sh", "init", title]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

def harness_get_status():
    cmd = ["bash", "scripts/task.sh", "status"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
        
    stdout = result.stdout
    
    # Parse status fields
    task_match = re.search(r"Active Task:\s*(.*)", stdout)
    file_match = re.search(r"File:\s*(.*)", stdout)
    phase_match = re.search(r"Phase:\s*(.*)", stdout)
    status_match = re.search(r"Status:\s*(.*)", stdout)
    
    research_approved = "[x]" in re.search(r"(\[.\].*Step 1: Research)", stdout).group(0) if re.search(r"(\[.\].*Step 1: Research)", stdout) else False
    plan_approved = "[x]" in re.search(r"(\[.\].*Step 2: Plan)", stdout).group(0) if re.search(r"(\[.\].*Step 2: Plan)", stdout) else False
    implement_approved = "[x]" in re.search(r"(\[.\].*Step 3: Implement)", stdout).group(0) if re.search(r"(\[.\].*Step 3: Implement)", stdout) else False
    
    return {
        "task": task_match.group(1).strip() if task_match else "Unknown",
        "file": file_match.group(1).strip() if file_match else "Unknown",
        "phase": phase_match.group(1).strip() if phase_match else "Unknown",
        "status": status_match.group(1).strip() if status_match else "Unknown",
        "checklist": {
            "researchApproved": research_approved,
            "planApproved": plan_approved,
            "implementApproved": implement_approved
        }
    }

def harness_approve_phase():
    cmd = ["bash", "scripts/task.sh", "approve"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

def handle_tools_call(request_id, name, arguments):
    if name == "harness_init_task":
        title = arguments.get("title")
        res = harness_init_task(title)
    elif name == "harness_get_status":
        res = harness_get_status()
    elif name == "harness_approve_phase":
        res = harness_approve_phase()
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
