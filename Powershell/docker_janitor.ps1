Write-Host "Rozpoczynam sprzątanie środowiska Docker..." -ForegroundColor Cyan

$danglingImages = docker images -f "dangling=true" -q
if ($danglingImages) {
    Write-Host "Znaleziono porzucone obrazy. Usuwam..."
    docker rmi $danglingImages
} else {
    Write-Host "Brak porzuconych obrazów."
}

$exitedContainers = docker ps -a -f "status=exited" -q
if ($exitedContainers) {
    Write-Host "Znaleziono zatrzymane kontenery. Usuwam..."
    docker rm $exitedContainers
} else {
    Write-Host "Brak zatrzymanych kontenerów."
}

Write-Host "Środowisko czyste!" -ForegroundColor Green