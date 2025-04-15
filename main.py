from flask import Flask, request
import requests
import os

app = Flask(__name__)

LINE_ACCESS_TOKEN = "QgHGfokoTBC9Zm8awXgPUN2O0nYduQ4Tq53rhKOWNwGC0+Fk7sy8nycfz8u6RoxMFBJeuJRATPErGNFrcQbF1B+4tfs9nFy3g8U5Rmwh+ffQY4aa4s1XVN7KMUyxSt8dHus1xu3vTrPzdPSjBH73hwdB04t891Ow1cDnyilFU="

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("★受信データ：", data)

        events = data.get("events", [])
        if not events:
            print("⚠️ events 配列が空です（検証用など）")
            return "OK", 200

        event = events[0]
        user_id = event["source"]["userId"]
        reply_token = event["replyToken"]

        print(f"\n✨✨ あなたの userId は：{user_id} ✨✨\n")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
        }
        body = {
            "replyToken": reply_token,
            "messages": [{
                "type": "text",
                "text": f"こんにちは！userId を取得しました 🙌\n\n{user_id}"
            }]
        }
        res = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)
        print("LINE API レスポンス：", res.status_code, res.text)

        return "OK", 200

    except Exception as e:
        print(f"❌ エラー発生：{e}")
        return "Internal Server Error", 500

# Render用
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
