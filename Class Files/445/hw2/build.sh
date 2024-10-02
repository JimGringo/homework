#!/bin/bash

SRC = "src/GPT2.py"
INPUT = "ed.txt"

if [! -f "$INPUT"]; then
    echo "$INPUT not found"
    exit 1
fi

python3 $SRC $INPUT