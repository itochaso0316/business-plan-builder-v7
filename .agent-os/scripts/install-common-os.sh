#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"

mkdir -p \
  "$ROOT_DIR/.agent-os/manifests" \
  "$ROOT_DIR/.agent-os/hooks/session-end" \
  "$ROOT_DIR/.agent-os/hooks/post-tool" \
  "$ROOT_DIR/.agent-os/hooks/pre-commit" \
  "$ROOT_DIR/.agent-os/commands" \
  "$ROOT_DIR/.agent-os/scripts" \
  "$ROOT_DIR/.agent-os/templates/project-memory" \
  "$ROOT_DIR/.agent-os/templates/reports" \
  "$ROOT_DIR/project-memory/agent-os/session-drafts" \
  "$ROOT_DIR/project-memory/agent-os/tool-logs" \
  "$ROOT_DIR/project-memory/agent-os/touched-files" \
  "$ROOT_DIR/project-memory/agent-os/reports" \
  "$ROOT_DIR/project-memory/agent-os/snapshots"

for required in \
  ".agent-os/project.yaml" \
  ".agent-os/manifests/common-os.schema.yaml" \
  ".agent-os/hooks/session-end/settings.json" \
  ".agent-os/hooks/post-tool/settings.json" \
  ".agent-os/hooks/pre-commit/settings.json"
do
  if [[ ! -f "$ROOT_DIR/$required" ]]; then
    echo "missing required file: $required" >&2
    exit 1
  fi
done

echo "Common OS Phase 1 scaffold is present in: $ROOT_DIR"
