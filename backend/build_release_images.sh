#!/usr/bin/env bash
# Script de construction et publication des images Docker PROSTATIA v1.0.0
# Usage: ./build_release_images.sh [--push]

set -euo pipefail

VERSION="1.0.0"
PUSH=false

if [[ "${1:-}" == "--push" ]]; then
    PUSH=true
fi

echo "======================================================="
echo " Construction des images Docker PROSTATIA v${VERSION}"
echo "======================================================="

cd "$(dirname "$0")"

SERVICES=("stats-engine:./stats_engine" "data-service:./data_service" "ai-orchestrator:./ai_orchestrator" "gateway:./gateway")

for item in "${SERVICES[@]}"; do
    NAME="${item%%:*}"
    CONTEXT="${item##*:}"
    IMG_VERSION="prostatia/${NAME}:${VERSION}"
    IMG_LATEST="prostatia/${NAME}:latest"

    echo ""
    echo ">>> [BUILD] ${NAME} (${IMG_VERSION}) <<<"
    docker build -t "${IMG_VERSION}" -t "${IMG_LATEST}" "${CONTEXT}"

    if [ "$PUSH" = true ]; then
        echo ">>> [PUSH] Publication de ${IMG_VERSION}..."
        docker push "${IMG_VERSION}"
        docker push "${IMG_LATEST}"
    fi
done

echo ""
echo "======================================================="
echo " Toutes les images v${VERSION} ont été générées avec succès !"
echo "======================================================="
