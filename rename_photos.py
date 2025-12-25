import os
from PIL import Image

# ========= 配置 =========
SRC_DIR = "./photos"
DST_DIR = "./photos_webp"
MAX_SIZE = 1536        # 最长边限制
WEBP_QUALITY = 80      # 75~85 通常都很不错
LOSSLESS = False       # False = 有损（更小）；True = 无损（更大）
# =======================

os.makedirs(DST_DIR, exist_ok=True)

def resize_keep_ratio(img, max_size):
    w, h = img.size
    if max(w, h) <= max_size:
        return img

    if w >= h:
        new_w = max_size
        new_h = int(h * max_size / w)
    else:
        new_h = max_size
        new_w = int(w * max_size / h)

    return img.resize((new_w, new_h), Image.LANCZOS)

def convert_one(png_path):
    name = os.path.splitext(os.path.basename(png_path))[0]
    webp_path = os.path.join(DST_DIR, name + ".webp")

    with Image.open(png_path) as img:
        # 确保是 RGB（PNG 可能是 RGBA）
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img = resize_keep_ratio(img, MAX_SIZE)

        img.save(
            webp_path,
            "WEBP",
            quality=WEBP_QUALITY,
            lossless=LOSSLESS,
            method=6   # 压缩算法等级（0~6，6 最好）
        )

    return webp_path

def main():
    files = [f for f in os.listdir(SRC_DIR) if f.lower().endswith(".png")]
    files.sort()

    if not files:
        print("❌ 没找到 PNG 文件")
        return

    print(f"📸 找到 {len(files)} 张 PNG，开始转换…")

    for i, f in enumerate(files, 1):
        src = os.path.join(SRC_DIR, f)
        dst = convert_one(src)
        print(f"[{i:02d}/{len(files)}] {f} → {os.path.basename(dst)}")

    print("✅ 全部转换完成！")

if __name__ == "__main__":
    main()
