import discord
import aiohttp
import os

# 設定
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "https://yang11421.app.n8n.cloud/webhook/discord-ai-companion")

intents = discord.Intents.default()
intents.message_content = True  # 必須開啟訊息內容意圖

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ 顧北辰 已上線：{client.user}")

@client.event
async def on_message(message):
    # 忽略自己的訊息（避免無限迴圈）
    if message.author.bot:
        return

    # 將訊息轉發到 n8n Webhook
    payload = {
        "content": message.content,
        "author": {
            "id": str(message.author.id),
            "username": message.author.name,
            "bot": message.author.bot
        },
        "channel_id": str(message.channel.id),
        "guild_id": str(message.guild.id) if message.guild else None,
        "message_id": str(message.id)
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_WEBHOOK_URL, json=payload) as resp:
                if resp.status != 200:
                    print(f"⚠️ n8n 回應錯誤：{resp.status}")
    except Exception as e:
        print(f"❌ 傳送失敗：{e}")

client.run(DISCORD_TOKEN)
