# PaperLens 小程序 UI 重构实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将小程序界面样式对齐至 stitch 设计参考，实现 Material Design 3 杂志编辑风格

**Architecture:** 纯样式重构，修改 5 个页面 + 1 个组件的 SCSS 样式，不涉及功能逻辑变更

**Tech Stack:** Vue 3 (uni-app), SCSS, Material Design 3 色彩系统

---

## 文件结构

```
paperlens-uniapp/
├── pages/
│   ├── home/
│   │   ├── index.vue      # 首页 - 卡片交互优化
│   │   └── detail.vue     # 详情页 - AI 摘要样式
│   └── profile/
│       ├── index.vue      # 个人中心 - 头像阴影
│       ├── bookmarks.vue  # 收藏页 - 元数据样式
│       └── settings.vue   # 设置页 - 无需修改
└── components/
    └── PaperCard.vue      # 论文卡片组件
```

---

### Task 1: 更新首页论文卡片样式

**Files:**
- Modify: `paperlens-uniapp/pages/home/index.vue` (style section)

- [ ] **Step 1: 更新 .paper-card 样式，添加 transform 过渡**

找到 `.paper-card` 样式块（约 230-240 行），修改为：

```scss
.paper-card {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	padding: 48rpx;
	box-shadow: 0 16rpx 60rpx rgba(0, 0, 0, 0.04);
	transition: all 0.3s ease;  // 添加过渡
}

.paper-card:active {
	box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
	transform: scale(0.99);  // 添加缩放效果
}
```

- [ ] **Step 2: 更新 .source-badge 添加字间距**

找到 `.source-badge` 样式块（约 250-259 行），添加 letter-spacing：

```scss
.source-badge {
	background-color: $color-surface-container-high;
	color: $color-on-surface-variant;
	font-family: 'Inter', sans-serif;
	font-size: 20rpx;
	font-weight: 700;
	letter-spacing: 0.1em;  // 添加大写字母间距
	padding: 8rpx 20rpx;
	border-radius: 999rpx;
}
```

- [ ] **Step 3: 优化收藏按钮 hover 逻辑**

找到 `.bookmark-icon` 相关样式（约 267-281 行），修改为：

```scss
.bookmark-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 48rpx;
	color: $color-primary-container;
	opacity: 0.2;
	transition: opacity 0.2s ease;
}

.paper-card:active .bookmark-icon:not(.bookmarked) {
	opacity: 0.5;
}

.bookmark-icon.bookmarked {
	opacity: 1;
}
```

- [ ] **Step 4: 在微信开发者工具中验证首页**

1. 打开微信开发者工具
2. 刷新首页
3. 验证项：
   - 点击卡片时有轻微缩放效果
   - 来源标签字母间距更宽
   - 未收藏的图标透明度 0.2，点击卡片时变为 0.5
   - 已收藏的图标始终显示为 opacity: 1

- [ ] **Step 5: 提交首页样式更新**

```bash
git add paperlens-uniapp/pages/home/index.vue
git commit -m "style(home): 优化首页论文卡片交互样式

- 添加卡片点击缩放效果
- 来源标签添加字间距
- 优化收藏按钮 hover 逻辑

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: 更新详情页 AI 摘要样式

**Files:**
- Modify: `paperlens-uniapp/pages/home/detail.vue` (style section)

- [ ] **Step 1: 更新 AI 图标为 filled 样式**

找到 `.ai-icon` 样式块（约 363-368 行），确保有 font-variation-settings：

```scss
.ai-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 36rpx;
	color: $color-primary-container;
	font-variation-settings: 'FILL' 1;  // 确保存在
}
```

- [ ] **Step 2: 更新 AI 标题使用 Manrope 字体**

找到 `.ai-title` 样式块（约 370-375 行），确保字体正确：

```scss
.ai-title {
	font-family: 'Manrope', sans-serif;  // 确保使用 Manrope
	font-size: 36rpx;
	font-weight: 700;
	color: $color-primary-container;
}
```

- [ ] **Step 3: 优化摘要列表项样式**

找到 `.ai-list-item`、`.bullet`、`.list-text` 样式（约 396-413 行），修改为：

```scss
.ai-list-item {
	display: flex;
	flex-direction: row;
	gap: 24rpx;
	align-items: flex-start;  // 改为 flex-start
}

.bullet {
	font-size: 32rpx;
	color: $color-primary-container;
	line-height: 1.6;  // 添加行高
}

.list-text {
	font-family: 'Inter', sans-serif;
	font-size: 36rpx;
	font-weight: 500;
	color: $color-on-surface;
	line-height: 1.6;
}
```

- [ ] **Step 4: 在微信开发者工具中验证详情页**

1. 从首页点击进入任意论文详情页
2. 验证项：
   - AI 摘要图标为 filled 样式（实心）
   - AI 标题使用 Manrope 字体（粗体感更强）
   - 列表项对齐正确

- [ ] **Step 5: 提交详情页样式更新**

```bash
git add paperlens-uniapp/pages/home/detail.vue
git commit -m "style(detail): 优化详情页 AI 摘要区块样式

- AI 图标使用 filled 样式
- AI 标题使用 Manrope 字体
- 列表项对齐优化

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: 更新个人中心头像区域样式

**Files:**
- Modify: `paperlens-uniapp/pages/profile/index.vue` (style section)

- [ ] **Step 1: 更新头像区域添加柔和阴影**

找到 `.avatar-wrapper` 样式块（约 259-267 行），修改 box-shadow：

```scss
.avatar-wrapper {
	width: 256rpx;
	height: 256rpx;
	border-radius: 50%;
	overflow: hidden;
	margin-bottom: 48rpx;
	background-color: $color-surface-container-high;
	box-shadow: 0 0 0 32rpx $color-surface-container-lowest,
	            0 8rpx 32rpx rgba(0, 0, 0, 0.08);  // 添加柔和阴影
}
```

- [ ] **Step 2: 更新用户名添加字间距**

找到 `.username` 样式块（约 289-294 行），添加 letter-spacing：

```scss
.username {
	font-family: 'Manrope', sans-serif;
	font-size: 48rpx;
	font-weight: 700;
	color: $color-on-surface;
	letter-spacing: -0.02em;  // 添加紧凑字间距
}
```

- [ ] **Step 3: 在微信开发者工具中验证个人中心**

1. 切换到「个人」标签页
2. 验证项：
   - 头像有柔和的外阴影效果
   - 用户名字间距更紧凑

- [ ] **Step 4: 提交个人中心样式更新**

```bash
git add paperlens-uniapp/pages/profile/index.vue
git commit -m "style(profile): 优化个人中心头像区域样式

- 头像添加柔和阴影效果
- 用户名添加紧凑字间距

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: 更新收藏页论文卡片样式

**Files:**
- Modify: `paperlens-uniapp/pages/profile/bookmarks.vue` (style section)

- [ ] **Step 1: 确保论文卡片有过渡效果**

找到 `.paper-card` 样式块（约 292-302 行），确保有 transition：

```scss
.paper-card {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	padding: 40rpx;
	transition: all 0.3s ease;  // 确保存在
}

.paper-card:active {
	background-color: $color-surface-container-low;
	transform: scale(0.99);  // 确保存在
}
```

- [ ] **Step 2: 确保元数据显示样式正确**

找到 `.meta-source` 和 `.meta-icon` 样式（约 340-356 行），确保样式正确：

```scss
.meta-source {
	display: flex;
	flex-direction: row;
	align-items: center;
	gap: 8rpx;
}

.meta-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 28rpx;
	color: $color-on-surface-variant;
}
```

- [ ] **Step 3: 在微信开发者工具中验证收藏页**

1. 从个人中心进入「我的收藏」
2. 验证项：
   - 点击卡片有缩放效果
   - 元数据图标和文字对齐正确

- [ ] **Step 4: 提交收藏页样式更新**

```bash
git add paperlens-uniapp/pages/profile/bookmarks.vue
git commit -m "style(bookmarks): 优化收藏页论文卡片样式

- 卡片添加过渡效果
- 元数据显示样式优化

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: 更新 PaperCard 组件样式

**Files:**
- Modify: `paperlens-uniapp/components/PaperCard.vue` (style section)

- [ ] **Step 1: 更新卡片过渡效果**

找到 `.paper-card` 样式块（约 71-82 行），修改为：

```scss
.paper-card {
	background-color: $color-surface-container-lowest;
	border-radius: 24rpx;
	padding: 48rpx;
	margin-bottom: 48rpx;
	box-shadow: 0 16rpx 60rpx rgba(0, 0, 0, 0.04);
	transition: all 0.3s ease;  // 添加过渡
}

.paper-card:active {
	box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
	transform: scale(0.99);  // 添加缩放
}
```

- [ ] **Step 2: 更新来源标签字间距**

找到 `.source-badge` 样式块（约 94-103 行），添加 letter-spacing：

```scss
.source-badge {
	background-color: $color-surface-container-high;
	color: $color-on-surface-variant;
	font-family: 'Inter', sans-serif;
	font-size: 20rpx;
	font-weight: 700;
	letter-spacing: 0.1em;  // 添加字间距
	padding: 8rpx 20rpx;
	border-radius: 999rpx;
}
```

- [ ] **Step 3: 更新收藏按钮样式**

找到 `.bookmark-icon` 样式块（约 111-125 行），修改为：

```scss
.bookmark-icon {
	font-family: 'Material Symbols Outlined';
	font-size: 48rpx;
	color: $color-primary-container;
	opacity: 0.2;
	transition: opacity 0.2s ease;
}

.paper-card:active .bookmark-icon:not(.bookmarked) {
	opacity: 0.5;
}

.bookmark-icon.bookmarked {
	opacity: 1;
}
```

- [ ] **Step 4: 提交组件样式更新**

```bash
git add paperlens-uniapp/components/PaperCard.vue
git commit -m "style(PaperCard): 优化论文卡片组件交互样式

- 添加卡片点击缩放效果
- 来源标签添加字间距
- 优化收藏按钮 hover 逻辑

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: 最终验证与合并提交

- [ ] **Step 1: 完整回归测试**

在微信开发者工具中测试所有页面：

1. **首页**：
   - 论文卡片点击有缩放效果
   - 收藏按钮交互正确
   - 来源标签字间距正确

2. **详情页**：
   - AI 摘要图标为 filled
   - 列表项样式正确

3. **个人中心**：
   - 头像阴影效果正确
   - 用户名字间距正确

4. **收藏页**：
   - 卡片交互正确
   - 元数据显示正确

- [ ] **Step 2: 确认所有更改已提交**

```bash
git status
# 应该显示 nothing to commit, working tree clean
```

- [ ] **Step 3: 查看提交历史确认**

```bash
git log --oneline -6
# 应该看到 5 个样式提交 + 1 个设计文档提交
```

---

## 验收标准

- [ ] 所有 5 个页面的样式与设计参考一致
- [ ] 卡片点击有 0.99 缩放效果
- [ ] 收藏按钮透明度逻辑正确
- [ ] AI 摘要图标为 filled 样式
- [ ] 头像有柔和阴影
- [ ] 所有过渡动画流畅
- [ ] 无功能回归问题

## 回滚方案

如果发现问题，可以逐个回滚：

```bash
git revert HEAD~N  # N 为需要回滚的提交数
```

或直接修改对应文件恢复原样式。