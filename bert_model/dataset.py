import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split


def tokenize_and_encode(tokenizer, texts, labels, max_length=128):
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels = torch.tensor(labels.values, dtype=torch.float32)

    return input_ids, attention_masks, labels


def prepare_dataloader_from_csv(
    file_path,
    text_column,
    label_columns,
    tokenizer_name='bert-base-chinese',
    batch_size=16,
    max_length=128,
    val_size=0.2
):
    df = pd.read_csv(file_path)
    texts = df[text_column]
    labels = df[label_columns]

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=val_size, random_state=42
    )

    tokenizer = BertTokenizer.from_pretrained(tokenizer_name)

    train_inputs, train_masks, train_targets = tokenize_and_encode(
        tokenizer, train_texts, train_labels, max_length
    )
    val_inputs, val_masks, val_targets = tokenize_and_encode(
        tokenizer, val_texts, val_labels, max_length
    )

    train_dataset = TensorDataset(train_inputs, train_masks, train_targets)
    val_dataset = TensorDataset(val_inputs, val_masks, val_targets)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader