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
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


# 特徴ベクトル取得
def get_vector(path):
    img = Image.open(path).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = model(tensor)
    return vec.flatten()


# 類似度計算
def is_same_product(img1, img2, threshold=0.85):
    v1 = get_vector(img1)
    v2 = get_vector(img2)
    similarity = F.cosine_similarity(v1, v2, dim=0).item()
    return similarity >= threshold
