import os
import pandas as pd
from datetime import datetime
import requests

def main():
    sheet_url = "https://docs.google.com/spreadsheets/d/1gbzLldXubReVoFp9ngR96Tcjsr_Jxxqh2FD6z8CnXxY/export?format=csv"
    
    try:
        df = pd.read_csv(sheet_url)
        # تحويل التاريخ للتنسيق الصحيح للترتيب
        df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], format='%m-%d-%Y')
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # ترتيب البيانات حسب اسم المؤسسة (Status) ثم التاريخ
    df = df.sort_values(by=['Status', 'Expiry_Date'])
    
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    today = datetime.now()
    
    # تجميع البيانات في مجموعات
    report_lines = []
    current_status = None
    
    for index, row in df.iterrows():
        try:
            status = str(row['Status'])
            name = str(row['Name'])
            iqama = str(row['Iqama_Number'])
            expiry = row['Expiry_Date']
            diff_days = (expiry - today).days
            
            if 0 <= diff_days <= 30:
                # إذا تغيرت المؤسسة، أضف عنواناً جديداً للقسم
                if status != current_status:
                    report_lines.append(f"\n📂 المؤسسة: {status}")
                    current_status = status
                
                expiry_str = expiry.strftime('%m-%d-%Y')
                report_lines.append(f"👤 {name} | 🆔 {iqama}\n📅 {expiry_str} (باقي {diff_days} يوم)")
        except Exception as e:
            continue
            
    # إرسال التقرير المجمع
    if report_lines:
        final_message = "⚠️ تقرير الإقامات (مقسّم حسب المؤسسة):\n" + "\n".join(report_lines)
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={final_message}"
        requests.get(url)

if __name__ == "__main__":
    main()
