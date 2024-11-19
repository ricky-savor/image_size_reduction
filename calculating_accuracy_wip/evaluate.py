import json

def boxes_overlap(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    overlapWidth = xB - xA
    overlapHeight = yB - yA

    return overlapWidth > 0 and overlapHeight > 0

def evaluate_detections(predictions, ground_truths):
    TP = 0
    FP = 0
    FN = 0

    gt_annotations = ground_truths['annotations']
    gt_matched = set()

    for pred in predictions:
        pred_image_id = pred['image_id']
        pred_category_id = pred['category_id']
        pred_bbox = pred['bbox']

        match_found = False
        for gt in gt_annotations:
            if gt['image_id'] != pred_image_id:
                continue
            if gt['category_id'] != pred_category_id:
                continue
            gt_bbox = gt['bbox']
            if boxes_overlap(pred_bbox, gt_bbox):
                if gt['id'] not in gt_matched:
                    TP += 1
                    gt_matched.add(gt['id'])
                    match_found = True
                    break
        if not match_found:
            FP += 1

    total_gt = len(gt_annotations)
    FN = total_gt - len(gt_matched)

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    return {'TP': TP, 'FP': FP, 'FN': FN, 'Precision': precision, 'Recall': recall}

with open('ground_truth.json') as f:
    ground_truths = json.load(f)

with open('predictions.json') as f:
    predictions = json.load(f)

results = evaluate_detections(predictions, ground_truths)

predicted_count = results['TP'] + results['FP']
manual_count = results['TP'] + results['FN']
accuracy = min(predicted_count, manual_count) / max(predicted_count, manual_count)

fp_percentage = results['FP'] / predicted_count * 100 if predicted_count > 0 else 0
fn_percentage = results['FN'] / manual_count * 100 if manual_count > 0 else 0

print("Evaluation Results:")
print(f"Accuracy: {accuracy:.2f}")
print(f"False Positives (FP): {results['FP']}")
print(f"False Negatives (FN): {results['FN']}")
print(f"FP%: {fp_percentage:.2f}%")
print(f"FN%: {fn_percentage:.2f}%")
