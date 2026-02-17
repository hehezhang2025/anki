#!/bin/bash
# CSV 转 Anki 格式 - 批量转换工具

cd "$(dirname "$0")" || exit

echo "╔════════════════════════════════════════════════════════╗"
echo "║          CSV 转 Anki - 批量转换工具                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 查找当前目录下的所有 CSV 文件
csv_files=(*.csv)

if [ ${#csv_files[@]} -eq 1 ] && [ "${csv_files[0]}" = "*.csv" ]; then
    echo "❌ 当前目录没有找到 CSV 文件"
    echo ""
    echo "请将 CSV 文件放到此目录下，然后重新运行"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo "📁 找到以下 CSV 文件："
echo ""
for i in "${!csv_files[@]}"; do
    echo "  $((i+1)). ${csv_files[i]}"
done
echo ""

read -p "是否转换所有文件？(y/n): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 开始批量转换..."
    echo ""
    
    success_count=0
    total_count=${#csv_files[@]}
    
    for csv_file in "${csv_files[@]}"; do
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📄 转换: $csv_file"
        
        # 运行转换（非交互模式）
        if python3 -c "
import sys
sys.path.append('.')
from csv_to_anki import AnkiPackageCreator
import os

csv_file = '$csv_file'
base_name = os.path.splitext(csv_file)[0]
output_file = f'{base_name}.apkg'

# 如果输出文件已存在，添加时间戳
if os.path.exists(output_file):
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'{base_name}_{timestamp}.apkg'

creator = AnkiPackageCreator(deck_name=f'导入的卡组 - {base_name}')
success = creator.create_apkg(csv_file, output_file)
exit(0 if success else 1)
        "; then
            echo "✅ 转换成功"
            ((success_count++))
        else
            echo "❌ 转换失败"
        fi
        echo ""
    done
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 批量转换完成！"
    echo ""
    echo "📊 转换结果："
    echo "   ✅ 成功: $success_count 个文件"
    echo "   ❌ 失败: $((total_count - success_count)) 个文件"
    echo "   📦 总计: $total_count 个文件"
    echo ""
    echo "📁 生成的 .apkg 文件在当前目录中"
else
    echo ""
    echo "❌ 取消转换"
fi

echo ""
read -p "按回车键退出..."