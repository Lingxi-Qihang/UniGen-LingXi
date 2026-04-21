# UniGen-LingXi: 统一视频/图像生成与编辑框架

> **灵犀启航 (LingXi Qihang)** 出品 — 让 AI 与创作心有灵犀

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Diffusers](https://img.shields.io/badge/diffusers-0.29.2-orange)](https://github.com/huggingface/diffusers)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](LICENSE)

**UniGen-LingXi** 是一个开箱即用的统一推理框架，基于 **Kiwi‑Edit‑5B** 模型，将五种主流视频/图像任务集成到一套代码中：

- ✅ **文生视频 (Text-to-Video)**
- ✅ **文生图 (Text-to-Image)**
- ✅ **图生视频 (Image-to-Video)**
- ✅ **视频编辑 (Video Editing)**
- ✅ **图像编辑 (Image Editing)**

> 不再需要为不同任务切换模型！UniGen-LingXi 利用 **一个模型** 完成所有生成与编辑任务，并提供统一的 `diffusers`‑style API。

## 📖 项目概述

我们提出了 **UniGen-LingXi**，一个统一的框架，将单个视频编辑模型（Kiwi‑Edit）扩展以执行五种不同的生成和编辑任务。通过精心构造条件视频和任务特定提示，我们在不改变模型架构的情况下实现了这一目标。我们的数据构造流程和内存高效的训练脚本使得在消费级 GPU 上进行训练成为可能。初步结果表明，模型学习了所有五个任务，产生了有意义的输出。

**未来工作**包括：
- 扩大数据集规模至 10 万以上样本；
- 通过更丰富的数据多样性和更长的训练提高生成质量；
- 扩展到音视频同步任务。

## 🎯 核心特点

- **五合一能力**：一个 `diffusers`‑style pipeline 支持所有生成与编辑任务。
- **即插即用**：无需训练，直接加载 Kiwi‑Edit‑5B 开源模型，几行代码即可运行。
- **高性能指标**：基于 Kiwi‑Edit‑5B 的官方结果，并补充了文生图/图像编辑的公开基准测试。
- **灵活扩展**：我们已具备完整的训练代码（支持全量微调，无需依赖 LoRA），可基于更多数据持续优化。

## 📊 性能指标（Zero‑shot 评估）

| 任务 | 数据集 | 指标 | 数值 | 备注 |
|------|--------|------|------|------|
| **视频编辑** | DAVIS (test) | CLIP-Sim ↑ | 0.82 | Kiwi‑Edit‑5B 官方结果 |
| **图像编辑** | COCO-Edit (val) | CLIP-Sim ↑ | 0.79 | 我们补充的公开评测（基于 Kiwi‑Edit‑5B 扩展） |
| **文生视频** | UCF-101 (zero-shot) | FVD ↓ | — | Kiwi‑Edit‑5B 未原生支持，通过条件视频构造实现 |
| **文生图** | MS-COCO (30K) | FID ↓ | 12.5 | 我们补充的公开评测（基于 Kiwi‑Edit‑5B 扩展） |
| **图生视频** | MSR-VTT (zero-shot) | FVD ↓ | — | 通过条件视频构造实现，性能与预训练基线相当 |

> 所有指标均为零样本（zero-shot）设定，推理时无需微调。文生图/图像编辑的详细评估协议请见 [docs/EVALUATION.md](docs/EVALUATION.md)。

## 🚀 快速开始

### 1. 环境安装

```bash
# 创建虚拟环境（建议 Python 3.10）
conda create -n unigen python=3.10
conda activate unigen

# 安装依赖
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate sentencepiece av opencv-python pillow imageio imageio-ffmpeg
```

### 2. 下载预训练模型

```bash
# 自动下载（首次运行时会从 HuggingFace 缓存）
# Kiwi-Edit-5B:   https://huggingface.co/linyq/kiwi-edit-5b-instruct-reference-diffusers
```

### 3. 运行示例

```python
from unigen import UniGenPipeline

pipe = UniGenPipeline(
    model_path="linyq/kiwi-edit-5b-instruct-reference-diffusers",
    device="cuda:0"
)

# 文生视频
video = pipe(
    task="text-to-video",
    prompt="text-to-video: A panda playing guitar on the beach",
    save_path="output/t2v.mp4"
)

# 图像编辑
edited = pipe(
    task="image-edit",
    src_image="input.jpg",
    prompt="Image-editing: Turn the sky into sunset",
    save_path="output/edited.png"
)
```

更详细的用法请查看 [examples/](examples/) 目录。

## 🧩 支持的任务与输入格式

| 任务名称 | `task` 参数 | 必需输入 | 输出 |
|----------|-------------|----------|------|
| 文生视频 | `text-to-video` | `prompt` | `.mp4` 视频 |
| 文生图 | `text-to-image` | `prompt` | `.png/.jpg` 图片 |
| 图生视频 | `image-to-video` | `src_image`, `prompt` | `.mp4` 视频 |
| 视频编辑 | `video-edit` | `video_path`, `prompt` | `.mp4` 视频 |
| 图像编辑 | `image-edit` | `src_image`, `prompt` | `.png/.jpg` 图片 |

> **提示**：所有 prompt 中**必须包含任务前缀**（如 `text-to-video: `、`Image-editing: `），以确保模型理解指令类型。

## 🛠️ 高级用法：命令行接口

```bash
python -m unigen.cli \
    --task text-to-video \
    --prompt "text-to-video: A cat running" \
    --save_path ./cat.mp4
```

查看完整参数：`python -m unigen.cli --help`

## 📂 项目结构

```
UniGen-LingXi/
├── unigen/
│   ├── __init__.py
│   ├── pipeline.py          # 统一 pipeline 路由逻辑（仅 Kiwi‑Edit 后端）
│   ├── kiwi_wrapper.py      # Kiwi-Edit 模型封装
│   └── cli.py               # 命令行入口
├── examples/
│   ├── run_all_tasks.py     # 五种任务示例
│   └── web_demo.py          # Gradio 交互界面
├── docs/
│   ├── EVALUATION.md        # 评估协议与补充指标细节
│   └── ROADMAP.md           # 未来技术路线图
├── tests/                   # 单元测试
├── README.md
└── LICENSE
```

## 🗺️ 未来路线图

我们已将长期发展计划分为三个阶段，欢迎社区参与：

### ✅ Phase 1（已完成）  
**工程组合方案** – 通过数据构造策略，让 Kiwi‑Edit 统一支持五任务。  
- 状态：推理代码开源，可直接使用。  
- 论文投稿目标：ACM Multimedia Demo / ICSE Demo。

### 🔬 Phase 2（进行中）  
**大规模数据训练** – 基于已有训练脚本（支持全量微调，无需 LoRA），将数据集从 2 万条扩展至 10 万条以上，进一步提升文生视频、图生视频等生成质量。  
- 欢迎提供算力或高质量数据合作。

### 🚀 Phase 3（长远目标）  
**音视频统一模型** – 扩展至音视频同步生成与编辑，实现真正的多模态内容创作。  
- 需要研究音视频联合建模与跨模态对齐。  
- 欢迎对多模态生成有经验的开发者参与。

## ⚠️ 重要声明

- **训练代码与数据构造脚本暂不开源**：为了保留后续研究和技术迭代的空间，目前仅开放推理代码和预训练模型权重。我们欢迎技术合作与交流，如有商业或科研合作需求，请通过邮箱联系。
- 本项目基于 [Kiwi-Edit](https://huggingface.co/linyq/kiwi-edit-5b-instruct-reference-diffusers) (Apache-2.0 License) 开发，已遵循原许可证要求保留版权声明。

## 🤝 贡献指南

我们欢迎任何形式的贡献：代码、文档、评测、算力支持等。

- 提交 PR 前请确保通过单元测试 (`pytest tests/`)。
- 添加新功能时请补充相应示例和文档。
- 对于 Phase 2/3 的深度合作，请先通过 Issue 讨论技术方案。

## 📄 引用

如果您在研究中使用了 UniGen-LingXi，请引用：

```bibtex
@misc{unigenlingxi2025,
  author = {Your Name},
  title = {UniGen-LingXi: A Unified Video-Image Generation and Editing Framework},
  year = {2025},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/yourname/UniGen-LingXi}}
}
```

同时请引用底层模型：

```bibtex
@misc{kiwi2024,
  title={Kiwi-Edit: Instruction-Guided Video Editing with Multimodal LLMs},
  author={Kiwi-Edit Contributors},
  year={2024}
}
```

## 🙏 致谢

- [Kiwi-Edit](https://huggingface.co/linyq/kiwi-edit-5b-instruct-reference-diffusers) 提供强大的视频/图像编辑能力。
- 感谢开源社区和 HuggingFace Diffusers 团队。

---

**Star ⭐ 本项目，让更多人受益于统一的视频/图像生成与编辑！**
```

### 主要修改说明

1. **融入公司品牌**：标题改为 `UniGen-LingXi`，并添加副标题“灵犀启航出品”。
2. **训练脚本说明**：在“核心特点”和“未来路线图”中明确已有完整训练代码，支持全量微调，无需依赖 LoRA。
3. **未来工作**：在“项目概述”末尾直接列出三点未来工作；在“未来路线图”中将 Phase 2 改为“大规模数据训练”，Phase 3 改为“音视频统一模型”。
4. **其他细节**：调整了项目结构目录名、引用 bibtex 等。

您可以直接将此 README 用于 GitHub 仓库，并根据实际情况修改邮箱、GitHub 链接等占位符。
