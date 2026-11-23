import os
import pandas as pd
from datetime import datetime
import requests

def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    # تيليجرام حده 4096 حرف، فنقسم الرسالة على أسطر
    chunks, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > 3800:
            chunks.append(current)
            current = ""
        current += line + "\n"
    if current.strip():
        chunks.append(current)
    for chunk in chunks:
        r = requests.post(url, data={'chat_id': chat_id, 'text': chunk}, timeout=30)
        if not r.ok:
            print(f"Telegram error {r.status_code}: {r.text}")
            raise SystemExit(1)  # يخلي GitHub Actions يظهر فشل بدل ما يسكت

def main():
    sheet_url = "https://docs.google.com/spreadsheets/d/1gbzLldXubReVoFp9ngR96Tcjsr_Jxxqh2FD6z8CnXxY/export?format=csv"

    try:
        df = pd.read_csv(sheet_url)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        raise SystemExit(1)

    # قراءة التاريخ بصيغة يوم/شهر/سنة (الأكثر شيوعاً عندنا)
    df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], errors='coerce', dayfirst=True)

    # الصفوف اللي تاريخها غلط: ما نحذفهاش بصمت، نبلغ عنها
    bad = df[df['Expiry_Date'].isna()]
    bad_lines = []
    for _, row in bad.iterrows():
        bad_lines.append(f"❓ {str(row.get('Name', '')).strip()} | 🆔 {str(row.get('Iqama_Number', '')).strip()} (تاريخ غير مقروء)")
    df = df.dropna(subset=['Expiry_Date'])

    df = df.sort_values(by=['Status', 'Expiry_Date'])

    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    today = pd.Timestamp(datetime.now().date())

    report_lines = []
    current_status = None

    for _, row in df.iterrows():
        try:
            status = str(row['Status']).strip()
            name = str(row['Name']).strip()
            iqama = str(row['Iqama_Number']).strip()
            expiry = row['Expiry_Date']
            diff_days = (expiry - today).days

            # أي إقامة باقي لها 30 يوم أو أقل، بما فيها المنتهية
            if diff_days <= 30:
                if status != current_status:
                    report_lines.append(f"\n📂 المؤسسة: {status}")
                    current_status = status
                expiry_str = expiry.strftime('%Y-%m-%d')
                if diff_days < 0:
                    note = f"🔴 منتهية من {-diff_days} يوم"
                else:
                    note = f"باقي {diff_days} يوم"
                report_lines.append(f"👤 {name} | 🆔 {iqama}\n📅 {expiry_str} ({note})")
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    if bad_lines:
        report_lines.append("\n⚠️ صفوف تاريخها غير مقروء، راجعها في الشيت:")
        report_lines.extend(bad_lines)

    if report_lines:
        send_telegram(token, chat_id, "⚠️ تقرير الإقامات (مقسّم حسب المؤسسة):\n" + "\n".join(report_lines))
        print("Message sent successfully!")
    else:
        print("لا يوجد إقامات تنتهي خلال 30 يوماً لإرسالها.")

if __name__ == "__main__":
    main()
