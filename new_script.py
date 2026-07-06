import pandas as pd
import requests
import os
from datetime import datetime

# إعدادات الرابط (تم استبدال الرابط بـ CSV للقراءة المباشرة)
SHEET_ID = '1gbzLldXubReVoFp9ngR96Tcjsr_Jxxqh2FD6z8CnXxY'
URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

def check_expiry():
    # تحميل البيانات
    df = pd.read_csv(URL)
    
    # تحويل تاريخ الانتهاء لـ datetime
    df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'])
    today = datetime.now()
    
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    for index, row in df.iterrows():
        # إذا كانت الحالة "valid" أو أي شيء آخر، نقارن التاريخ
        # نحسب الفرق بالأيام
        delta = (row['Expiry_Date'] - today).days
        
        # إذا بقيت 30 يوماً أو أقل، نرسل تنبيه
        if 0 <= delta <= 30:
            msg = f"⚠️ تنبيه إقامة اقتربت على الانتهاء:\n\nالاسم: {row['Name']}\nرقم الإقامة: {row['Iqama_Number']}\nتاريخ الانتهاء: {row['Expiry_Date'].date()}\nمتبقي: {delta} يوم."
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg})

if __name__ == "__main__":
    check_expiry()
