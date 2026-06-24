#!/usr/bin/env bash

# Bootstraps the toolchain required to work on MachineReturnProto.
# Installs the .NET 8 SDK and the Tessl CLI. Safe to re-run (idempotent).

set -euo pipefail

DOTNET_CHANNEL="8.0"
TESSL_VERSION="0.87.0"
DOTNET_DIR="${DOTNET_ROOT:-$HOME/.dotnet}"

# Persists an env var both for Devin blueprint runs ($ENVRC) and human shells (~/.bashrc).
persist_env() {
  local key="$1" value="$2"
  if [ -n "${ENVRC:-}" ]; then
    echo "${key}=${value}" >> "$ENVRC"
  fi
  local profile="$HOME/.bashrc"
  local line="export ${key}=\"${value}\""
  if [ -f "$profile" ] && ! grep -qF "$line" "$profile"; then
    echo "$line" >> "$profile"
  fi
}

# 1. .NET 8 SDK
if command -v dotnet >/dev/null 2>&1 || [ -x "$DOTNET_DIR/dotnet" ]; then
  echo ".NET SDK already present, skipping."
else
  echo "Installing .NET SDK channel ${DOTNET_CHANNEL} into ${DOTNET_DIR}..."
  curl -sSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel "$DOTNET_CHANNEL" --install-dir "$DOTNET_DIR"
  persist_env DOTNET_ROOT "$DOTNET_DIR"
  persist_env PATH "${DOTNET_DIR}:\$PATH"
  export DOTNET_ROOT="$DOTNET_DIR"
  export PATH="${DOTNET_DIR}:$PATH"
fi

# 2. Tessl CLI
if command -v tessl >/dev/null 2>&1; then
  echo "Tessl CLI already present, skipping."
else
  echo "Installing Tessl CLI ${TESSL_VERSION}..."
  npm install -g "tessl@${TESSL_VERSION}"
fi

echo "Toolchain ready. Next: run 'tessl install' to sync plugin rules/skills into .tessl/"
