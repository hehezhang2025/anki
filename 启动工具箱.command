#!/bin/bash
# CSV 转 Anki 工具箱 - 主启动器

cd "$(dirname "$0")" || exit

while true; do
    clear
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║              CSV 转 Anki 工具箱 v1.0                  ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "🛠️  请选择功能："
    echo ""
    echo "   1️⃣  单个文件转换"
    echo "   2️⃣  批量文件转换"
    echo "   3️⃣  检查 CSV 格式"
    echo "   4️⃣  查看示例文件"
    echo "   5️⃣  查看使用说明"
    echo "   0️⃣  退出"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 显示当前目录的 CSV 文件
    csv_count=$(ls -1 *.csv 2>/dev/null | wc -l)
    if [ $csv_count -gt 0 ]; then
        echo "📁 当前目录的 CSV 文件 ($csv_count 个)："
        ls -1 *.csv 2>/dev/null | head -5 | while read file; do
            echo "   📄 $file"
        done
        if [ $csv_count -gt 5 ]; then
            echo "   ... 还有 $((csv_count - 5)) 个文件"
        fi
    else
        echo "📁 当前目录没有 CSV 文件"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    read -p "请输入选项 (0-5): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔄 启动单个文件转换..."
            echo ""
            python3 csv_to_anki.py
            ;;
        2)
            echo ""
            echo "🔄 启动批量转换..."
            echo ""
            ./批量转换.command
            ;;
        3)
            echo ""
            echo "🔍 启动格式检查..."
            echo ""
            python3 检查CSV格式.py
            ;;
        4)
            echo ""
            echo "📋 示例文件列表："
            echo ""
            echo "   📄 示例.csv - 基础示例 (10 张卡片)"
            echo "   📄 英语单词.csv - 英语词汇 (20 张卡片)"
            echo "   📄 编程术语.csv - 编程术语 (20 张卡片)"
            echo "   📄 日语基础.csv - 日语基础 (20 张卡片)"
            echo ""
            echo "💡 你可以用这些文件测试转换功能"
            echo ""
            read -p "按回车键继续..."
            ;;
        5)
            echo ""
            echo "📖 打开使用说明..."
            echo ""
            if command -v open >/dev/null 2>&1; then
                open "使用说明.txt"
            else
                cat "使用说明.txt"
            fi
            echo ""
            read -p "按回车键继续..."
            ;;
        0)
            echo ""
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo ""
            echo "❌ 无效选项，请输入 0-5"
            echo ""
            read -p "按回车键继续..."
            ;;
    esac
done