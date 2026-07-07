#!/usr/bin/env python3
import sys
import json
import subprocess
import os
import xml.etree.ElementTree as ET
import shutil
import uuid

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
            "serverInfo": {"name": "mcp-dotnet-tests", "version": "1.0.0"}
        }
    })

def handle_tools_list(request_id):
    send_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "run_dotnet_tests",
                    "description": "Runs dotnet tests on the solution/project and returns a token-efficient JSON summary of failures.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "projectPath": {
                                "type": "string",
                                "description": "Absolute or relative path to the solution or test project."
                            },
                            "filter": {
                                "type": "string",
                                "description": "Optional dotnet test filter expression."
                            }
                        },
                        "required": ["projectPath"]
                    }
                }
            ]
        }
    })

def run_dotnet_tests(project_path, test_filter=None):
    if not os.path.isabs(project_path):
        project_path = os.path.join(WORKSPACE_ROOT, project_path)

    run_id = str(uuid.uuid4())[:8]
    results_dir = os.path.join(WORKSPACE_ROOT, f"TestResults_{run_id}")
    
    cmd = ["dotnet", "test", project_path, "--logger", f"trx;LogFileName={run_id}.trx", "--results-directory", results_dir]
    if test_filter:
        cmd.extend(["--filter", test_filter])
        
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=WORKSPACE_ROOT)
    except Exception as e:
        return {"error": f"Failed to execute dotnet test: {str(e)}"}
        
    trx_file = os.path.join(results_dir, f"{run_id}.trx")
    if not os.path.exists(trx_file):
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)
        return {
            "error": "No test results file (.trx) was generated. The build might have failed.",
            "stdout": result.stdout[:2000],
            "stderr": result.stderr[:2000]
        }
        
    try:
        tree = ET.parse(trx_file)
        root = tree.getroot()
        ns = {"t": "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"}
        
        summary_elem = root.find(".//t:ResultSummary", ns)
        counters = summary_elem.find("t:Counters", ns) if summary_elem is not None else None
        
        total = int(counters.get("total", 0)) if counters is not None else 0
        passed = int(counters.get("passed", 0)) if counters is not None else 0
        failed = int(counters.get("failed", 0)) if counters is not None else 0
        
        failures = []
        for res in root.findall(".//t:UnitTestResult", ns):
            outcome = res.get("outcome")
            if outcome == "Failed":
                test_name = res.get("testName")
                error_info = res.find(".//t:ErrorInfo", ns)
                message = ""
                stack_trace = ""
                if error_info is not None:
                    msg_elem = error_info.find("t:Message", ns)
                    st_elem = error_info.find("t:StackTrace", ns)
                    if msg_elem is not None and msg_elem.text:
                        message = msg_elem.text.strip()
                    if st_elem is not None and st_elem.text:
                        stack_trace = st_elem.text.strip()
                
                failures.append({
                    "test": test_name,
                    "message": message,
                    "stackTrace": stack_trace
                })
                
        shutil.rmtree(results_dir)
        return {
            "success": failed == 0,
            "summary": {"total": total, "passed": passed, "failed": failed},
            "failures": failures
        }
    except Exception as e:
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)
        return {"error": f"Failed to parse test results: {str(e)}"}

def handle_tools_call(request_id, name, arguments):
    if name == "run_dotnet_tests":
        project_path = arguments.get("projectPath")
        test_filter = arguments.get("filter")
        res = run_dotnet_tests(project_path, test_filter)
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
    if len(sys.argv) > 1:
        project = sys.argv[1]
        test_filter = sys.argv[2] if len(sys.argv) > 2 else None
        res = run_dotnet_tests(project, test_filter)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("success", False) else 1)
    else:
        main()
