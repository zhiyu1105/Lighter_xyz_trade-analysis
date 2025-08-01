# 贡献指南

感谢您对 TradeAnalysis 项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 Bug 报告
- 💡 功能建议
- 📝 文档改进
- 🔧 代码贡献
- 🧪 测试用例

## 如何贡献

### 1. Fork 项目

1. 访问 [TradeAnalysis GitHub 页面](https://github.com/zhiyu1105/Lighter_xyz_trade-analysis)
2. 点击右上角的 "Fork" 按钮
3. 这将在您的 GitHub 账户下创建一个副本

### 2. 克隆您的 Fork

```bash
git clone https://github.com/zhiyu1105/Lighter_xyz_trade-analysis.git
cd trade-analysis
```

### 3. 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -e ".[dev]"
```

### 4. 创建功能分支

```bash
git checkout -b feature/your-feature-name
```

### 5. 进行更改

- 编写代码
- 添加测试
- 更新文档
- 确保代码符合项目规范

### 6. 运行测试

```bash
# 运行所有测试
pytest

# 运行代码检查
flake8 .
black --check .
mypy .
```

### 7. 提交更改

```bash
git add .
git commit -m "feat: add your feature description"
```

### 8. 推送更改

```bash
git push origin feature/your-feature-name
```

### 9. 创建 Pull Request

1. 访问您的 GitHub Fork 页面
2. 点击 "Compare & pull request"
3. 填写 PR 描述，包括：
   - 更改的目的
   - 解决的问题
   - 测试情况
   - 相关 Issue 链接

## 代码规范

### Python 代码风格

我们使用以下工具来保持代码质量：

- **Black**: 代码格式化
- **Flake8**: 代码检查
- **MyPy**: 类型检查

### 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型包括：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 分支命名规范

- `feature/feature-name`: 新功能
- `fix/bug-description`: Bug 修复
- `docs/documentation-update`: 文档更新
- `refactor/refactoring-description`: 代码重构

## 报告 Bug

如果您发现了 Bug，请：

1. 检查 [Issues](https://github.com/yourusername/trade-analysis/issues) 是否已有相关报告
2. 创建新的 Issue，包含：
   - Bug 的详细描述
   - 重现步骤
   - 预期行为
   - 实际行为
   - 环境信息（操作系统、Python 版本等）
   - 错误日志（如果有）

## 功能建议

如果您有功能建议，请：

1. 检查 [Issues](https://github.com/yourusername/trade-analysis/issues) 是否已有相关讨论
2. 创建新的 Issue，包含：
   - 功能的详细描述
   - 使用场景
   - 预期效果
   - 可能的实现方案（如果有）

## 文档贡献

文档改进同样重要！您可以：

- 修正拼写错误
- 改进示例代码
- 添加更多使用场景
- 翻译文档
- 添加更多图表和说明

## 测试贡献

测试用例的贡献非常欢迎！您可以：

- 添加单元测试
- 添加集成测试
- 改进现有测试
- 添加性能测试

## 发布流程

### 版本号规范

我们使用 [Semantic Versioning](https://semver.org/)：

- `MAJOR.MINOR.PATCH`
- `MAJOR`: 不兼容的 API 更改
- `MINOR`: 向后兼容的功能添加
- `PATCH`: 向后兼容的 Bug 修复

### 发布步骤

1. 更新版本号（在 `setup.py` 中）
2. 更新 `CHANGELOG.md`
3. 创建 Release Tag
4. 发布到 PyPI（如果需要）

## 社区行为准则

我们致力于为每个人提供友好、安全和欢迎的环境。请：

- 尊重他人
- 使用包容性语言
- 接受建设性批评
- 关注社区利益
- 对其他社区成员表现出同理心

## 联系方式

如果您有任何问题或需要帮助：

- 创建 [Issue](https://github.com/zhiyu1105/Lighter_xyz_trade-analysis/issues)
- 发送邮件到：your.email@example.com
- 加入我们的讨论区

## 致谢

感谢所有为这个项目做出贡献的开发者！您的贡献让这个项目变得更好。

---

**再次感谢您的贡献！** 🎉 