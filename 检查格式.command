#!/bin/bash
# CSV 格式检查工具

cd "$(dirname "$0")" || exit

if [ $# -gt 0 ]; then
    python3 检查CSV格式.py "$1"
else
    python3 检查CSV格式.py
fi