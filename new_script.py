import os
import pandas as pd
from datetime import datetime
import requests

def main():
    # الرابط المباشر للـ CSV المستخرج من ملفك
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5qK-vFq_mJ3l0n88-F_9P4Bq8j2hK_N9s8u1E9yA6O2u7J5p-5oZJgOQ1Q8P_hY5CgOqA1P5m/pub?output=csv"
    
    # تحميل البيانات
    df = pd.read_csv(sheet_url)
    
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    today = datetime.now()
    
    for index, row in df.iterrows():
        try:
            name = str(row['Name'])
            # تحويل التاريخ من صيغة MM-DD-YYYY
            raw_date = str(row['Expiry_Date'])
            expiry_date = datetime.strptime(raw_date, "%m-%d-%Y")
            
            diff_days = (expiry_date - today).days
            
            # إرسال تنبيه إذا كانت الإقامة تنتهي خلال 30 يوم
            if 0 <= diff_days <= 30:
                message = f"⚠️ تنبيه: إقامة الموظف {name} تنتهي خلال {diff_days} يوم."
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url)
        except Exception as e:
            print(f"Error processing {name}: {e}")

if __name__ == "__main__":
    main()
