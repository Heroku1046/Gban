import json
import os
import asyncio

from pyrogram import Client, filters

app = Client("gban bot", api_id=int(os.environ["21556511"]), api_hash=os.environ["e0405128cb3ee6ecf7cbb0e64e665587"], bot_token=os.environ["6019599109:AAHsBK80H1PkfE8wvNpDEX74aC9g0OM_0sU"])

@app.on_message(filters.command("gban") & filters.me)
async def gban_handler(client: Client, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    user = await app.get_users(user_id)
    await msg.edit_text(f"GBanned user {user.first_name} ({user.id}).")

    # Load the banned users list from a JSON file
    with open("banned_users.json", "r") as f:
        banned_users = json.load(f)

    # Add the new user to the banned users list
    banned_users.append(user_id)

    # Save the updated banned users list to the JSON file
    with open("banned_users.json", "w") as f:
        json.dump(banned_users, f)

    # Iterate through all dialogs and ban the user from each dialog
    for dialog in await app.get_dialogs():
        if dialog.chat.type == "supergroup" or dialog.chat.type == "group":
            try:
                await app.ban_chat_member(dialog.chat.id, user_id)
            except Exception as e:
                print(e)

app.run()