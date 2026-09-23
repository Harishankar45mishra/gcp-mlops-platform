#!/bin/bash

for i in {1..100}
do
curl -s -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d "{
\"sepal_length\": $((RANDOM%3+4)).$((RANDOM%9)),
\"sepal_width\": $((RANDOM%3+2)).$((RANDOM%9)),
\"petal_length\": $((RANDOM%5+1)).$((RANDOM%9)),
\"petal_width\": $((RANDOM%3)).$((RANDOM%9))
}" > /dev/null
done

echo "Generated 100 predictions."
