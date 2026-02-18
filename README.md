# CSV 转 Anki 格式工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/weipengzhang/codebuddy_anki)

> **一键转换 CSV 文件为 Anki 可导入的 .apkg 格式**

## 📦 安装

### 方法1：从 GitHub 克隆
```bash
git clone https://github.com/weipengzhang/codebuddy_anki.git
cd codebuddy_anki
```

### 方法2：直接下载
[下载最新版本](https://github.com/weipengzhang/codebuddy_anki/archive/refs/heads/main.zip)

解压后即可使用，无需安装额外依赖！

---

## 📦 功能特点

- ✅ 支持标准 CSV 格式（UTF-8 编码）
- ✅ 自动识别并跳过标题行
- ✅ 生成 Anki 标准 .apkg 格式
- ✅ 支持拖拽文件快速转换
- ✅ 自动处理文件名冲突
- ✅ 零依赖，使用 Python 标准库

---

## 🚀 快速开始

### 🎯 工具箱启动器（推荐）

**双击 `启动工具箱.command`** - 图形化菜单，包含所有功能

### 方式1：拖拽转换（最简单）

1. **双击打开** `一键转换.command`
2. **拖拽 CSV 文件** 到终端窗口
3. **按回车**，自动转换完成

### 方式2：拖拽到图标

直接将 CSV 文件**拖拽到** `一键转换.command` 图标上，自动转换。

### 方式3：批量转换

**双击 `批量转换.command`** - 一次转换多个 CSV 文件

### 方式4：格式检查

**双击 `检查格式.command`** - 验证 CSV 文件格式是否正确

### 方式5：命令行

```bash
# 转换指定文件
python3 csv_to_anki.py 你的文件.csv

# 批量转换
./批量转换.command

# 格式检查
python3 检查CSV格式.py 你的文件.csv
```

---

## 📄 CSV 文件格式要求

### 标准格式（推荐）

```csv
正面,背面
What is Python?,一种编程语言
Hello,你好
```

### 简化格式（无标题行）

```csv
What is Python?,一种编程语言
Hello,你好
Apple,苹果
```

### 格式说明

- **第一列**：卡片正面（问题）
- **第二列**：卡片背面（答案）
- **编码**：UTF-8（推荐）或 UTF-8 with BOM
- **分隔符**：英文逗号 `,`

---

## 📝 示例

### 示例 CSV 文件

创建一个名为 `english_words.csv` 的文件：

```csv
front,back
apple,苹果
banana,香蕉
cat,猫
dog,狗
```

### 转换后

生成 `english_words.apkg` 文件，包含 4 张卡片。

---

## 💡 使用技巧

### 1. 批量转换

将多个 CSV 文件依次拖拽转换即可。

### 2. 文件名冲突

如果 `.apkg` 文件已存在，会自动添加时间戳：
```
单词表.apkg
单词表_20260105_143052.apkg  ← 新生成
```

### 3. 制作 CSV 文件

**推荐工具：**
- Excel / Numbers：另存为 CSV (UTF-8)
- Google Sheets：文件 → 下载 → CSV
- 文本编辑器：手动编写

---

## 📥 导入到 Anki

### 步骤

1. **打开 Anki 应用**
2. 点击菜单：**文件** → **导入**
3. 选择生成的 `.apkg` 文件
4. 确认导入设置
5. ✅ 完成！

### 导入选项

- **牌组名称**：默认为「导入的卡组」
- **笔记类型**：基础（正面/背面）
- **重复处理**：根据需要选择

---

## 🔧 高级配置

### 自定义牌组名称

编辑 `csv_to_anki.py` 第 16 行：

```python
def __init__(self, deck_name="导入的卡组"):  # 修改这里
```

改为：

```python
def __init__(self, deck_name="我的单词本"):
```

### 支持多列

当前版本支持 2 列（正面/背面）。如需更多字段，可以修改代码中的 `flds` 字段定义。

---

## ❓ 常见问题

### Q1: 转换后中文乱码？

**原因：** CSV 文件编码不是 UTF-8

**解决：**
- Excel: 另存为 → CSV UTF-8（逗号分隔）
- 文本编辑器：保存时选择 UTF-8 编码

### Q2: 提示文件格式错误？

**检查：**
1. 文件扩展名是否为 `.csv`
2. 至少有 2 列数据
3. 逗号分隔符正确

### Q3: 导入 Anki 后卡片为空？

**原因：** CSV 文件只有标题行，没有实际数据

**解决：** 确保 CSV 有至少一行数据

### Q4: 需要安装什么软件？

**必需：**
- ✅ Python 3.x（macOS 自带）

**不需要：**
- ❌ 不需要安装 Anki 到电脑（手机 App 即可）
- ❌ 不需要安装额外的 Python 包

---

## 📂 项目结构

```
codebuddy_anki/
├── 🎯 启动工具箱.command      # 主启动器（推荐使用）
├── 🔄 一键转换.command        # 单文件转换
├── 📦 批量转换.command        # 批量转换
├── 🔍 检查格式.command        # 格式验证
├── csv_to_anki.py           # 核心转换脚本
├── 检查CSV格式.py           # 格式检查脚本
├── 📖 README.md             # 详细说明（本文件）
├── 📄 使用说明.txt           # 快速指南
├── 📝 示例.csv              # 基础示例
├── 📚 英语单词.csv          # 英语词汇示例
├── 💻 编程术语.csv          # 编程术语示例
└── 🗾 日语基础.csv          # 日语基础示例
```

---

## 🎯 使用场景

- 📚 **背单词**：英语、日语等外语学习
- 📖 **记忆知识点**：考试复习、知识积累
- 🔤 **术语记忆**：专业术语、行业知识
- 💻 **代码记忆**：编程语法、API 记忆

---

## 🔄 更新日志

### v1.0.0 - 2026-01-05

- ✨ 首次发布
- ✅ 支持 CSV 转 Anki .apkg 格式
- ✅ 支持拖拽文件转换
- ✅ 自动识别标题行
- ✅ 自动处理文件名冲突

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

- 📝 [提交 Issue](https://github.com/weipengzhang/codebuddy_anki/issues)
- 🔧 [提交 Pull Request](https://github.com/weipengzhang/codebuddy_anki/pulls)
- 📖 查看 [贡献指南](CONTRIBUTING.md)

### 贡献者

感谢所有为本项目做出贡献的开发者！

---

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐️

---

## 📞 联系方式

- 💬 [GitHub Issues](https://github.com/weipengzhang/codebuddy_anki/issues)
- 📧 Email: [你的邮箱]

---

**提示：** 首次使用建议先用示例 CSV 文件测试，熟悉流程后再转换正式文件。
