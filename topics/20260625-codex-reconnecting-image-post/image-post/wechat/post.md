# Codex 重连修复

Codex 每次回答前都 Reconnecting？可能不是模型慢，而是 WebSocket 传输层不稳。改用户级 config，让 Responses API 直接走 HTTPS。
