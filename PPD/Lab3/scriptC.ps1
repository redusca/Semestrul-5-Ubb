
$param1 = $args[0] # Nume fisier exe (ex: varianta1_standard.exe)
$param2 = $args[1] # No of processes (pentru MPI)
$param3 = $args[2] # No of runs
$param4 = $args[3] # Numar1.txt (fisier input 1)
$param5 = $args[4] # Numar2.txt (fisier input 2)
$param6 = $args[5] # Varianta (0=secvential, 1=standard, 2=scatter, 3=asincron)
$param7 = $args[6] # Test size identifier (ex: "16", "1000", "10000")

$output_file = $args[7] # Nume fisier output CSV

# Determine test description
$test_size = $param7
$varianta_name = switch ($param6) {
    0 { "Sequential" }
    1 { "MPI Standard" }
    2 { "MPI Scatter/Gather" }
    3 { "MPI Asynchronous" }
    default { "Unknown" }
}

# Determine output filename based on variant
$output_filename = switch ($param6) {
    0 { "Numar3_var0.txt" }
    1 { "Numar3_var1.txt" }
    2 { "Numar3_var2.txt" }
    3 { "Numar3_var3.txt" }
    default { "Numar3.txt" }
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Test: $test_size digits - $varianta_name" -ForegroundColor Cyan
Write-Host "Processes: $param2, Runs: $param3" -ForegroundColor Cyan
Write-Host "Output: $output_filename" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$suma = 0
$times = @()

for ($i = 0; $i -lt $param3; $i++){
    Write-Host "Rulare" ($i+1) -NoNewline
    
    # Copy input files to standard names
    Copy-Item $param4 Numar1.txt -Force
    Copy-Item $param5 Numar2.txt -Force
    
    if ($param6 -eq 0) {
        # Sequential version
        $output = & ".\$param1" 2>&1
    } else {
        # MPI versions
        $output = mpiexec -n $param2 ".\$param1" 2>&1
    }
    
    # Extract time from output
    # Expected format: "Timp executie ... : X.XXXX secunde"
    $timeMatch = $output | Select-String -Pattern "Timp.*?:\s*([\d.]+)\s*secunde"
    
    if ($timeMatch) {
        $time = [double]$timeMatch.Matches.Groups[1].Value
        $times += $time
        $suma += $time
        Write-Host " - $time secunde" -ForegroundColor Green
    } else {
        Write-Host " - ERROR: Could not extract time" -ForegroundColor Red
        Write-Host $output
    }
}

# Log the output result
Write-Host ""
Write-Host "Logging output to log_output.txt..." -ForegroundColor Yellow

$log_file = "log_output.txt"
$log_entry = @"

========================================
Test: $test_size digits - $varianta_name
Processes: $param2
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
========================================
"@

Add-Content $log_file $log_entry

if (Test-Path $output_filename) {
    $result_content = Get-Content $output_filename -Raw
    Add-Content $log_file "Result from ${output_filename}:"
    Add-Content $log_file $result_content
    Write-Host "Output logged successfully" -ForegroundColor Green
} else {
    Add-Content $log_file "ERROR: Output file $output_filename not found"
    Write-Host "Warning: Output file not found" -ForegroundColor Yellow
}

Write-Host ""

# Calculate statistics
if ($param3 -gt 0 -and $times.Count -gt 0) {
    $media = $suma / $param3
    $min_time = ($times | Measure-Object -Minimum).Minimum
    $max_time = ($times | Measure-Object -Maximum).Maximum
    
    Write-Host "Timp de executie mediu: $media secunde" -ForegroundColor Cyan
    Write-Host "Timp minim: $min_time secunde" -ForegroundColor Cyan
    Write-Host "Timp maxim: $max_time secunde" -ForegroundColor Cyan
} else {
    Write-Host "Nu s-au putut calcula statistici - nu exista masuratori valide" -ForegroundColor Red
    $media = 0
    $min_time = 0
    $max_time = 0
}

Write-Host ""

# Create CSV file if it doesn't exist
if ($output_file -and !(Test-Path $output_file)){
    New-Item $output_file -ItemType File
    Set-Content $output_file 'Test Size,Varianta,Nr Procese,Timp Mediu (s),Timp Min (s),Timp Max (s)'
}

# Prepare process count string
if ($param2 -eq 1 -or $param6 -eq 0) {
    $proc_str = "1 (Sequential)"
} else {
    $proc_str = $param2
}

# Append results
if ($output_file) {
    Add-Content $output_file "$($test_size),$($varianta_name),$($proc_str),$($media),$($min_time),$($max_time)"
    Write-Host "Results appended to $output_file" -ForegroundColor Green
} else {
    Write-Host "Warning: No output file specified" -ForegroundColor Yellow
}
