$disk = Get-Volume -DriveLetter C
$freeSpaceGB = [math]::Round($disk.SizeRemaining / 1GB, 2)
$totalSpaceGB = [math]::Round($disk.Size / 1GB, 2)
$freePercentage = [math]::Round(($disk.SizeRemaining / $disk.Size) * 100, 2)

$os = Get-CimInstance Win32_OperatingSystem
$freeRamGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)

Write-Host "Raport Systemowy:" -ForegroundColor Cyan
Write-Host "Dysk C: Wolne $freePercentage% ($freeSpaceGB GB / $totalSpaceGB GB)"
Write-Host "Wolny RAM: $freeRamGB GB"

if ($freePercentage -lt 15) {
    $alertMsg = "ALARM! Mało miejsca na serwerze. Pozostało tylko $freePercentage%."
    Write-Warning $alertMsg
    
    # $payload = @{ text = $alertMsg } | ConvertTo-Json
    # Invoke-RestMethod -Uri "LINK_WEBHOOKA" -Method Post -Body $payload -ContentType "application/json"
}