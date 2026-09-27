# 安装

本指南介绍安装与配置 Purepy 的各种方式。

## 环境要求

- Python 3.10 或更高版本
- pip（Python 包安装器）

## 安装方式

### 1. 从 PyPI 安装（推荐）

安装 Purepy 最简单的方式是用 pip：

```bash
pip install yonld-purepy
```

### 2. 从源码安装

如果你想要最新的开发版本：

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
pip install -e .
```

### 3. 安装到虚拟环境（推荐）

建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv purepy-env

# 激活虚拟环境
# Windows 下：
purepy-env\Scriptsctivate
# macOS/Linux 下：
source purepy-env/bin/activate

# 安装 Purepy
pip install yonld-purepy
```

## 验证安装

安装之后，验证一下 Purepy 是否工作正常：

```python
# test_purepy.py
from pure.html import div, h1, p


def test_installation():
    element = div(
        h1('Purepy 安装测试'),
        p('如果你能看到这行字，说明 Purepy 工作正常！'),
    ).class_name('test-container')

    print('HTML 输出：')
    element.print()

    # 保存到文件
    element.save('test.html')
    print("\nHTML 文件已保存为 'test.html'")


if __name__ == '__main__':
    test_installation()
```

运行测试：

```bash
python test_purepy.py
```

预期输出：

```html
<div class="test-container"><h1>Purepy 安装测试</h1><p>如果你能看到这行字，说明 Purepy 工作正常！</p></div>
```

::: tip 输出不会被重新缩进
Purepy 输出的就是它渲染的字节，不会自动换行排版。 :::

## 开发环境搭建

如果你打算为 Purepy 贡献代码，或需要开发版本：

### 1. 克隆仓库

```bash
git clone https://github.com/YonLD/purepy.git
cd purepy
```

### 2. 创建开发环境

```bash
python -m venv dev-env
source dev-env/bin/activate  # Windows 下：dev-env\Scriptsctivate
```

### 3. 以开发模式安装

```bash
pip install -e .
```

### 4. 安装开发依赖

```bash
pip install -r requirements-dev.txt  # 如果存在该文件
```

### 5. 运行测试

```bash
python -m pytest tests/  # 如果存在测试
```

## IDE 配置

### Visual Studio Code

要让 VS Code 获得最佳开发体验：

1. 安装 Python 扩展
2. 配置好虚拟环境
3. 指定 Python 解释器

创建 `.vscode/settings.json`：

```json
{
    "python.defaultInterpreterPath": "./purepy-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### PyCharm

1. 在 PyCharm 中打开项目
2. 依次进入 File → Settings → Project → Python Interpreter
3. 添加你的虚拟环境解释器
4. 启用代码补全与类型提示

## 项目结构

新建 Purepy 项目时，可以参考这个结构：

```
my-purepy-project/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── header.py
│   │   ├── footer.py
│   │   └── card.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   └── about.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── output/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── requirements.txt
└── main.py
```

`requirements.txt` 示例：

```txt
yonld-purepy>=1.0.0
```

`main.py` 示例：

```python
from src.pages.about import create_about_page
from src.pages.home import create_home_page


def build_site():
    # 生成页面
    home = create_home_page()
    about = create_about_page()

    # 保存页面
    home.save('output/index.html')
    about.save('output/about.html')

    print('站点构建成功！')


if __name__ == '__main__':
    build_site()
```

## 常见问题

### 导入错误

如果遇到导入错误：

```python
# 错误
from purepy.html import div  # 这样不行

# 正确
from pure.html import div
```

### 找不到模块

如果遇到「Module not found」错误：

1. 确认 Purepy 已安装：`pip list | grep yonld-purepy`
2. 检查 Python 路径：`python -c "import sys; print(sys.path)"`
3. 确认虚拟环境已激活

### 权限错误

在某些系统上，你可能需要使用 `pip install --user yonld-purepy`，或者以更高权限运行。

## 更新 Purepy

升级到最新版本：

```bash
pip install --upgrade yonld-purepy
```

查看当前版本：

```python
import pure

print(pure.__version__)
```

版本号来自已安装的发行版元数据，因此它与 `pyproject.toml` 保持一致。

## 卸载

卸载 Purepy：

```bash
pip uninstall yonld-purepy
```

## 下一步

装好 Purepy 之后：

1. [快速开始](/zh/guide/getting-started)——写出你的第一个 Purepy 应用
2. [基本用法](/zh/guide/basic-usage)——掌握核心概念
3. [API 参考](/zh/api/)——浏览全部可用功能

## 获取帮助

如果遇到问题：

1. 先查[文档](/zh/guide/)
2. 搜索已有的 [GitHub issue](https://github.com/YonLD/purepy/issues)
3. 必要时新建 issue

## 系统要求

### 最低要求

- Python 3.10+
- 50MB 磁盘空间
- 任意操作系统（Windows、macOS、Linux）

### 推荐配置

- Python 3.11+
- 虚拟环境
- 支持 Python 的代码编辑器
- Git（开发时需要）
