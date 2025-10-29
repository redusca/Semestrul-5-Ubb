
$param1 = $args[0] # Nume fisier exe
$param2 = $args[1] # No of threads
$param3 = $args[2] # No of runs
$param4 = "input/" + $args[3] # Nume fisier input
$param5 = $args[4] # Caz 1 - secvential , 2 - paralele orizontal , 3 - paralele vertical

$Matrice = $args[5] 
$TipAlocare = $args[6] 

$output_file = $args[7] # Nume fisier output

if ($Matrice -eq 1) {
    $tip_matrice = "Matrice 10x10"
}
if ($Matrice -eq 2) {
    $tip_matrice = "Matrice 1000x1000"
}
if ($Matrice -eq 3) {
    $tip_matrice = "Matrice 10x10000"
}
if ($Matrice -eq 4) {
    $tip_matrice = "Matrice 10000x10"
}
if ($Matrice -eq 5) {
    $tip_matrice = "Matrice 10000x10000"
}

# Executare exe in cmd mode 1,2
if ($TipAlocare -eq 1) {
    $tip_alocare = "static"
} else {
    $tip_alocare = "dinamic"
}

$suma = 0

for ($i = 0; $i -lt $param3; $i++){
    Write-Host "Rulare" ($i+1)
    $a = (cmd /c .\$param1 $param4 $param2 $param5 2`>`&1)
    Write-Host $a
    $suma += $a
    Write-Host ""
}

# Validate output if not sequential (mode 2 or 3)
if ($param5 -ne 1) {
    if ($param5 -eq 2) {
        $tip_alocare = $tip_alocare + " (orizontal)"
    } else {
        $tip_alocare = $tip_alocare + " (vertical)"
    }
    Write-Host ""
    Write-Host "Validating parallel output against sequential baseline..."
    
    # Determine the parallel output directory
    $parallel_dir = ""
    if ($param5 -eq 2) {
        $parallel_dir = "output/po"
        $mode_name = "Parallel Horizontal"
    } elseif ($param5 -eq 3) {
        $parallel_dir = "output/pv"
        $mode_name = "Parallel Vertical"
    }
    
    # Path to sequential output
    $sequential_file = "output/sec/$output_file"
    $parallel_file = "$parallel_dir/$output_file"
    
    # Check if both files exist
    if ((Test-Path $sequential_file) -and (Test-Path $parallel_file)) {
        # Compare file contents
        $seq_content = Get-Content $sequential_file -Raw
        $par_content = Get-Content $parallel_file -Raw
        
        if ($seq_content -eq $par_content) {
            Write-Host "[OK] VALIDATION PASSED: $mode_name output matches sequential output" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] VALIDATION FAILED: $mode_name output differs from sequential output!" -ForegroundColor Red
            Write-Host "Sequential file: $sequential_file"
            Write-Host "Parallel file: $parallel_file"
            Write-Host "STOPPING EXECUTION DUE TO VALIDATION FAILURE" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "[WARN] Cannot validate - one or both output files not found" -ForegroundColor Yellow
        if (-not (Test-Path $sequential_file)) {
            Write-Host "  Missing: $sequential_file"
            exit 1
        }
        if (-not (Test-Path $parallel_file)) {
            Write-Host "  Missing: $parallel_file"
            exit 1
        }
    }
    Write-Host ""
}

$media = $suma / $i
#Write-Host $suma
Write-Host "Timp de executie mediu:" $media

# Creare fisier .csv
if (!(Test-Path outC.csv)){
    New-Item outC.csv -ItemType File
    #Scrie date in csv
    Set-Content outC.csv 'Tip Matrice,Tip alocare,Nr threads,Timp executie'
}

if ($args[1] -ne 1) {
    $t = $args[1]
} else {
    $t = "secvential"
}

# Append
Add-Content outC.csv "$($tip_matrice),$($tip_alocare),$($t),$($media) ns"