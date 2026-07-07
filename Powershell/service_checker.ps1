$services = @(
    [PSCustomObject]@{ Name = "Publiczny DNS"; Host = "8.8.8.8"; Port = 53 }
    [PSCustomObject]@{ Name = "Lokalny Postgres"; Host = "127.0.0.1"; Port = 5432 }
    [PSCustomObject]@{ Name = "Fikcyjny Serwis"; Host = "10.20.30.40"; Port = 8080 }
)

$results = foreach ($service in $services) {
    $test = Test-NetConnection -ComputerName $service.Host -Port $service.Port -WarningAction SilentlyContinue
    
    [PSCustomObject]@{
        Usluga = $service.Name
        Adres = "$($service.Host):$($service.Port)"
        Status = if ($test.TcpTestSucceeded) { "ONLINE" } else { "OFFLINE" }
        PingMS = $test.PingReplyDetails.RoundtripTime
    }
}

$results | Format-Table -AutoSize