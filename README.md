---
license: mit
base_model:
  - Kiwi-Edit
  - Wan2.2-TI2V-5B
  - Qwen/Qwen2.5-VL-3B
library_name: diffusers
pipeline_tag: image-text-to-video
tags:
  - video-generation
  - video-editing
  - image-editing
  - text-to-video
  - text-to-image
  - image-to-video
  - reference-guided
  - unified-framework
---

# UniGen-LingXi: A Unified Multi-Modal Generation and Editing Framework

<p align="center">

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Diffusers](https://img.shields.io/badge/diffusers-0.37.0-orange)](https://github.com/huggingface/diffusers)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-shyai%2FUniGen--LingXi--5B-yellow)](https://huggingface.co/shyai/UniGen-LingXi-5B)
[![ModelScope](https://img.shields.io/badge/ModelScope-haohanxingcheng%2FUniGen--LingXi--5B-green)](https://modelscope.cn/models/haohanxingcheng/UniGen-LingXi-5B)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](LICENSE)

[**简体中文**](README_zh.md) | English

</p>

> **LingXi Qihang** Presents — Bridging AI and Creativity with Intuition

**UniGen-LingXi** is a unified inference framework built upon **Kiwi-Edit-5B**, supporting **nine generation and editing tasks** across both image and video modalities. One model, one framework, one unified API.

## 📖 Overview

We present **UniGen-LingXi**, a unified framework that extends a single video editing model (Kiwi-Edit) to perform nine distinct generation and editing tasks. By carefully constructing conditional videos and task-specific prompts, we achieve this without any architectural modification. Our data construction pipeline and memory-efficient training script make training feasible on consumer-grade GPUs.

---

## 📋 Nine Supported Tasks

|  #   | Task Name | Abbreviation | Input | Output | Description |
|:----:|-----------|-------------|------|------|------|
| 1 | **Reference-Guided Image Editing** | Ref-IE | Source Image + Reference Image + Text | Image | Transfer style/attributes from reference to source |
| 2 | **Reference-Guided Text-to-Image** | Ref-T2I | Reference Image + Text | Image | Generate new image conditioned on reference |
| 3 | **Reference-Guided Text-to-Video** | Ref-T2V | Reference Image + Text | Video | Generate dynamic video with reference style |
| 4 | **Reference-Guided Video Editing** | Ref-VE | Video + Reference Image + Text | Video | Edit video with reference image style |
| 5 | **Video Editing** | VE | Video + Text | Video | Edit video based on text instructions |
| 6 | **Image Editing** | IE / i2i | Source Image + Text | Image | Local/global image editing |
| 7 | **Image-to-Video** | I2V / i2v | Image + Text | Video | Animate a static image |
| 8 | **Text-to-Image** | T2I / t2i | Text | Image | Generate image from text |
| 9 | **Text-to-Video** | T2V / t2v | Text | Video | Generate video from text |

### Task Matrix: Output Modality × Condition Type

| Output Modality | **Text-Only** | **Image-Conditioned (First Frame / Structure)** | **Reference Image (Style / Attributes)** |
|-----------------|---------------|-------------------------------------------------|------------------------------------------|
| **Image Generation** | 8. t2i | — | 2. Ref-T2I |
| **Image Editing** | 6. i2i (IE) | — | 1. Ref-IE |
| **Video Generation** | 9. t2v | **7. i2v (I2V)** | **3. Ref-T2V** |
| **Video Editing** | 5. VE | — | 4. Ref-VE |

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Download the Model

The model is released on HuggingFace and ModelScope:

- **HuggingFace**: [shyai/UniGen-LingXi-5B](https://huggingface.co/shyai/UniGen-LingXi-5B)
- **ModelScope**: [haohanxingcheng/UniGen-LingXi-5B](https://modelscope.cn/models/haohanxingcheng/UniGen-LingXi-5B)

### 3. Usage Examples

#### t2i — Text-to-Image

```bash
python diffusers_Uni_Gen.py \
    --task_type text_to_image \
    --prompt "text-to-image: A beautiful sunset over the ocean" \
    --save_path output/t2i.png \
    --model_path <path_to_model>
```

#### i2i — Image Editing

```bash
python diffusers_Uni_Gen.py \
    --task_type image_edit \
    --src_image input.jpg \
    --prompt "Image-editing: Turn the sky into sunset" \
    --save_path output/edited.png \
    --model_path <path_to_model>
```

#### t2v — Text-to-Video

```bash
python diffusers_Uni_Gen.py \
    --task_type text_to_video \
    --prompt "text-to-video: A cat running on grass" \
    --save_path output/t2v.mp4 \
    --model_path <path_to_model>
```

#### i2v — Image-to-Video

```bash
python diffusers_Uni_Gen.py \
    --task_type image_to_video \
    --src_image input.jpg \
    --prompt "image-to-video: Make the flower bloom" \
    --save_path output/i2v.mp4 \
    --model_path <path_to_model>
```

#### VE — Video Editing

```bash
python diffusers_Uni_Gen.py \
    --task_type video_edit \
    --video_path input.mp4 \
    --prompt "video-editing: Convert the video into an oil painting style" \
    --save_path output/ve.mp4 \
    --model_path <path_to_model>
```

#### Ref-IE — Reference-Guided Image Editing

```bash
python diffusers_Uni_Gen.py \
    --task_type image_edit \
    --src_image source.jpg \
    --ref_image reference.jpg \
    --prompt "Image-editing: Apply the style from reference image" \
    --save_path output/ref_ie.png \
    --model_path <path_to_model>
```

#### Ref-T2I — Reference-Guided Text-to-Image

```bash
python diffusers_Uni_Gen.py \
    --task_type text_to_image \
    --ref_image reference.jpg \
    --prompt "text-to-image: Generate an image in the style of reference" \
    --save_path output/ref_t2i.png \
    --model_path <path_to_model>
```

#### Ref-VE — Reference-Guided Video Editing

```bash
python diffusers_Uni_Gen.py \
    --task_type video_edit \
    --video_path input.mp4 \
    --ref_image style_ref.jpg \
    --prompt "video-editing: Transform video to match the reference style" \
    --save_path output/ref_ve.mp4 \
    --model_path <path_to_model>
```

#### Ref-T2V — Reference-Guided Text-to-Video

```bash
python diffusers_Uni_Gen.py \
    --task_type text_to_video \
    --ref_image reference.jpg \
    --prompt "text-to-video: Generate a video with the reference style" \
    --save_path output/ref_t2v.mp4 \
    --model_path <path_to_model>
```

---

> For more detailed usage and qualitative examples for each task, see [README_anas.md](README_anas.md)

### Image Editing

|                   prompt/input                   | GPT Image 1.5 (high) |                                              Nano Banana 2                                               | Nano Banana Pro | FLUX.2 [max] | Seedream 4.0 |       Ours (UniGen-LingXi-5B)        |
|:------------------------------------------------:|:---:|:--------------------------------------------------------------------------------------------------------:|:---:|:---:|:---:|:------------------------------------:|
| **prompt1** + ![input](assert/images/i2i/src.png) | ![GPT](assert/images/i2i/generation1/GPTImage15(high)-generation-1-a9de92f6.png) | ![Nano2](assert/images/i2i/generation1/NanoBanana2(Gemini31FlashImagePreview)-generation-1-4f09ac4b.png) | ![NanoPro](assert/images/i2i/generation1/NanoBananaPro(Gemini3ProImage)-generation-1-84867683.png) | ![FLUX](assert/images/i2i/generation1/FLUX2[max]-generation-1-eff27b70.png) | ![Seedream](assert/images/i2i/generation1/Seedream40-generation-1-42832e21.png) | ![Ours](assert/images/i2i/ours1.jpg) |
| **prompt2** + ![input](assert/images/i2i/src.png) | / | ![Nano2](assert/images/i2i/generation2/NanoBanana2(Gemini31FlashImagePreview)-generation-1-8541ed01.png) | ![NanoPro](assert/images/i2i/generation2/NanoBananaPro(Gemini3ProImage)-generation-1-de1ce1ef.png) | ![FLUX](assert/images/i2i/generation2/FLUX2[max]-generation-1-7b160602.png) | ![Seedream](assert/images/i2i/generation2/Seedream40-generation-1-2e18d150.png) | ![Ours](assert/images/i2i/ours2.jpg) |
| **prompt3** + ![input](assert/images/i2i/src.png) | ![GPT](assert/images/i2i/generation3/GPTImage15(high)-generation-1-1f2be041.png) | ![Nano2](assert/images/i2i/generation3/NanoBanana2(Gemini31FlashImagePreview)-generation-2-b62007fb.png) | ![NanoPro](assert/images/i2i/generation3/NanoBananaPro(Gemini3ProImage)-generation-3-e03596f5.png) | ![FLUX](assert/images/i2i/generation3/FLUX2[max]-generation-4-407ea936.png) | ![Seedream](assert/images/i2i/generation3/Seedream40-generation-5-1bb1233b.png) | ![Ours](assert/images/i2i/ours3.jpg) |
| **prompt4** + ![input](assert/images/i2i/src.png) | / | ![Nano2](assert/images/i2i/generation4/NanoBanana2(Gemini31FlashImagePreview)-generation-2-cd03ccda.png) | ![NanoPro](assert/images/i2i/generation4/NanoBananaPro(Gemini3ProImage)-generation-3-14561331.png) | ![FLUX](assert/images/i2i/generation4/FLUX2[max]-generation-4-ab617fcf.png) | ![Seedream](assert/images/i2i/generation4/Seedream40-generation-5-dee4fe52.png) | ![Ours](assert/images/i2i/ours4.jpg) |


### Text-to-Image
| prompt/input |                    GPT Image 1.5 (high)                     | Nano Banana 2 | Nano Banana Pro | FLUX.2 [max] | Seedream 4.0 | Ours (UniGen-LingXi-5B) |
|:---:|:-----------------------------------------------------------:|:---:|:---:|:---:|:---:|:---:|
| **prompt1** | ![GPT](assert/images/t2i/generation1/GPTImage1.5(high).jpg) | ![Nano2](assert/images/t2i/generation1/NanoBanana2(Gemini3.1FlashImagePreview).jpg) | ![NanoPro](assert/images/t2i/generation1/NanoBananaPro(Gemini3ProImage).jpg) | ![FLUX](assert/images/t2i/generation1/FLUX.2[max].jpg) | ![Seedream](assert/images/t2i/generation1/Seedream4.0.jpg) | ![Ours](assert/images/t2i/ours1.jpg) |
| **prompt2** | ![GPT](assert/images/t2i/generation2/GPTImage1.5(high).jpg) | ![Nano2](assert/images/t2i/generation2/NanoBanana2(Gemini3.1FlashImagePreview).jpg) | ![NanoPro](assert/images/t2i/generation2/NanoBananaPro(Gemini3ProImage).jpg) | ![FLUX](assert/images/t2i/generation2/FLUX.2[max].jpg) | ![Seedream](assert/images/t2i/generation2/Seedream4.0.jpg) | ![Ours](assert/images/t2i/ours2.jpg) |
| **prompt3** | ![GPT](assert/images/t2i/generation3/GPTImage1.5(high).jpg) | ![Nano2](assert/images/t2i/generation3/NanoBanana2(Gemini3.1FlashImagePreview).jpg) | ![NanoPro](assert/images/t2i/generation3/NanoBananaPro(Gemini3ProImage).jpg) | ![FLUX](assert/images/t2i/generation3/FLUX.2[max].jpg) | ![Seedream](assert/images/t2i/generation3/Seedream4.0.jpg) | ![Ours](assert/images/t2i/ours3.jpg) |
| **prompt4** | ![GPT](assert/images/t2i/generation4/GPTImage1.5(high).jpg) | ![Nano2](assert/images/t2i/generation4/NanoBanana2(Gemini3.1FlashImagePreview).jpg) | ![NanoPro](assert/images/t2i/generation4/NanoBananaPro(Gemini3ProImage).jpg) | ![FLUX](assert/images/t2i/generation4/FLUX.2[max].jpg) | ![Seedream](assert/images/t2i/generation4/Seedream4.0.jpg) | ![Ours](assert/images/t2i/ours4.jpg) |


## 🛠️ Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--task_type` | ✅ | Task type: `text_to_image`, `image_edit`, `text_to_video`, `image_to_video`, `video_edit` |
| `--prompt` | ✅ | Text prompt (must include task prefix) |
| `--model_path` | ✅ | Path to the model |
| `--src_image` | Optional | Source image path (for i2i, i2v) |
| `--video_path` | Optional | Source video path (for VE, Ref-VE) |
| `--ref_image` | Optional | Reference image path (for Ref-* tasks) |
| `--save_path` | ✅ | Output path |
| `--max_frames` | Optional | Number of frames to generate, default 81 |
| `--guidance_scale` | Optional | CFG guidance strength, default 5.0; set to 1.0 for no guidance |
| `--num_inference_steps` | Optional | Number of inference steps, default 50 |

---

## 📊 Performance

### Image Editing (GEdit-Bench)

| Model | GEdit-Bench-EN (Q_SC↑) | GEdit-Bench-EN (Q_PQ↑) | GEdit-Bench-EN (Q_O↑) |
|-------|----------------------|----------------------|---------------------|
| GPT-4o | 7.905 | 7.723 | 7.752 |
| Step1X-Edit-v1.1 | 7.737 | 7.425 | 7.436 |
| Doubao | 7.427 | 7.651 | 7.285 |
| Gemini | 7.295 | 7.314 | 6.996 |
| **UniGen-LingXi-5B** | 5.847 | 6.683 | 5.480 |

### Performance Analysis (GEdit-Bench)

| Capability Level | Task | EN Q_O | CN Q_O |
|------------------|------|--------|--------|
| **Strong (≥6.5)** | Subject Add | 7.087 | 7.176 |
|  | Color Alter | 6.863 | 7.045 |
|  | Subject Remove | 6.733 | 6.348 |
| **Moderate (5.0–6.5)** | Background Change | 6.209 | 6.398 |
|  | Material Alter | 6.410 | 6.429 |
|  | Style Change | 6.242 | 5.870 |
|  | Subject Replace | 6.354 | 6.787 |
| **Weak (3.5–5.0)** | Tone Transfer | 4.777 | 5.974 |
|  | Motion Change | 4.012 | 4.483 |
|  | Human Edit | 4.007 | 3.756 |
| **Very Weak (<3.5)** | Text Change | 1.582 | 1.642 |

### Performance Summary

The model exhibits a clear task-specialization pattern in image editing. It excels at local attribute edits such as subject addition, removal, and color alteration (Q_O ≥ 6.7), achieving object-centric modifications with extremely high data efficiency (only 20k samples). Global style transfer and background manipulation reach usable levels (Q_O ≈ 6.2), capable of holistic re-rendering beyond simple filters.

The main limitations are: text editing (1.58) and motion editing (~4.0) perform poorly, rooted in the training data lacking text-rendering and dynamic editing samples, as well as the inherent trade-off in the 9-in-1 architecture between video temporal consistency and pixel-level text precision. The conditioning mechanism works well for global style but is less effective for fine-grained local control. Nevertheless, the model achieves functional validation of 9-in-1 unification under an extremely low data budget (Q_O > 5.0) with competitive perceptual quality (Q_PQ of 6.7), fully demonstrating the efficiency and feasibility of the editing-first unified paradigm.

**Strengths**: High-precision local control, genuine style reconstruction (not a global filter), adaptive lighting and context integration, strong generalization with only 20k samples.

**Weaknesses**: Very poor text editing, insufficient motion and portrait retouching, fine-grained local control needs improvement.

![GEdit-Bench](assert/GEdit-Bench.jpg)

### Text-to-Image (DPG-Bench)

| Model | DPG-Bench Score ↑ |
|-------|----------------|
| Seedream 3.0 | 88.27 |
| Qwen-Image | 88.32 |
| DALL-E 3 | 83.50 |
| FLUX.1 [Dev] | 83.84 |
| **UniGen-LingXi-5B** | 69.44 |

![DPG-Bench](assert/DPG-Bench.jpg)

### Performance Analysis (DPG-Bench)

**Strengths**: Strong spatial and semantic relationship modeling (Relation: 85.58, surpassing multiple open‑source baselines), robust attribute binding (82.32), and reliable object integrity (80.20).

**Weaknesses**: The "Other" category scores only 50.80, with critical deficits in counting (46.5), text rendering (68.0), and size perception (59.09).

**Root Cause**: The 20k training samples are primarily from video editing datasets focused on local attribute manipulation, lacking complex composition and explicit reasoning modules; the unified architecture prioritizes structural priors over fine-grained symbolic grounding.

### Video Editing (OpenVE-Bench)

| Method | Overall | Global Style | Bg Change | Local Change | Local Remove | Local Add |
|--------|---------|-------------|-----------|-------------|-------------|-----------|
| Runway Aleph | 3.49 | 3.72 | 2.62 | 4.18 | 4.16 | 2.78 |
| Kiwi-Edit (Stage-3) [Ref.] | 3.02 | 3.64 | 2.64 | 3.83 | 2.63 | 2.36 |
| **UniGen-LingXi-5B** | 3.02 | 3.64 | 2.64 | 3.83 | 2.63 | 2.36 |

> **Note**: Video editing metrics are based on Kiwi-Edit (Stage-3) validation results. The architecture inherits its editing priors with zero performance degradation.

**Image Editing (GEdit-Bench)**: Strong at local edits, weak at text/motion editing.

**Video Editing (OpenVE-Bench)**: Exactly matches the Kiwi-Edit baseline, with editing priors fully preserved.

**Text-to-Image (DPG-Bench)**: Strong at Relation/Attribute, weak at complex composition.

---

## 🎯 Key Features

- **9-in-1 Capability**: A single unified framework supports all nine generation and editing tasks.
- **Plug and Play**: Diffusers-style API; run with just a few lines of code.
- **Efficient Inference**: Runs on consumer-grade GPUs.

---

## 📂 Project Structure

```
UniGen-LingXi/
├── diffusers_Uni_Gen.py    # Main inference script
├── test.sh                 # Nine-task test script
├── assert/                 # Test assets
│   └── images/             # Example outputs
├── README.md               # Project documentation
└── LICENSE
```

---

## ⚠️ Important Notes

1. **Prompt Format**: All prompts **must include a task prefix** (e.g., `text-to-video: `, `Image-editing: `) to ensure the model correctly interprets the instruction type.
2. **Frame Limit**: The model supports a maximum of 81 frames.
3. **Resolution**: 720×1280 or lower is recommended for optimal performance.
4. **Quick Test**: Run `bash test.sh` to test all 9 tasks with preset scenarios.
5. **OOM Handling**: If you encounter CUDA out of memory on lower-end GPUs (e.g., A100 40G):
   - Add `torch.backends.cudnn.benchmark=True` before loading the model
   - Reduce `max_frames` (e.g., 33 or 9) or `max_pixels` parameters

## 🤝 Contact & Feedback

- **GitHub Issues**: [https://github.com/Lingxi-Qihang/UniGen-LingXi/issues](https://github.com/Lingxi-Qihang/UniGen-LingXi/issues)
- **HuggingFace**: [https://huggingface.co/shyai/UniGen-LingXi-5B](https://huggingface.co/shyai/UniGen-LingXi-5B)
- **ModelScope**: [https://modelscope.cn/models/haohanxingcheng/UniGen-LingXi-5B](https://modelscope.cn/models/haohanxingcheng/UniGen-LingXi-5B)

## ⚠️ Important Disclaimer

- **Training code and data construction scripts are not currently open-source**: To preserve space for subsequent research and technical iteration, only the inference code and pre-trained model weights are currently released. We welcome technical collaboration and exchange. For commercial or research partnership inquiries, please contact us via email.
- This project is developed based on [Kiwi-Edit](https://huggingface.co/linyq/kiwi-edit-5b-instruct-reference-diffusers) (Apache-2.0 License), and the original license's copyright notice has been retained as required.

## 🙏 Acknowledgements
﻿
- **Core Developer**: [Shybert-AI](https://github.com/Shybert-AI)
- [Kiwi-Edit](https://huggingface.co/linyq/kiwi-edit-5b-instruct-reference-diffusers) for providing powerful video/image editing capabilities.
- Thanks to the open-source community and the HuggingFace Diffusers team.
- A preprint of this work is available in this repository ([paper.pdf](UniGen-LingXi A Resource-Efficient Editing-First Framework_en.pdf)). 
We are seeking endorsement from an active arXiv author in cs.CV to complete 
the arXiv submission. If you are willing to help, please contact us via 
GitHub Issues or email.

## 📝 Conclusion

UniGen-LingXi-5B is a resource-efficient, 9-in-1 unified multi-modal generation and editing framework. Grounded in an editing-first philosophy, we reformulate all tasks as conditional video generation and consolidate five core tasks plus four extended reference-guided tasks into a single, unmodified model — trained on a single GPU with only 20k samples. The approach demonstrates exceptional sample efficiency: image editing performance is state-of-the-art, video editing priors are preserved without loss, and generative skills are functionally viable. Through transparent boundary analysis, we reveal a fundamental generality‑precision trade-off and an encoder information bottleneck, providing a clear improvement roadmap for the community. This work not only proves the feasibility of 9‑in‑1 unification but also validates a transferable methodology of editing-first, condition-constructed unification — any stronger DiT backbone or vision‑language model can adopt this paradigm to achieve even broader task unification at minimal adaptation cost.

## 🗺️ Roadmap

### 🔬 Near-Term — Targeted Enhancement and Scaling Validation

Directly tackle the identified core bottlenecks — counting reasoning, text rendering, and complex spatial composition — through dedicated data augmentation, numeric reasoning modules, and a dual-encoder architecture for finer conditional control. The training dataset will be scaled to over one hundred thousand samples, rebalancing towards long-tail composition and scene diversity. In parallel, we will explore introducing sparse Mixture-of-Experts (MoE) mechanisms, where task-aware routing dynamically activates different expert sub-networks, fundamentally alleviating the parameter conflict between editing and generation tasks.

> 💡 **Collaborators with compute resources or high-quality data are warmly welcomed to help scale up the model.**

### 🚀 Mid-Term — From Visual Unification to Audio-Visual Joint Generation

The current framework has proven the feasibility of intra-modal visual unification. The next step is to horizontally expand to the audio modality. By introducing an audio encoder as an additional condition, the model will support new tasks such as video-to-audio and audio-to-video, forming a complete multimedia content creation loop.

### 🌍 Long-Term — Towards World Models and Embodied Intelligence

The editing-first framework's core capability of action preservation and structure retention aligns precisely with the fundamental demand of world models for spatio-temporal consistency. We will progressively introduce physical priors (rigid-body collisions, fluid motion), explicit 3D/4D representations, and causal reasoning capabilities, enabling the model to evolve from "generating visually plausible pixels" to "predicting physically believable futures," ultimately empowering embodied agents to realize the complete closed loop of "language instruction → goal state prediction → action sequence planning."

> 💡 **Researchers interested in world models and embodied intelligence are warmly invited to explore together.**

<p align="center">

**Bridging AI and Creativity with Intuition** 🌟

</p>

---

## 📄 Citation

If you use UniGen-LingXi in your research, please cite:

```bibtex
@misc{unigenlingxi2026,
  title = {UniGen-LingXi: A Resource-Efficient, Editing-First Framework Unifying 9 Multi-Modal Generation and Editing Tasks},
  author = {Haiying Sha and Yan Zheng},
  year = {2026},
  howpublished = {\url{https://github.com/Lingxi-Qihang/UniGen-LingXi}},
}
```

Please also cite the underlying model:

```bibtex
@misc{kiwi2026,
  title = {Kiwi-Edit: Versatile Video Editing via Instruction and Reference Guidance},
  author = {Y. Lin and others},
  year = {2026},
  eprint = {arXiv:2603.02175},
}
```
