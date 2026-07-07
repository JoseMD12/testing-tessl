#!/usr/bin/env bash

# AI Task Harness CLI
# Guides AI tasks through: Research -> Plan (Generates Spec) -> Implement
# With mandatory human validation at each step.

set -euo pipefail

TASK_DIR="tasks"
ACTIVE_FILE="${TASK_DIR}/.active"
TEMPLATE_FILE="${TASK_DIR}/task-template.md"

# Ensure the task directory exists
mkdir -p "$TASK_DIR"

usage() {
  echo "AI Task Harness CLI"
  echo "Usage:"
  echo "  $0 init \"<Task Title>\"   Initialize a new task"
  echo "  $0 status                Show the status of the current active task"
  echo "  $0 approve               Approve and advance the current phase"
  echo "  $0 help                  Show this help message"
  exit 1
}

# Helper to get the current active task file
get_active_task_file() {
  if [ ! -f "$ACTIVE_FILE" ]; then
    echo "Error: No active task. Run '$0 init \"<Task Title>\"' first." >&2
    exit 1
  fi
  local file
  file=$(cat "$ACTIVE_FILE" | tr -d '\r' | xargs)
  if [ ! -f "$file" ]; then
    echo "Error: Active task file '$file' does not exist." >&2
    exit 1
  fi
  echo "$file"
}

# Helper to sanitize string for filename
sanitize_filename() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g'
}

init_task() {
  local title="$1"
  if [ -z "$title" ]; then
    echo "Error: Task title cannot be empty." >&2
    exit 1
  fi

  if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: Template file '$TEMPLATE_FILE' not found." >&2
    exit 1
  fi

  local date_str
  date_str=$(date +'%Y-%m-%d')
  local task_id
  task_id=$(date +'%Y%m%d%H%M%S')
  local sanitized
  sanitized=$(sanitize_filename "$title")
  local filename="${TASK_DIR}/task-${date_str}-${sanitized}.md"

  # Create the task file from template using Python for safety against title special characters (like slashes)
  python3 -c "
import sys
title, task_id, date_str, template_file, out_file = sys.argv[1:6]
tmpl = open(template_file, 'r', encoding='utf-8').read()
tmpl = tmpl.replace('{{TASK_TITLE}}', title).replace('{{TASK_ID}}', task_id).replace('{{CREATED_DATE}}', date_str)
open(out_file, 'w', encoding='utf-8').write(tmpl)
" "$title" "$task_id" "$date_str" "$TEMPLATE_FILE" "$filename"

  # Set active task
  echo "$filename" > "$ACTIVE_FILE"

  echo "========================================================="
  echo "🎉 Task initialized successfully!"
  echo "Task File:   $filename"
  echo "Active Step: Research"
  echo "========================================================="
  echo "Please begin by exploring the codebase. Write your findings under 'Research Notes'"
  echo "in the task file, and then run '$0 approve' or ask the user to approve."
}

show_status() {
  local task_file
  task_file=$(get_active_task_file)

  local title
  title=$(grep "^# Task:" "$task_file" | sed -E 's/# Task:[[:space:]]*//' | tr -d '\r')
  local phase
  phase=$(grep "Current Phase:" "$task_file" | sed -E 's/.*Current Phase:\*\*//' | tr -d '\r' | xargs)
  local status
  status=$(grep "Status:" "$task_file" | sed -E 's/.*Status:\*\*//' | tr -d '\r' | xargs)

  echo "========================================================="
  echo "📋 Active Task: $title"
  echo "   File:        $task_file"
  echo "   Phase:       $phase"
  echo "   Status:      $status"
  echo "========================================================="

  # Check validation status
  local research_approved="[ ]"
  local plan_approved="[ ]"
  local implement_approved="[ ]"

  if grep -q "\- \[x\] Research Phase Approved" "$task_file"; then
    research_approved="[x]"
  fi
  if grep -q "\- \[x\] Plan Phase Approved" "$task_file"; then
    plan_approved="[x]"
  fi
  if grep -q "\- \[x\] Implementation Phase Approved" "$task_file"; then
    implement_approved="[x]"
  fi

  echo "Validation Steps Checklists:"
  echo "  $research_approved Step 1: Research (Code exploration & notes)"
  echo "  $plan_approved Step 2: Plan (Architecture & Spec file generation)"
  echo "  $implement_approved Step 3: Implement (Code, tests, build & verify)"
  echo "========================================================="

  case "$phase" in
    "Research")
      echo "👉 Next Action: Run research, update 'Research Notes', and run '$0 approve' (requires human approval)."
      ;;
    "Plan")
      echo "👉 Next Action: Document implementation plan, create the Spec file, specify its path in the task file, and run '$0 approve' (requires human approval)."
      ;;
    "Implement")
      echo "👉 Next Action: Implement changes, write/run tests, and run '$0 approve' (requires human approval)."
      ;;
    "Completed")
      echo "✅ Task completed!"
      ;;
  esac
}

approve_phase() {
  local task_file
  task_file=$(get_active_task_file)

  local phase
  phase=$(grep "Current Phase:" "$task_file" | sed -E 's/.*Current Phase:\*\*//' | tr -d '\r' | xargs)

  local timestamp
  timestamp=$(date +'%Y-%m-%d %H:%M:%S')

  case "$phase" in
    "Research")
      # Transition: Research -> Plan
      python3 -c "
import sys
f = sys.argv[1]
content = open(f, 'r', encoding='utf-8').read()
content = content.replace('- [ ] Research Phase Approved', f'- [x] Research Phase Approved (Approved on {sys.argv[2]})')
content = content.replace('Current Phase:** Research', 'Current Phase:** Plan')
open(f, 'w', encoding='utf-8').write(content)
" "$task_file" "$timestamp"
      echo "✅ Research Phase Approved! Advanced task to 'Plan' phase."
      echo "Please write the design plan and generate the spec file under specs/spec-*.md."
      ;;

    "Plan")
      # Extract spec file path using a robust Python script
      local spec_path
      spec_path=$(python3 -c "
import re, sys
content = open(sys.argv[1], 'r', encoding='utf-8').read()
matches = re.findall(r'Path:\s*(.*)', content)
path = ''
for m in matches:
    m = m.strip()
    if '*' not in m and m != 'specs/':
        path = m
        break
path = re.sub(r'[\`\*\_]', '', path)
link_match = re.search(r'\[.*?\]\((.*?)\)', path)
if link_match:
    path = link_match.group(1)
else:
    path = re.sub(r'[\[\]]', '', path)
if path.startswith('file://'):
    path = path[7:]
print(path.strip())
" "$task_file" | tr -d '\r' | xargs)

      if [ -z "$spec_path" ] || [ "$spec_path" = "specs/" ] || [ ! -f "$spec_path" ]; then
        echo "❌ Validation Error: You must generate a spec file (e.g. specs/spec-*.md) and link it in the task file." >&2
        echo "   Current specified path: '$spec_path'" >&2
        echo "   Please make sure the file exists and update the 'Path: <file-path>' line in: $task_file" >&2
        exit 1
      fi

      # Transition: Plan -> Implement
      python3 -c "
import sys
f = sys.argv[1]
content = open(f, 'r', encoding='utf-8').read()
content = content.replace('- [ ] Plan Phase Approved', f'- [x] Plan Phase Approved (Approved on {sys.argv[2]})')
content = content.replace('Current Phase:** Plan', 'Current Phase:** Implement')
open(f, 'w', encoding='utf-8').write(content)
" "$task_file" "$timestamp"
      echo "✅ Plan Phase Approved (Spec validated: $spec_path)!"
      echo "Advanced task to 'Implement' phase. You can now begin implementing the changes."
      ;;

    "Implement")
      # Transition: Implement -> Completed
      python3 -c "
import sys
f = sys.argv[1]
content = open(f, 'r', encoding='utf-8').read()
content = content.replace('- [ ] Implementation Phase Approved', f'- [x] Implementation Phase Approved (Approved on {sys.argv[2]})')
content = content.replace('Current Phase:** Implement', 'Current Phase:** Completed')
content = content.replace('Status:** In Progress', 'Status:** Completed')
open(f, 'w', encoding='utf-8').write(content)
" "$task_file" "$timestamp"
      echo "🎉 Implementation Phase Approved! Task has been marked as COMPLETED."
      ;;

    "Completed")
      echo "Task is already completed!"
      ;;

    *)
      echo "Error: Unknown phase '$phase' in task file." >&2
      exit 1
      ;;
  esac
}

# Parse command line args
if [ $# -lt 1 ]; then
  usage
fi

CMD="$1"
shift

case "$CMD" in
  init)
    if [ $# -lt 1 ]; then
      echo "Error: Missing task title." >&2
      usage
    fi
    init_task "$1"
    ;;
  status)
    show_status
    ;;
  approve)
    approve_phase
    ;;
  help)
    usage
    ;;
  *)
    echo "Unknown command: $CMD" >&2
    usage
    ;;
esac
