import asyncio
import json
import os
import re
from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession

app = Flask(__name__)

# --- [ CONFIG ] ---
API_ID = 37240169 
API_HASH = 'bb19cf12abff06bbb2a0df3927b0bb32'
SESSION_STR = "1BVtsOIABu3trPQsSg1gpTz-g_PrerWpeT3cJEsNper-TZooB9n3S351QTrpuv_Wx0miGdWAe0wzLCX4Yn7UVp09qn4EoICWEgeAqgPIDbL9tmx2gpdKFbpFTtEAa0lmqGLCQigxM18LVsrDK2XBnRH-YpYenfMcOSKW3TLY_I5x6lqFEJVe_TqlZTPwu1lxaybmMzaaeSdDujURllQBony-Dip0J2WkRwAfRYuvSbz3DFwMLOQ5XIpglskjfQcEfLUWQDcRmGZ89D1AUN-k0vhOKzOveh2bhG3zGaxuB2WbJbV2WQhq84tRv9QBFGJQ8WnrnY9GfXdBU9g5aA6MUusi0_q0V-N8="
GROUP_LINK = 'shivamnim'

# key.txt se password uthane ke liye
def get_stored_key():
    try:
        path = os.path.join(os.path.dirname(__file__), '..', 'key.txt')
        with open(path, 'r') as f: return f.read().strip()
    except: return "SHIVAM-786"

# Faltu data saaf karke Shivam Boss likhne ke liye
def clean_result(raw_text):
    junk = [r"(?i)⏰.*delete", r"(?i)seconds", r"(?i)scanning", r"(?i)https?://\S+", r"(?i)join.*@"]
    header = "🚀 **SHIVAM BOSS PREMIUM SEARCH** 🚀\n━━━━━━━━━━━━━━━━━━━━\n"
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🔥 **BY: SHIVAM BOSS**"
    lines = [l for l in raw_text.split('\n') if not any(re.search(p, l) for p in junk)]
    text = "\n".join(lines).strip()
    return header + text + footer

async def fetch_tg(cmd, val):
    client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)
    try:
        await client.connect()
        sent = await client.send_message(GROUP_LINK, f"{cmd} {val}")
        for _ in range(8):
            await asyncio.sleep(1.2)
            async for msg in client.iter_messages(GROUP_LINK, limit=5):
                if msg.id != sent.id and str(val) in msg.text:
                    return clean_result(msg.text)
    finally: await client.disconnect()
    return "❌ No Data Found."

@app.route('/api/<path:endpoint>')
def handler(endpoint):
    user_key = request.args.get('key')
    if user_key != get_stored_key(): return jsonify({"data": "Wrong Key"}), 403
    val = request.args.get('num') or request.args.get('id')
    cmd_map = {"numinfo": "/num", "aadhar": "/aadhar", "insta": "/insta", "rto": "/rto"}
    result = asyncio.run(fetch_tg(cmd_map.get(endpoint, "/num"), val))
    return app.response_class(response=json.dumps({"data": result}, ensure_ascii=False), mimetype='application/json')
          
