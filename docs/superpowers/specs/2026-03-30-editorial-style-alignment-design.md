# PaperLens 小程序风格对齐设计

## 背景

将现有 uni-app 小程序风格从「Apple iOS Settings」风格完全对齐到 stitch 参考设计的「编辑部/杂志」风格。

## 设计系统变更

### 色彩系统

| 角色 | 原值 | 新值 | 用途 |
|------|------|------|------|
| `$color-primary` | `#007AFF` | `#002045` | 主色：深海军蓝，用于标题、激活态 |
| `$color-primary-container` | 无 | `#1a365d` | 主色容器：中海军蓝，用于 bento 卡片、按钮背景 |
| `$color-primary-fixed` | 无 | `#d6e3ff` | 主色浅色：淡蓝，用于选中标签背景 |
| `$color-primary-fixed-dim` | 无 | `#adc7f7` | 主色高亮：用于链接、hover |
| `$color-bg` | `#FFFFFF` | `#f7fafc` | 页面背景：微冷灰白 |
| `$color-bg-grouped` | `#F2F2F7` | `#f1f4f6` | 分组背景 |
| `$color-bg-card` | `#FFFFFF` | `#ffffff` | 卡片背景（不变） |
| `$color-surface-container` | 无 | `#ebeef0` | 表面容器 |
| `$color-surface-container-low` | 无 | `#f1f4f6` | 低层级表面 |
| `$color-surface-variant` | 无 | `#e0e3e5` | 表面变体：未激活标签背景 |
| `$color-text-primary` | `#1D1D1F` | `#181c1e` | 主文字 |
| `$color-text-secondary` | `#86868B` | `#43474e` | 次文字 |
| `$color-text-tertiary` | `#AEAEB2` | `#74777f` | 三级文字 |
| `$color-separator` | `#E5E5EA` | `#c4c6cf` | 分割线（使用 20% 透明度） |
| `$color-tertiary-fixed` | 无 | `#9ff5c1` | 强调绿：标签背景 |
| `$color-on-tertiary-container` | 无 | `#5caf81` | 强调绿文字 |
| `$color-on-surface-variant` | 无 | `#43474e` | 表面文字 |

### 字体系统

```scss
// 标题字体（模拟 Noto Serif）
$font-family-headline: 'Songti SC', 'STSong', 'Noto Serif SC', Georgia, serif;

// 正文字体（模拟 Manrope）
$font-family-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

// 标签字体
$font-family-label: $font-family-body;
```

### 新增字号

```scss
$font-size-label-xs: 20rpx;   // 10px - 大写标签
$font-size-headline-lg: 48rpx; // 24px - 大标题
$font-size-headline-xl: 60rpx; // 30px - Hero 标题
```

### 间距系统扩展

```scss
$spacing-8: 64rpx;   // 32px
$spacing-12: 96rpx;  // 48px - 论文卡片间距
$spacing-16: 128rpx; // 64px
```

## 首页改造

### 自定义顶部导航栏

取代原生 navigationBar，实现 stitch 风格：

```
┌─────────────────────────────────────┐
│ 📖 The Editorial Scholar    🔍 PaperLens │
├─────────────────────────────────────┤
```

- 左侧：书本 emoji + 衬线粗体标题 "The Editorial Scholar"
- 右侧：搜索 emoji + 衬线斜体小字 "PaperLens"
- 底部 1px 分割线
- 背景 `#f7fafc`，sticky 固定顶部

### Hero 区域（新增）

```
CURATED INSIGHTS
Discovery Through
Intellectual Rigor
━━━━━━━━━━━━━
```

- 标签：`CURATED INSIGHTS` — 大写、加粗、超宽字距 (tracking-widest)、`$font-size-label-xs`
- 标题：衬线体，`Discovery Through` 换行 `<em>Intellectual Rigor</em>`（斜体）
- 分割线：深蓝短粗线 `#1a365d`，宽 24rpx，圆角

### 分类筛选器

替换现有 SegmentedControl，改为横向滚动 pill 标签：

- 激活态：深蓝底 `$color-primary-container` + 白字
- 未激活：灰底 `$color-surface-variant` + `$color-on-surface-variant` 字
- 圆角 full，字号 `$font-size-label-xs`，大写加粗宽字距

### 论文卡片（PaperCard）

**从卡片式 → 文章列表式：**

- 去掉白色卡片背景和圆角
- 改为底部细线分割，大间距 `padding-bottom: $spacing-12`
- 分类标签：绿底圆角 `$color-tertiary-fixed` + `$color-on-tertiary-container` 字
- 标题：衬线体 `$font-family-headline`，大号 `$font-size-headline-lg`，深蓝 `$color-primary`
- 作者：无衬线体，小号加粗，`$color-text-secondary`
- 摘要：衬线体斜体，`$color-text-secondary`，`line-clamp: 3`
- AI 状态：去掉状态点，改为轻量文字标签

## 我的页面改造

### 用户区域

- 去掉圆头像
- 标签：`READER PROFILE` 大写宽字距
- 用户名：衬线体大号标题
- 副文字：无衬线灰色小字

### 统计区域（Bento 卡片）

深蓝底圆角卡片 `$color-primary-container`：

```
┌───────────────────────────────┐
│ ◆ WEEKLY STATS                │
│ 01  本周阅读 12               │
│ 02  收藏     5                │
│ 03  跳过     3                │
└───────────────────────────────┘
```

- 编号用 `$color-tertiary-fixed` 绿色
- 内容白字

### 菜单区域

- 浅灰底圆角卡片 `$color-surface-container-low`
- 列表项：无 emoji，纯文字 + 右箭头
- 分割线 `$color-separator` 20% 透明度

## 自定义底部导航栏

去掉原生 tabBar，实现自定义导航：

```
┌─────────────────────────────────────┐
│  [首页]     [我的]                   │
└─────────────────────────────────────┘
```

- 固定底部，毛玻璃背景 `backdrop-filter: blur(10px)`
- 激活态：深蓝渐变圆角背景 `linear-gradient(#002045, #1a365d)`
- 未激活：灰色 `$color-text-secondary`
- 文字：大写、`$font-size-label-xs`、加粗宽字距
- 图标：用 unicode emoji（📖 首页、👤 我的）

## 文件改动清单

1. `styles/variables.scss` — 色彩/字体体系重写
2. `styles/common.scss` — 新增编辑部风格公共类
3. `components/PaperCard.vue` — 文章列表式改造
4. `components/SearchBar.vue` — 适配新色彩
5. `components/SegmentedControl.vue` — 改为 pill 筛选器（或新建 FilterPills.vue）
6. `pages/home/index.vue` — 自定义 header + Hero + 新布局
7. `pages/profile/index.vue` — 重新排版个人中心
8. `components/TabBar.vue` — 新建自定义底部导航
9. `App.vue` — 引入 TabBar 组件
10. `pages.json` — 删除原生 tabBar 配置，首页/我的页隐藏原生 navigationBar

## 实现顺序

1. 设计系统变量 (`variables.scss`)
2. 公共样式类 (`common.scss`)
3. 自定义底部导航 (`TabBar.vue`)
4. 首页改造 (`home/index.vue` + 相关组件)
5. 我的页面改造 (`profile/index.vue`)