# Codex百万上下文，需手动开启

GPT-6 Astra 支持百万级上下文，但 Codex 默认窗口目前仍约 258K，需要手动配置扩大。方法放在图里了。

配置文件位置：
Windows：%USERPROFILE%\.codex\config.toml
macOS / Linux：~/.codex/config.toml

把下面两行放在文件顶部（任何 [分组] 之前）；已有同名配置就修改，不要重复添加：

```toml
model_context_window = 1000000
model_auto_compact_token_limit = 900000
```

保存后重启 Codex，新建任务，在模型选择器中选 GPT-6 Astra，再查看窗口大小。

这两行是全局设置，不会自动切换模型，也不只对 Astra 生效。换到其他模型，Codex 会按该模型的上限调整窗口和自动压缩阈值：支持大窗口的也会尝试扩大，小窗口的不会被强行设成百万。

注意：填 100 万不代表实际能用满百万。目前社区 Astra 案例生效约 828K，具体以自己的窗口显示为准。

#Codex #GPT6

<!-- 发布备注：图片为 AI 生成的配置说明图，非产品截图。发布时使用平台的 AI 内容标识。信息核对日期：2026-09-06。来源留档见主题 research.md。 -->
