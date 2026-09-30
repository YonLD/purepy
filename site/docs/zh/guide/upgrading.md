# 升级指南

**本页内容**：运行环境要求、升级步骤与回滚方法。

## 环境要求

| 方面 | 要求 | 说明 |
| --- | --- | --- |
| 运行时 | Python 3.10+ | 用生产环境实际使用的 Python 版本做测试。 |
| 依赖 | 通过 PyPI 安装 | `import pure` 即可——没有构建步骤，也不需要 require 自动加载器。 |
| 生产 | 字节码缓存（可选） | 加载生成的 `*.pure.py` 和 `*.plain.py` 文件时有帮助。 |

## 升级清单

升级到某个正式版本时，更新应用里的版本约束并执行：

```bash
pip install --upgrade purepy
```

如果跟随默认分支，请在应用中固定经过测试的 commit，而不是自己编一个版本号。部署
该 commit 之前：

1. 阅读 [CHANGELOG](https://github.com/YonLD/purepy/blob/main/CHANGELOG.md)，
   了解改了什么、读者需要做什么。
2. 对组件与 shape 单元运行 `pure check <paths>`。
3. 重新生成严格产物与 plain 产物：

   ```bash
   pure compile <paths>
   pure compile --plain <paths>
   pure compile --check --plain <paths>
   ```

4. 如果应用使用了 `Compile.cachePath()`，在版本要求重新生成时，只删除属于 Purepy
   的缓存文件。这个操作有明确的 API：`Compile.clearCache()`。
5. 验证渲染输出与文档头，然后把源码与生成的产物一起部署。

不要手工编辑 `*.pure.py` 或 `*.plain.py`。它们内含缓存版本或 shape 指纹契约，必须
由配套的编译器重新生成。

::: warning 生成产物会对照编译器版本校验
`.pure.py` 文件会记录它构建时的 `CACHE_VERSION`，两者不一致时会抛出
`stale purepy artifact: generated for cache version N; run pure compile to
rebuild`。plain 视图用同样的方式记录 shape 指纹。这是有意设计的失败，而不是悄悄
产出错误文档——所以请把这条消息当作它字面所说的指令来处理。
:::

## 回滚

如果部署失败，把应用源码和它的生成产物作为一个整体回滚。然后清空 Purepy 的
渲染器缓存，重新执行 `pure compile --check`，并检查第一个出问题的路由。把已知良好
的产物和它的源码放在一起，比只恢复其中之一更安全。

针对具体症状的修复方法，请继续阅读
[故障排查](/zh/guide/troubleshooting)。
