# Script pentru compilare si testare - Lab3
# Compilare si rulare programe MPI

Write-Host "=== Lab3 - Big Number Addition with MPI ===" -ForegroundColor Green
Write-Host ""

# Compile sequential version
Write-Host "Compilare varianta secventiala..." -ForegroundColor Yellow
g++ -std=c++20 -o varianta0_secvential.exe varianta0_secvential.cpp
if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilare reusita!" -ForegroundColor Green
} else {
    Write-Host "Eroare la compilare!" -ForegroundColor Red
    exit 1
}

# Compile MPI versions
Write-Host ""
Write-Host "Compilare varianta 1 (standard communication)..." -ForegroundColor Yellow
g++ -std=c++20 -o varianta1_standard.exe varianta1_standard.cpp -I"C:/Program Files (x86)/Microsoft SDKs/MPI/Include" -L"C:/Program Files (x86)/Microsoft SDKs/MPI/Lib/x64" -lmsmpi
if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilare reusita!" -ForegroundColor Green
} else {
    Write-Host "Eroare la compilare!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Compilare varianta 2 (scatter/gather)..." -ForegroundColor Yellow
g++ -std=c++20 -o varianta2_scatter_gather.exe varianta2_scatter_gather.cpp -I"C:/Program Files (x86)/Microsoft SDKs/MPI/Include" -L"C:/Program Files (x86)/Microsoft SDKs/MPI/Lib/x64" -lmsmpi
if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilare reusita!" -ForegroundColor Green
} else {
    Write-Host "Eroare la compilare!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Compilare varianta 3 (asynchronous)..." -ForegroundColor Yellow
g++ -std=c++20 -o varianta3_asincron.exe varianta3_asincron.cpp -I"C:/Program Files (x86)/Microsoft SDKs/MPI/Include" -L"C:/Program Files (x86)/Microsoft SDKs/MPI/Lib/x64" -lmsmpi
if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilare reusita!" -ForegroundColor Green
} else {
    Write-Host "Eroare la compilare!" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Compilare finalizata ===" -ForegroundColor Green
