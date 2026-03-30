"""
Seed mock paper data into the database for development/demo purposes.

Usage:
    cd backend
    python seed_mock_data.py

This script inserts ~30 papers with realistic AI-generated summaries
so you can preview the mini program without waiting for the scheduler.
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(__file__))

MOCK_PAPERS = [
    {
        "id": "arxiv:2403.19888v1",
        "arxiv_id_base": "2403.19888",
        "title": "Jamba: A Hybrid Transformer-Mamba Language Model",
        "authors": ["Opher Lieber", "Barak Lenz", "Hofit Bata"],
        "abstract": "We present Jamba, a new base large language model based on a novel hybrid Transformer-Mamba mixture-of-experts (MoE) architecture. Specifically, Jamba interleaves blocks of Transformer and Mamba layers, enjoying the benefits of both model families.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.AI"],
        "summary_what": "Jamba 是一种新型混合架构大语言模型，将 Transformer 和 Mamba（状态空间模型）层交替组合，并引入混合专家（MoE）机制。该模型在保持高效长上下文处理能力的同时，实现了与纯 Transformer 模型相当的性能。",
        "summary_how": "模型架构核心创新在于交替堆叠 Transformer 注意力层和 Mamba SSM 层，并在部分层中使用 MoE 替代标准 FFN。Mamba 层提供线性复杂度的序列建模能力，而 Transformer 层补充全局注意力。通过这种混合设计，模型在 256K 上下文窗口下仍能高效运行。",
        "summary_why": "纯 Transformer 模型在超长上下文场景下面临二次复杂度瓶颈，而纯 SSM 模型在某些任务上表现不如 Transformer。Jamba 的混合架构首次证明两种范式可以高效融合，为未来大模型架构设计开辟了新方向。",
    },
    {
        "id": "arxiv:2403.20329v1",
        "arxiv_id_base": "2403.20329",
        "title": "ReALM: Reference Resolution As Language Modeling",
        "authors": ["Joel Ruben Antony Moniz", "Soundarya Krishnan", "Melis Ozyildirim"],
        "abstract": "Reference resolution is an important problem, one that is especially hard in conversational systems that need to take into account context including references on their screens. We demonstrate that LLMs can be fine-tuned to resolve references effectively.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.AI"],
        "summary_what": "ReALM 将指代消解问题（如「打开那个」中的「那个」指什么）重新定义为语言建模任务，使大语言模型能够理解对话中的屏幕元素引用、会话引用和背景引用。",
        "summary_how": "将屏幕上的 UI 元素编码为文本描述，与对话历史拼接后输入 LLM 进行微调。模型学会在给定上下文中识别用户所指的具体实体。实验覆盖了屏幕指代、对话指代和背景知识指代三类场景。",
        "summary_why": "在语音助手和多模态交互场景中，用户经常用模糊代词引用屏幕内容。传统方法依赖启发式规则，泛化能力弱。ReALM 证明 LLM 微调可以统一处理多种指代类型，为端侧 AI 助手的交互理解提供了新思路。",
    },
    {
        "id": "arxiv:2403.18103v1",
        "arxiv_id_base": "2403.18103",
        "title": "AIOS: LLM Agent Operating System",
        "authors": ["Kai Mei", "Zelong Li", "Shuyuan Xu"],
        "abstract": "The integration and deployment of large language model (LLM)-based intelligent agents currently face significant challenges in terms of efficiency and scalability. We propose AIOS, an LLM agent operating system, to address these challenges.",
        "primary_category": "cs.AI",
        "categories": ["cs.AI", "cs.OS"],
        "summary_what": "AIOS 提出了一个专为 LLM Agent 设计的操作系统架构，通过统一的调度、内存管理和工具调用接口，解决多 Agent 并发运行时的资源竞争和效率问题。",
        "summary_how": "设计了 LLM 内核层，包含 Agent 调度器（支持 FIFO/RR 等策略）、上下文管理器（处理长对话的换入换出）、以及统一的工具服务层。多个 Agent 共享底层 LLM 推理资源，由 OS 层统一调度。",
        "summary_why": "随着 LLM Agent 应用爆发，单机上常需同时运行多个 Agent（如编码助手 + 搜索助手 + 分析助手），缺乏统一管理会导致 GPU 内存浪费和上下文冲突。AIOS 的 OS 抽象为 Agent 生态的规模化部署奠定了基础。",
    },
    {
        "id": "arxiv:2403.17297v1",
        "arxiv_id_base": "2403.17297",
        "title": "LLaVA-UHD: an LMM Perceiving Any Aspect Ratio and High-Resolution Images",
        "authors": ["Ruyi Xu", "Yuan Yao", "Zonghao Guo"],
        "abstract": "Visual encoding constitutes the basis of large multimodal models (LMMs) in understanding the visual world. Conventional LMMs process images in fixed sizes and limited resolutions, which is not optimal. We present LLaVA-UHD for efficient perception of high-resolution images.",
        "primary_category": "cs.CV",
        "categories": ["cs.CV", "cs.AI"],
        "summary_what": "LLaVA-UHD 让多模态大模型能够高效处理任意宽高比和超高分辨率图像，解决了传统方法将图片强制缩放到固定尺寸导致的细节丢失问题。",
        "summary_how": "核心设计包含三部分：1) 自适应图像切片策略，根据原始宽高比将图片切分为多个子区域；2) 压缩层将每个子区域的视觉 token 压缩到可控长度；3) 空间位置编码保留切片间的相对位置关系。",
        "summary_why": "在文档 OCR、遥感图像分析等场景中，图像细节至关重要。固定分辨率的编码方式无法满足这些需求，而简单放大分辨率会导致 token 数量爆炸。LLaVA-UHD 在不显著增加计算量的前提下，将细粒度视觉理解能力提升了一个档次。",
    },
    {
        "id": "arxiv:2403.15388v1",
        "arxiv_id_base": "2403.15388",
        "title": "Can large language models explore in-context?",
        "authors": ["Akshay Krishnamurthy", "Keegan Harris", "Dylan J. Foster"],
        "abstract": "We investigate the extent to which large language models (LLMs) are capable of exploration, a core capability in reinforcement learning and decision making. We focus on multi-armed bandit problems to study whether LLMs can explore effectively.",
        "primary_category": "cs.LG",
        "categories": ["cs.LG", "cs.AI"],
        "summary_what": "本文系统研究了大语言模型在多臂老虎机问题上的探索能力——即 LLM 是否能在不确定环境中主动尝试未知选项以获取更多信息，而非仅利用已知最优策略。",
        "summary_how": "设计了一系列 in-context 多臂老虎机实验，将历史交互结果作为 prompt 输入 LLM，测试其是否能展现类似 UCB/Thompson Sampling 的探索行为。对比了 GPT-4、Claude 等模型在不同问题规模下的表现。",
        "summary_why": "探索-利用权衡是智能决策的核心能力。如果 LLM 能自主探索，就能直接用于推荐系统、实验设计等场景。本文发现 LLM 的探索能力有限且脆弱，揭示了当前 LLM 在序贯决策方面的根本局限。",
    },
    {
        "id": "arxiv:2403.14608v1",
        "arxiv_id_base": "2403.14608",
        "title": "LLM2LLM: Boosting LLMs with Novel Iterative Data Enhancement",
        "authors": ["Nicholas Lee", "Thanakul Wattanawong", "Sehoon Kim"],
        "abstract": "Pretrained large language models (LLMs) are currently state-of-the-art for solving the vast majority of natural language processing tasks. While many real-world applications still require fine-tuning to reach satisfactory levels of performance, many of them are in the low-data regime.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.LG"],
        "summary_what": "LLM2LLM 提出了一种迭代式数据增强方法：用一个强大的 LLM（教师）为小数据集生成针对性的训练样本，帮助另一个 LLM（学生）在数据稀缺场景下提升微调效果。",
        "summary_how": "流程为：1) 在小数据集上微调学生模型；2) 找出学生模型出错的样本；3) 用教师模型根据错误模式生成类似但正确的新样本；4) 将新样本加入训练集，重复迭代。每轮聚焦于学生的薄弱环节。",
        "summary_why": "低资源场景（如医疗、法律领域）中标注数据稀缺是微调的最大瓶颈。传统数据增强方法缺乏针对性，而 LLM2LLM 让数据生成精准对准模型弱点，在仅有几百条样本时就能显著提升性能。",
    },
    {
        "id": "arxiv:2403.13793v1",
        "arxiv_id_base": "2403.13793",
        "title": "ReFT: Representation Finetuning for Language Models",
        "authors": ["Zhengxuan Wu", "Aryaman Arora", "Zheng Wang"],
        "abstract": "Parameter-efficient fine-tuning (PEFT) methods operate on a fraction of model weights yet achieve performance close to full fine-tuning. We introduce a new family of PEFTs that operate on a semantically richer level: model representations.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.LG"],
        "summary_what": "ReFT 提出了一种全新的参数高效微调范式：不修改模型权重，而是学习对模型中间层表示（representation）的干预函数，以更少的参数实现等价甚至更优的微调效果。",
        "summary_how": "在 Transformer 每一层的隐藏状态上学习一个低秩线性变换作为干预。训练时冻结所有原始权重，仅优化干预参数。推理时，干预函数直接修改前向传播中的中间表示。参数量仅为 LoRA 的 10-50%。",
        "summary_why": "现有 PEFT 方法（LoRA, Adapter 等）本质上都在修改权重，而表示空间携带了更丰富的语义信息。ReFT 从因果推断角度重新理解微调，证明直接操作表示比操作权重更高效，为 PEFT 研究开辟了新方向。",
    },
    {
        "id": "arxiv:2403.12881v1",
        "arxiv_id_base": "2403.12881",
        "title": "Grok-1: A Large Language Model with Mixture of Experts",
        "authors": ["xAI Team"],
        "abstract": "We introduce Grok-1, a large language model with 314 billion parameters that uses a mixture of experts architecture. Grok-1 was trained from scratch by xAI and achieves competitive performance across various benchmarks.",
        "primary_category": "cs.AI",
        "categories": ["cs.AI", "cs.CL"],
        "summary_what": "Grok-1 是 xAI 公司发布的 3140 亿参数开源大语言模型，采用混合专家架构（MoE），每次推理仅激活约 25% 的参数，在多项基准测试中表现出色。",
        "summary_how": "基于 Transformer 架构，在部分 FFN 层替换为 MoE 层（8 个专家，激活 2 个）。使用大规模互联网数据从头训练，训练过程中采用了多阶段学习率调度和数据配比策略。模型权重以 Apache 2.0 协议开源。",
        "summary_why": "在 GPT-4、Claude 等闭源模型主导的格局下，Grok-1 的开源为研究社区提供了首个超大规模 MoE 模型的完整权重。其开源策略推动了大模型民主化，也为 MoE 架构的深入研究提供了宝贵资源。",
    },
    {
        "id": "arxiv:2403.11901v1",
        "arxiv_id_base": "2403.11901",
        "title": "Agent-FLAN: Designing Data and Methods of Effective Agent Tuning for Large Language Models",
        "authors": ["Zehui Chen", "Kuikun Liu", "Qicheng Wang"],
        "abstract": "Open-sourced Large Language Models (LLMs) have achieved great success in various NLP tasks, yet they still fall behind commercial models in agent tasks. We investigate the key challenges in agent tuning and propose Agent-FLAN.",
        "primary_category": "cs.AI",
        "categories": ["cs.AI", "cs.CL"],
        "summary_what": "Agent-FLAN 系统研究了如何通过数据设计和训练方法，让开源 LLM 获得接近闭源模型的 Agent 能力（工具调用、规划、反思等），并提出了一套有效的 Agent 微调方案。",
        "summary_how": "核心发现：1) Agent 训练数据中对话格式不统一会严重损害效果，需要标准化；2) 引入负样本（错误的工具调用示例）能显著提升鲁棒性；3) 将 Agent 能力分解为子任务分阶段训练优于端到端训练。基于 Llama-2 验证了方案有效性。",
        "summary_why": "Agent 是 LLM 应用的核心方向，但开源模型在工具调用准确性和多步推理方面远逊于 GPT-4。Agent-FLAN 首次系统性地解剖了 Agent 微调中的关键因素，为社区提供了可复现的训练配方。",
    },
    {
        "id": "arxiv:2403.10131v1",
        "arxiv_id_base": "2403.10131",
        "title": "MM1: Methods, Analysis & Insights from Multimodal LLM Pre-training",
        "authors": ["Brandon McKinzie", "Zhe Gan", "Jean-Philippe Fauconnier"],
        "abstract": "We discuss building performant Multimodal Large Language Models (MLLMs). We study the importance of various architecture components and data choices through careful and comprehensive ablations of the image encoder, the vision-language connector, and various pre-training data mixtures.",
        "primary_category": "cs.CV",
        "categories": ["cs.CV", "cs.CL", "cs.AI"],
        "summary_what": "MM1 是 Apple 发布的多模态大模型系列，论文系统性地研究了构建高性能多模态 LLM 的关键设计选择，包括视觉编码器、连接器架构和预训练数据配比。",
        "summary_how": "通过大规模消融实验，逐一测试了：1) 不同视觉编码器（CLIP vs SigLIP vs DINOv2）的影响；2) 连接器类型（线性/MLP/Cross-attention）的效果；3) 图文对、交织文档、纯文本三类数据的最优配比。最终训练了 3B 到 30B 参数量的模型族。",
        "summary_why": "多模态 LLM 的设计空间巨大，此前缺乏系统性的消融研究来指导架构选择。MM1 提供了迄今最全面的多模态预训练经验总结，其核心发现（如图像分辨率比编码器选择更重要）对整个社区都有实用价值。",
    },
    {
        "id": "arxiv:2403.09611v1",
        "arxiv_id_base": "2403.09611",
        "title": "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking",
        "authors": ["Eric Zelikman", "Georges Harik", "Yijia Shao", "Nick Haber"],
        "abstract": "When writing and talking, people sometimes pause to think. Although reasoning-focused works have proposed chain-of-thought prompting and similar methods, the language model that generates the reasoning is still trained only on text that was produced without reasoning.",
        "primary_category": "cs.LG",
        "categories": ["cs.LG", "cs.CL", "cs.AI"],
        "summary_what": "Quiet-STaR 让语言模型在生成每个 token 之前，先在内部产生隐式的推理过程（\"内心独白\"），从而提升对需要推理的文本的预测能力，且无需标注的推理链数据。",
        "summary_how": "在每个 token 位置插入一段可学习的\"思考 token\"序列，模型学会在这些隐藏位置进行推理，然后用推理后的表示来预测下一个 token。通过 REINFORCE 算法优化思考质量，并引入 meta-token 让模型自主决定何时需要思考。",
        "summary_why": "传统 CoT 方法依赖显式推理链标注或特定 prompt，难以泛化到所有场景。Quiet-STaR 的突破在于让模型自发学会在需要时「三思而后行」，这更接近人类的思维方式，且可以从普通文本中自监督学习推理能力。",
    },
    {
        "id": "arxiv:2403.08295v1",
        "arxiv_id_base": "2403.08295",
        "title": "Simple and Scalable Strategies to Continually Pre-train Large Language Models",
        "authors": ["Adam Ibrahim", "Benjamin Therien", "Kshitij Gupta"],
        "abstract": "Large language models (LLMs) are routinely pre-trained on billions of tokens, only to be re-trained from scratch when new data becomes available. We investigate strategies to continually pre-train LLMs without catastrophic forgetting.",
        "primary_category": "cs.LG",
        "categories": ["cs.LG", "cs.CL"],
        "summary_what": "本文研究了如何在新数据到来时持续预训练大语言模型，而无需从头重新训练，同时避免灾难性遗忘。提出了简单有效的持续预训练策略组合。",
        "summary_how": "系统评估了多种策略：1) 学习率重预热（re-warming）避免训练不稳定；2) 新旧数据混合回放缓解遗忘；3) 学习率余弦衰减的重新调度。在 Llama 系列模型上验证，发现简单的学习率重预热 + 5% 旧数据回放即可达到接近从头训练的效果。",
        "summary_why": "每次有新数据就从头训练，成本高达数百万美元。持续预训练如果能保持模型质量，将极大降低大模型更新成本。本文的策略足够简单可直接落地，对所有运营大模型的团队都有直接的经济价值。",
    },
    {
        "id": "arxiv:2403.07691v1",
        "arxiv_id_base": "2403.07691",
        "title": "Branch-Train-MiX: Mixing Expert LLMs into a Mixture-of-Experts LLM",
        "authors": ["Sainbayar Sukhbaatar", "Olga Golovneva", "Vasu Sharma"],
        "abstract": "We investigate efficient methods for training a mixture-of-experts large language model. Our approach, BTX, starts from a seed model that is copied into multiple expert branches.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.LG"],
        "summary_what": "Branch-Train-MiX (BTX) 提出了一种高效构建 MoE 大模型的方法：从一个基础模型复制出多个专家分支，各自在不同领域数据上独立训练，最后通过 MoE 路由器合并为一个统一模型。",
        "summary_how": "三步流程：1) Branch：从种子模型复制 N 个副本；2) Train：每个副本在特定领域（代码、数学、科学等）上独立微调；3) MiX：冻结专家权重，仅训练路由器和注意力层来学习如何组合专家。这避免了从头训练 MoE 的通信开销。",
        "summary_why": "传统 MoE 训练需要大量 GPU 间通信，扩展困难。BTX 将 MoE 训练分解为可并行的独立任务，大幅降低训练成本。同时，每个专家保留了领域专长，整合后的模型在通用和专业任务上都表现优异。",
    },
    {
        "id": "arxiv:2403.07368v1",
        "arxiv_id_base": "2403.07368",
        "title": "VideoMamba: State Space Model for Efficient Video Understanding",
        "authors": ["Kunchang Li", "Xinhao Li", "Yi Wang"],
        "abstract": "Addressing the dual challenges of local redundancy and global dependencies in video understanding, this paper introduces VideoMamba, a model that adapts the Mamba architecture for video tasks.",
        "primary_category": "cs.CV",
        "categories": ["cs.CV", "cs.AI"],
        "summary_what": "VideoMamba 将 Mamba（状态空间模型）引入视频理解领域，在处理长视频时实现线性复杂度，同时保持对全局时空依赖的建模能力，性能媲美 Video Transformer。",
        "summary_how": "将视频帧序列展开为 patch token 序列，使用双向 Mamba 块进行空间建模，再沿时间维度用单向 Mamba 块建模运动信息。相比 Video ViT 的二次复杂度注意力，Mamba 的线性扫描在长视频上速度优势显著（16 帧以上快 3-5 倍）。",
        "summary_why": "视频理解需要处理的 token 数量是图像的数十倍，Transformer 的二次复杂度成为瓶颈。VideoMamba 首次验证了 SSM 架构在视频领域的可行性，为高效长视频理解提供了新的架构选择。",
    },
    {
        "id": "arxiv:2403.06977v1",
        "arxiv_id_base": "2403.06977",
        "title": "ERA-CoT: Improving Chain-of-Thought through Entity Relationship Analysis",
        "authors": ["Yanming Liu", "Xinyue Peng", "Jiannan Cao"],
        "abstract": "Large language models (LLMs) have achieved remarkable performance in reasoning tasks. Chain-of-thought (CoT) prompting has been proposed to elicit reasoning capabilities. However, LLMs still struggle with complex reasoning involving multiple entities.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.AI"],
        "summary_what": "ERA-CoT 提出在 Chain-of-Thought 推理之前，先让 LLM 提取和分析问题中的实体关系，从而提升多实体复杂推理任务的准确率。",
        "summary_how": "三阶段推理：1) 实体提取——从问题中识别所有关键实体；2) 关系分析——构建实体间的关系图；3) 基于关系图的 CoT 推理——沿着实体关系链条逐步推导答案。整个过程通过 prompt 模板实现，不需要额外训练。",
        "summary_why": "在涉及多个人物、物品、地点的推理题（如「A 把书给 B，B 放在桌上，C 拿走了桌上的东西，谁有书？」）中，标准 CoT 容易混淆实体关系导致错误。ERA-CoT 通过显式建模关系图来规避这一问题，在多个推理基准上显著提升了准确率。",
    },
    {
        "id": "arxiv:2403.06563v1",
        "arxiv_id_base": "2403.06563",
        "title": "GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection",
        "authors": ["Jiawei Zhao", "Zhenyu Zhang", "Beidi Chen", "Zhangyang Wang"],
        "abstract": "Training large language models (LLMs) presents significant memory challenges due to the storage of optimizer states. We propose GaLore, a training strategy that allows full-parameter learning but is more memory-efficient than common low-rank adaptation methods.",
        "primary_category": "cs.LG",
        "categories": ["cs.LG", "cs.CL"],
        "summary_what": "GaLore 提出了一种内存高效的 LLM 训练策略：通过对梯度进行低秩投影来压缩优化器状态，在不牺牲全参数训练质量的前提下，将训练内存占用降低至 LoRA 级别。",
        "summary_how": "核心观察：训练过程中梯度矩阵的有效秩远低于其维度。GaLore 周期性地对梯度矩阵做 SVD 分解，仅保留前 k 个奇异向量方向的投影梯度来更新优化器状态（如 Adam 的一阶/二阶矩）。投影矩阵每 T 步更新一次以跟踪梯度子空间的变化。",
        "summary_why": "全参数训练 7B 模型需要 ~58GB 显存（主要被 Adam 状态占用），超出消费级 GPU 容量。LoRA 虽然省内存但限制了模型表达能力。GaLore 让单张 24GB GPU 就能全参数训练 7B 模型，真正实现了「穷人也能从头训大模型」。",
    },
    {
        "id": "arxiv:2403.05530v1",
        "arxiv_id_base": "2403.05530",
        "title": "Yi: Open Foundation Models by 01.AI",
        "authors": ["01.AI Team"],
        "abstract": "We introduce the Yi model family, a series of language and multimodal models that demonstrate strong multi-dimensional capabilities. The Yi model family is based on 6B and 34B pretrained language models, with chat models, vision-language models, and long-context variants.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.AI"],
        "summary_what": "Yi 是零一万物发布的开源大模型系列，涵盖 6B/34B 语言模型、视觉语言模型和 200K 长上下文版本，在多项中英文基准上达到同参数量级最优水平。",
        "summary_how": "基于标准 Transformer 架构，核心改进在数据工程：1) 构建了高质量 3.1T token 预训练语料库，数据清洗流水线包含重复检测、质量打分、毒性过滤等步骤；2) SFT 阶段使用少量（<10K）高质量人工标注数据。技术报告详细公开了数据处理流程。",
        "summary_why": "Yi 的价值不仅在模型本身，更在于其对数据工程最佳实践的透明分享。在「数据质量 > 模型架构」的共识下，Yi 的数据处理流水线为社区提供了可复现的参考方案。",
    },
    {
        "id": "arxiv:2403.04652v1",
        "arxiv_id_base": "2403.04652",
        "title": "ShortGPT: Layers in Large Language Models are More Redundant Than You Expect",
        "authors": ["Xin Men", "Mingyu Xu", "Qingyu Zhang"],
        "abstract": "As Large Language Models (LLMs) continue to advance, the demand for computational resources has surged. We discover that LLMs exhibit significant redundancy across layers and propose a pruning approach based on Block Importance (BI) metric.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.LG"],
        "summary_what": "ShortGPT 发现大语言模型中存在大量冗余层——直接删除 25% 的层后模型性能仅下降 2-5%。基于此提出了一种基于层重要性度量的简单剪枝方法。",
        "summary_how": "定义了 Block Importance (BI) 指标：计算每层输入和输出隐藏状态之间的余弦相似度。BI 越高说明该层对表示的改变越小（越冗余）。按 BI 分数排序后，直接删除最冗余的层，无需重新训练。在 Llama-2 和 Baichuan 系列上验证。",
        "summary_why": "模型压缩通常需要量化或蒸馏等复杂流程。ShortGPT 证明了最简单的层剪枝就能达到显著的压缩效果，且其 BI 指标揭示了 LLM 内部信息流动的有趣特性——中间层普遍比首尾层更冗余，这对理解 LLM 的工作机制有重要启示。",
    },
    {
        "id": "arxiv:2403.04132v1",
        "arxiv_id_base": "2403.04132",
        "title": "KnowAgent: Knowledge-Augmented Planning for LLM-Based Agents",
        "authors": ["Yuqi Zhu", "Shuofei Qiao", "Yixin Ou"],
        "abstract": "Large Language Models (LLMs) have demonstrated great potential in complex reasoning tasks, yet they fall short when tackling more sophisticated challenges, especially when interacting with environments by generating action plans.",
        "primary_category": "cs.AI",
        "categories": ["cs.AI", "cs.CL"],
        "summary_what": "KnowAgent 通过引入外部知识库来增强 LLM Agent 的行动规划能力，解决了 Agent 在复杂环境中容易产生幻觉动作（调用不存在的工具或错误参数）的问题。",
        "summary_how": "构建了 Action Knowledge Base（AKB），存储每个可用动作的前置条件、参数约束和预期效果。规划时，LLM 先从 AKB 检索相关动作知识，再基于这些约束生成合法的行动序列。引入自我反思机制，在执行失败时回溯并修正计划。",
        "summary_why": "LLM Agent 最常见的失败模式就是「幻觉动作」——生成看似合理但环境不支持的操作。KnowAgent 通过知识约束将行动空间限定在合法范围内，在 HotPotQA 和 ALFWorld 基准上显著减少了无效动作率。",
    },
    {
        "id": "arxiv:2403.03507v1",
        "arxiv_id_base": "2403.03507",
        "title": "The Claude 3 Model Family: A New Standard for Intelligence",
        "authors": ["Anthropic Team"],
        "abstract": "We introduce the Claude 3 family of models, comprising Claude 3 Haiku, Claude 3 Sonnet, and Claude 3 Opus. These models set new benchmarks across a wide range of cognitive tasks, from expert knowledge to mathematical reasoning.",
        "primary_category": "cs.AI",
        "categories": ["cs.AI", "cs.CL"],
        "summary_what": "Claude 3 系列包含三个定位不同的模型（Haiku/Sonnet/Opus），在多项认知基准上达到了新的 SOTA，同时首次在多模态能力上追平了视觉专用模型。",
        "summary_how": "在预训练、RLHF、Constitutional AI 等多阶段训练中进行了全面优化。技术亮点包括：1) 改进的长上下文处理（200K token 窗口）；2) 增强的多模态理解能力；3) 更精准的指令跟随能力；4) 系统性降低拒绝率同时保持安全性。",
        "summary_why": "Claude 3 Opus 在 MMLU、GSM8K、HumanEval 等基准上超越了 GPT-4，标志着 Anthropic 从追赶者转变为领先者。系列化的产品策略（快/中/强）也为不同场景提供了最优性价比选择。",
    },
    {
        "id": "arxiv:2403.02884v1",
        "arxiv_id_base": "2403.02884",
        "title": "Design2Code: How Far Are We From Automating Front-End Engineering?",
        "authors": ["Chenglei Si", "Yanzhe Zhang", "Zhengyuan Yang"],
        "abstract": "We formalize the Design2Code task: given a screenshot of a web page, generate the corresponding HTML code that renders the same visual output. We collect a benchmark of 484 real-world web pages and evaluate state-of-the-art multimodal LLMs.",
        "primary_category": "cs.CV",
        "categories": ["cs.CV", "cs.SE", "cs.AI"],
        "summary_what": "Design2Code 建立了首个系统性的视觉稿到代码生成基准：给定网页截图，自动生成等效的 HTML/CSS 代码。评估了 GPT-4V 等多模态模型在这一任务上的能力边界。",
        "summary_how": "收集了 484 个真实网页作为测试集，设计了多维评估指标（视觉相似度、DOM 结构匹配、元素对齐等）。测试了 GPT-4V、Gemini Pro Vision 等模型的 zero-shot 和 few-shot 能力。还训练了专用的 Design2Code 微调模型作为对比。",
        "summary_why": "前端开发占据了大量重复性工作，自动化设计稿到代码的转换有巨大的工程价值。研究发现 GPT-4V 已能生成 49% 视觉相似度的网页代码，但在复杂布局和交互上仍有明显差距，指明了未来改进方向。",
    },
    {
        "id": "arxiv:2403.02181v1",
        "arxiv_id_base": "2403.02181",
        "title": "StarCoder 2 and The Stack v2: The Next Generation",
        "authors": ["Anton Lozhkov", "Raymond Li", "Loubna Ben Allal"],
        "abstract": "The BigCode project introduces StarCoder2, a family of open code LLMs trained on The Stack v2, a new large-scale code dataset. StarCoder2 models range from 3B to 15B parameters and achieve competitive performance with models trained on proprietary data.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.SE"],
        "summary_what": "StarCoder 2 是 BigCode 开源社区推出的新一代代码大模型系列（3B/7B/15B），基于全新构建的 The Stack v2 数据集训练，在代码补全和生成任务上达到了开源最佳水平。",
        "summary_how": "The Stack v2 数据集从 Software Heritage 档案馆收集，包含 619 种编程语言的 67.5TB 去重代码。训练策略包括：1) 多语言代码 + 技术文档混合训练；2) Fill-in-the-Middle 目标函数；3) 仓库级上下文窗口（最长 16K token）。所有数据处理流程和训练代码完全开源。",
        "summary_why": "代码 AI 是 LLM 商业化最成功的方向之一，但主流产品（Copilot/Codex）都基于闭源模型。StarCoder 2 证明开源模型可以匹敌闭源方案，同时其数据集构建方法论和许可合规流程，为后续开源代码模型树立了标杆。",
    },
    {
        "id": "arxiv:2403.01081v1",
        "arxiv_id_base": "2403.01081",
        "title": "Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models",
        "authors": ["Soham De", "Samuel L. Smith", "Anushan Fernando"],
        "abstract": "Recurrent models offer fast inference for long sequences but are challenging to train efficiently. We propose Griffin, a model that mixes gated linear recurrences with local attention, combining the strengths of both approaches.",
        "primary_category": "cs.LG",
        "categories": ["cs.LG", "cs.CL"],
        "summary_what": "Griffin 提出了一种混合架构：将门控线性循环单元与局部注意力交替组合，在保持线性推理复杂度的同时，匹配 Transformer 的训练质量和效率。",
        "summary_how": "架构设计：交替堆叠 Real-Gated Linear Recurrence（RGLRU）层和局部滑窗注意力层。RGLRU 使用对角化线性递推实现高效并行训练，局部注意力补充短程精细交互。在 300B token 上训练了 1B/3B/7B/14B 系列模型。",
        "summary_why": "Google DeepMind 的这项工作直接对标 Mamba，证明了线性循环 + 局部注意力的混合方案在质量和效率上都优于纯 SSM。对于工业级部署，Griffin 的混合策略提供了比纯 Transformer 更低的推理成本，比纯循环模型更稳定的训练收敛。",
    },
    {
        "id": "arxiv:2403.00858v1",
        "arxiv_id_base": "2403.00858",
        "title": "Towards Optimal Learning of Language Models",
        "authors": ["Yuxian Gu", "Li Dong", "Yaru Hao", "Furu Wei"],
        "abstract": "This work studies the general principles of improving learning efficiency of language models. We derive a theoretical framework showing that the optimal learning rate schedule and data curriculum should follow specific scaling laws.",
        "primary_category": "cs.LG",
        "categories": ["cs.LG", "cs.CL"],
        "summary_what": "本文从理论角度推导了语言模型最优训练策略，包括学习率调度和数据课程（curriculum）应遵循的 scaling law，并在实验中验证理论预测与实际训练高度吻合。",
        "summary_how": "基于在线学习理论框架，推导出：1) 最优学习率应按 1/sqrt(t) 衰减（而非常用的余弦调度）；2) 训练数据应从简单到复杂逐步引入，难度增长速率与模型容量相关。在 125M-1.3B 模型上的实验验证了理论预测，相同算力下训练效率提升约 5-10%。",
        "summary_why": "大模型训练的超参调优成本极高（一次 7B 训练 ~$100K），理论指导能显著减少试错。本文的 scaling law 为从业者提供了先验知识，在给定算力预算下可以直接推算出近似最优的训练配置。",
    },
    {
        "id": "arxiv:2402.19427v1",
        "arxiv_id_base": "2402.19427",
        "title": "Sora: A Review on Background, Technology, Limitations, and Opportunities of Large Vision Models",
        "authors": ["Yixin Liu", "Kai Zhang", "Yuan Li"],
        "abstract": "Sora is a text-to-video generative AI model, released by OpenAI in February 2024. This survey provides a comprehensive review of Sora's background, related technologies, current limitations, and future opportunities.",
        "primary_category": "cs.CV",
        "categories": ["cs.CV", "cs.AI"],
        "summary_what": "本文是对 OpenAI Sora 视频生成模型的全面综述，系统梳理了文生视频技术的发展脉络、Sora 可能采用的技术路线、当前局限性以及未来应用前景。",
        "summary_how": "从四个维度展开：1) 技术背景——Diffusion Transformer (DiT) 架构、视频 VAE、时空 patch 化方案；2) 能力分析——长视频一致性、物理世界模拟、多视角生成；3) 局限——物理规律违反、因果关系错误、人体结构异常；4) 应用前景——影视制作、游戏、教育、仿真。",
        "summary_why": "Sora 的发布标志着视频生成从 4 秒低分辨率片段跃升至 60 秒高清视频，引发了 AI 视频领域的范式转移。本综述在信息碎片化的早期阶段提供了系统性的技术分析，帮助研究者快速理解这一领域的全貌。",
    },
    {
        "id": "arxiv:2402.17764v1",
        "arxiv_id_base": "2402.17764",
        "title": "LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens",
        "authors": ["Yiran Ding", "Li Lyna Zhang", "Chengruidong Zhang"],
        "abstract": "Large context window is a desirable feature of large language models. We present LongRoPE that, for the first time, extends the context window of pre-trained LLMs to an impressive 2048k tokens.",
        "primary_category": "cs.CL",
        "categories": ["cs.CL", "cs.LG"],
        "summary_what": "LongRoPE 首次将预训练 LLM 的有效上下文窗口扩展到超过 200 万 token，且仅需 1000 步微调，同时在短文本上保持原有性能不退化。",
        "summary_how": "三个关键技术：1) 非均匀位置插值——对 RoPE 的不同频率维度采用不同的缩放因子（通过进化搜索优化）；2) 渐进式扩展——先扩展到 256K，再扩展到 2048K，每阶段仅需少量微调；3) 短文本性能修复——对短序列使用接近原始的位置编码以保持性能。",
        "summary_why": "超长上下文对于处理完整代码库、长篇文档、多轮对话等场景至关重要。此前方法在 128K 以上就会性能严重退化。LongRoPE 实现了数量级的突破，且方法简单、计算成本极低，为 LLM 的长文本应用铺平了道路。",
    },
]


async def main():
    from app.db import engine, AsyncSessionLocal
    from app.models.base import Base
    from app.models.paper import Paper

    # Create tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    now = datetime.utcnow()

    async with AsyncSessionLocal() as db:
        for i, data in enumerate(MOCK_PAPERS):
            # Spread published_at over the last 3 days
            days_ago = i % 3
            hours_offset = random.randint(0, 12)
            published = now - timedelta(days=days_ago, hours=hours_offset)

            paper = Paper(
                id=data["id"],
                arxiv_id_base=data["arxiv_id_base"],
                title=data["title"],
                authors=data["authors"],
                abstract=data["abstract"],
                published_at=published,
                url=f"https://arxiv.org/abs/{data['arxiv_id_base']}",
                pdf_url=f"https://arxiv.org/pdf/{data['arxiv_id_base']}.pdf",
                categories=data["categories"],
                primary_category=data["primary_category"],
                source_name="arxiv",
                summary_what=data["summary_what"],
                summary_how=data["summary_how"],
                summary_why=data["summary_why"],
                summary_status="done",
                summary_model="mock-gpt4o",
                fetched_at=now,
            )

            # Merge = insert or update
            merged = await db.merge(paper)

        await db.commit()
        print(f"Successfully seeded {len(MOCK_PAPERS)} mock papers into database.")


if __name__ == "__main__":
    asyncio.run(main())
