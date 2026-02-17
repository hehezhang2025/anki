#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV 转 Anki 格式工具
支持将 CSV 文件转换为 Anki 可导入的 .apkg 格式
"""

import csv
import os
import sys
import random
import time
import zipfile
import json
import sqlite3
from datetime import datetime


class AnkiPackageCreator:
    """Anki 包创建器"""
    
    def __init__(self, deck_name="导入的卡组"):
        self.deck_name = deck_name
        self.deck_id = random.randrange(1 << 30, 1 << 31)
        self.model_id = random.randrange(1 << 30, 1 << 31)
        self.timestamp = int(time.time() * 1000)
        
    def create_apkg(self, csv_file, output_file):
        """
        创建 .apkg 文件
        :param csv_file: CSV 文件路径
        :param output_file: 输出的 .apkg 文件路径
        """
        print(f"📖 正在读取 CSV 文件: {os.path.basename(csv_file)}")
        
        # 读取 CSV 文件
        cards = self._read_csv(csv_file)
        if not cards:
            print("❌ CSV 文件为空或格式错误")
            return False
        
        print(f"✅ 成功读取 {len(cards)} 张卡片")
        
        # 创建临时目录
        temp_dir = f"temp_anki_{self.timestamp}"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # 创建数据库
            db_path = os.path.join(temp_dir, "collection.anki2")
            self._create_database(db_path, cards)
            
            # 创建 media 文件
            media_path = os.path.join(temp_dir, "media")
            with open(media_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            
            # 打包成 .apkg
            print(f"📦 正在打包成 Anki 格式...")
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(db_path, "collection.anki2")
                zipf.write(media_path, "media")
            
            print(f"✅ 成功创建: {os.path.basename(output_file)}")
            return True
            
        finally:
            # 清理临时文件
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def _read_csv(self, csv_file):
        """读取 CSV 文件"""
        cards = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                
                # 跳过标题行（如果有）
                first_row = next(reader, None)
                if not first_row:
                    return cards
                
                # 检查是否是标题行
                if self._is_header_row(first_row):
                    # 如果是标题行，跳过
                    pass
                else:
                    # 如果不是标题行，添加到卡片
                    if len(first_row) >= 2:
                        cards.append({
                            'front': first_row[0].strip(),
                            'back': first_row[1].strip() if len(first_row) > 1 else ''
                        })
                
                # 读取剩余行
                for row in reader:
                    if len(row) >= 2 and row[0].strip():
                        cards.append({
                            'front': row[0].strip(),
                            'back': row[1].strip() if len(row) > 1 else ''
                        })
                        
        except Exception as e:
            print(f"❌ 读取 CSV 文件失败: {e}")
            return []
        
        return cards
    
    def _is_header_row(self, row):
        """判断是否是标题行"""
        if not row:
            return False
        
        # 常见的标题关键词
        header_keywords = ['front', 'back', '正面', '背面', '问题', '答案', 'question', 'answer']
        first_cell = row[0].strip().lower()
        
        return any(keyword in first_cell for keyword in header_keywords)
    
    def _create_database(self, db_path, cards):
        """创建 Anki 数据库"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建表结构
        cursor.execute('''
            CREATE TABLE col (
                id INTEGER PRIMARY KEY,
                crt INTEGER NOT NULL,
                mod INTEGER NOT NULL,
                scm INTEGER NOT NULL,
                ver INTEGER NOT NULL,
                dty INTEGER NOT NULL,
                usn INTEGER NOT NULL,
                ls INTEGER NOT NULL,
                conf TEXT NOT NULL,
                models TEXT NOT NULL,
                decks TEXT NOT NULL,
                dconf TEXT NOT NULL,
                tags TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY,
                guid TEXT NOT NULL,
                mid INTEGER NOT NULL,
                mod INTEGER NOT NULL,
                usn INTEGER NOT NULL,
                tags TEXT NOT NULL,
                flds TEXT NOT NULL,
                sfld TEXT NOT NULL,
                csum INTEGER NOT NULL,
                flags INTEGER NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE cards (
                id INTEGER PRIMARY KEY,
                nid INTEGER NOT NULL,
                did INTEGER NOT NULL,
                ord INTEGER NOT NULL,
                mod INTEGER NOT NULL,
                usn INTEGER NOT NULL,
                type INTEGER NOT NULL,
                queue INTEGER NOT NULL,
                due INTEGER NOT NULL,
                ivl INTEGER NOT NULL,
                factor INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                lapses INTEGER NOT NULL,
                left INTEGER NOT NULL,
                odue INTEGER NOT NULL,
                odid INTEGER NOT NULL,
                flags INTEGER NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE revlog (
                id INTEGER PRIMARY KEY,
                cid INTEGER NOT NULL,
                usn INTEGER NOT NULL,
                ease INTEGER NOT NULL,
                ivl INTEGER NOT NULL,
                lastIvl INTEGER NOT NULL,
                factor INTEGER NOT NULL,
                time INTEGER NOT NULL,
                type INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('CREATE TABLE graves (usn INTEGER NOT NULL, oid INTEGER NOT NULL, type INTEGER NOT NULL)')
        
        # 插入集合数据
        col_data = self._create_col_data()
        cursor.execute('INSERT INTO col VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', col_data)
        
        # 插入笔记和卡片
        for i, card in enumerate(cards):
            note_id = self.timestamp + i
            card_id = note_id + 1000000
            
            # 插入笔记
            note_data = self._create_note_data(note_id, card)
            cursor.execute('INSERT INTO notes VALUES (?,?,?,?,?,?,?,?,?,?,?)', note_data)
            
            # 插入卡片
            card_data = self._create_card_data(card_id, note_id)
            cursor.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', card_data)
        
        conn.commit()
        conn.close()
    
    def _create_col_data(self):
        """创建集合数据"""
        now = int(time.time())
        
        models = {
            str(self.model_id): {
                "id": self.model_id,
                "name": "基础",
                "type": 0,
                "mod": now,
                "usn": -1,
                "sortf": 0,
                "did": self.deck_id,
                "tmpls": [
                    {
                        "name": "卡片 1",
                        "ord": 0,
                        "qfmt": "{{正面}}",
                        "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{背面}}",
                        "did": None,
                        "bqfmt": "",
                        "bafmt": ""
                    }
                ],
                "flds": [
                    {
                        "name": "正面",
                        "ord": 0,
                        "sticky": False,
                        "rtl": False,
                        "font": "Arial",
                        "size": 20
                    },
                    {
                        "name": "背面",
                        "ord": 1,
                        "sticky": False,
                        "rtl": False,
                        "font": "Arial",
                        "size": 20
                    }
                ],
                "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
                "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
                "latexPost": "\\end{document}",
                "latexsvg": False,
                "req": [[0, "all", [0]]]
            }
        }
        
        decks = {
            str(self.deck_id): {
                "id": self.deck_id,
                "name": self.deck_name,
                "extendRev": 50,
                "usn": -1,
                "collapsed": False,
                "newToday": [0, 0],
                "timeToday": [0, 0],
                "dyn": 0,
                "extendNew": 10,
                "conf": 1,
                "revToday": [0, 0],
                "lrnToday": [0, 0],
                "mod": now,
                "desc": ""
            },
            "1": {
                "id": 1,
                "name": "默认",
                "extendRev": 50,
                "usn": -1,
                "collapsed": False,
                "newToday": [0, 0],
                "timeToday": [0, 0],
                "dyn": 0,
                "extendNew": 10,
                "conf": 1,
                "revToday": [0, 0],
                "lrnToday": [0, 0],
                "mod": now,
                "desc": ""
            }
        }
        
        dconf = {
            "1": {
                "id": 1,
                "mod": 0,
                "name": "默认",
                "usn": 0,
                "maxTaken": 60,
                "autoplay": True,
                "timer": 0,
                "replayq": True,
                "new": {
                    "bury": True,
                    "delays": [1, 10],
                    "initialFactor": 2500,
                    "ints": [1, 4, 7],
                    "order": 1,
                    "perDay": 20
                },
                "lapse": {
                    "delays": [10],
                    "leechAction": 0,
                    "leechFails": 8,
                    "minInt": 1,
                    "mult": 0
                },
                "rev": {
                    "bury": True,
                    "ease4": 1.3,
                    "fuzz": 0.05,
                    "ivlFct": 1,
                    "maxIvl": 36500,
                    "minSpace": 1,
                    "perDay": 100
                }
            }
        }
        
        conf = {
            "curDeck": self.deck_id,
            "activeDecks": [self.deck_id],
            "newSpread": 0,
            "collapseTime": 1200,
            "timeLim": 0,
            "estTimes": True,
            "dueCounts": True,
            "curModel": self.model_id,
            "nextPos": 1,
            "sortType": "noteFld",
            "sortBackwards": False,
            "addToCur": True
        }
        
        return (
            1,
            now,
            now,
            now,
            11,
            0,
            0,
            0,
            json.dumps(conf),
            json.dumps(models),
            json.dumps(decks),
            json.dumps(dconf),
            json.dumps({})
        )
    
    def _create_note_data(self, note_id, card):
        """创建笔记数据"""
        import hashlib
        
        guid = f"{note_id:x}"
        flds = f"{card['front']}\x1f{card['back']}"
        sfld = card['front']
        csum = int(hashlib.sha1(sfld.encode('utf-8')).hexdigest()[:8], 16)
        
        return (
            note_id,
            guid,
            self.model_id,
            int(time.time()),
            -1,
            "",
            flds,
            sfld,
            csum,
            0,
            ""
        )
    
    def _create_card_data(self, card_id, note_id):
        """创建卡片数据"""
        return (
            card_id,
            note_id,
            self.deck_id,
            0,
            int(time.time()),
            -1,
            0,
            0,
            note_id,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ""
        )


def main():
    """主函数"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║          CSV 转 Anki 格式工具 v1.0                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # 获取 CSV 文件路径
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        print("请输入 CSV 文件路径（或拖拽文件到此窗口）：")
        csv_file = input().strip().strip('"').strip("'")
    
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print(f"❌ 文件不存在: {csv_file}")
        input("\n按回车键退出...")
        return
    
    # 检查文件扩展名
    if not csv_file.lower().endswith('.csv'):
        print(f"❌ 请提供 CSV 格式文件（当前: {os.path.splitext(csv_file)[1]}）")
        input("\n按回车键退出...")
        return
    
    # 生成输出文件名
    base_name = os.path.splitext(csv_file)[0]
    output_file = f"{base_name}.apkg"
    
    # 如果输出文件已存在，添加时间戳
    if os.path.exists(output_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{base_name}_{timestamp}.apkg"
    
    print()
    print("=" * 60)
    print(f"📄 输入文件: {os.path.basename(csv_file)}")
    print(f"📦 输出文件: {os.path.basename(output_file)}")
    print("=" * 60)
    print()
    
    # 创建 Anki 包
    creator = AnkiPackageCreator(deck_name="导入的卡组")
    success = creator.create_apkg(csv_file, output_file)
    
    if success:
        print()
        print("=" * 60)
        print("🎉 转换完成！")
        print(f"📍 文件位置: {os.path.abspath(output_file)}")
        print()
        print("💡 使用方法：")
        print("   1. 打开 Anki 应用")
        print("   2. 点击「文件」→「导入」")
        print("   3. 选择生成的 .apkg 文件")
        print("=" * 60)
    else:
        print()
        print("❌ 转换失败")
    
    print()
    input("按回车键退出...")


if __name__ == "__main__":
    main()
