import functools
import pytesseract
from PIL import Image
import io

import asyncio


async def ocr_from_file(file: io.BytesIO) -> dict:
    loop = asyncio.get_event_loop()
    img = await loop.run_in_executor(None, Image.open, file)
    data = await loop.run_in_executor(
        None,
        functools.partial(
            pytesseract.image_to_data,
            img,
            output_type=pytesseract.Output.DICT,
            lang="vie",
        ),
    )
    # print(data)
    to_return = []
    for word, confidence in zip(data["text"], data["conf"]):
        if float(confidence) != -1:
            to_return.append({"text": word, "confidence": float(confidence)})

    return to_return
