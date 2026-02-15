#!/bin/bash
echo -e "\e[1;34m=== DIAGNOSTYKA SIECI ===\e[0m"

read -p "Podaj adres docelowy (np. google.com): " TARGET

if [[ -z "$TARGET" ]]; then
    TARGET="google.com"
    echo "Nie podano adresu, używam domyślnego: $TARGET"
fi

echo "1. Sprawdzam DNS..."
IP=$(dig +short $TARGET 2>/dev/null)

if [[ -z "$IP" ]]; then 
    echo "❌ Błąd DNS (brak IP)"
else 
    echo " DNS OK: $IP"
fi

echo "2. Sprawdzam trasę (Gateway)..."
ip route | grep default

echo "3. Sprawdzam HTTP..."
CODE=$(curl -o /dev/null -s -w "%{http_code}" -L https://$TARGET)

if [ "$CODE" -eq "200" ] || [ "$CODE" -eq "301" ] || [ "$CODE" -eq "302" ]; then
     echo " Kod odpowiedzi: $CODE"
else
     echo " Kod odpowiedzi: $CODE"
fi