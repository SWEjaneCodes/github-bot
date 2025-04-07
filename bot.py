from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask("Snowflake")
WEBHOOK_SECRET = "your_webhook_secret"  # Match GitHub App secret

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Verify signature
    sig = request.headers.get('X-Hub-Signature-256', '')
    body = request.get_data()
    hash = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(f"sha256={hash}", sig):
        return "Invalid signature", 403

    # Handle events
    event = request.json
    if request.headers.get('X-GitHub-Event') == 'pull_request':
        if event['action'] in ['opened', 'synchronize']:
            print(f"New PR: {event['pull_request']['title']}")
            # Add your bot logic here
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)