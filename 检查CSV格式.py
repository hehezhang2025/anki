#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV 格式检查工具
验证 CSV 文件是否符合 Anki 转换要求
"""

import csv
import os
import sys
import chardet


def check_csv_format(csv_file):
    """检查 CSV 文件格式"""
    print(f"🔍 检查文件: {os.path.basename(csv_file)}")
    print("=" * 50)
    
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print("❌ 文件不存在")
        return False
    
    # 检查文件扩展名
    if not csv_file.lower().endswith('.csv'):
        print(f"⚠️  文件扩展名不是 .csv (当前: {os.path.splitext(csv_file)[1]})")
    else:
        print("✅ 文件扩展名正确")
    
    # 检查文件编码
    try:
        with open(csv_file, 'rb') as f:
            raw_data = f.read()
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result['encoding']
            confidence = encoding_result['confidence']
        
        print(f"📝 文件编码: {encoding} (置信度: {confidence:.2%})")
        
        if encoding.lower() in ['utf-8', 'utf-8-sig']:
            print("✅ 编码格式正确")
        else:
            print("⚠️  建议使用 UTF-8 编码")
    except Exception as e:
        print(f"❌ 编码检查失败: {e}")
        return False
    
    # 检查 CSV 内容
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if not rows:
            print("❌ 文件为空")
            return False
        
        print(f"📊 总行数: {len(rows)}")
        
        # 检查列数
        if len(rows[0]) < 2:
            print("❌ 第一行少于 2 列，需要至少 2 列（正面,背面）")
            return False
        else:
            print(f"✅ 列数: {len(rows[0])} (≥2)")
        
        # 检查是否有标题行
        first_row = rows[0]
        header_keywords = ['front', 'back', '正面', '背面', '问题', '答案', 'question', 'answer']
        is_header = any(keyword in first_row[0].lower() for keyword in header_keywords)
        
        if is_header:
            print("✅ 检测到标题行，将自动跳过")
            data_rows = rows[1:]
        else:
            print("ℹ️  未检测到标题行，第一行将作为数据")
            data_rows = rows
        
        # 统计有效数据行
        valid_rows = 0
        empty_rows = 0
        
        for i, row in enumerate(data_rows, start=2 if is_header else 1):
            if len(row) >= 2 and row[0].strip():
                valid_rows += 1
            elif not row[0].strip():
                empty_rows += 1
                print(f"⚠️  第 {i} 行正面为空")
        
        print(f"📈 有效卡片: {valid_rows} 张")
        if empty_rows > 0:
            print(f"⚠️  空行: {empty_rows} 行")
        
        # 显示前几行预览
        print("\n📋 数据预览:")
        print("-" * 50)
        preview_rows = data_rows[:5]
        for i, row in enumerate(preview_rows, start=1):
            if len(row) >= 2:
                front = row[0][:30] + "..." if len(row[0]) > 30 else row[0]
                back = row[1][:30] + "..." if len(row[1]) > 30 else row[1]
                print(f"  {i}. {front} → {back}")
        
        if len(data_rows) > 5:
            print(f"  ... 还有 {len(data_rows) - 5} 行")
        
        # 总结
        print("\n" + "=" * 50)
        if valid_rows > 0:
            print("✅ CSV 格式检查通过！")
            print(f"📦 可以生成 {valid_rows} 张 Anki 卡片")
            return True
        else:
            print("❌ 没有有效的卡片数据")
            return False
            
    except Exception as e:
        print(f"❌ 读取 CSV 文件失败: {e}")
        return False


def main():
    """主函数"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║            CSV 格式检查工具 v1.0                      ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # 获取文件路径
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        print("请输入 CSV 文件路径（或拖拽文件到此窗口）：")
        csv_file = input().strip().strip('"').strip("'")
    
    print()
    
    # 检查格式
    success = check_csv_format(csv_file)
    
    print()
    if success:
        print("💡 建议：")
        print("   1. 使用 '一键转换.command' 转换此文件")
        print("   2. 或运行: python3 csv_to_anki.py", os.path.basename(csv_file))
    else:
        print("💡 修复建议：")
        print("   1. 确保文件是 UTF-8 编码")
        print("   2. 确保至少有 2 列（正面,背面）")
        print("   3. 确保有实际的数据行")
        print("   4. 参考 '示例.csv' 的格式")
    
    print()
    input("按回车键退出...")


if __name__ == "__main__":
    main()