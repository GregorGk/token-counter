#!/bin/bash
# Test script for the token counter

echo "=== Token Counter Test Script ==="
echo

echo "1. Testing with sample.txt (standard output):"
python count_tokens_for_file.py examples/sample.txt
echo

echo "2. Testing JSON output:"
python count_tokens_for_file.py examples/sample.txt --json | python -m json.tool | head -20
echo "..."
echo

echo "3. Testing CSV output:"
python count_tokens_for_file.py examples/sample.txt --csv
echo

echo "4. Testing with the main CLI tool (list models):"
python -m token_counter.cli --list-models | head -15
echo "..."
echo

echo "5. Testing direct token counting for each model:"
for model in gemini-3.0 claude-opus-4.5 chatgpt-5.2; do
    echo -n "$model: "
    echo "Hello, world!" | python -m token_counter.cli -m $model | grep "Total tokens"
done

echo
echo "=== All tests completed ==="