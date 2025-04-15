from flask import Flask, request
import requests
import os  # ← 追記で必要

app = Flask(__name__)

LINE_ACCESS_TOKEN = 'QgHGfokoTBC9Zm8awXgPUN2O0nYduQ4Tq53rhKOWNwGC0+Fk7sy8nycfz8u6RoxMFBJeuJRATPErGNFrcQbF1B+4tfs9nFy3g8U5Rmwh+ffQY4aa4s1XVN7KMUyxSt8dHus1xu3vTrPzdPSjBH73hwdB04t89/1O/w1cDnyilFU='

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("★受信データ：", data)

    try:
        user_id = data["events"][0]["source"]["userId"]
        reply_token = data["events"][0]["replyToken"]

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
        requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

    except Exception as e:
        print(f"エラー：{e}")

# ← ここからが Render 対応の追記部分！
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
