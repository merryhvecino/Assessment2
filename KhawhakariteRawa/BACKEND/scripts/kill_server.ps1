#!/usr/bin/env pwsh
# Kill existing Python server processes to free up ports

Write-Host "Checking for existing Python processes..."

# Get all Python processes
$pythonProcesses = Get-Process | Where-Object {$_.ProcessName -like "*python*"}

if ($pythonProcesses) {
    Write-Host "Found Python processes:"
    $pythonProcesses | Format-Table Id, ProcessName, CPU -AutoSize
    
    Write-Host "Killing Python processes..."
    $pythonProcesses | ForEach-Object {
        try {
            Stop-Process -Id $_.Id -Force
            Write-Host "Killed process ID: $($_.Id)" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to kill process ID: $($_.Id) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "No Python processes found." -ForegroundColor Yellow
}

Write-Host "Process cleanup complete." -ForegroundColor Green 