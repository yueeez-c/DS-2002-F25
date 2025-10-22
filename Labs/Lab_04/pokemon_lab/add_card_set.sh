##!/usr/bin/env bash
read -r -p "TCG Card Set ID (e.g., base1, base4): " SET_ID
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi
URL="https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}"
echo "Fetching data for %SET_ID...."
curl -sS -f "$URL" -o "card_set_lookup/${SET_ID}.json"
echo "Saved to card_set_lookup/${SET_ID}.json"
