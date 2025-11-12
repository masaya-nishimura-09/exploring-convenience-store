import torch
from PIL import Image
import torch.nn.functional as F
import open_clip
from utils.config_utils import get_similarity_threshold
from libs.correct_image_mapping import correct_image_mapping
from utils.output_utils import write_image_processing_result

# 特徴ベクトルをキャッシュ化
cached_data = {}

# 類似度のしきい値を取得
threshold = get_similarity_threshold()

# モデル準備
device = torch.device("cpu")
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32", pretrained="openai"
)
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
    cached_data[path] = vec
    return vec


# 類似度計算
def calculate_similarity(img1, img2):
    v1 = get_vector(img1)
    v2 = get_vector(img2)
    similarity = F.cosine_similarity(v1, v2, dim=0).item()
    return similarity >= threshold


def verify_image_processing(shopping_cart):
    for item in shopping_cart:
        cart_item_name = item["name"]
        cart_item_symbol = item["symbol"]

        for row in correct_image_mapping:
            if row["name"] == cart_item_name and row["symbol"] != cart_item_symbol:
                write_image_processing_result(
                    row["name"], row["symbol"], cart_item_name, cart_item_symbol
                )
