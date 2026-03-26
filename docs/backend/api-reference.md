# PaperLens 后端 API 参考文档

> **状态**：待补充
>
> 本文档将在后端 API 实现完成后补充，包含完整的接口定义、请求/响应示例、错误码说明。
>
> 临时参考：FastAPI 自动生成的 Swagger 文档位于 `/docs` 路径。

---

## 待补充内容

1. **认证接口**
   - POST `/auth/wx-login` — 微信登录
   - POST `/auth/refresh` — Token 刷新

2. **论文接口**
   - GET `/papers` — 论文列表
   - GET `/papers/today` — 今日论文
   - GET `/papers/{id}` — 论文详情
   - POST `/papers/search` — 实时搜索

3. **AI 接口**
   - GET `/ai/summarize/{id}/stream` — SSE 流式摘要
   - GET `/ai/summarize/{id}/status` — 摘要状态

4. **用户接口**
   - GET `/users/me` — 当前用户
   - GET `/settings` — 获取设置
   - PUT `/settings` — 更新设置
   - POST `/settings/test-llm` — 测试连通性

5. **收藏接口**
   - GET `/bookmarks` — 收藏列表
   - POST `/bookmarks/{id}` — 添加收藏
   - DELETE `/bookmarks/{id}` — 取消收藏

---

*本文档由后端开发者在 V1.0 完成后补充。*