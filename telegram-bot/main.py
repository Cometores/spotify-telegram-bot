import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

#Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
TOP_TRACKS, ALBUMS, TRACKS_FROM_ALBUM = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    text_hi = (
        "Hi! I am Spotify Bot"
    )
    text = (
        "You can choose from a variety of options."
    )

    keyboard = [
        [
            InlineKeyboardButton("top tracks", callback_data=str(TOP_TRACKS)),
            InlineKeyboardButton("albums by artist", callback_data=str(ALBUMS))
        ],
        [
            InlineKeyboardButton("tracks from album", callback_data=str(ALBUMS))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text_hi)

    # Send message with text and appended InlineKeyboard
    await update.message.reply_text(text, reply_markup=reply_markup)

    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("top tracks", callback_data=str(TOP_TRACKS)),
            InlineKeyboardButton("albums by artist", callback_data=str(ALBUMS))
        ],
        [
            InlineKeyboardButton("tracks from album", callback_data=str(ALBUMS))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return START_ROUTES


async def top_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("start over", callback_data=str(START_ROUTES)),
            InlineKeyboardButton("end", callback_data=str(END_ROUTES)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Type your artist", reply_markup=reply_markup
    )
    return END_ROUTES


async def albums(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("start over", callback_data=str(START_ROUTES)),
            InlineKeyboardButton("end", callback_data=str(END_ROUTES)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Type your artist", reply_markup=reply_markup
    )
    return END_ROUTES


async def tracks_from_album(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("start over", callback_data=str(START_ROUTES)),
            InlineKeyboardButton("end", callback_data=str(END_ROUTES)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Type your artist", reply_markup=reply_markup
    )
    return END_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("6085384433:AAGwBrwLcgioU8w8NESqsaYcpjybxV6tSi4").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(top_tracks, pattern="^" + str(TOP_TRACKS) + "$"),
                CallbackQueryHandler(albums, pattern="^" + str(ALBUMS) + "$"),
                CallbackQueryHandler(tracks_from_album, pattern="^" + str(TRACKS_FROM_ALBUM) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(START_ROUTES) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(END_ROUTES) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()