import pandas as pd
from datetime import datetime
import os
import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

def process_hr_data():
    # افترضنا أنك تقرأ ملف الإكسل أو CSV
    df = pd.read_csv('your_data_file.csv') # استبدل باسم ملفك الفعلي
    
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    
    today = datetime.now()
    
    for index, row in df.iterrows():
        name = row['Name']
        # التعديل هنا: تحويل التاريخ من صيغة MM-DD-YYYY
        try:
            expiry_date = datetime.strptime(str(row['Expiry_Date']), "%m-%d-%Y")
        except ValueError:
            continue # تخطي الصف إذا كان التنسيق غير صحيح
            
        diff_days = (expiry_date - today).days
        
        if 0 <= diff_days <= 30:
            message = f"⚠️ تنبيه هام: إقامة الموظف {name} تنتهي خلال {diff_days} يوم."
            send_telegram_message(token, chat_id, message)

if __name__ == "__main__":
    process_hr_data()
