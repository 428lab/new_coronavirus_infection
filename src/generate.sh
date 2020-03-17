#!/bin/bash
JSON=$(cat country.json)
JSON=$(echo $JSON | jq ".country" -c) # | to_entries | map(.key)" -c)
BLACKLIST='["Hong Kong"]'

len=$(echo $BLACKLIST | jq length)
for i in $(seq 0 $(($len -1 )) ); do
    data=$(echo $BLACKLIST | jq ".[$i]")
    JSON=$(echo $JSON | jq "del(.[$data])")
done

JSON=$(echo $JSON | jq "to_entries | map(.key)" -c)
echo $JSON
len=$(echo $JSON | jq length)
for i in $(seq 0 $(($len - 1)) ); do
    python estimate_new_coronavirus_infection.py "$(echo $JSON | jq ".[$i]" -r)" &
done
wait