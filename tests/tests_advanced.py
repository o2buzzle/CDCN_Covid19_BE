from difflib import unified_diff
import unittest
import os
import sys

sys.path.append(os.path.abspath("../src"))

from core.core_ocr import ocr_from_file
from core.core_ner import ner_from_text


class OCR_NER_Intg_test(unittest.IsolatedAsyncioTestCase):
    async def test_single_line(self):
        counter = 0
        with open("test_resources/singleline_ner.txt", "r") as results:
            lines = results.readlines()
            for files in sorted(os.listdir("test_resources/singleline")):
                with self.subTest("Subtest {}".format(counter + 1)):
                    with open("test_resources/singleline/" + files, "rb") as image:
                        ocr_res = await ocr_from_file(image)
                        ocr_text = str.join(" ", [x["text"] for x in ocr_res])
                        ner_res = await ner_from_text(ocr_text)
                        ner_text = str.join(" ", [x["prediction"] for x in ner_res])
                        self.assertEqual(ner_text, lines[counter].strip())
                counter += 1
