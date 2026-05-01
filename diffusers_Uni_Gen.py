import os
import argparse
import torch
from PIL import Image
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
import numpy as np
import cv2

#os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
torch.backends.cudnn.benchmark=True
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

TASK_SYSTEM_PROMPTS = {
    "text-to-video": "You are an AI that generates dynamic videos from text descriptions. Given only a text prompt, you must create a coherent, moving video that accurately depicts the described scene or action.",
    "text-to-image": "You are an AI that generates static images from text descriptions. IMPORTANT: The output must be a static video where every frame is identical, showing the generated image. Do not introduce any motion or animation.",
    "Image-editing": "You are an AI that edits static images based on instructions. Given a source static image video and an editing instruction, you must output a new static image video with the edit applied. Both input and output videos contain identical frames throughout — do not add motion.",
    "image-to-video": "You are an AI that animates static images into dynamic videos. Given a single static image as the first frame (the rest of the input video is black), you must generate a coherent moving video that naturally extends from that starting image, following the text instruction if provided.",
    "video-editing": "You are an AI that edits existing videos based on instructions. Given a source video and an editing instruction, you must generate a new video that faithfully applies the requested changes while preserving all unrelated content and maintaining temporal consistency.",
}

TASK_PREFIX_MAP = {
    "text_to_video": "text-to-video",
    "text_to_image": "text-to-image",
    "image_edit": "Image-editing",
    "image_to_video": "image-to-video",
    "video_edit": "video-editing",
}


# def load_video_frames(video_path, max_frames=81, max_pixels=720 * 1280):
#     """Load video frames as a list of PIL Images, resized to fit max_pixels."""
#     from torchvision.io import read_video
#     vframes, _, _ = read_video(video_path, pts_unit="sec")
#     frames = []
#     for i in range(min(len(vframes), max_frames)):
#         img = Image.fromarray(vframes[i].numpy())
#         w, h = img.size
#         scale = min(1.0, (max_pixels / (w * h)) ** 0.5)
#         if scale < 1.0:
#             new_w = int(w * scale) // 16 * 16
#             new_h = int(h * scale) // 16 * 16
#             img = img.resize((new_w, new_h), Image.LANCZOS)
#         frames.append(img)
#     return frames

def load_video_frames(video_path, max_frames=81, max_pixels=720*1280):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        # 调整尺寸（保持宽高比，对齐16的倍数）...
        frames.append(img)
    cap.release()
    return frames


def generate_white_frames(num_frames, width, height):
    """Generate a list of white PIL images (白视频用于 condition)."""
    white_img = Image.new('RGB', (width, height), (255, 255, 255))
    return [white_img.copy() for _ in range(num_frames)]


def image_to_repeat_frames(image_path, num_frames, max_pixels=720*1280):
    """Load an image and repeat it to create a list of identical frames."""
    img = Image.open(image_path).convert('RGB')
    w, h = img.size
    scale = min(1.0, (max_pixels / (w * h)) ** 0.5)
    if scale < 1.0:
        new_w = int(w * scale) // 16 * 16
        new_h = int(h * scale) // 16 * 16
        img = img.resize((new_w, new_h), Image.LANCZOS)
    return [img.copy() for _ in range(num_frames)]


def first_frame_plus_white_frames(image_path, num_frames, max_pixels=720*1280):
    """First frame from image, rest white."""
    img = Image.open(image_path).convert('RGB')
    w, h = img.size
    scale = min(1.0, (max_pixels / (w * h)) ** 0.5)
    if scale < 1.0:
        new_w = int(w * scale) // 16 * 16
        new_h = int(h * scale) // 16 * 16
        img = img.resize((new_w, new_h), Image.LANCZOS)
    white = Image.new('RGB', img.size, (255, 255, 255))
    frames = [img] + [white.copy() for _ in range(num_frames - 1)]
    return frames

def main():
    parser = argparse.ArgumentParser(description="UniGen-LingXi diffusers multi-task demo v2")
    parser.add_argument("--model_path", type=str, default="/root/.cache/modelscope/hub/models/haohanxingcheng/UniGen-LingXi-5B")
    parser.add_argument("--task_type", type=str, required=True,
                        choices=["text_to_video", "text_to_image", "image_edit", "image_to_video", "video_edit"],
                        help="Type of task to perform")
    parser.add_argument("--prompt", type=str, required=True,
                        help="User prompt (without task prefix)")
    parser.add_argument("--ref_image", type=str, default=None,
                        help="Path to reference image (optional)")
    parser.add_argument("--video_path", type=str, default=None,
                        help="Path to input video (required for video_edit)")
    parser.add_argument("--src_image", type=str, default=None,
                        help="Path to source image (required for image_edit, image_to_video)")
    parser.add_argument("--save_path", type=str, default="./output.mp4",
                        help="Output path (video .mp4 or image .png/.jpg)")
    parser.add_argument("--max_frames", type=int, default=81,
                        help="Number of frames to process (model max 81)")
    parser.add_argument("--max_pixels", type=int, default=720 * 648,
                        help="Max pixels for resizing")
    parser.add_argument("--num_inference_steps", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--device", type=str, default="cuda:0")
    parser.add_argument("--guidance_scale", type=float, default=5.0)
    parser.add_argument("--tiled", action="store_true", default=True,
                        help="Use tiled VAE decoding")
    args = parser.parse_args()

    # --- 构建带系统提示词的 prompt ---
    task_key = TASK_PREFIX_MAP[args.task_type]
    prompt_with_task = TASK_SYSTEM_PROMPTS[task_key] + args.prompt
    print(f"Task: {task_key}")
    print(f"Full prompt: {prompt_with_task[:100]}...")

    # --- 1. Load pipeline ---
    print(f"Loading pipeline from {args.model_path} ...")
    pipe = DiffusionPipeline.from_pretrained(
        args.model_path,
        trust_remote_code=True,
    )
    pipe.to(args.device, dtype=torch.bfloat16)

    # --- 2. Construct source_frames and ref_image based on task_type ---
    source_frames = None
    ref_image = None
    width, height = None, None
    if args.task_type == "text_to_video":
        # Condition: white video; need dimensions (default 720x1280)
        width, height = 720, 1280
        source_frames = generate_white_frames(args.max_frames, width, height)
        print(f"text-to-video: white condition video, {len(source_frames)} frames, {width}x{height}")

    elif args.task_type == "text_to_image":
        width, height = 1280, 1280
        source_frames = generate_white_frames(args.max_frames, width, height)
        print(f"text-to-image: white condition video, output will be first frame saved as image")

    elif args.task_type == "image_edit":
        if args.src_image is None:
            raise ValueError("--src_image required for image_edit task")
        source_frames = image_to_repeat_frames(args.src_image, args.max_frames, args.max_pixels)
        width, height = source_frames[0].size
        print(f"image_edit: source image repeated {len(source_frames)} frames, {width}x{height}")

    elif args.task_type == "image_to_video":
        if args.src_image is None:
            raise ValueError("--src_image required for image_to_video task")
        source_frames = first_frame_plus_white_frames(args.src_image, args.max_frames, args.max_pixels)
        width, height = source_frames[0].size
        print(f"image_to_video: first frame from image + white rest, {len(source_frames)} frames")

    elif args.task_type == "video_edit":
        if args.video_path is None:
            raise ValueError("--video_path required for video_edit task")
        source_frames = load_video_frames(args.video_path, args.max_frames, args.max_pixels)
        width, height = source_frames[0].size
        print(f"video_edit: loaded {len(source_frames)} frames from {args.video_path}")

    # --- 3. Optionally load reference image ---
    if args.ref_image:
        ref_image = [Image.open(ref).convert("RGB") for ref in args.ref_image.split(";")]
        print(f"Using reference image: {args.ref_image}")
    # --- 4. Run inference ---
    print(f"Running inference: \"{args.prompt}\"")
    video_tensor = pipe(
        prompt=prompt_with_task,
        source_video=source_frames,
        ref_image=ref_image,
        height=height,
        width=width,
        num_frames=len(source_frames),
        num_inference_steps=args.num_inference_steps,
        guidance_scale=args.guidance_scale,
        seed=args.seed,
        tiled=args.tiled,
    )

    # --- 5. Save output based on task type ---
    os.makedirs(os.path.dirname(args.save_path) or ".", exist_ok=True)
    if args.task_type in ["text_to_image", "image_edit"]:
        # Save first frame as image
        if isinstance(video_tensor, list):
            first_frame = video_tensor[0]
        elif torch.is_tensor(video_tensor):
            first_frame = Image.fromarray(video_tensor[0].cpu().numpy())
        else:
            first_frame = video_tensor[0]
        first_frame.save(args.save_path)
        print(f"Saved image to {args.save_path}")
    else:
        # Save as video (fps=16 to match training)
        export_to_video(video_tensor, args.save_path, fps=16)
        print(f"Saved video to {args.save_path}")


if __name__ == "__main__":
    main()
