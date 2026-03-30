<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&amp;family=Manrope:wght@400;500;700;800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "inverse-on-surface": "#eef1f3",
              "on-primary-fixed": "#001b3c",
              "on-secondary-container": "#596376",
              "tertiary-fixed-dim": "#83d8a6",
              "on-tertiary": "#ffffff",
              "surface-container": "#ebeef0",
              "on-primary": "#ffffff",
              "on-surface": "#181c1e",
              "primary-container": "#1a365d",
              "error-container": "#ffdad6",
              "surface-variant": "#e0e3e5",
              "surface-container-highest": "#e0e3e5",
              "on-secondary-fixed": "#121c2c",
              "tertiary-fixed": "#9ff5c1",
              "surface-container-high": "#e5e9eb",
              "on-tertiary-fixed": "#002111",
              "on-tertiary-container": "#5caf81",
              "background": "#f7fafc",
              "surface": "#f7fafc",
              "surface-container-low": "#f1f4f6",
              "tertiary": "#002715",
              "surface-tint": "#455f88",
              "secondary-container": "#d6e0f6",
              "on-secondary": "#ffffff",
              "tertiary-container": "#003f25",
              "secondary-fixed": "#d9e3f9",
              "on-primary-container": "#86a0cd",
              "on-surface-variant": "#43474e",
              "primary-fixed": "#d6e3ff",
              "surface-dim": "#d7dadc",
              "outline": "#74777f",
              "error": "#ba1a1a",
              "outline-variant": "#c4c6cf",
              "secondary": "#555f71",
              "on-secondary-fixed-variant": "#3d4759",
              "secondary-fixed-dim": "#bdc7dc",
              "on-tertiary-fixed-variant": "#005231",
              "surface-bright": "#f7fafc",
              "inverse-surface": "#2d3133",
              "surface-container-lowest": "#ffffff",
              "on-error-container": "#93000a",
              "inverse-primary": "#adc7f7",
              "on-primary-fixed-variant": "#2d476f",
              "on-error": "#ffffff",
              "on-background": "#181c1e",
              "primary": "#002045",
              "primary-fixed-dim": "#adc7f7"
            },
            fontFamily: {
              "headline": ["Noto Serif"],
              "body": ["Manrope"],
              "label": ["Manrope"]
            },
            borderRadius: {"DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px"},
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        body { font-family: 'Manrope', sans-serif; }
        .font-noto-serif { font-family: 'Noto Serif', serif; }
        .font-manrope { font-family: 'Manrope', sans-serif; }
    </style>
<style>
        body {
          min-height: max(884px, 100dvh);
        }
    </style>
</head>
<body class="bg-background text-on-surface min-h-screen pb-32">
<!-- Shared TopAppBar -->
<header class="bg-[#f7fafc] dark:bg-slate-900 sticky top-0 z-50">
<div class="flex items-center justify-between px-6 py-4 w-full">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-[#002045] dark:text-blue-100" data-icon="menu_book">menu_book</span>
<h1 class="font-noto-serif font-bold text-xl tracking-tight text-[#002045] dark:text-blue-100">The Editorial Scholar</h1>
</div>
<div class="flex items-center gap-4">
<button class="p-2 rounded-full hover:bg-[#f1f4f6] dark:hover:bg-slate-800 transition-colors duration-200">
<span class="material-symbols-outlined text-[#43474e] dark:text-slate-400" data-icon="search">search</span>
</button>
<div class="font-noto-serif text-[#002045] dark:text-white font-bold italic text-sm">PaperLens</div>
</div>
</div>
<div class="h-[1px] w-full bg-[#f1f4f6] dark:bg-slate-800"></div>
</header>
<main class="max-w-4xl mx-auto px-6 pt-12">
<!-- Hero Section -->
<section class="mb-12">
<p class="font-manrope font-bold text-[11px] uppercase tracking-widest text-on-surface-variant mb-4">Curated Insights</p>
<h2 class="font-headline text-4xl md:text-5xl text-primary leading-tight mb-6">Discovery Through <br/><span class="italic">Intellectual Rigor</span></h2>
<div class="h-1 w-24 bg-primary-container rounded-full"></div>
</section>
<!-- Search/Filter Bar -->
<div class="mb-16 flex flex-wrap gap-3">
<span class="px-5 py-2 rounded-full bg-primary-container text-white font-label text-sm font-bold tracking-wide">Recent</span>
<span class="px-5 py-2 rounded-full bg-surface-container-highest text-on-surface-variant font-label text-sm font-medium hover:bg-surface-container-high transition-colors cursor-pointer">Computer Vision</span>
<span class="px-5 py-2 rounded-full bg-surface-container-highest text-on-surface-variant font-label text-sm font-medium hover:bg-surface-container-high transition-colors cursor-pointer">NLP</span>
<span class="px-5 py-2 rounded-full bg-surface-container-highest text-on-surface-variant font-label text-sm font-medium hover:bg-surface-container-high transition-colors cursor-pointer">Ethics</span>
</div>
<!-- Paper Feed (Text Only) -->
<div class="space-y-16">
<!-- Paper Card 1 -->
<article class="group cursor-pointer border-b border-outline-variant/20 pb-12 last:border-0">
<div class="space-y-4">
<div class="flex gap-2 items-center">
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-tertiary-container bg-tertiary-fixed px-2 py-0.5 rounded">CVPR 2024</span>
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-surface-variant bg-surface-variant px-2 py-0.5 rounded">Spotlight</span>
</div>
<h3 class="font-headline text-2xl font-bold text-primary leading-snug group-hover:text-surface-tint transition-colors">Latent Diffusion Models for High-Fidelity Neural Rendering</h3>
<p class="font-label text-sm text-on-surface-variant font-semibold">Chen, W., Zhang, Y., &amp; Miller, J.</p>
<p class="font-noto-serif text-on-surface-variant leading-relaxed line-clamp-3">We present a novel approach to neural rendering that leverages the structured latent space of diffusion models to achieve unprecedented detail in 3D scene reconstruction. By decoupling geometry from appearance, our method enables real-time high-fidelity synthesis across diverse lighting conditions.</p>
</div>
</article>
<!-- Paper Card 2 -->
<article class="group cursor-pointer border-b border-outline-variant/20 pb-12 last:border-0">
<div class="space-y-4">
<div class="flex gap-2 items-center">
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-tertiary-container bg-tertiary-fixed px-2 py-0.5 rounded">NeurIPS 2023</span>
</div>
<h3 class="font-headline text-2xl font-bold text-primary leading-snug group-hover:text-surface-tint transition-colors">The Geometry of Linguistic Representation in Transformers</h3>
<p class="font-label text-sm text-on-surface-variant font-semibold">Siddiqui, A., &amp; Thorne, E.</p>
<p class="font-noto-serif text-on-surface-variant leading-relaxed line-clamp-3">This paper investigates the topological structures formed by attention mechanisms in large-scale transformer models. We demonstrate that semantic relationships are encoded as specific geometric manifolds, providing a new framework for understanding interpretability in NLP.</p>
</div>
</article>
<!-- Paper Card 3 -->
<article class="group cursor-pointer border-b border-outline-variant/20 pb-12 last:border-0">
<div class="space-y-4">
<div class="flex gap-2 items-center">
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-tertiary-container bg-tertiary-fixed px-2 py-0.5 rounded">ICML 2024</span>
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-surface-variant bg-surface-variant px-2 py-0.5 rounded">Best Paper</span>
</div>
<h3 class="font-headline text-2xl font-bold text-primary leading-snug group-hover:text-surface-tint transition-colors">Optimal Transport for Large-Scale Graph Alignment</h3>
<p class="font-label text-sm text-on-surface-variant font-semibold">Luo, H., et al.</p>
<p class="font-noto-serif text-on-surface-variant leading-relaxed line-clamp-3">Aligning massive heterogeneous graphs remains a computational challenge. Our research introduces a scalable optimal transport formulation that reduces complexity from cubic to near-linear while maintaining high accuracy in node correspondence tasks.</p>
</div>
</article>
<!-- Paper Card 4 -->
<article class="group cursor-pointer border-b border-outline-variant/20 pb-12 last:border-0">
<div class="space-y-4">
<div class="flex gap-2 items-center">
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-tertiary-container bg-tertiary-fixed px-2 py-0.5 rounded">arXiv:2405.01234</span>
</div>
<h3 class="font-headline text-2xl font-bold text-primary leading-snug group-hover:text-surface-tint transition-colors">Real-time Scene Reconstruction from Sparse Monocular Views</h3>
<p class="font-label text-sm text-on-surface-variant font-semibold">Patel, R., &amp; Garcia, M.</p>
<p class="font-noto-serif text-on-surface-variant leading-relaxed line-clamp-3">We address the problem of generating dense 3D maps from limited camera perspectives. By utilizing a temporal-consistent transformer architecture, we achieve low-latency performance on mobile hardware without compromising on geometric precision.</p>
</div>
</article>
</div>
<!-- Abstract Preview Section -->
<section class="mt-24 mb-12 p-8 bg-surface-container-low rounded-xl border border-outline-variant/10">
<div class="flex items-start justify-between mb-4">
<span class="font-label text-[10px] font-extrabold uppercase tracking-widest text-on-primary-fixed-variant">Editor's Pick</span>
<span class="material-symbols-outlined text-primary/30" data-icon="auto_awesome">auto_awesome</span>
</div>
<div class="max-w-2xl">
<h4 class="font-headline text-2xl text-primary mb-4 italic">The Future of Scholarly Communication in the Age of Generative AI</h4>
<p class="font-noto-serif text-on-surface-variant leading-relaxed mb-6">
                    As large language models begin to permeate the academic workflow, the very nature of peer review and manuscript preparation is undergoing a radical shift. This investigation explores the ethical boundaries and the potential for a "hybrid intellect" model in future research journals.
                </p>
<div class="flex justify-end">
<button class="font-manrope font-bold uppercase text-[11px] tracking-widest text-on-primary-fixed-variant hover:text-primary transition-colors flex items-center gap-2">
                        Read Full Editorial <span class="material-symbols-outlined text-sm" data-icon="arrow_forward">arrow_forward</span>
</button>
</div>
</div>
</section>
</main>
<!-- Shared BottomNavBar -->
<nav class="fixed bottom-0 left-0 w-full flex justify-around items-center px-8 pb-6 pt-3 bg-[#f7fafc]/90 dark:bg-slate-900/90 backdrop-blur-md shadow-[0_-4px_24px_rgba(0,32,69,0.04)] z-50">
<!-- Home Tab (Active) -->
<a class="flex flex-col items-center justify-center bg-gradient-to-br from-[#002045] to-[#1a365d] text-white rounded-xl px-6 py-2 active:scale-95 duration-150 group" href="#">
<span class="material-symbols-outlined" data-icon="home_storage" style="font-variation-settings: 'FILL' 1;">home_storage</span>
<span class="font-manrope text-[11px] font-bold uppercase tracking-widest mt-1">首页</span>
</a>
<!-- Profile Tab (Inactive) -->
<a class="flex flex-col items-center justify-center text-[#43474e] dark:text-slate-400 px-6 py-2 active:scale-95 duration-150 hover:text-[#002045] dark:hover:text-white transition-all" href="#">
<span class="material-symbols-outlined" data-icon="person_search">person_search</span>
<span class="font-manrope text-[11px] font-bold uppercase tracking-widest mt-1">我的</span>
</a>
</nav>
</body></html>