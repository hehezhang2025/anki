#!/bin/bash
# CSV 转 Anki 格式 - 一键转换工具（macOS）

# 获取脚本所在目录
cd "$(dirname "$0")" || exit

# 如果有参数（拖拽文件），直接转换
if [ $# -gt 0 ]; then
    python3 csv_to_anki.py "$1"
else
    # 否则运行交互式转换
    python3 csv_to_anki.py
fi
