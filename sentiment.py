

import transformers
import torch

# Load pre-trained DistilBERT tokenizer and model
tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = transformers.DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

#function for inserting the reviews and getting the setiment score
def get_sentiment(review):
    tokens = tokenizer.encode_plus(review, max_length=128, truncation=True, padding='max_length', return_tensors='pt')
    input_ids = tokens['input_ids']
    model.eval()
    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs[0]
        probabilities = torch.softmax(logits, dim=1).flatten().tolist()

    # Print sentiment label and score
    if probabilities[1] > probabilities[0]:
        return probabilities[1]
    else:
        return probabilities[0]


