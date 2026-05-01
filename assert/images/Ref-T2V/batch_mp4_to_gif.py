#!/usr/bin/env python3
"""
Batch convert MP4 videos to GIF using OpenCV and imageio.
No direct ffmpeg subprocess calls.
Dependencies: opencv-python, imageio, pillow
Install: pip install opencv-python imageio pillow
"""

import os
import argparse
from pathlib import Path
import cv2
import imageio
from PIL import Image

def convert_mp4_to_gif(input_path, output_path, fps=10, max_width=480, max_frames=None):
    """
    Convert a single MP4 file to GIF.
    :param input_path: Path to input MP4
    :param output_path: Path to output GIF
    :param fps: Output GIF frame rate (frames per second)
    :param max_width: Maximum width (height scales proportionally)
    :param max_frames: Maximum number of frames to use (None = all frames)
    """
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        print(f"  Error: Cannot open video {input_path}")
        return False

    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine frame step to achieve target fps
    if orig_fps > fps and orig_fps > 0:
        step = max(1, int(orig_fps / fps))
    else:
        step = 1

    frames = []
    frame_count = 0
    processed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % step == 0:
            if max_frames is not None and len(frames) >= max_frames:
                break
            # Convert BGR (OpenCV) to RGB (PIL)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize if needed
            h, w = rgb_frame.shape[:2]
            if w > max_width:
                new_h = int(h * max_width / w)
                rgb_frame = cv2.resize(rgb_frame, (max_width, new_h))
            frames.append(rgb_frame)
            processed += 1
        frame_count += 1

    cap.release()

    if not frames:
        print(f"  No frames extracted from {input_path}")
        return False

    # Write GIF using imageio
    try:
        # Convert frames to PIL Images to ensure consistent mode
        pil_frames = [Image.fromarray(frame) for frame in frames]
        # Save as GIF
        pil_frames[0].save(
            output_path,
            save_all=True,
            append_images=pil_frames[1:],
            duration=int(1000 / fps),
            loop=0,
            optimize=True
        )
    except Exception as e:
        print(f"  Error writing GIF: {e}")
        return False

    print(f"  Converted {input_path} -> {output_path} ({len(frames)} frames)")
    return True

def find_mp4_files(root_dir, recursive=True):
    """Find all .mp4 files in directory."""
    root = Path(root_dir)
    pattern = "**/*.mp4" if recursive else "*.mp4"
    return list(root.glob(pattern))

def main():
    parser = argparse.ArgumentParser(description="Batch convert MP4 to GIF (no ffmpeg CLI)")
    parser.add_argument("--input_dir", default=".", help="Directory containing MP4 files")
    parser.add_argument("--output_dir", type=str, default=None,
                        help="Output directory (default: same as input, adds '_gif' suffix or replaces extension)")
    parser.add_argument("--fps", type=int, default=10, help="Output GIF frame rate (default: 10)")
    parser.add_argument("--max_width", type=int, default=480, help="Max width in pixels (default: 480)")
    parser.add_argument("--max_frames", type=int, default=None, help="Max frames to use (default: all)")
    parser.add_argument("--recursive", action="store_true", default=True,
                        help="Search subdirectories recursively (default: True)")
    parser.add_argument("--no-recursive", dest="recursive", action="store_false",
                        help="Do not search subdirectories")
    parser.add_argument("--suffix", type=str, default="_converted",
                        help="Suffix for output filename (before extension, default: '_converted')")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} does not exist.")
        sys.exit(1)

    output_root = Path(args.output_dir) if args.output_dir else input_dir
    output_root.mkdir(parents=True, exist_ok=True)

    mp4_files = find_mp4_files(input_dir, recursive=args.recursive)
    if not mp4_files:
        print(f"No MP4 files found in {input_dir}")
        return

    print(f"Found {len(mp4_files)} MP4 files.")
    for mp4_path in mp4_files:
        # Preserve relative path structure if output_dir different
        if args.output_dir:
            rel_path = mp4_path.relative_to(input_dir) if args.recursive else mp4_path.name
            out_path = output_root / rel_path.with_suffix(f"{args.suffix}.gif")
            out_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            # Output in same directory, modify name
            out_path = mp4_path.with_name(f"{mp4_path.stem}{args.suffix}.gif")
        if out_path.exists():
            print(f"Skipping {mp4_path} -> {out_path} already exists")
            continue
        print(f"Processing {mp4_path} ...")
        convert_mp4_to_gif(
            mp4_path, out_path,
            fps=args.fps,
            max_width=args.max_width,
            max_frames=args.max_frames
        )

if __name__ == "__main__":
    import sys
    main()