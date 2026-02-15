#!/bin/bash

RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[0;33m'
NC='\e[0m'

echo -e "\e[1;34m=== DOCKER JANITOR ===\e[0m"

CONTAINERS=$(docker ps -q -f status=exited | wc -l)
echo -e "$YELLOW$CONTAINERS$NC exited containers found."

MEMORY_USAGE=$(docker system df)
echo "$MEMORY_USAGE"

DECISION=$(read -p "Do you want to clean up unused Docker resources? (y/n) " -n 1 -r)
if [[ $CONTAINERS -gt 5 ]]; then
    echo -e "$YELLOW Removing exited containers...$NC"
    docker container prune -f
else
    echo -e "$GREEN No exited containers to remove.$NC"
fi