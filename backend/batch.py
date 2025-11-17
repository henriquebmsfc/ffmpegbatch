import subprocess
from multiprocessing import Pool, cpu_count
from pathlib import Path
from PIL import Image
from utils import get_pairs

TARGET_W = 1280
TARGET_H = 720
CRF = 23
PRESET = "veryfast"


def resize_image(img_path):
    out_path = img_path.with_suffix(".resized.jpg")
    if out_path.exists():
        return out_path

    img = Image.open(img_path)
    img = img.convert("RGB")
    img.thumbnail((TARGET_W, TARGET_H))

    canvas = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
    x = (TARGET_W - img.width) // 2
    y = (TARGET_H - img.height) // 2
    canvas.paste(img, (x, y))
    canvas.save(out_path, quality=95)

    return out_path


def process_pair(pair):
    img, aud, out = pair
    out.parent.mkdir(exist_ok=True, parents=True)

    resized = resize_image(img)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(resized),
        "-i", str(aud),
        "-c:v", "libx264", "-preset", PRESET, "-crf", str(CRF),
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest", str(out)
    ]

    print("Rodando:", " ".join(cmd))
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return str(out)


def run_batch(input_dir="data/input"):
    pairs = get_pairs(input_dir)
    print(f"Encontrados {len(pairs)} pares.")

    if not pairs:
        return []

    workers = cpu_count()
    print(f"Processando em paralelo ({workers} workers).")

    with Pool(workers) as pool:
        results = pool.map(process_pair, pairs)

    return results
