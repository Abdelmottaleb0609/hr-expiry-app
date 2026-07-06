import gspread
import os
import pandas as pd
from datetime import datetime
import requests
from oauth2client.service_account import ServiceAccountCredentials

def main():
    # إعداد الاتصال
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    # فتح ملف الإكسل (استبدل الاسم بالاسم الصحيح للملف)
    sheet = client.open("HR_Data").worksheet("HR_Data")
    
    # --- السطر الناقص كان هنا ---
    # تحويل بيانات جوجل شيت إلى DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    # ---------------------------
    
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    today = datetime.now()
    
    for index, row in df.iterrows():
        name = row['Name']
        raw_date = str(row['Expiry_Date']) 
        
        try:
            expiry_date = datetime.strptime(raw_date, "%m-%d-%Y")
            diff_days = (expiry_date - today).days
            
            if 0 <= diff_days <= 30:
                message = f"⚠️ تنبيه: إقامة {name} تنتهي خلال {diff_days} يوم."
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
