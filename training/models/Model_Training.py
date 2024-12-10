import os
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from sklearn.model_selection import train_test_split
import torch

print("GPU 可用:", torch.cuda.is_available())

file_path = "./Source/simplifyweibo_4_moods.csv"
data_df = pd.read_csv(file_path)
data_df.columns = ['label', 'text']

class_counts = data_df['label'].value_counts()
class_weights = 1.0 / class_counts
class_weights_tensor = torch.tensor(class_weights.sort_index().values, dtype=torch.float)

train_df, test_df = train_test_split(data_df, test_size=0.2, stratify=data_df['label'], random_state=42)
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)
dataset = DatasetDict({"train": train_dataset, "test": test_dataset})

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=4)

def preprocess_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)

encoded_dataset = dataset.map(preprocess_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer)

class WeightedTrainer(Trainer):
    def training_step(self, model, inputs, *args, **kwargs):
        model.train()
        inputs = self._prepare_inputs(inputs)
        labels = inputs.pop("labels")

        outputs = model(**inputs)
        logits = outputs.get("logits")

        loss_fct = torch.nn.CrossEntropyLoss(weight=class_weights_tensor.to(logits.device))
        loss = loss_fct(logits, labels)

        loss.backward()
        return loss

training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy="steps",
    save_steps=500,
    save_total_limit=3,
)

trainer = WeightedTrainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["test"],
    data_collator=data_collator,
    tokenizer=tokenizer
)

''' 
latest_checkpoint = "./results/checkpoint-xxxx"当程序中断时，可填入相应的检查点，从最新进度重新训练

if latest_checkpoint:
    print("恢复训练从检查点:", latest_checkpoint)
    trainer.train(resume_from_checkpoint=latest_checkpoint)
else:
    trainer.train()
'''
model.save_pretrained('./sentiment_model')
tokenizer.save_pretrained('./sentiment_model')
