# 贡献指南

感谢你考虑为本项目做出贡献！🎉

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请：

1. 在 GitHub Issues 中搜索是否已有相关问题
2. 如果没有，创建新的 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 你的环境信息（操作系统、Python 版本等）

### 提出新功能

如果你有功能建议：

1. 先在 Issues 中讨论你的想法
2. 说明为什么这个功能有用
3. 如果可能，提供使用场景示例

### 提交代码

1. **Fork 本仓库**
   ```bash
   # 点击 GitHub 页面的 Fork 按钮
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/你的用户名/codebuddy_anki.git
   cd codebuddy_anki
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **进行修改**
   - 保持代码简洁易读
   - 添加必要的注释
   - 遵循现有代码风格

5. **测试你的修改**
   ```bash
   # 运行测试脚本
   ./测试转换.sh
   ```

6. **提交修改**
   ```bash
   git add .
   git commit -m "Add: 添加某某功能"
   ```
   
   提交信息格式：
   - `Add: 添加新功能`
   - `Fix: 修复某个问题`
   - `Update: 更新某个功能`
   - `Docs: 更新文档`

7. **推送到你的 Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

8. **创建 Pull Request**
   - 在 GitHub 上打开你的 Fork
   - 点击 "New Pull Request"
   - 填写 PR 描述，说明你的改动

## 代码规范

- 使用 Python 3.x 标准库
- 保持代码简洁，避免过度复杂
- 添加适当的错误处理
- 遵循 PEP 8 风格指南

## 文档

如果你的修改影响用户使用，请同时更新：
- `README.md`
- `使用说明.txt`
- 相关注释

## 问题讨论

如有任何问题，欢迎在 Issues 中讨论！

---

再次感谢你的贡献！❤️
