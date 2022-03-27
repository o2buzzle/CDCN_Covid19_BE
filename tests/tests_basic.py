import unittest
import os
import sys

sys.path.append(os.path.abspath("../src"))

from core.core_ocr import ocr_from_file
from core.core_ner import ner_from_text


class OCR_Tests(unittest.IsolatedAsyncioTestCase):
    async def test_single_line(self):
        counter = 0
        with open("test_resources/singleline.txt", "r") as results:
            lines = results.readlines()
            for files in sorted(os.listdir("test_resources/singleline")):
                with self.subTest("Subtest {}".format(counter + 1)):
                    with open("test_resources/singleline/" + files, "rb") as image:
                        ocr_res = await ocr_from_file(image)
                        result = str.join(" ", [x["text"] for x in ocr_res])
                        self.assertEqual(result, lines[counter].strip())
                counter += 1

    async def test_multi_line(self):
        self.maxDiff = None
        counter = 0
        with open("test_resources/multiline.txt", "r") as results:
            lines = results.readlines()
            for files in sorted(os.listdir("test_resources/multiline")):
                with self.subTest("Subtest {}".format(counter + 1)):
                    with open("test_resources/multiline/" + files, "rb") as image:
                        ocr_res = await ocr_from_file(image)
                        result = str.join(" ", [x["text"] for x in ocr_res])
                        self.assertEqual(result, lines[counter].strip())
                counter += 1


class NER_Tests(unittest.IsolatedAsyncioTestCase):
    async def test_single_line(self):
        counter = 0
        with open("test_resources/singleline_ner.txt") as result_fp:
            results = result_fp.readlines()
            with open("test_resources/singleline.txt", "r") as text_fp:
                text = text_fp.readlines()
                for line in text:
                    with self.subTest("Subtest {}".format(counter + 1)):
                        ner_res = await ner_from_text(line)
                        result = str.join(" ", [x["prediction"] for x in ner_res])
                        self.assertEqual(result, results[counter].strip())
                    counter += 1
