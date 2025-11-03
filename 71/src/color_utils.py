# 色取得ユーティリティ

import torch
from PIL import Image
import torch.nn.functional as F
import open_clip

# モデル準備
device = torch.device("cpu")
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
model = model.to(device)
model.eval()


# 特徴ベクトル取得
def get_vector(path):
    img = Image.open(path).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        vec = model.encode_image(tensor)
        vec = F.normalize(vec, dim=-1)
    return vec.squeeze(0)


# 類似度計算
def get_image_similarity(img1, img2):
    v1 = get_vector(img1)
    v2 = get_vector(img2)
    similarity = F.cosine_similarity(v1, v2, dim=0).item()
    return similarity


# 店内商品と買い物リストの類似度を計算し、結果をリストにして返す
def compute_similarities(shopping_list, store_items):
    results = []
    for item in shopping_list:
        tmp_list = []
        for store_item in store_items:
            similarity = get_image_similarity(item["path"], store_item["path"])
            tmp_list.append(
                    {
                        "name1": item["name"],
                        "name2": store_item["name"],
                        "similarity": similarity,
                        }
                    )
        tmp_list.sort(key=lambda x: x["name2"])
        results.append(tmp_list)
    return results
