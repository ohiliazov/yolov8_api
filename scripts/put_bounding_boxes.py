from pathlib import Path

import cv2
import numpy as np
import torch

IMAGE_OUT_PATH = Path(__file__).parent / "pic2.jpg"
PRED_PATH = Path(__file__).parent / "masks.pt"

pred = torch.load(PRED_PATH)
img = pred.orig_img.copy()

names = pred.names
colors = np.random.uniform(0, 255, size=(len(names), 3))


for idx, box_data in enumerate(pred.boxes.data):
    print(box_data)
    x0, y0, x1, y1, _, class_id = box_data.int().tolist()
    conf = box_data[4]
    label = f"{pred.names[class_id].title()} ({conf:.0%})"
    color = colors[int(class_id)]
    cv2.rectangle(img, (x0, y0), (x1, y1), color, 2)

    (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    cv2.rectangle(img, (x0, y0), (x0 + text_w, y0 - 2 * text_h), color, -1)

    cv2.putText(
        img,
        label,
        (x0, y0 - text_h // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2,
    )
    mask = pred.masks.data[idx]
    # equal color where mask, else image
    # this would paint your object silhouette entirely with `color`
    img = np.where(mask[..., None], color, img)


img = cv2.addWeighted(pred.orig_img, 0.5, img.astype(pred.orig_img.dtype), 0.5, 0)
cv2.imwrite(str(IMAGE_OUT_PATH), img)
