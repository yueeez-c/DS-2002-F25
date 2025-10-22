#!/usr/bin/env bash
echo "Refreshing all card sets in card_set_lookup"
for FILE in card_set_lookup/*.json; do
    SET_ID=$(basename "$FILE" .json)
    echo "Updating set: $SET_ID..."
    if curl -sS -f "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$FILE"; then
        echo "Wrote data to $FILE"
    else
        echo "Error: Failed to update $FILE" >&2
    fi
done
echo "All card sets have been refreshed"
