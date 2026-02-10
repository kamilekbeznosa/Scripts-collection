#!/bin/bash

echo -e "\e[1;34m=== NETWORK PORTS SCANNER ===\e[0m"
printf "%-10s %-10s %-20s %-10s\n" "PROTO" "PORT" "PROCESS" "STATUS"
echo "--------------------------------------------------------"

sudo ss -tulpn | grep 'LISTEN' | awk '{
    # $1=Netid(tcp/udp), $5=Local Address:Port, $7=Process info
    
    # Wyciągamy sam port (wszystko po dwukropku)
    split($5, a, ":"); 
    port = a[length(a)];
    
    # Kolorowanie (Prosta logika w awk)
    status = "\033[1;32mOPEN\033[0m";
    
    printf "%-10s %-10s %-20s %-10b\n", $1, port, $7, status
}'