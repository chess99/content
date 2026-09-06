# 来源与事实核对

核对日期：2026-09-06。来自本次会话实际读取的官方文档、社区issue正文与公开代码。

1. GPT-6 Astra 官方规格：https://developers.openai.com/api/docs/models/gpt-6-astra
   总窗口1,050,000 tokens，最大输入922,000，最大输出128,000。不能直接作为Codex实际窗口值。
2. Codex配置参考：https://developers.openai.com/codex/config-reference
   model_context_window 配置窗口；model_auto_compact_token_limit 配置自动压缩阈值。
3. Astra社区运行记录：https://github.com/openai/codex/issues/43015
   Windows、ChatGPT Pro、CLI 0.153.4，配置1000000/900000，运行时窗口828400；已完成请求输入482479。该issue本意报告图片历史导致的传输问题，不代表长上下文稳定性保证。属于用户报告，非作者实测，也非官方承诺。
4. 上限分析（Sol，不作为Astra直接实测）：https://github.com/openai/codex/issues/41325
   服务器目录872000上限，95%有效窗口=828400；自动压缩最多90%=784800。
5. 已读取公开代码：
   https://github.com/openai/codex/blob/6be2a6ca952ac9f70676ce4dd07fda27175aa9dd/codex-rs/models-manager/src/model_info.rs
   https://github.com/openai/codex/blob/6be2a6ca952ac9f70676ce4dd07fda27175aa9dd/codex-rs/protocol/src/openai_models.rs
   配置窗口取配置与max_context_window的较小值；有效窗口乘目录百分比；自动压缩取配置与窗口90%的较小值。
6. 本机会话已读Astra目录：默认272000，最大872000，有效比例95%；272000×95%=258400。未把本机账号、认证、完整配置或私有路径放入公开图片。

## 编辑决定

不使用“Codex已支持完整百万上下文，开启即可用满”的标题。正文保留唯一必要限制：社区案例约828K，以实际窗口为准。不加入API价格与实验性记忆开关，避免分散这篇简单配置告知的重点。
