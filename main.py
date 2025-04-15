from flask import Flask, request
import requests
import os
import traceback  # ← エラー詳細表示用に追加！

app = Flask(__name__)  # Flaskアプリを初期化

# あなたのLINEチャネルアクセストークン（""で囲んでね）
LINE_ACCESS_TOKEN = "QgHGfokoTBC9Zm8awXgPUN2O0nYduQ4Tq53rhKOWNwGC0+Fk7sy8nycfz8u6RoxMFBJeuJRATPErGNFrcQbF1B+4tfs9nFy3g8U5Rmwh+ffQY4aa4s1XVN7KMUyxSt8dHus1xu3vTrPzdPSjBH73hwdB04t891Ow1cDnyilFU="

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("★受信データ：", data)

        if not data or "events" not in data:
            print("⚠️ JSONが不正、または 'events' キーが存在しません")
            return "Bad Request", 400

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
        response = requests.post(
            "https://api.line.me/v2/bot/message/reply",
            headers=headers,
            json=body
        )

        print("📨 LINEへの返信結果:", response.status_code, response.text)

        return "OK", 200

    except Exception as e:
        traceback.print_exc()  # ← スタックトレースをログに出す
        print(f"❌ エラー発生：{e}")
        return "Internal Server Error", 500

# Render対応（ポート）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
