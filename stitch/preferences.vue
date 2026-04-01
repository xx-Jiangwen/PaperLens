<!DOCTYPE html>

<html class="light" lang="zh-CN"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Manrope:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "on-surface-variant": "#414753",
              "tertiary": "#883700",
              "on-primary-fixed-variant": "#00458e",
              "primary-fixed-dim": "#aac7ff",
              "outline": "#727784",
              "on-tertiary-fixed-variant": "#793000",
              "surface-dim": "#d9dadc",
              "surface-container-lowest": "#ffffff",
              "on-tertiary": "#ffffff",
              "secondary": "#5e5e63",
              "surface-variant": "#e2e2e4",
              "error": "#ba1a1a",
              "secondary-fixed-dim": "#c7c6cb",
              "on-tertiary-container": "#ffe3d6",
              "surface-container-highest": "#e2e2e4",
              "inverse-surface": "#2f3132",
              "on-surface": "#1a1c1d",
              "secondary-fixed": "#e3e2e7",
              "on-error-container": "#93000a",
              "inverse-on-surface": "#f0f0f2",
              "surface": "#f9f9fb",
              "primary": "#004e9f",
              "on-secondary-container": "#626267",
              "inverse-primary": "#aac7ff",
              "surface-container": "#eeeef0",
              "on-primary": "#ffffff",
              "secondary-container": "#e0dfe4",
              "on-error": "#ffffff",
              "tertiary-fixed": "#ffdbcb",
              "surface-tint": "#005cba",
              "surface-container-low": "#f3f3f5",
              "on-secondary-fixed": "#1a1b1f",
              "tertiary-fixed-dim": "#ffb692",
              "on-secondary-fixed-variant": "#46464b",
              "on-primary-fixed": "#001b3e",
              "tertiary-container": "#af4900",
              "surface-bright": "#f9f9fb",
              "primary-container": "#0066cc",
              "outline-variant": "#c1c6d5",
              "surface-container-high": "#e8e8ea",
              "on-primary-container": "#dfe8ff",
              "error-container": "#ffdad6",
              "background": "#f9f9fb",
              "on-tertiary-fixed": "#341100",
              "on-secondary": "#ffffff",
              "primary-fixed": "#d7e3ff",
              "on-background": "#1a1c1d"
            },
            fontFamily: {
              "headline": ["Manrope"],
              "body": ["Inter"],
              "label": ["Inter"]
            },
            borderRadius: {"DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px"},
          },
        },
      }
    </script>
<style>
        body { font-family: 'Inter', sans-serif; }
        .font-headline { font-family: 'Manrope', sans-serif; }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            display: inline-block;
            line-height: 1;
            text-transform: none;
            letter-spacing: normal;
            word-wrap: normal;
            white-space: nowrap;
            direction: ltr;
        }
        .tonal-transition { transition: background-color 0.3s ease; }
    </style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="bg-surface text-on-surface min-h-screen pb-32">
<!-- TopAppBar -->
<header class="fixed top-0 w-full z-50 bg-white/70 dark:bg-zinc-950/70 backdrop-blur-xl flex items-center justify-between px-6 py-4 w-full">
<div class="flex items-center gap-4">
<button class="active:scale-95 transition-transform hover:opacity-70 transition-opacity text-zinc-500">
<span class="material-symbols-outlined" data-icon="arrow_back">arrow_back</span>
</button>
<h1 class="font-headline font-bold text-lg tracking-tight text-zinc-900">偏好设置</h1>
</div>
<div class="flex items-center gap-4">
<button class="active:scale-95 transition-transform hover:opacity-70 transition-opacity text-blue-600">
<span class="material-symbols-outlined" data-icon="search">search</span>
</button>
</div>
</header>
<main class="pt-24 px-6 max-w-2xl mx-auto space-y-8">
<!-- Intro Hero Section (Editorial Style) -->
<section class="space-y-2">
<h2 class="text-3xl font-headline font-extrabold tracking-tight text-on-surface">定制您的阅读体验</h2>
<p class="text-on-surface-variant text-sm leading-relaxed max-w-md">调整研究算法，让我们为您筛选最相关的学术动态。</p>
</section>
<!-- Group 1: 研究方向 (Bento-style selection) -->
<section class="space-y-4">
<h3 class="text-xs font-bold text-on-surface-variant uppercase tracking-widest px-1">研究方向</h3>
<div class="bg-surface-container-lowest rounded-xl p-6 space-y-4">
<div class="flex flex-wrap gap-2">
<!-- Active Chips -->
<div class="inline-flex items-center px-4 py-2 bg-primary-container text-on-primary rounded-full text-sm font-medium transition-all cursor-pointer">
                        NLP
                    </div>
<div class="inline-flex items-center px-4 py-2 bg-primary-container text-on-primary rounded-full text-sm font-medium transition-all cursor-pointer">
                        CV
                    </div>
<!-- Inactive Chips -->
<div class="inline-flex items-center px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-sm font-medium hover:bg-surface-container transition-all cursor-pointer">
                        ML
                    </div>
<div class="inline-flex items-center px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-sm font-medium hover:bg-surface-container transition-all cursor-pointer">
                        Robotics
                    </div>
<div class="inline-flex items-center px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-sm font-medium hover:bg-surface-container transition-all cursor-pointer">
                        Bio-Medical
                    </div>
<div class="inline-flex items-center px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-sm font-medium hover:bg-surface-container transition-all cursor-pointer">
                        Optimization
                    </div>
<div class="inline-flex items-center px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-sm font-medium hover:bg-surface-container transition-all cursor-pointer">
                        Graph Theory
                    </div>
<!-- Add more chip button -->
<button class="inline-flex items-center justify-center w-9 h-9 border-2 border-dashed border-outline-variant text-outline-variant rounded-full hover:border-primary hover:text-primary transition-colors">
<span class="material-symbols-outlined text-sm" data-icon="add">add</span>
</button>
</div>
<p class="text-[11px] text-on-surface-variant italic">选择您的核心研究领域，PaperLens 将优先为您推荐相关领域的顶级期刊论文。</p>
</div>
</section>
<!-- Group 2: 每日推送数量 (Apple List style Slider) -->
<section class="space-y-4">
<h3 class="text-xs font-bold text-on-surface-variant uppercase tracking-widest px-1">每日推送数量</h3>
<div class="bg-surface-container-lowest rounded-xl divide-y divide-surface-container-low overflow-hidden">
<div class="p-6 space-y-6">
<div class="flex justify-between items-end">
<div class="space-y-1">
<span class="text-2xl font-bold text-primary tracking-tight">5 篇/日</span>
<p class="text-xs text-on-surface-variant">推荐频率：深度阅读模式</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-30" data-icon="auto_awesome">auto_awesome</span>
</div>
<div class="relative w-full h-12 flex items-center">
<div class="absolute w-full h-1.5 bg-surface-container-high rounded-full"></div>
<div class="absolute w-1/2 h-1.5 bg-primary-container rounded-full"></div>
<div class="absolute left-1/2 -translate-x-1/2 w-6 h-6 bg-white shadow-lg border-2 border-primary-container rounded-full cursor-pointer hover:scale-110 transition-transform"></div>
</div>
<div class="flex justify-between text-[10px] font-bold text-on-surface-variant/50 uppercase tracking-tighter">
<span>1 篇</span>
<span>10 篇</span>
</div>
</div>
</div>
</section>
<!-- Action Area -->
<section class="pt-10 pb-12">
<button class="w-full bg-primary-container text-white py-4 rounded-xl font-bold text-sm shadow-xl active:scale-[0.98] transition-all hover:brightness-110">
                保存我的偏好
            </button>
<p class="text-center text-[11px] text-on-surface-variant/60 mt-4 leading-relaxed">
                您的更改将立即同步至所有已登录设备。
            </p>
</section>
</main>
<!-- BottomNavBar -->
<nav class="fixed bottom-0 left-0 w-full flex justify-around items-center px-8 pb-8 pt-4 bg-white/70 dark:bg-zinc-950/70 backdrop-blur-xl z-50 rounded-t-3xl shadow-[0_-4px_40px_rgba(26,28,29,0.04)]">
<a class="flex flex-col items-center justify-center text-zinc-400 dark:text-zinc-500 px-6 py-1.5 hover:text-zinc-900 dark:hover:text-zinc-50 transition-colors active:scale-90 transition-transform duration-200" href="#">
<span class="material-symbols-outlined" data-icon="home">home</span>
<span class="font-['Inter'] text-[11px] font-medium leading-tight mt-1">首页</span>
</a>
<a class="flex flex-col items-center justify-center text-blue-600 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/20 rounded-2xl px-6 py-1.5 active:scale-90 transition-transform duration-200" href="#">
<span class="material-symbols-outlined" data-icon="person" style="font-variation-settings: 'FILL' 1;">person</span>
<span class="font-['Inter'] text-[11px] font-medium leading-tight mt-1">我的</span>
</a>
</nav>
</body></html>