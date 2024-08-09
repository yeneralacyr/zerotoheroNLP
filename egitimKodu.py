import logging
import os
import re
from collections import Counter

import numpy as np
import pandas as pd
from google.colab import drive
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
import torch
from datasets import Dataset, DatasetDict
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

# Google Drive'ı bağla
drive.mount('/content/drive')

# Loglama ayarlarını yap
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# Model kaydetme yolu
model_save_path = '/content/drive/My Drive/trained_bert_model3'

# --- Yardımcı Fonksiyonlar ---

def clean_text(text: str) -> str:
    """
    Giriş metnini temizler.
    """
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\S*@\S*\s?", "", text)
    text = re.sub(r"@[A-Za-z0-9]+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("*", "")
    text = text.strip()
    return text

def save_model_to_drive(model, tokenizer, save_path):
    """
    İnce ayarlanmış modeli ve tokenleştiriciyi Google Drive'a kaydeder.
    """
    try:
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)
        logger.info(f"Model şuraya kaydedildi: {save_path}")
    except Exception as e:
        logger.error(f"Model kaydedilirken hata oluştu: {e}")

def compute_metrics(pred):
    """
    Değerlendirme için doğruluk, hassasiyet, geri çağırma ve F1 puanını hesaplar.
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)
    return {
        "accuracy": acc,
        "eval_accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

def tokenize_function(examples):
    """
    Yüklenen tokenleştiriciyi kullanarak giriş örneklerini tokenleştirir.
    """
    tokenized_inputs = tokenizer(
        examples["text"], padding="max_length", truncation=True
    )
    tokenized_inputs["labels"] = examples["label"]
    return tokenized_inputs

# --- Veri Görselleştirme ---
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_confusion_matrix(y_true, y_pred, labels):
    """
    Karışıklık matrisini çizer.

    Args:
        y_true: Gerçek etiketler.
        y_pred: Tahmin edilen etiketler.
        labels: Etiketlerin listesi.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel('Tahmin Edilen Etiket')
    plt.ylabel('Gerçek Etiket')
    plt.title('Karışıklık Matrisi')
    plt.show()


# --- Veri Yükleme ve Ön İşleme ---

# Verileri yükle
try:
    data = pd.read_csv("dataset.csv")
    logger.info("Veriler başarıyla yüklendi.")
except Exception as e:
    logger.error(f"Veri yüklenirken hata oluştu: {e}")
    raise

# Metin temizleme
data['text'] = data['text'].apply(clean_text)
logger.info("Metin temizleme tamamlandı.")

# Etiketleri al ve sayısallaştır
labels = data["label"].unique().tolist()
label_to_id = {label: idx for idx, label in enumerate(labels)}
id_to_label = {idx: label for label, idx in label_to_id.items()}
data["label"] = data["label"].map(label_to_id)
logger.info(
    f"Etiket eşleme tamamlandı. Benzersiz etiket sayısı: {len(label_to_id)}"
)

# Veri kümesini aşırı örnekle
X = data["text"]
y = data["label"]

ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X.to_frame(), y)

logger.info(f"Orijinal veri kümesi şekli: {Counter(y)}")
logger.info(f"Yeniden örneklenmiş veri kümesi şekli: {Counter(y_resampled)}")

oversampled_data = pd.DataFrame({"text": X_resampled["text"], "label": y_resampled})

# Veri kümesini oluştur ve böl
dataset = Dataset.from_pandas(oversampled_data)

train_data, test_data, train_labels, test_labels = train_test_split(
    dataset["text"],
    dataset["label"],
    test_size=0.2,
    random_state=42,
    stratify=dataset["label"],
)

dataset_dict = DatasetDict(
    {
        "train": Dataset.from_dict({"text": train_data, "label": train_labels}),
        "test": Dataset.from_dict({"text": test_data, "label": test_labels}),
    }
)
logger.info(
    f"Veri kümesi bölme tamamlandı. Eğitim boyutu: {len(dataset_dict['train'])}, Test boyutu: {len(dataset_dict['test'])}"
)

# --- Model ve Tokenizer Yükleme ---

model_name = (
    "dbmdz/convbert-base-turkish-mc4-uncased"
)
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=len(label_to_id)
    )
    logger.info("Model ve tokenleştirici başarıyla yüklendi.")
except Exception as e:
    logger.error(f"Model veya tokenleştirici yüklenirken hata oluştu: {e}")
    raise

# --- Tokenleştirme ---
tokenized_datasets = dataset_dict.map(tokenize_function, batched=True)
logger.info("Tokenleştirme tamamlandı.")

# --- Model Eğitimi ve Kaydı ---

# Önceden eğitilmiş bir model varsa yükle
if os.path.exists(os.path.join(model_save_path, "config.json")):
    # Eğitimli Modeli Drive'dan Yükle
    try:
        model = AutoModelForSequenceClassification.from_pretrained(model_save_path)
        tokenizer = AutoTokenizer.from_pretrained(model_save_path)
        logger.info(f"Model şu konumdan yüklendi: {model_save_path}")
    except Exception as e:
        logger.error(f"Model yüklenirken hata oluştu: {e}")
        raise
else:
    # En iyi parametrelerinizi kullanarak modeli eğitin
    best_params = {
        "per_device_train_batch_size": 16,
        "per_device_eval_batch_size": 16,
        "per_gpu_train_batch_size": None,
        "per_gpu_eval_batch_size": None,
        "gradient_accumulation_steps": 1,
        "eval_accumulation_steps": None,
        "eval_delay": 0,
        "torch_empty_cache_steps": None,
        "learning_rate": 3.8050087906112006e-05,
        "weight_decay": 0.041347999655503814,
        "adam_beta1": 0.9,
        "adam_beta2": 0.999,
        "adam_epsilon": 1e-08,
        "max_grad_norm": 1.0,
        "num_train_epochs": 5,
        "max_steps": -1,
        "lr_scheduler_type": "linear",
        "lr_scheduler_kwargs": {},
        "warmup_ratio": 0.0,
        "warmup_steps": 987,
    }

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        **best_params,
        save_strategy="epoch",
        load_best_model_at_end=True,
        push_to_hub=False,
        logging_dir="./logs",
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        compute_metrics=compute_metrics,
    )

    try:
        train_history = trainer.train()
        logger.info("Son eğitim tamamlandı.")
    except Exception as e:
        logger.error(f"Son eğitim sırasında hata oluştu: {e}")
        raise

    # En iyi modeli kaydet
    save_model_to_drive(model, tokenizer, model_save_path)

    # Eğitim sonuçlarını kullanarak karışıklık matrisini çiz
    predictions = trainer.predict(tokenized_datasets["test"])
    predicted_labels = np.argmax(predictions.predictions, axis=1)
    plot_confusion_matrix(test_labels, predicted_labels, labels)

# Cihaz ayarını yap
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Metin sınıflandırma fonksiyonu
def classify_text(text):
    """
    Verilen metni sınıflandırır.
    """
    inputs = tokenizer(text, return_tensors="pt").to(device)
    outputs = model(**inputs)
    predicted_class_id = outputs.logits.argmax().item()
    return id_to_label[
        predicted_class_id
    ]


while True:
    text = input(
        "Sınıflandırmak istediğiniz metni girin (Çıkmak için 'çıkış' yazın): "
    )
    if text.lower() == "çıkış":
        break
    predicted_class = classify_text(text)
    print(f"Metnin tahmini sınıfı: {predicted_class}")