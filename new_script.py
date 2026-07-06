import os
import requests
from datetime import datetime
import pandas as pd

# هذا الكود يقرأ من الشيت مباشرة دون تعديله
def main():
    # ... (كود الاتصال الخاص بك كما هو) ...
    
    # عند قراءة البيانات:
    for row in data:
        # نقوم بتحويل التاريخ يدوياً في الكود ليفهم أي صيغة
        raw_date = str(row['Expiry_Date']) 
        
        # الكود سيحاول قراءة التاريخ مهما كان التنسيق
        try:
            # محاولة قراءة الصيغة الجديدة
            expiry_date = datetime.strptime(raw_date, "%m-%d-%Y")
        except:
            # إذا فشل، سيحاول قراءة الصيغ الأخرى تلقائياً
            expiry_date = pd.to_datetime(raw_date)

        # باقي الكود للمقارنة وإرسال التنبيه...
