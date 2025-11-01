# 色取得ユーティリティ

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F

# モデル準備
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model = torch.nn.Sequential(*(list(model.children())[:-1]))
model.eval()

# 画像前処理
transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])


# 特徴ベクトル取得
def get_vector(path):
    img = Image.open(path).convert("RGB")
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = model(tensor)
    return vec.flatten()


# 類似度計算
def get_image_similarity(img1, img2):
    v1 = get_vector(img1)
    v2 = get_vector(img2)
    similarity = F.cosine_similarity(v1, v2, dim=0).item()
    return similarity


# 店内商品と買い物リストの類似度を計算し、結果をリストにして返す
def compute_similarities(store_items, shopping_list):
    results = []
    for store_item in store_items:
        tmp_list = []
        for item in shopping_list:
            similarity = get_image_similarity(store_item["path"], item["path"])
            tmp_list.append(
                {
                    "name1": store_item["name"],
                    "name2": item["name"],
                    "similarity": similarity,
                }
            )
        tmp_list.sort(key=lambda x: x["name2"])
        results.append(tmp_list)
    return results
