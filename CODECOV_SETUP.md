# 📊 Codecov 设置指南

## 问题说明

当前 GitHub Actions 中的 Codecov 上传遇到了速率限制错误：
```
429 - {"message":"Rate limit reached. Please upload with the Codecov repository upload token to resolve issue."}
```

这是因为没有使用 Codecov 仓库上传令牌。

## 🔧 解决方案

### 方法 1: 设置 Codecov 令牌（推荐）

1. **访问 Codecov 网站**：
   - 打开 https://codecov.io
   - 使用 GitHub 账户登录

2. **添加仓库**：
   - 点击 "Add new repository"
   - 选择 `zhiyu1105/Lighter_xyz_trade-analysis`
   - 授权访问

3. **获取上传令牌**：
   - 在仓库设置中找到 "Upload Token"
   - 复制令牌值

4. **设置 GitHub Secrets**：
   - 访问：https://github.com/zhiyu1105/Lighter_xyz_trade-analysis/settings/secrets/actions
   - 点击 "New repository secret"
   - 名称：`CODECOV_TOKEN`
   - 值：粘贴从 Codecov 复制的令牌
   - 点击 "Add secret"

### 方法 2: 暂时禁用 Codecov（临时方案）

如果您暂时不想设置 Codecov，可以注释掉相关步骤：

```yaml
# - name: Upload coverage to Codecov
#   uses: codecov/codecov-action@v3
#   with:
#     file: ./coverage.xml
#     flags: unittests
#     name: codecov-umbrella
#     fail_ci_if_error: false
#     token: ${{ secrets.CODECOV_TOKEN }}
```

### 方法 3: 使用公共令牌（不推荐）

可以暂时使用公共令牌，但这不是最佳实践：

```yaml
token: ${{ secrets.CODECOV_TOKEN || 'public-token' }}
```

## 🎯 推荐操作

1. **立即操作**：设置 Codecov 令牌（方法 1）
2. **临时方案**：暂时禁用 Codecov 上传（方法 2）
3. **长期方案**：完成 Codecov 设置以获得完整的覆盖率报告

## 📊 Codecov 的好处

设置完成后，您将获得：
- ✅ 代码覆盖率徽章
- ✅ 详细的覆盖率报告
- ✅ 覆盖率趋势图
- ✅ 未覆盖代码的详细分析
- ✅ 与 GitHub 的集成

## 🔍 验证设置

设置完成后：
1. 推送代码触发新的 GitHub Actions 运行
2. 检查 Codecov 上传是否成功
3. 在仓库主页查看覆盖率徽章
4. 访问 Codecov 网站查看详细报告

## 📞 获取帮助

如果遇到问题：
- Codecov 文档：https://docs.codecov.io/
- GitHub Actions 文档：https://docs.github.com/en/actions
- 项目 Issues：https://github.com/zhiyu1105/Lighter_xyz_trade-analysis/issues 