#!/usr/bin/env bash

# Bootstraps the toolchain required to work on MachineReturnProto.
# Installs the .NET 8 SDK and the Tessl CLI. Safe to re-run (idempotent).

set -euo pipefail

DOTNET_CHANNEL="8.0"
TESSL_VERSION="0.87.0"
DOTNET_DIR="${DOTNET_ROOT:-$HOME/.dotnet}"

# Returns 0 if a .NET SDK matching $DOTNET_CHANNEL is available (on PATH or in $DOTNET_DIR).
dotnet_channel_installed() {
  local bin
  for bin in "$(command -v dotnet 2>/dev/null)" "$DOTNET_DIR/dotnet"; do
    [ -n "$bin" ] && [ -x "$bin" ] || continue
    if "$bin" --list-sdks 2>/dev/null | grep -q "^${DOTNET_CHANNEL}\."; then
      return 0
    fi
  done
  return 1
}

# Persists an env var both for Devin blueprint runs ($ENVRC) and human shells (~/.bashrc).
persist_env() {
  local key="$1" value="$2"
  if [ -n "${ENVRC:-}" ]; then
    local entry="${key}=${value}"
    if ! { [ -f "$ENVRC" ] && grep -qF "$entry" "$ENVRC"; }; then
      echo "$entry" >> "$ENVRC"
    fi
  fi
  local profile="$HOME/.bashrc"
  local line="export ${key}=\"${value}\""
  touch "$profile"
  if ! grep -qF "$line" "$profile"; then
    echo "$line" >> "$profile"
  fi
}

# 1. .NET 8 SDK
if dotnet_channel_installed; then
  echo ".NET SDK ${DOTNET_CHANNEL} already present, skipping."
else
  echo "Installing .NET SDK channel ${DOTNET_CHANNEL} into ${DOTNET_DIR}..."
  curl -sSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel "$DOTNET_CHANNEL" --install-dir "$DOTNET_DIR"
  persist_env DOTNET_ROOT "$DOTNET_DIR"
  persist_env PATH "${DOTNET_DIR}:\$PATH"
  export DOTNET_ROOT="$DOTNET_DIR"
  export PATH="${DOTNET_DIR}:$PATH"
fi

# 2. Tessl CLI
if command -v tessl >/dev/null 2>&1 && tessl --version 2>/dev/null | grep -qF "$TESSL_VERSION"; then
  echo "Tessl CLI ${TESSL_VERSION} already present, skipping."
else
  if ! command -v npm >/dev/null 2>&1; then
    echo "Error: npm (Node.js) is required to install the Tessl CLI but was not found on PATH." >&2
    echo "Install Node.js (which provides npm) and re-run this script." >&2
    exit 1
  fi
  echo "Installing Tessl CLI ${TESSL_VERSION}..."
  npm install -g "tessl@${TESSL_VERSION}"
fi

echo "Toolchain ready. Next: run 'tessl install' to sync plugin rules/skills into .tessl/"
