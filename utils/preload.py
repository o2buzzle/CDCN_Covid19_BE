from transformers import AutoModelForTokenClassification
from vncorenlp import VnCoreNLP

print("Preloading model and data...")

phobert_ner = AutoModelForTokenClassification.from_pretrained(
    "huyenbui117/Covid19_phoNER"
)
rdrsegmenter = VnCoreNLP(
    "../VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size="-Xmx500m"
)
