import json
import logging
from os import environ

import requests
from spotify_api.api import SpotifyClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler, MessageHandler, filters,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_SEARCH_TYPE, TOP_TRACKS, ALBUMS, TRACKS_FROM_ALBUM = range(4)

keyboard_start = [
    [
        InlineKeyboardButton("top tracks by artist", callback_data="top tracks by artist"),
        InlineKeyboardButton("albums by artist", callback_data="albums by artist")
    ],
    [
        InlineKeyboardButton("tracks from album", callback_data="tracks from album")
    ]
]

keyboard_question = [
    [
        InlineKeyboardButton("Restart", callback_data="Restart"),
        InlineKeyboardButton("End", callback_data="End"),
    ]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    reply_markup = InlineKeyboardMarkup(keyboard_start)

    await update.message.reply_text("Hi! I am Spotify Bot")
    await update.message.reply_text("You can choose from a variety of options.", reply_markup=reply_markup)

    return INPUT_SEARCH_TYPE


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(keyboard_start)

    await query.edit_message_text(text="Start again", reply_markup=reply_markup)
    return INPUT_SEARCH_TYPE


async def input_top_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(keyboard_question)
    await query.edit_message_text(text="Type your artist", reply_markup=reply_markup)

    return TOP_TRACKS


async def get_top_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    artist = update.message.text
    top_tracks = spotify_client.get_top_tracks_by_artist(artist)
    answer = f"Top Tracks from {artist}:" + '\n' + \
             '\n'.join(top_tracks)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer
    )

    return ConversationHandler.END


async def input_albums(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(keyboard_question)
    await query.edit_message_text(text="Type your artist", reply_markup=reply_markup)

    return ALBUMS


async def get_albums(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    artist = update.message.text
    albums = spotify_client.get_albums_by_artist(artist)
    answer = f"Albums by {artist}:" + '\n' + \
             '\n'.join(albums)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer
    )

    return ConversationHandler.END


async def input_tracks_from_album(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(keyboard_question)
    await query.edit_message_text(text="Type your album", reply_markup=reply_markup)

    return TRACKS_FROM_ALBUM


async def get_tracks_from_album(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    album = update.message.text
    tracks = spotify_client.get_albums_by_artist(album)
    answer = f"Tracks from {album}:" + '\n' + \
             '\n'.join(tracks)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer
    )

    return ConversationHandler.END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(token).build()

    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INPUT_SEARCH_TYPE: [
                CallbackQueryHandler(input_top_tracks, pattern="^top tracks by artist$"),
                CallbackQueryHandler(input_albums, pattern="^albums by artist$"),
                CallbackQueryHandler(input_tracks_from_album, pattern="^tracks from album$"),
            ],
            TOP_TRACKS: [
                CallbackQueryHandler(start_over, pattern="^Restart$"),
                CallbackQueryHandler(end, pattern="^End$"),
                MessageHandler(filters.TEXT & ~(filters.COMMAND), get_top_tracks)
            ],
            ALBUMS: [
                CallbackQueryHandler(start_over, pattern="^Restart$"),
                CallbackQueryHandler(end, pattern="^End$"),
                MessageHandler(filters.TEXT & ~(filters.COMMAND), get_albums)
            ],
            TRACKS_FROM_ALBUM: [
                CallbackQueryHandler(start_over, pattern="^Restart$"),
                CallbackQueryHandler(end, pattern="^End$"),
                MessageHandler(filters.TEXT & ~(filters.COMMAND), get_tracks_from_album)
            ],
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    settings_file_path = environ.get('settings_file_path') \
        if environ.get('settings_file_path') is not None else "settings.json"
    with open(settings_file_path) as settings_file:
        settings = json.load(settings_file)
    spotify_client = SpotifyClient(settings)
    token = settings["TOKEN"]
    main()
