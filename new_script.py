import os
import requests
import pandas as pd
from datetime import datetime

def main():
    # هذا الجزء يفترض أنك تستخدم مكتبة لربط Google Sheets
    # (تأكد أن المتغيرات TOKEN و CHAT_ID معرفة في الـ Secrets)
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    
    # تحميل البيانات (استخدم الطريقة التي تعتمدها في سكربتك الحالي)
    # هنا نفترض أنك تحمل البيانات في df (DataFrame)
    # df = ... (كود الاتصال الخاص بك)
    
    today = datetime.now()
    
    for index, row in df.iterrows():
        name = row['Name']
        raw_date = str(row['Expiry_Date']) 
        
        # الذكاء هنا: الكود سيحاول فهم التاريخ بغض النظر عن تنسيقه
        try:
            # محاولة قراءة التنسيق الحالي الذي أرسلته (MM-DD-YYYY)
            expiry_date = datetime.strptime(raw_date, "%m-%d-%Y")
        except:
            # إذا فشل، سيحاول تحويله تلقائياً لأي تنسيق تاريخ آخر
            expiry_date = pd.to_datetime(raw_date)
            
        diff_days = (expiry_date - today).days
        
        # التنبيه في حال كانت المدة 30 يوم أو أقل
        if 0 <= diff_days <= 30:
            message = f"⚠️ تنبيه: إقامة {name} تنتهي خلال {diff_days} يوم."
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url)

if __name__ == "__main__":
    main()
