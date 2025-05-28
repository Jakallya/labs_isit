import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = '8179088457:AAF1KMTfZM82LBaOGpGOD1d4l0WvglsH***'
VK_ACCESS_TOKEN = 'vk1.a.q***FSetEl3QPzvJwDY15qCNnIZAfM2nAxNzClEhloM80gMtoeumUrRtuM7MT-OwTPD_SEEzKml_CfFb2ZClyWFhRTL3padp5tEQMlXf_No0uo4AMlpzZe-jsaLxGpV8gaZR-gUqauDYkOgzj6ud3wMvWwPJvWTrR0NGaPIeIuKJmHluIksuhfIeBzegLPKPx39fYZ5MsOlbSkNeKbVinQ'
VK_USER_ID = '231117416'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправь мне сообщение, и я добавлю его как комментарий в VK.')


def get_last_post_id() -> dict:
    url = "https://api.vk.com/method/wall.get"
    params = {
        'owner_id': VK_USER_ID,
        'count': 1,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    return response.json()


def add_comment(post_id: int, message: str) -> dict:
    url = "https://api.vk.com/method/wall.createComment"
    params = {
        'owner_id': VK_USER_ID,
        'post_id': post_id,
        'message': message,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    return response.json()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        last_post = get_last_post_id()

        if 'error' in last_post:
            await update.message.reply_text(f"Ошибка VK: {last_post['error']['error_msg']}")
            return

        post_id = last_post['response']['items'][0]['id']
        result = add_comment(post_id, update.message.text)

        if 'error' in result:
            await update.message.reply_text(f"Ошибка комментария: {result['error']['error_msg']}")
        else:
            await update.message.reply_text(f"Комментарий добавлен! ID: {result['response']['comment_id']}")

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == '__main__':
    main()