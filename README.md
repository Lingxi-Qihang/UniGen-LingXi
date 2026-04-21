# UniGen-LingXi: 统一视频/图像生成与编辑框架

> **灵犀启航 (LingXi Qihang)** 出品 — 一个模型，五种任务

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Diffusers](https://img.shields.io/badge/diffusers-0.29.2-orange)](https://github.com/huggingface/diffusers)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](LICENSE)

**UniGen-LingXi** 基于 Kiwi‑Edit‑5B 模型，将五种主流视频/图像任务集成到一套代码中：

- ✅ 文生视频 (Text-to-Video)
- ✅ 文生图 (Text-to-Image)
- ✅ 图生视频 (Image-to-Video)
- ✅ 视频编辑 (Video Editing)
- ✅ 图像编辑 (Image Editing)

> 不再需要为不同任务切换模型！一个模型完成所有生成与编辑任务。

## 🚀 快速开始

### 环境安装

```bash
conda create -n unigen python=3.10
conda activate unigen
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate sentencepiece av opencv-python pillow imageio imageio-ffmpeg
```

### 五种任务示例

```bash
# 1. 文生视频
python diffusers_Uni_Gen.py \
    --task_type text_to_video \
    --prompt "text-to-video: 一位紫发女性在舞台上表演，灯光闪烁..." \
    --save_path output/t2v.mp4 \
    --model_path /path/to/kiwi-edit-5b-instruct

# 2. 文生图
python diffusers_Uni_Gen.py \
    --task_type text_to_image \
    --prompt "text-to-image: 一位紫发女性在舞台上表演..." \
    --save_path output/t2i.png \
    --model_path /path/to/kiwi-edit-5b-instruct

# 3. 图像编辑
python diffusers_Uni_Gen.py \
    --task_type image_edit \
    --src_image input.jpg \
    --prompt "Image-editing: 将上衣修改为低胸V领款式" \
    --save_path output/edited.png \
    --model_path /path/to/kiwi-edit-5b-instruct

# 4. 图生视频（静态图动画化）
python diffusers_Uni_Gen.py \
    --task_type image_to_video \
    --src_image input.png \
    --prompt "image-to-video: A cinematic video of a woman standing on a snowy beach..." \
    --save_path output/i2v.mp4 \
    --model_path /path/to/kiwi-edit-5b-instruct

# 5. 视频编辑
python diffusers_Uni_Gen.py \
    --task_type video_edit \
    --video_path input.mp4 \
    --prompt "video-editing: Remove the monkey." \
    --save_path output/edited_video.mp4 \
    --model_path /path/to/kiwi-edit-5b-instruct
```

> **提示**：`prompt` 中**必须包含任务前缀**（如 `text-to-video:`、`Image-editing:`），以便模型识别指令类型。

## 📦 开源计划

- **推理代码**：预计 **2026 年 5 月** 在 GitHub 仓库开源。
- **预训练权重**：届时一并发布（基于 Apache 2.0 许可）。

## 📄 引用

如果您在研究中使用了 UniGen-LingXi，请引用：

```bibtex
@misc{unigenlingxi2026,
  author = {LingXi Qihang},
  title = {UniGen-LingXi: A Unified Video-Image Generation and Editing Framework},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/Shybert-AI/UniGen-LingXi}
}
```

同时请引用底层模型 Kiwi-Edit：

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
