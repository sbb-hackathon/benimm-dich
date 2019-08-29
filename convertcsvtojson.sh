#!/usr/bin/env bash

items=( )
while IFS=';' read -r id cont auth title year link hash grading _; do
  printf -v item '{ "id": %s,\n "cont": %s,\n "auth": %s,\n "title": %s,\n "year": %s,\ "link": %s,\n "hash": {%s},\n "grading": %s\n }\n' "$id" "$cont" "$auth" "$title" "$year" "$link" "$hash" "$grading"
  items+=( "$item" )
done <'sbb-hackathon - Sheet1.csv'

IFS=','
printf '[%s]\n' "${items[*]}" > output.json