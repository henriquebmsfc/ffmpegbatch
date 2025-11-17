from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}

def get_pairs(input_dir):
    input_dir = Path(input_dir)
    images = {}
    audios = {}

    for p in input_dir.rglob("*"):
        if p.is_file():
            ext = p.suffix.lower()
            name = p.stem.lower()

            if ext in IMAGE_EXTS:
                images[name] = p
            elif ext in AUDIO_EXTS:
                audios[name] = p

    pairs = []
    for n in set(images.keys()).intersection(audios.keys()):
        img = images[n]
        aud = audios[n]
        out = input_dir.parent / "output" / f"{n}.mp4"
        pairs.append((img, aud, out))

    return pairs
