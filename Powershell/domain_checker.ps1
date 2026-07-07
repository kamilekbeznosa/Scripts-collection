$domains = @("google.com", "microsoft.com", "expired.badssl.com")

foreach ($domain in $domains) {
    try {
        $req = [Net.HttpWebRequest]::Create("https://$domain")
        $req.Timeout = 5000
        $response = $req.GetResponse()
        
        $certBase = $req.ServicePoint.Certificate
        $cert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new($certBase)
        
        $daysLeft = ($cert.NotAfter - (Get-Date)).Days
        
        if ($daysLeft -lt 30) {
            Write-Host "[WARNING] $domain wygasa za $daysLeft dni!" -ForegroundColor Yellow
        } else {
            Write-Host "[OK] $domain jest bezpieczny. Pozostało $daysLeft dni." -ForegroundColor Green
        }
    } catch {
        Write-Host "[ERROR] Nie udało się sprawdzić $domain. Błąd: $($_.Exception.Message)" -ForegroundColor Red
    }
}