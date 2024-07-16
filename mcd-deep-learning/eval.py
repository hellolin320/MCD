import paddle
import numpy as np


# 构建验证集evaluate函数
@paddle.no_grad()
def evaluate(model, criterion, metric, data_loader):
    model.eval()
    metric.reset()
    losses = []
    for batch in data_loader:
        input_ids, token_type_ids, labels = batch['input_ids'], batch['token_type_ids'], batch['labels']

        logits = model(input_ids, token_type_ids)
        loss = criterion(logits, labels)
        losses.append(loss.numpy())
        correct = metric.compute(logits, labels)
        metric.update(correct)
        
    accu = metric.accumulate()
    print("eval loss: %.5f, accuracy: %.5f" % (np.mean(losses), accu))
    model.train()
    metric.reset()
    return accu