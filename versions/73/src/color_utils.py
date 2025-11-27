# 色取得ユーティリティ

import torch
from PIL import Image
import torch.nn.functional as F
import open_clip
from io_utils import get_similarity_threshold

# 特徴ベクトルをキャッシュ化
cached_data = {}

# 類似度のしきい値を取得
threshold = get_similarity_threshold()

# モデル準備
device = torch.device("cpu")
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
model = model.to(device)
model.eval()


# 特徴ベクトル取得
def get_vector(path):
    if path in cached_data:
        return cached_data[path]
    img = Image.open(path).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        vec = model.encode_image(tensor)
        vec = F.normalize(vec, dim=-1)
    vec = vec.squeeze(0)
    cached_data[path] = vec  # 特徴ベクトルをキャッシュ
    return vec


# 類似度計算
def is_same_product(img1, img2):
    v1 = get_vector(img1)
    v2 = get_vector(img2)
    similarity = F.cosine_similarity(v1, v2, dim=0).item()
    return similarity >= threshold
