import asyncio
import logging
from pyrogram import filters, Client, errors
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

def main_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Channel", url=cfg.CHANNEL_URL),
                InlineKeyboardButton("🛠 Support", url=cfg.SUPPORT_URL)
            ],
            [
                InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{cfg.BOT_USERNAME}?startgroup=true"),
                InlineKeyboardButton("❓ Help", callback_data="help_main")
            ]
        ]
    )

@app.on_chat_join_request()
async def approve(_, m):
    chat = m.chat
    user = m.from_user
    try:
        add_group(chat.id)
        await app.approve_chat_join_request(chat.id, user.id)
        await app.send_message(
            user.id,
            f"Hello {user.mention}, welcome to {chat.title}!\n\n"
            "You have been auto-approved.\n\nPowered by: @RadhaSprt.",
        )
        add_user(user.id)
    except errors.PeerIdInvalid:
        logger.warning("User hasn't started the bot or group issue.")
    except Exception as err:
        logger.error(f"Error in approve: {err}", exc_info=True)

@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except Exception:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except Exception as e:
            await m.reply(f"Make sure I am admin in your channel.\nError: {e}")
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Join Channel", url=invite_link.invite_link),
                    InlineKeyboardButton("Check Again", callback_data="chk")
                ]
            ]
        )
        await m.reply(
            "Access Denied! Please join my update channel and click 'Check Again' to confirm.",
            reply_markup=keyboard
        )
        return

    add_user(m.from_user.id)
    await m.reply_photo(
        cfg.START_IMG,
        caption=(
            f"👋 Hello {m.from_user.mention}!\n"
            "I am your auto-approve bot.\n\n"
            "Add me as admin with 'add members' permission in your group or channel, "
            "and I will automatically approve join requests.\n\n"
            "Powered by: @RadhaSprt."
        ),
        reply_markup=main_keyboard()
    )

@app.on_callback_query(filters.regex("chk"))
async def check_channel(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except Exception:
        await cb.answer(
            "You are not joined in the channel. Please join and check again.",
            show_alert=True
        )
        return

    add_user(cb.from_user.id)
    try:
        await cb.edit_message_caption(
            caption=(
                f"👋 Hello {cb.from_user.mention}!\n"
                "I am your auto-approve bot.\n\n"
                "Add me as admin with 'add members' permission in your group or channel, "
                "and I will automatically approve join requests.\n\n"
                "Powered by: @RadhaSprt."
            ),
            reply_markup=main_keyboard()
        )
    except Exception:
        await cb.message.edit_text(
            f"👋 Hello {cb.from_user.mention}!\n"
            "I am your auto-approve bot.\n\n"
            "Add me as admin with 'add members' permission in your group or channel, "
            "and I will automatically approve join requests.\n\n"
            "Powered by: @RadhaSprt.",
            reply_markup=main_keyboard()
        )

HELP_TEXTS = {
    "bcast": "📣 /bcast\nReply to a message to broadcast it to all users.",
    "fcast": "📤 /fcast\nReply to a message to forward it to all users.",
    "users": "👥 /users\nShows the total number of users and groups (SUDO only).",
    "start": "👋 /start\nStart the bot and check channel access."
}

@app.on_callback_query(filters.regex("help_main"))
async def help_main(_, cb: CallbackQuery):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📣 Broadcast", callback_data="help_bcast"),
            InlineKeyboardButton("📤 Forward", callback_data="help_fcast")
        ],
        [
            InlineKeyboardButton("👥 Users", callback_data="help_users"),
            InlineKeyboardButton("👋 Start", callback_data="help_start")
        ],
        [
            InlineKeyboardButton("🏠 Back", callback_data="help_main")
        ]
    ])
    await cb.answer()
    await cb.message.edit_text(
        "❓ **Help Menu**\n\nSelect a command to view its details:",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex(r"help_(.*)"))
async def show_command_help(_, cb: CallbackQuery):
    cmd = cb.data.split("_")[1]
    text = HELP_TEXTS.get(cmd, "No info available for this command.")
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅ Back", callback_data="help_main")
        ]
    ])
    await cb.answer()
    await cb.message.edit_text(f"**{cmd.upper()} Command**\n\n{text}", reply_markup=keyboard)

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def show_stats(_, m: Message):
    try:
        total_users = all_users()
        total_groups = all_groups()
        await m.reply_text(
            f"👤 Users: {total_users}\n📢 Groups: {total_groups}\n🔢 Total: {total_users + total_groups}"
        )
    except Exception as e:
        await m.reply_text(f"Error fetching stats: {e}")

BATCH_SIZE = 100
WORKERS = 10
BATCH_DELAY = 1
semaphore = asyncio.Semaphore(WORKERS)

async def send_message(message, user_id, action="copy"):
    while True:
        try:
            if action == "copy":
                await message.copy(user_id)
            else:
                await message.forward(user_id)
            return "success"
        except errors.FloodWait as e:
            await asyncio.sleep(e.value)
        except errors.InputUserDeactivated:
            remove_user(user_id)
            return "deactivated"
        except errors.UserIsBlocked:
            remove_user(user_id)
            return "blocked"
        except Exception as e:
            logger.error(f"Broadcast error to {user_id}: {e}", exc_info=True)
            return "failed"

async def broadcast_message(message, action="copy"):
    success = failed = blocked = deactivated = 0
    async for doc in users.find({}, {"user_id": 1}):
        user_id = int(doc["user_id"])
        async with semaphore:
            result = await send_message(message, user_id, action)
        if result == "success":
            success += 1
        elif result == "blocked":
            blocked += 1
        elif result == "deactivated":
            deactivated += 1
        else:
            failed += 1
        await asyncio.sleep(BATCH_DELAY)
    return success, failed, blocked, deactivated

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast_handler(_, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a message to broadcast.")
    status_msg = await m.reply_text("🚀 Broadcasting message...")
    success, failed, blocked, deactivated = await broadcast_message(
        m.reply_to_message, action="copy"
    )
    await status_msg.edit(
        f"✅ Success: {success}\n🚫 Blocked: {blocked}\n🗑️ Deactivated: {deactivated}\n❌ Failed: {failed}"
    )

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast_handler(_, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a message to forward broadcast.")
    status_msg = await m.reply_text("🚀 Forwarding message...")
    success, failed, blocked, deactivated = await broadcast_message(
        m.reply_to_message, action="forward"
    )
    await status_msg.edit(
        f"✅ Success: {success}\n🚫 Blocked: {blocked}\n🗑️ Deactivated: {deactivated}\n❌ Failed: {failed}"
    )

print("Bot is running...")
app.run()