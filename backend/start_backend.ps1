# Se placer dans le dossier du script
Set-Location -Path $PSScriptRoot

$env:PATH = "C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;" + $env:PATH

Write-Host "Installation des dependances Python (Stats Engine)..."
cd stats_engine
poetry install
cd ..

Write-Host "Installation des dependances Python (AI Orchestrator)..."
cd ai_orchestrator
poetry install
cd ..

Write-Host "Installation des dependances Python (Viz Service)..."
cd viz_service
poetry install
cd ..

Write-Host "Installation des dependances Python (Geo Service)..."
cd geo_service
poetry install
cd ..

Write-Host "Compilation Rust (Data Service)..."
cd data_service
cargo build
cd ..

Write-Host "Compilation Rust (Gateway)..."
cd gateway
cargo build
cd ..

Write-Host "Demarrage des 6 services dans de nouvelles fenetres..."
Start-Process powershell -ArgumentList "-NoExit -Command `" `$env:PATH = 'C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;' + `$env:PATH; cd '$PSScriptRoot\stats_engine'; poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload `""
Start-Process powershell -ArgumentList "-NoExit -Command `" `$env:PATH = 'C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;' + `$env:PATH; cd '$PSScriptRoot\ai_orchestrator'; poetry run uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload `""
Start-Process powershell -ArgumentList "-NoExit -Command `" `$env:PATH = 'C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;' + `$env:PATH; cd '$PSScriptRoot\viz_service'; poetry run uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload `""
Start-Process powershell -ArgumentList "-NoExit -Command `" `$env:PATH = 'C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;' + `$env:PATH; cd '$PSScriptRoot\geo_service'; poetry run uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload `""
Start-Process powershell -ArgumentList "-NoExit -Command `" `$env:PATH = 'C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;' + `$env:PATH; cd '$PSScriptRoot\data_service'; cargo run `""
Start-Process powershell -ArgumentList "-NoExit -Command `" `$env:PATH = 'C:\Users\HP\AppData\Local\Programs\Python\Python312;C:\Users\HP\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\HP\.cargo\bin;' + `$env:PATH; cd '$PSScriptRoot\gateway'; cargo run `""

Write-Host "Tous les 6 services ont ete lances ! (Les premieres compilations Rust peuvent prendre un peu de temps dans les nouvelles fenetres)."
