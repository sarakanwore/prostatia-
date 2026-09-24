# Script de construction et publication des images Docker PROSTATIA v1.0.0
# Usage: ./build_release_images.ps1 [-Push]

param (
    [switch]$Push = $false
)

$VERSION = "1.0.0"
$SERVICES = @(
    @{ Name = "stats-engine"; Context = "./stats_engine" },
    @{ Name = "data-service"; Context = "./data_service" },
    @{ Name = "ai-orchestrator"; Context = "./ai_orchestrator" },
    @{ Name = "gateway"; Context = "./gateway" }
)

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host " Construction des images Docker PROSTATIA v$VERSION" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

Set-Location -Path $PSScriptRoot

foreach ($s in $SERVICES) {
    $imgVersion = "prostatia/$($s.Name):$VERSION"
    $imgLatest = "prostatia/$($s.Name):latest"

    Write-Host "`n>>> [BUILD] $($s.Name) ($imgVersion) <<<" -ForegroundColor Yellow
    docker build -t $imgVersion -t $imgLatest $($s.Context)

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Échec de la construction de l'image $($s.Name)"
        exit 1
    }

    if ($Push) {
        Write-Host ">>> [PUSH] Publication de $imgVersion..." -ForegroundColor Green
        docker push $imgVersion
        docker push $imgLatest
    }
}

Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host " Toutes les images v$VERSION ont été générées avec succès !" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Cyan
