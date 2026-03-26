# PaperLens 文档中心

欢迎来到 PaperLens 文档中心。本文档涵盖产品设计、技术开发、架构决策等方面的完整资料。

---

## 产品文档

- [**产品需求文档（PRD）**](product/PRD.md) — 产品定位、功能需求、技术架构、数据库设计、API 接口清单、版本迭代计划

---

## 开发文档

### 微信小程序（主力 V1.0）

- [**小程序技术规范**](miniprogram/technical-spec.md) — 文件结构、页面规范、API 集成、组件设计、UI 设计系统、路由导航、认证流程、BYOK 配置、错误处理、V2 扩展路线图

### 后端

- [**后端 API 参考**](backend/api-reference.md) — 接口定义、请求/响应示例、错误码说明（待补充）

### Web 前端（V2.0）

- [**Web 技术规范**](web/technical-spec.md) — 项目结构、路由设计、状态管理、组件规范（V2.0 补充）

---

## 架构决策记录（ADR）

记录关键技术决策的背景、理由和后果。

- [ADR-001: BYOK API Key 加密方案](adr/001-byok-encryption.md) — 为何采用 AES-256-GCM 加密存储用户 API Key
- [ADR-002: 微信小程序选用原生框架](adr/002-native-miniprogram.md) — 为何选择原生而非 Taro/uni-app
- [ADR-003: SSE 流式摘要传输方案](adr/003-sse-streaming.md) — 为何用 SSE 而非 WebSocket/轮询

---

## 快速导航

| 我想了解... | 请阅读 |
|---|---|
| 产品是做什么的 | [产品需求文档](product/PRD.md) |
| 小程序怎么开发 | [小程序技术规范](miniprogram/technical-spec.md) |
| API 怎么调用 | [后端 API 参考](backend/api-reference.md) |
| 为什么这样设计 | [架构决策记录](adr/) |

---

## 文档维护

- 文档位置：`/docs`
- 格式：Markdown
- 更新原则：随代码同步更新，保持一致性

---

*如有疑问，请在 GitHub 提交 Issue 或 PR。*