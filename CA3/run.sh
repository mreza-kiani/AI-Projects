#!/usr/bin/env bash

LOOP_LIMIT=10
for (( VAR = 0; VAR < ${LOOP_LIMIT}; ++VAR )); do
    echo "iterate ${VAR}"
    python3 spam_detector.py ${VAR} > output/${VAR}-4.out
done
