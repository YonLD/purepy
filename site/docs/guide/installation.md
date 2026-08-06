# 安装

本指南将帮助你安装 Purepy。

## 环境要求

- Python 3.8 或更高版本
- pip

## 安装方法

### 使用 pip 安装

在你的项目目录中运行：

```bash
pip install yonld-purepy
```

### 验证安装

创建一个简单的测试文件 `test.py`：

```python
from pure.html import div, h1, p

div(
    h1('Purepy 安装成功'),
    p('恭喜！Purepy 已经正确安装。')
).to_print()
```

运行测试文件：

```bash
python test.py
```

如果看到输出的 HTML，说明安装成功。

## 开发环境安装

如果你想参与 Purepy 的开发或运行测试，可以从源码安装：

```bash
# 克隆仓库
git clone https://github.com/YonLD/purepy.git
cd purepy

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"
```

## 下一步

- [快速开始](/guide/getting-started) - 创建你的第一个 Purepy 应用
- [基本概念](/guide/concepts) - 了解 Purepy 的核心概念
- [基本用法](/guide/basic-usage) - 学习基础语法
