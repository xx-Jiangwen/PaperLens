# ADR-003: SSE 流式摘要传输方案

## 状态

已采纳

## 背景

PaperLens 的 AI 摘要生成采用大模型流式输出（打字机效果），需将 token 实时推送到客户端。传输方案选择：

1. **SSE (Server-Sent Events)**：单向推送
2. **WebSocket**：双向通信
3. **HTTP 轮询**：定期请求

## 决策

采用 **SSE (Server-Sent Events)**。

## 理由

### 1. 单向推送足够

- 场景：服务端推送 token → 客户端渲染
- 不需要客户端实时回传（WebSocket 的优势用不上）
- SSE 完美匹配单向流式场景

### 2. 实现简单

- 后端：FastAPI 原生支持 `StreamingResponse`
- Web 前端：`EventSource` API 标准化
- 微信小程序：`wx.request` + `enableChunkedTransfer`（V2）或云函数代理

### 3. HTTP 基础设施友好

- SSE 复用 HTTP 连接，无需新建 WebSocket 握手
- Nginx/CDN 配置简单（仅需禁用缓冲）
- 调试工具支持好（Chrome DevTools、curl）

### 4. 自动重连

- `EventSource` 内置重连机制
- 断线后自动恢复，无需手动实现心跳

## 替代方案

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| **SSE** | 简单、HTTP 原生、单向推送最优 | 微信小程序需特殊处理 | ✅ 采纳 |
| WebSocket | 双向通信、低延迟 | 过度设计、需维护连接状态 | ❌ 不需要 |
| HTTP 轮询 | 兼容性好 | 延迟高、服务端压力大 | ❌ 体验差 |

## 微信小程序特殊处理

微信小程序不原生支持 `EventSource`，V2 采用以下方案之一：

1. **方案 A**：`wx.request` + `enableChunkedTransfer: true`（基础库 2.20.0+）
   ```javascript
   wx.request({
     url: '...',
     enableChunkedTransfer: true,
     success: (res) => { /* 解析 SSE 数据 */ },
   });
   ```

2. **方案 B**：云函数代理 SSE → WebSocket
   - 云函数订阅 SSE 流，通过 WebSocket 推送给小程序

**V1.0 临时方案**：后台预生成摘要，前端直接读取（无实时流式）

## 后果

- **正面**：
  - 后端实现简单，FastAPI 直接 `yield`
  - Web 端体验流畅，打字机效果
  - 资源占用低（对比 WebSocket 长连接）

- **负面**：
  - 微信小程序需特殊处理（已规划 V2 方案）

- **风险缓解**：
  - V1.0 采用预生成模式，降级可用
  - V2.0 补充小程序流式方案

## 参考

- [MDN: Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [微信小程序 enableChunkedTransfer](https://developers.weixin.qq.com/miniprogram/dev/api/network/request/wx.request.html)