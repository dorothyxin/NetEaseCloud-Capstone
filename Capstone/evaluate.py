import numpy as np
import torch


def hit(gt_item, pred_items):
    if gt_item in pred_items:
        return 1
    return 0


def ndcg(gt_item, pred_items):
    if gt_item in pred_items:
        index = pred_items.index(gt_item)
        return np.reciprocal(np.log2(index + 2))
    return 0


def metrics(model, test_loader, top_k, device):
    HR, NDCG = [], []

    print('evaluation starts here')

    for user_cat, user_num, item_cat, item_num in test_loader:
        user_cat = user_cat.to(device)
        user_num = user_num.to(device)
        item_cat = item_cat.to(device)
        item_num = item_num.to(device)
        predictions = model(user_cat, user_num, item_cat, item_num)
        _, indices = torch.topk(predictions, top_k)
        recommends = torch.take(
            item_cat, indices).cpu().numpy().tolist()

        gt_item = item_cat[0].item()
        HR.append(hit(gt_item, recommends))
        NDCG.append(ndcg(gt_item, recommends))

    return np.mean(HR), np.mean(NDCG)
