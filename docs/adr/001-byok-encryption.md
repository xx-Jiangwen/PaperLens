# ADR-001: BYOK API Key 加密方案

## 状态

已采纳

## 背景

PaperLens 允许用户自带大模型 API Key（BYOK），存储在服务端以便跨设备使用。API Key 是敏感凭证，必须防止泄露。

## 决策

采用 **AES-256-GCM** 加密存储 API Key。

### 加密流程

1. 服务端生成 256-bit 主密钥（环境变量 `MASTER_KEY`）
2. 用户提交 `api_key` 时：
   - 生成随机 96-bit nonce
   - 使用 AES-256-GCM 加密
   - 存储密文 + nonce 到 `user_settings.llm_api_key_enc`
3. 调用 LLM 时：
   - 从数据库读取密文和 nonce
   - 解密得到明文 Key（仅在内存中）
   - 请求完成后，明文 Key 从内存释放

### 安全保障

- **密钥不明文落库**：数据库只存储密文
- **密钥不落日志**：日志中不记录明文 Key
- **Nonce 唯一性**：每次加密使用新 nonce，防止重放攻击
- **认证标签**：GCM 模式提供完整性校验

## 替代方案

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| 明文存储 | 简单 | 安全风险极高 | ❌ 不考虑 |
| 前端加密 | 服务端不接触明文 | 无法跨设备使用，密钥管理复杂 | ❌ 不适用 |
| Vault/KMS | 企业级安全 | 架构复杂，V1.0 过度设计 | ⏸️ V2.0 可考虑 |
| **AES-256-GCM** | 安全、简单、Python 标准库支持 | 需妥善保管主密钥 | ✅ 采纳 |

## 后果

- **正面**：API Key 安全存储，用户信任度提升
- **负面**：需确保 `MASTER_KEY` 不泄露，环境变量管理需谨慎
- **风险缓解**：
  - 生产环境 `MASTER_KEY` 通过 Secrets 管理注入
  - 定期轮换主密钥（V2.0）
  - 监控异常解密失败（可能为攻击）

## 参考

- [NIST SP 800-38D](https://csrc.nist.gov/publications/detail/sp/800-38d/final) — GCM 规范
- Python `cryptography` 库文档