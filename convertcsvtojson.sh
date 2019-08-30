#!/usr/bin/env bash

items=( )
while IFS=';' read -r cont auth title year link hash grading _; do
  printf -v item '{ "cont": %s,\n "auth": %s,\n "title": %s,\n "year": %s,\ "link": %s,\n "hash": {%s},\n "grading": %s\n }\n' "$cont" "$auth" "$title" "$year" "$link" "$hash" "$grading"
  items+=( "$item" )
done <'sbb-hackathon-2.csv'

IFS=','
printf '[%s]\n' "${items[*]}" > output.json
