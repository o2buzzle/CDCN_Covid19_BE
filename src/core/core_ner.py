from transformers import AutoTokenizer, AutoModelForTokenClassification
from tasks import NER
import torch
from vncorenlp import VnCoreNLP
import pandas as pd
import asyncio
import io

phobert_ner = AutoModelForTokenClassification.from_pretrained(
    "huyenbui117/Covid19_phoNER"
)

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

labels = NER().get_labels(None)

rdrsegmenter = VnCoreNLP(
    "../VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size="-Xmx500m"
)


def do_ner(sentences_list: list) -> list:
    df = pd.DataFrame(columns=["token", "prediction"])
    for sentences in sentences_list:
        if sentences == "":
            continue
        tokenized_sentences = rdrsegmenter.tokenize(sentences)
        for sentence in tokenized_sentences:
            sequence = " ".join(sentence)  # tạo câu mới đã được tokenized

            input_ids = torch.tensor(
                [tokenizer.encode(sequence)]
            )  # lấy id của các tokens tương ứng
            # không dùng tokenize(decode(encode)), text sẽ bị lỗi khi tokenize do conflict với tokenizer mặc định
            tokens = tokenizer.convert_ids_to_tokens(
                tokenizer.encode(sequence)
            )  # lấy các token để đánh tags

            outputs = phobert_ner(input_ids).logits
            predictions = torch.argmax(outputs, dim=2)
            # print(predictions)

            for i in [
                [token, labels[prediction]]
                for token, prediction in zip(tokens, predictions[0].numpy())
            ]:
                if i[0] in ["<s>", "</s>"]:
                    continue
                a_series = pd.Series(i, index=df.columns)
                # print(a_series)
                df = pd.concat([df, a_series.to_frame().T], ignore_index=True)
            # print('---------------------------------------------')
        # Insert a line break after each paragraph
        df.loc[len(df)] = ["LINEBREAK", "X-LINEBREAK"]

    # Remove any string instance that contains ""@@"" that may be in the result
    for index, row in df.iterrows():
        if row["token"].find("@@") != -1:
            row["token"] = row["token"].replace("@@", "")
    return list(df.to_dict(orient="index").values())


async def do_ner_async(sentences_list: list) -> list:
    loop = asyncio.get_event_loop()
    df = await loop.run_in_executor(None, do_ner, sentences_list)
    return df


async def ner_from_file(file: io.BytesIO) -> list:
    sentences_list = file.read().decode("utf-8").split("\n")
    return await do_ner_async(sentences_list)


async def ner_from_text(text: str) -> list:
    sentences_list = text.split("\n")
    return await do_ner_async(sentences_list)
