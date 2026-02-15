#!/bin/bash

echo -e "\e[1;34m=== SSL CERTIFICATE EXPIRY CHECKER ===\e[0m"
read -p "Podaj domenę do sprawdzenia: " DOMAIN

PORT="443"

END_DATE=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:$PORT 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)

echo "Certyfikat dla $DOMAIN wygasa: $END_DATE"