import os
import pandas as pd
from datetime import datetime
import requests

def main():
    # الرابط المباشر لتحميل ملف الإكسل بصيغة CSV
    sheet_url = "https://docs.google.com/spreadsheets/d/1gbzLldXubReVoFp9ngR96Tcjsr_Jxxqh2FD6z8CnXxY/export?format=csv"
    
    # تحميل البيانات
    try:
        df = pd.read_csv(sheet_url)
    except Exception as e:
        print(f"Error reading sheet: {e}")
        return
    
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    today = datetime.now()
    
    # التأكد من معالجة البيانات
    for index, row in df.iterrows():
        try:
            name = str(row['Name'])
            raw_date = str(row['Expiry_Date'])
            
            # تحويل التاريخ من صيغة MM-DD-YYYY
            expiry_date = datetime.strptime(raw_date, "%m-%d-%Y")
            diff_days = (expiry_date - today).days
            
            # إرسال تنبيه إذا كانت الإقامة تنتهي خلال 30 يوم
            if 0 <= diff_days <= 30:
                message = f"⚠️ تنبيه: إقامة الموظف {name} تنتهي خلال {diff_days} يوم."
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url)
        except Exception as e:
            print(f"Error processing row {index}: {e}")

if __name__ == "__main__":
    main()
