#!/usr/bin/env bash
set -e

./wait_for_database.sh && python migrate.py
