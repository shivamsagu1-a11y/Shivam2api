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

# --- [ KEY LOADER ] ---
def get_stored_key():
    try:
        # Code ke bahar wali key.txt file ko read karega
        path = os.path.join(os.path.dirname(__file__), '..', 'key.txt')
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return "SHIVAM-786" # Default key agar file na mile

# --- [ CLEANING & BRANDING ] ---
def clean_result(raw_text):
    junk = [r"(?i)⏰.*delete", r"(?i)seconds", r"(?i)scanning", r"(?i)https?://\S+", r"(?i)join.*@"]
    lines = raw_text.split('\n')
    
    header = "🚀 **SHIVAM BOSS PREMIUM SEARCH** 🚀\n━━━━━━━━━━━━━━━━━━━━\n"
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🔥 **BY: SHIVAM BOSS**"
    
    clean_lines = []
    for line in lines:
        if not any(re.search(p, line) for p in junk):
            line = re.sub(r"(?i)owner|powered by|by|dev|@\w+", "Owner: SHIVAM BOSS", line)
            clean_lines.append(line)
    
    text = "\n".join(clean_lines).strip()
    try:
        start = text.find('[') if '[' in text else text.find('{')
        end = (text.rfind(']') + 1) if ']' in text else (text.rfind('}') + 1)
        if start != -1 and end != -1:
            data = json.loads(text[start:end])
            items = data if isinstance(data, list) else [data]
            res = ""
            for i, item in enumerate(items, 1):
                res += f"📍 **DATA SET #{i}**\n"
                for k, v in item.items():
                    if v and str(v).lower() != "null" and k.lower() not in ["id", "_powered_by"]:
                        res += f"🔹 **{k.upper()}:** `{v}`\n"
                res += "\n"
            return header + res.strip() + footer
    except: pass
    return header + text + footer

# --- [ TURBO SEARCH ENGINE ] ---
async def fetch_tg(cmd, val):
    client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)
    try:
        await client.connect()
        sent = await client.send_message(GROUP_LINK, f"{cmd} {val}")
        for _ in range(8):
            await asyncio.sleep(1.2)
            async for msg in client.iter_messages(GROUP_LINK, limit=5):
                if msg.id != sent.id and str(val) in msg.text:
                    if "SCANNING" in msg.text.upper() and len(msg.text) < 60: continue
                    return clean_result(msg.text)
    finally: await client.disconnect()
    return "❌ No Data Found."

@app.route('/api/<path:endpoint>')
def handler(endpoint):
    # Key check from key.txt
    user_key = request.args.get('key')
    if user_key != get_stored_key():
        return jsonify({"data": "Wrong Key! Access Denied."}), 403
    
    val = request.args.get('num') or request.args.get('id') or request.args.get('user')
    cmd_map = {"numinfo": "/num", "aadhar": "/aadhar", "insta": "/insta", "rto": "/rto"}
    
    result = asyncio.run(fetch_tg(cmd_map.get(endpoint, "/num"), val))
    return app.response_class(
        response=json.dumps({"status": "success", "data": result}, ensure_ascii=False),
        mimetype='application/json'
          )
          
