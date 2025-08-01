#!/usr/bin/env python3
"""
GitHub 上传准备检查脚本
检查项目是否准备好上传到 GitHub
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (缺失)")
        return False

def check_directory_exists(dir_path, description):
    """检查目录是否存在"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (缺失)")
        return False

def check_file_content(file_path, required_strings, description):
    """检查文件内容是否包含必需字符串"""
    if not os.path.exists(file_path):
        print(f"❌ {description}: {file_path} (文件不存在)")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing_strings = []
        for required_string in required_strings:
            if required_string not in content:
                missing_strings.append(required_string)
        
        if missing_strings:
            print(f"⚠️  {description}: {file_path} (缺少: {', '.join(missing_strings)})")
            return False
        else:
            print(f"✅ {description}: {file_path}")
            return True
    except Exception as e:
        print(f"❌ {description}: {file_path} (读取错误: {e})")
        return False

def main():
    """主检查函数"""
    print("🔍 检查 TradeAnalysis 项目 GitHub 上传准备状态")
    print("=" * 60)
    
    # 检查必需文件
    required_files = [
        ("README.md", "项目文档"),
        ("LICENSE", "许可证文件"),
        ("requirements.txt", "Python 依赖"),
        ("setup.py", "项目打包配置"),
        ("pyproject.toml", "现代 Python 项目配置"),
        ("MANIFEST.in", "分发包配置"),
        ("CHANGELOG.md", "变更日志"),
        ("CONTRIBUTING.md", "贡献指南"),
        ("BADGES.md", "项目徽章"),
        ("GITHUB_UPLOAD_GUIDE.md", "GitHub 上传指南"),
        (".gitignore", "Git 忽略文件"),
        ("app.py", "Streamlit 应用"),
        ("example_analysis.py", "示例脚本"),
    ]
    
    # 检查必需目录
    required_dirs = [
        ("trade_analyzer", "核心代码包"),
        ("tests", "测试文件"),
        ("data", "数据文件夹"),
        ("analysis_charts", "图表输出"),
        (".github/workflows", "GitHub Actions 配置"),
    ]
    
    # 检查 GitHub Actions 工作流文件
    workflow_files = [
        (".github/workflows/python-app.yml", "自动化测试工作流"),
        (".github/workflows/pages.yml", "GitHub Pages 部署工作流"),
    ]
    
    # 检查测试文件
    test_files = [
        ("tests/__init__.py", "测试包初始化"),
        ("tests/test_trade_analyzer.py", "核心功能测试"),
    ]
    
    # 检查核心代码文件
    core_files = [
        ("trade_analyzer/__init__.py", "核心包初始化"),
        ("trade_analyzer/data_processor.py", "数据处理模块"),
        ("trade_analyzer/analyzer.py", "分析计算模块"),
        ("trade_analyzer/visualizer.py", "可视化模块"),
    ]
    
    # 执行检查
    all_passed = True
    
    print("\n📄 检查必需文件:")
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    print("\n📁 检查必需目录:")
    for dir_path, description in required_dirs:
        if not check_directory_exists(dir_path, description):
            all_passed = False
    
    print("\n⚙️ 检查 GitHub Actions 工作流:")
    for file_path, description in workflow_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    print("\n🧪 检查测试文件:")
    for file_path, description in test_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    print("\n🔧 检查核心代码文件:")
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    # 检查文件内容
    print("\n📋 检查文件内容:")
    
    # 检查 README.md 是否包含关键信息
    readme_checks = [
        "交易数据分析",
        "快速开始",
        "安装依赖",
        "streamlit run app.py"
    ]
    if not check_file_content("README.md", readme_checks, "README.md 包含关键信息"):
        all_passed = False
    
    # 检查 requirements.txt 是否包含关键依赖
    requirements_checks = [
        "pandas",
        "numpy",
        "matplotlib",
        "streamlit"
    ]
    if not check_file_content("requirements.txt", requirements_checks, "requirements.txt 包含关键依赖"):
        all_passed = False
    
    # 检查 .gitignore 是否包含 Python 相关内容
    gitignore_checks = [
        "__pycache__",
        "*.py[cod]",
        ".venv",
        "venv"
    ]
    if not check_file_content(".gitignore", gitignore_checks, ".gitignore 包含 Python 相关内容"):
        all_passed = False
    
    # 检查 LICENSE 是否包含 MIT 许可证
    license_checks = [
        "MIT License",
        "Permission is hereby granted"
    ]
    if not check_file_content("LICENSE", license_checks, "LICENSE 包含 MIT 许可证"):
        all_passed = False
    
    # 总结
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 恭喜！项目已准备好上传到 GitHub！")
        print("\n📋 下一步操作:")
        print("1. 更新配置文件中的 GitHub 用户名")
        print("2. 运行: git init")
        print("3. 运行: git add .")
        print("4. 运行: git commit -m 'feat: initial commit'")
        print("5. 在 GitHub 创建仓库")
        print("6. 运行: git remote add origin <repository-url>")
        print("7. 运行: git push -u origin main")
        print("\n📖 详细步骤请参考: GITHUB_UPLOAD_GUIDE.md")
    else:
        print("❌ 项目还需要一些调整才能上传到 GitHub")
        print("\n🔧 请修复上述问题后重新运行此检查脚本")
    
    print("\n" + "=" * 60)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 