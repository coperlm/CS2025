import os
from PIL import Image

# 用户设置参数
image_folder = '图像篡改-深北莫 黄继武'  # 图片文件夹路径
target_size = (4624, 2080)  # 标准模式尺寸
mode = 1  # 1 = 标准缩放模式，2 = 原图直接拼接模式

# 自动生成输出路径
folder_name = os.path.basename(os.path.normpath(image_folder))
output_path = f"{folder_name}.pdf"  # 保存到主目录

# 获取图像列表
image_list = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_list.sort()

processed_images = []

for filename in image_list:
    img_path = os.path.join(image_folder, filename)
    img = Image.open(img_path).convert('RGB')

    if mode == 1:
        # 模式1：缩放填充裁剪至 target_size
        orig_width, orig_height = img.size
        ratio_w = target_size[0] / orig_width
        ratio_h = target_size[1] / orig_height
        scale = max(ratio_w, ratio_h)

        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 裁剪中心区域
        left = (new_width - target_size[0]) // 2
        top = (new_height - target_size[1]) // 2
        img_cropped = img_resized.crop((left, top, left + target_size[0], top + target_size[1]))
        processed_images.append(img_cropped)

    elif mode == 2:
        # 模式2：原图直接使用
        processed_images.append(img)

# 生成 PDF
if processed_images:
    processed_images[0].save(output_path, save_all=True, append_images=processed_images[1:])

print(f"✅ PDF 生成完毕：{output_path}")
