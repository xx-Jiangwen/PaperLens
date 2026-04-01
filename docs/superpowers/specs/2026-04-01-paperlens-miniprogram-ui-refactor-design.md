# PaperLens 小程序 UI 重构设计文档

## 概述

将 PaperLens 小程序界面重构对齐至 stitch 设计参考版本，采用 Material Design 3 风格，实现杂志编辑风格的学术阅读体验。

**设计参考文件**：
- `stitch/home_page.vue` - 首页设计
- `stitch/detail.vue` - 详情页设计
- `stitch/mine.vue` - 个人中心设计
- `stitch/collections.vue` - 收藏页设计
- `stitch/preferences.vue` - 设置页设计

**影响范围**：
- `paperlens-uniapp/pages/home/index.vue` - 首页
- `paperlens-uniapp/pages/home/detail.vue` - 详情页
- `paperlens-uniapp/pages/profile/index.vue` - 个人中心
- `paperlens-uniapp/pages/profile/bookmarks.vue` - 收藏页
- `paperlens-uniapp/pages/profile/settings.vue` - 设置页
- `paperlens-uniapp/components/PaperCard.vue` - 论文卡片组件
- `paperlens-uniapp/components/TabBar.vue` - 底部导航组件
- `paperlens-uniapp/styles/variables.scss` - 设计变量

## 设计系统

### 色彩系统

设计参考采用完整的 Material Design 3 色彩系统，已在 `variables.scss` 中定义：

| 变量名 | 色值 | 用途 |
|--------|------|------|
| `$color-primary` | #004e9f | 主色 |
| `$color-primary-container` | #0066cc | 主色容器（按钮、标签） |
| `$color-on-primary` | #ffffff | 主色上的文字 |
| `$color-surface` | #F5F5F7 | 背景色 |
| `$color-surface-container-lowest` | #ffffff | 卡片背景 |
| `$color-surface-container-high` | #e8e8ea | 标签背景 |
| `$color-on-surface` | #1a1c1d | 主要文字 |
| `$color-on-surface-variant` | #414753 | 次要文字 |

### 字体系统

双字体策略：
- **Manrope**：标题、品牌名，粗体感强
- **Inter**：正文、标签，阅读舒适

字号规范：
- Hero 标题：60rpx (30px) - extrabold
- 页面标题：40rpx (20px) - bold
- 正文：28-34rpx (14-17px)
- 标签：20-24rpx (10-12px) - uppercase tracking

### 视觉效果

- **玻璃拟态导航栏**：`rgba(255,255,255,0.7)` + `backdrop-filter: blur(40px)`
- **柔和阴影**：`0 16rpx 60rpx rgba(0,0,0,0.04)`
- **圆角**：卡片 24rpx，标签 999rpx（药丸形）
- **过渡动画**：150-250ms ease

## 页面重构规范

### 1. 首页 (home/index.vue)

**当前状态**：基本对齐，细节需调整

**调整项**：

#### 1.1 论文卡片 hover 效果

```scss
// 当前
.paper-card:active {
  box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
}

// 调整为（参考 design-reference）
.paper-card {
  transition: all 0.3s ease;
  &:active {
    box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
    transform: scale(0.99);
  }
}
```

#### 1.2 收藏按钮交互

```scss
// 当前：默认 opacity 0.2，hover 时显示
.bookmark-icon {
  opacity: 0.2;
  transition: opacity 0.2s ease;
}
.paper-card:active .bookmark-icon {
  opacity: 1;
}

// 调整为：保持 group hover 效果，但收藏状态下始终显示
.bookmark-icon {
  opacity: 0.2;
  transition: opacity 0.2s ease;
}
.bookmark-icon.bookmarked {
  opacity: 1;
}
.paper-card:active .bookmark-icon:not(.bookmarked) {
  opacity: 0.5; // 轻微提示
}
```

#### 1.3 来源标签

```scss
// 当前已对齐，确保 letter-spacing
.source-badge {
  letter-spacing: 0.1em; // 添加大写字母间距
}
```

### 2. 详情页 (home/detail.vue)

**当前状态**：基本对齐，AI 摘要区块需优化

**调整项**：

#### 2.1 AI 摘要区块

```scss
// AI 图标使用 filled 样式
.ai-icon {
  font-variation-settings: 'FILL' 1;
}

// AI 标题使用 Manrope 字体
.ai-title {
  font-family: 'Manrope', sans-serif;
  font-size: 36rpx;
  font-weight: 700;
}

// 摘要列表项优化
.ai-list-item {
  display: flex;
  gap: 24rpx;
  align-items: flex-start;
}
.bullet {
  color: $color-primary-container;
  font-size: 32rpx;
  line-height: 1.6;
}
.list-text {
  font-size: 36rpx;
  font-weight: 500;
  line-height: 1.6;
}
```

#### 2.2 关键词标签

```scss
// 当前已使用白色背景，确保阴影效果
.keyword-tag {
  background-color: $color-surface-container-lowest;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
```

#### 2.3 原文摘要卡片

```scss
// 当前已对齐
.abstract-card {
  background-color: $color-surface-container-lowest;
  border-radius: 48rpx;
  padding: 64rpx;
}
```

### 3. 个人中心 (profile/index.vue)

**当前状态**：基本对齐，头像阴影需优化

**调整项**：

#### 3.1 头像区域阴影

```scss
// 当前
.avatar-wrapper {
  box-shadow: 0 0 0 32rpx $color-surface-container-lowest;
}

// 调整为（添加柔和阴影）
.avatar-wrapper {
  box-shadow: 0 0 0 32rpx $color-surface-container-lowest,
              0 8rpx 32rpx rgba(0, 0, 0, 0.08);
}
```

#### 3.2 用户名字间距

```scss
.username {
  letter-spacing: -0.02em; // 添加紧凑字间距
}
```

#### 3.3 菜单卡片分隔线

```scss
// 当前已对齐，确保分隔线颜色
.menu-divider {
  height: 2rpx;
  margin: 0 48rpx;
  background-color: $color-surface-container;
}
```

### 4. 收藏页 (profile/bookmarks.vue)

**当前状态**：基本对齐，元数据显示需优化

**调整项**：

#### 4.1 论文卡片布局

```scss
// 当前已对齐
.paper-card {
  padding: 40rpx;
  transition: all 0.3s ease;
}
.paper-card:active {
  background-color: $color-surface-container-low;
  transform: scale(0.99);
}
```

#### 4.2 元数据显示

```scss
// 确保图标 + 文字组合样式
.meta-source {
  display: flex;
  align-items: center;
  gap: 8rpx;
}
.meta-icon {
  font-size: 28rpx;
  color: $color-on-surface-variant;
}
```

#### 4.3 查看更多按钮

```scss
// 当前已对齐
.load-more {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16rpx;
  padding: 96rpx 0;
}
```

### 5. 设置页 (profile/settings.vue)

**当前状态**：基本对齐，分类芯片和滑块需优化

**调整项**：

#### 5.1 Hero 区域

```scss
// 当前已对齐
.hero-title {
  font-family: 'Manrope', sans-serif;
  font-size: 60rpx;
  font-weight: 800;
  letter-spacing: -0.02em;
}
```

#### 5.2 分类芯片选中态

```scss
// 当前已对齐
.category-chip.active {
  background-color: $color-primary-container;
  color: $color-on-primary;
}
```

#### 5.3 滑块样式

```scss
// 当前使用自定义样式覆盖原生滑块，已对齐
.slider-thumb {
  width: 48rpx;
  height: 48rpx;
  background-color: #ffffff;
  border: 4rpx solid $color-primary-container;
  border-radius: 50%;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);
}
```

## 组件更新

### PaperCard 组件

```vue
<!-- 更新 hover 交互 -->
<template>
  <view class="paper-card" @tap="onTap">
    <view class="card-top">
      <view class="source-badge">{{ displaySource }}</view>
      <view class="bookmark-btn" @tap.stop="onBookmark">
        <text class="bookmark-icon" :class="{ bookmarked: isBookmarked }">bookmark</text>
      </view>
    </view>
    <view class="card-title">{{ paper.title }}</view>
    <view class="card-authors">{{ authorText }}</view>
    <view class="card-abstract">{{ paper.abstract }}</view>
  </view>
</template>

<style lang="scss">
.paper-card {
  transition: all 0.3s ease;
  &:active {
    transform: scale(0.99);
    box-shadow: 0 16rpx 80rpx rgba(0, 0, 0, 0.08);
  }
}
.source-badge {
  letter-spacing: 0.1em;
}
</style>
```

### TabBar 组件

```vue
<!-- 当前已对齐，确保圆角背景高亮 -->
<style lang="scss">
.tab-item.active {
  background-color: rgba(59, 130, 246, 0.1);
}
.tab-item.active .tab-icon {
  color: #3b82f6;
  font-variation-settings: 'FILL' 1;
}
</style>
```

## 实现清单

### 必须修改

1. **首页论文卡片**
   - [ ] 添加 `letter-spacing: 0.1em` 到 `.source-badge`
   - [ ] 优化 `.paper-card:active` 添加 `transform: scale(0.99)`
   - [ ] 调整收藏按钮 hover 逻辑

2. **详情页 AI 摘要**
   - [ ] AI 图标添加 `font-variation-settings: 'FILL' 1`
   - [ ] AI 标题使用 Manrope 字体
   - [ ] 优化摘要列表项样式

3. **个人中心头像**
   - [ ] 添加柔和阴影到 `.avatar-wrapper`
   - [ ] 用户名添加 `letter-spacing: -0.02em`

### 可选优化

- 统一所有页面的过渡动画时长
- 添加骨架屏加载状态
- 优化空状态插图

## 测试要点

1. **视觉一致性**：在各页面间切换，确保风格统一
2. **交互反馈**：点击卡片、按钮时的视觉反馈
3. **性能**：确保动画流畅，无卡顿
4. **兼容性**：在微信开发者工具和真机上测试

## 文件变更清单

```
paperlens-uniapp/
├── pages/
│   ├── home/
│   │   ├── index.vue      # 首页样式微调
│   │   └── detail.vue     # AI 摘要样式优化
│   └── profile/
│       ├── index.vue      # 头像阴影优化
│       ├── bookmarks.vue  # 元数据显示优化
│       └── settings.vue   # 已对齐
├── components/
│   ├── PaperCard.vue      # 卡片交互优化
│   └── TabBar.vue         # 已对齐
└── styles/
    └── variables.scss     # 无需修改
```

## 风险评估

- **低风险**：当前实现已接近设计参考，主要是细节调整
- **向后兼容**：纯样式修改，不影响功能逻辑
- **性能影响**：添加过渡动画可能轻微影响性能，需真机测试