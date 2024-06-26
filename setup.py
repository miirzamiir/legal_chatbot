
import pandas as pd
import re

from model.case_analyzer.case_retrieval import BM25Retrival
from model.feature_extraction.feature_extractor import FeatureExtractor
    
class Run():
    
    def __init__(self) -> None:
        case_df = pd.read_csv("resource/case/case.csv")
        self._case_matcher = BM25Retrival(case_df.text.tolist())
        self._feature_extractor = FeatureExtractor()
        
    def run(self, input: str):
        features = self._feature_extractor.extract(input)
        
        pattern = r'<(\d+)>$'
        match = re.search(pattern, input)
        if match:
            number = int(match.group(1))
            cases = self._case_matcher.get_similar_text(input, number)
        else:
            cases = None
        

        f = open('cases.txt', 'r+')
        f.flush()
        if cases:
            f.write(f'جمله ی {input}\n\n')
            f.write('پرونده های زیر پیدا شدند:\n')

            for i, case in enumerate(cases):
                f.write(f'{i+1}) {case[0]}\n')
                f.write(f'میزان مشابهت: {case[1]}\n\n')

        else:
            f.write('هیچ پرونده مشابهی پیدا نشد.')

        return features          


# text = "بنا بر اعلام گزارش پایگاه اطلاع رسانی دولت، هیئت وزیران در جلسه ۱۳۹۷/۱/۲۲ به استناد اصل یکصد و سی و هشتم قانون اساسی جمهوری اسلامی ایران و تبصره (۳) ماده (۷) قانون مبارزه با قاچاق کالا و ارز – مصوب ۱۳۹۲- و به منظور ساماندهی و مدیریت بازار ارز تصویب کرد."
# text += '<3>'
# # print(text)
# r = Run()
# a = r.run(text)
# print(a)
# # <پرونده:۳>
