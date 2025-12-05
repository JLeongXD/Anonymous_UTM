import asyncio
import logging
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
import google.generativeai as genai


# ====================================================================
load_dotenv() #read .env file

#从.env 拿key，id，token等
try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
except TypeError:
    print("❌ Error: Unable to read the .env file or its contents are missing. \n"
          "Please make sure the .env file exists and is correctly formatted.")
    exit()


# ==============================================================================

# 设置日志，方便在 VS Code 下方终端看到运行情况
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

bot = TelegramClient('confession_bot_session', API_ID, API_HASH) #创建一个连接Telegram的client
genai.configure(api_key=GEMINI_API_KEY) #告诉Gemini什么API Key
model = genai.GenerativeModel('gemini-2.5-flash') #选择用gemini2.5flash

user_mode = {} #用来记住每个用户目前处于什么mode(anonymous or named)


# ==============================================================================
#telegrambot主要的界面，user会看到的
async def send_main_menu(event_or_user_id, message_text=None):
    text = message_text or (
        "🎛️ **Main Menu**\n\nChoose how you want to send messages to the channel:"
    )
    buttons = [
        #主页面3行的button
        [Button.inline("🕵️ Anonymous Mode", b"anonymous")],
        [Button.inline("👤 Named Mode", b"named")],
        [Button.inline("ℹ️ Help", b"help"), Button.inline("❓ About", b"about")]
    ]
    
    #判断传入的是ID还是Event
    if isinstance(event_or_user_id, int):
        await bot.send_message(event_or_user_id, text, buttons=buttons)
    else:
        try:
            await event_or_user_id.edit(text, buttons=buttons)
        except:
            await event_or_user_id.respond(text, buttons=buttons)

#用gemini2.5flash审核照片
async def check_image_safety(media_bytes, mime_type):
    try:
        logging.info("⏳ Sending image to AI for safety check...") #正在审核照片
        
        #不让让google自动拦截，让gemini来判断
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        #prompt让ai判断照片是否安全
        prompt = (
            "You are a content moderator. Analyze this image carefully. "
            "Is this image safe to post on a public Telegram channel? "
            "Reply 'UNSAFE' if it contains: Nudity, Genitals, Pornography, Blood, Gore, Extreme Violence. "
            "Reply 'SAFE' for everything else including selfies, daily life photos, text, memes, casual swimwear, or shirtless men. "
            "Output only one word: SAFE or UNSAFE."
        )

        #让gemini知道图片格式，bytes
        image_part = {
            "mime_type": mime_type,
            "data": media_bytes
        }

        #把prompt和图片送给gemini分析
        response = await asyncio.to_thread(
            model.generate_content,
            [prompt, image_part],
            safety_settings=safety_settings
        )
        
        #获取结果
        try:
            result_text = response.text.strip().upper()
            #terminal会显示审核结果（SAFE or UNSAFE）
            print(f"🧐 AI Safety Review Result: [{result_text}]") 
            
            if "SAFE" in result_text and "UNSAFE" not in result_text:
                return True
            else:
                return False
                
        except ValueError:
            #如果google提前过滤
            print("🚫 Image was blocked by Google's internal safety layer.")
            if response.prompt_feedback:
                print(response.prompt_feedback)
            return False

    #任何错误都当作失败
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return False

#determine 照片的minetype
def get_mime_type(event):
    if event.photo:
        return "image/jpeg"
    if event.document:
        return event.document.mime_type
    return "image/jpeg"

#===================================================================================

#处理/start的command
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_text = (
        f"👋 Hello, {event.sender.first_name}!\n\n"
        "Welcome to the Submission Bot. You can send messages or images to be posted on the channel."
    )
    await send_main_menu(event.sender_id, welcome_text)

#处理/help的command
@bot.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    await event.respond(
        "📖 **Help Guide**\n\n"
            "This bot helps you submit messages or images to the channel safely.\n\n"
            "🔹 **Anonymous Mode**: Your identity is hidden.\n"
            "🔹 **Named Mode**: Your full name is displayed.\n"
            "🔹 **Content Review**: All submissions are automatically reviewed by AI to ensure they are safe.\n"
            "🔹 **Supported Content**: Text messages, images (selfies, memes, daily photos).\n"
            "🔹 **Blocked Content**: Nudity, violence, pornography, gore, hate speech.\n\n"
            "💡 Click 'Back' to return to the main menu.",
            buttons=[[Button.inline("🔙 Back to Menu", b"back")]]
    )

#处理click按钮后会发生什么
@bot.on(events.CallbackQuery)
async def on_button(event):
    user_id = event.sender_id
    choice = event.data.decode()

    #anonymous mode button
    if choice == "anonymous":
        user_mode[user_id] = "anonymous"
        await event.edit(
            "🕵️ **Anonymous Mode Activated**\n\n"
            "✅ You are now in Anonymous Mode.\n"
            "- Your identity will **not** be shown when your submission is posted.\n"
            "- You can send **text messages** or **images** freely.\n\n"
            "💡 Tip: Keep your messages clear and concise for the audience.",
            buttons=[[Button.inline("🔙 Back to Menu", b"back")]]
        )

    #named mode button
    elif choice == "named":
        user_mode[user_id] = "named"
        sender = await event.get_sender()
        name = f"{sender.first_name} {sender.last_name or ''}".strip()
        await event.edit(
            f"👤 **Named Mode Activated**\n"
            f"Displayed Name: **{name}**\n\n"
            "✅ You are now in Named Mode.\n"
            "- Your full name will be visible with your submission.\n"
            "- You can send **text messages** or **images**.\n\n"
            "💡 Tip: Make sure you are comfortable sharing your name publicly.",
            buttons=[[Button.inline("🔙 Back to Menu", b"back")]]
        )

    #help button
    elif choice == "help":
        await event.edit(
            "📖 **Help Guide**\n\n"
            "This bot helps you submit messages or images to the channel safely.\n\n"
            "🔹 **Anonymous Mode**: Your identity is hidden.\n"
            "🔹 **Named Mode**: Your full name is displayed.\n"
            "🔹 **Content Review**: All submissions are automatically reviewed by AI to ensure they are safe.\n"
            "🔹 **Supported Content**: Text messages, images (selfies, memes, daily photos).\n"
            "🔹 **Blocked Content**: Nudity, violence, pornography, gore, hate speech.\n\n"
            "💡 Click 'Back' to return to the main menu.",
            buttons=[[Button.inline("🔙 Back", b"back")]]
        )
    
    #about button
    elif choice == "about":
        await event.edit(
            "🤖 **About This Bot**\n\n"
            "This bot is powered by **Google Gemini AI** for:\n"
            "- Automatic content moderation\n"
            "- Safe posting of messages and images\n\n"
            "📌 Features:\n"
            "1. Anonymous and Named submission modes.\n"
            "2. Real-time AI safety checks.\n"
            "3. Admin notifications for every submission.\n\n"
            "💡 Safe, simple, and fast way to share confessions or messages with the community.",
            buttons=[[Button.inline("🔙 Back", b"back")]]
        )

    #back button
    elif choice == "back":
        if user_id in user_mode:
            del user_mode[user_id]
        await send_main_menu(event)

#处理user发的消息
@bot.on(events.NewMessage)
async def handle_input(event):
    
    #忽略start with '/'的command
    if event.text and event.text.startswith('/'):
        return

    user_id = event.sender_id
    
    #如果user没有选择模式，不处理（或者可以提示他去按/start）
    if user_id not in user_mode:
        return

    mode = user_mode[user_id]
    
    # Send"processing"message，让user知道正在处理
    processing_msg = await event.reply("⏳ Submission received. Processing now...")

    #获取user的信息
    sender = await event.get_sender()
    full_name = f"{sender.first_name} {sender.last_name or ''}".strip() or "User"
    text_content = event.text or ""

    #发在channel的template with user的发的信息
    if mode == "anonymous":
        caption_public = f"🕵️ **Confession (Anonymous)**\n\n{text_content}"
        admin_log = f"🕵️ [Anonymous Submission] From: [{full_name}](tg://user?id={user_id})\nContent: {text_content}"
    else:
        caption_public = f"👤 **Confession ({full_name})**\n\n{text_content}"
        admin_log = f"👤 [Named Submission] From: [{full_name}](tg://user?id={user_id})\nContent: {text_content}"

    try:
        #Case1：如果user发的是image
        if event.photo or (event.document and 'image' in event.document.mime_type):
            
            #下载image
            await processing_msg.edit("🤖 AI is reviewing the image for safety...")
            media_bytes = await event.download_media(file=bytes)
            mime_type = get_mime_type(event)

            #用Gemini 审核
            is_safe = await check_image_safety(media_bytes, mime_type)

            #如果unsafe，不发布
            if not is_safe:
                await processing_msg.edit(
                    "⚠️ **Submission Blocked**\n\nThe image was detected by AI as containing inappropriate content (e.g., nudity, violence) and cannot be posted."
                )
                #通知admin
                await bot.send_message(ADMIN_ID, f"🚫 **Blocked Submission**\n{admin_log}\nReason: AI marked it as unsafe.")
                
                #Reset user mode
                del user_mode[user_id]
                await send_main_menu(user_id)
                return

            #如果Safe,send to channel
            await bot.send_file(CHANNEL_ID, event.media, caption=caption_public)
            #发给admin做记录
            await bot.send_file(ADMIN_ID, event.media, caption=f"📢 **New Submission (Image)**\n{admin_log}")

        #Case2：如果user发的是text
        elif text_content:
            await bot.send_message(CHANNEL_ID, caption_public)
            await bot.send_message(ADMIN_ID, f"📢 **New Submission (Text)**\n{admin_log}")
        
        else:
            #if user发的不是text or image
            await processing_msg.edit("❌ Unsupported file type. Please send text or an image.")
            return

        await processing_msg.edit("✅ **Submission Successful!**")
    
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await processing_msg.edit(f"❌ System Error: {e}")
    
    #Reset user mode， 再发main menu给user
    if user_id in user_mode:
        del user_mode[user_id]
    await send_main_menu(user_id)


# ========================================================================
async def main():
    print("🤖 Connecting to Telegram servers...")
    await bot.start(bot_token=BOT_TOKEN) #登录bot
    print("✅ Bot started successfully! Listening for messages... (Press Ctrl+C to stop)")
    await bot.run_until_disconnected() #bot一直运行，直到手动停止

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        print("🤖 Starting Bot...") #bot start
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped manually.") #ctrl+c停止bot
    except Exception as e:
        print(f"\n❌ Error occurred: {e}") #maybe caused by network or token
    finally:
        loop.close()