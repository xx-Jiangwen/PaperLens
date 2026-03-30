<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&amp;family=Manrope:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
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
        .drop-cap::first-letter {
            float: left;
            font-family: 'Noto Serif', serif;
            font-size: 3.5rem;
            line-height: 1;
            padding-right: 0.5rem;
            font-weight: 700;
            color: #002045;
        }
        body {
            background-color: #f7fafc;
            color: #181c1e;
            font-family: 'Manrope', sans-serif;
        }
    </style>
</head>
<body class="flex flex-col min-h-screen max-w-[430px] mx-auto overflow-x-hidden shadow-2xl bg-surface">
<!-- TopAppBar -->
<header class="sticky top-0 z-50 flex items-center justify-between px-6 py-4 w-full bg-[#f7fafc] dark:bg-slate-900 tonal-shift">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-[#002045] dark:text-blue-100">menu_book</span>
<h1 class="font-noto-serif font-bold text-xl tracking-tight text-[#002045] dark:text-blue-100">The Editorial Scholar</h1>
</div>
<div class="flex items-center gap-4">
<span class="material-symbols-outlined text-[#43474e] dark:text-slate-400">bookmark</span>
<span class="material-symbols-outlined text-[#43474e] dark:text-slate-400">share</span>
</div>
</header>
<main class="flex-1 px-6 pt-6 pb-32 space-y-8 overflow-y-auto">
<!-- Hero Metadata -->
<section class="space-y-4">
<div class="space-y-2">
<span class="inline-flex px-3 py-1 rounded-full bg-surface-variant text-on-surface-variant font-label text-[10px] font-bold uppercase tracking-widest">
                    Computer Science • LLMs
                </span>
<h2 class="font-headline text-3xl font-bold leading-tight text-primary">
                    Constitutional AI: Harmlessness from AI Feedback
                </h2>
</div>
<div class="flex flex-col gap-1">
<p class="font-body text-sm font-semibold text-on-surface">Yuntao Bai, Saurav Kadavath, et al.</p>
<p class="font-body text-xs text-on-surface-variant italic">Presented at NeurIPS 2023 • 42 min read</p>
</div>
</section>
<!-- AI Synthesis Bento Card -->
<section class="bg-primary-container rounded-xl p-6 text-white shadow-sm relative overflow-hidden">
<div class="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -mr-16 -mt-16"></div>
<div class="flex items-center gap-2 mb-4">
<span class="material-symbols-outlined text-tertiary-fixed">bolt</span>
<h3 class="font-label text-xs font-extrabold uppercase tracking-[0.2em]">AI Synthesis</h3>
</div>
<ul class="space-y-3 font-body text-sm leading-relaxed opacity-90">
<li class="flex gap-3">
<span class="font-bold text-tertiary-fixed">01</span>
                    Proposes a method for training harmless assistants without human labels.
                </li>
<li class="flex gap-3">
<span class="font-bold text-tertiary-fixed">02</span>
                    Uses a "Constitution" to guide the model's self-critique process.
                </li>
<li class="flex gap-3">
<span class="font-bold text-tertiary-fixed">03</span>
                    Matches human performance in safety while maintaining helpfulness.
                </li>
</ul>
</section>
<!-- Abstract Section with Drop Cap -->
<section class="space-y-4">
<h3 class="font-headline text-lg font-bold text-primary flex items-center gap-2">
                Abstract
            </h3>
<div class="bg-surface-container-lowest p-6 rounded-xl shadow-sm">
<p class="font-headline text-on-surface leading-relaxed drop-cap text-justify italic">
                    As AI systems become more capable, it is critical that they are aligned with human values. This paper explores Constitutional AI (CAI), a technique to train a language model to be harmless by having it follow a set of written principles. Unlike previous methods that rely on thousands of human-provided labels for safety, CAI uses the model itself to critique and revise its own responses based on the constitution. Our results show that this approach creates assistants that are both safer and more transparent in their reasoning...
                </p>
<p class="mt-4 font-headline text-on-surface leading-relaxed text-justify italic">
                    The paper further examines the trade-offs between helpfulness and harmlessness, demonstrating that Reinforcement Learning from AI Feedback (RLAIF) can achieve comparable results to traditional human-based reinforcement learning (RLHF). This shift suggests a more scalable path toward aligning highly advanced AI systems where human supervision might become a bottleneck. We conclude that constitutional alignment offers a robust framework for ethical AI development.
                </p>
<div class="mt-6 flex justify-end">
<button class="font-label text-xs font-bold text-primary-fixed-dim uppercase tracking-widest hover:text-primary transition-colors">
                        View Full Manuscript →
                    </button>
</div>
</div>
</section>
</main>
<!-- Ask Assistant Bar (Floating Interaction) -->
<div class="fixed bottom-[110px] left-1/2 -translate-x-1/2 w-[90%] z-40">
<div class="bg-surface-container-lowest/90 backdrop-blur-md rounded-full px-6 py-3 shadow-[0_8px_32px_rgba(0,32,69,0.12)] border border-outline-variant/15 flex items-center gap-3">
<span class="material-symbols-outlined text-primary text-xl" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
<input class="bg-transparent border-none focus:ring-0 flex-1 font-body text-sm text-on-surface placeholder:text-on-surface-variant" placeholder="Ask the scholar about this paper..." type="text"/>
<button class="bg-primary text-white p-2 rounded-full hover:scale-95 transition-transform duration-150">
<span class="material-symbols-outlined text-sm">arrow_upward</span>
</button>
</div>
</div>
<!-- BottomNavBar -->
<nav class="fixed bottom-0 left-0 w-full flex justify-around items-center px-8 pb-6 pt-3 bg-[#f7fafc]/80 dark:bg-slate-900/80 backdrop-blur-md z-50 border-t border-[#c4c6cf]/15 shadow-[0_-4px_24px_rgba(0,32,69,0.04)]">
<a class="flex flex-col items-center justify-center text-[#43474e] dark:text-slate-400 px-6 py-2 hover:text-[#002045] dark:hover:text-white transition-all active:scale-90 duration-150" href="#">
<span class="material-symbols-outlined">home_storage</span>
<span class="font-manrope text-[11px] font-bold uppercase tracking-widest mt-1">首页</span>
</a>
<a class="flex flex-col items-center justify-center text-[#43474e] dark:text-slate-400 px-6 py-2 hover:text-[#002045] dark:hover:text-white transition-all active:scale-90 duration-150" href="#">
<span class="material-symbols-outlined">person_search</span>
<span class="font-manrope text-[11px] font-bold uppercase tracking-widest mt-1">我的</span>
</a>
</nav>
</body></html>