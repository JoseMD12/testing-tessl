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

  # Create the task file from template
  sed -e "s/{{TASK_TITLE}}/${title}/g" \
      -e "s/{{TASK_ID}}/${task_id}/g" \
      -e "s/{{CREATED_DATE}}/${date_str}/g" \
      "$TEMPLATE_FILE" > "$filename"

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
  title=$(grep "^# Task:" "$task_file" | sed 's/# Task: //' | tr -d '\r')
  local phase
  phase=$(grep "^Current Phase:" "$task_file" | sed 's/Current Phase: //' | tr -d '\r' | xargs)
  local status
  status=$(grep "^Status:" "$task_file" | sed 's/Status: //' | tr -d '\r' | xargs)

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
  phase=$(grep "^Current Phase:" "$task_file" | sed 's/Current Phase: //' | tr -d '\r' | xargs)

  local timestamp
  timestamp=$(date +'%Y-%m-%d %H:%M:%S')

  case "$phase" in
    "Research")
      # Transition: Research -> Plan
      # Replace first occurrence of "- [ ] Research Phase Approved"
      # Using a temp file or python/perl to avoid sed issues across OSes
      sed -i "s/- \[ \] Research Phase Approved/- [x] Research Phase Approved (Approved on $timestamp)/" "$task_file"
      sed -i "s/Current Phase: Research/Current Phase: Plan/" "$task_file"
      echo "✅ Research Phase Approved! Advanced task to 'Plan' phase."
      echo "Please write the design plan and generate the spec file under specs/spec-*.md."
      ;;

    "Plan")
      # Check if Spec file was specified and exists
      # Extract spec file path from "Path: <value>" line under "## Spec File Generated"
      local spec_line
      spec_line=$(grep -A 2 "### Spec File Generated" "$task_file" | grep "Path:" || true)
      local spec_path
      spec_path=$(echo "$spec_line" | sed 's/Path:[[:space:]]*//' | tr -d '\r' | xargs || true)

      if [ -z "$spec_path" ] || [ "$spec_path" = "specs/" ] || [ ! -f "$spec_path" ]; then
        echo "❌ Validation Error: You must generate a spec file (e.g. specs/spec-*.md) and link it in the task file." >&2
        echo "   Current specified path: '$spec_path'" >&2
        echo "   Please make sure the file exists and update the 'Path: <file-path>' line in: $task_file" >&2
        exit 1
      fi

      # Transition: Plan -> Implement
      sed -i "s/- \[ \] Plan Phase Approved/- [x] Plan Phase Approved (Approved on $timestamp)/" "$task_file"
      sed -i "s/Current Phase: Plan/Current Phase: Implement/" "$task_file"
      echo "✅ Plan Phase Approved (Spec validated: $spec_path)!"
      echo "Advanced task to 'Implement' phase. You can now begin implementing the changes."
      ;;

    "Implement")
      # Transition: Implement -> Completed
      sed -i "s/- \[ \] Implementation Phase Approved/- [x] Implementation Phase Approved (Approved on $timestamp)/" "$task_file"
      sed -i "s/Current Phase: Implement/Current Phase: Completed/" "$task_file"
      sed -i "s/Status: In Progress/Status: Completed/" "$task_file"
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
