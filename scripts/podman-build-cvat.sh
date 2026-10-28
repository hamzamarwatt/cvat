#!/usr/bin/env bash
# Build CVAT server and UI images locally for Podman (assessment branch).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Building docker.io/cvat/server:dev (this takes a long time)..."
podman build -t docker.io/cvat/server:dev -f Dockerfile .

echo "Building docker.io/cvat/ui:dev ..."
podman build -t docker.io/cvat/ui:dev -f Dockerfile.ui .

echo "Done. Start stack with:"
echo "  export CVAT_HOST=localhost"
echo "  docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.podman.yml up -d"
