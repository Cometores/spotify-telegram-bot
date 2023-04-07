import json
import logging
from os import environ
from typing import Dict

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


class TelegramBot:
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

    def __init__(self, settings: Dict[str, str]):
        self.spotify_client = SpotifyClient(settings)
        self.application = Application.builder().token(settings["TOKEN"]).build()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.message.from_user
        logger.info("User %s started the conversation.", user.first_name)
        reply_markup = InlineKeyboardMarkup(self.keyboard_start)

        await update.message.reply_text("Hi! I am Spotify Bot")
        await update.message.reply_text("You can choose from a variety of options.", reply_markup=reply_markup)

        return self.INPUT_SEARCH_TYPE

    async def start_over(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        reply_markup = InlineKeyboardMarkup(self.keyboard_start)

        await query.edit_message_text(text="Start again", reply_markup=reply_markup)
        return self.INPUT_SEARCH_TYPE

    async def input_top_tracks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        reply_markup = InlineKeyboardMarkup(self.keyboard_question)
        await query.edit_message_text(text="Type your artist", reply_markup=reply_markup)

        return self.TOP_TRACKS

    async def get_top_tracks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        artist = update.message.text
        top_tracks = self.spotify_client.get_top_tracks_by_artist(artist)
        answer = f"Top Tracks from {artist}:" + '\n' + \
                 '\n'.join(top_tracks)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=answer
        )

        return ConversationHandler.END

    async def input_albums(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        reply_markup = InlineKeyboardMarkup(self.keyboard_question)
        await query.edit_message_text(text="Type your artist", reply_markup=reply_markup)

        return self.ALBUMS

    async def get_albums(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        artist = update.message.text
        albums = self.spotify_client.get_albums_by_artist(artist)
        answer = f"Albums by {artist}:" + '\n' + \
                 '\n'.join(albums)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=answer
        )

        return ConversationHandler.END

    async def input_tracks_from_album(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        await query.answer()

        reply_markup = InlineKeyboardMarkup(self.keyboard_question)
        await query.edit_message_text(text="Type your album", reply_markup=reply_markup)

        return self.TRACKS_FROM_ALBUM

    async def get_tracks_from_album(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        album = update.message.text
        tracks = self.spotify_client.get_albums_by_artist(album)
        answer = f"Tracks from {album}:" + '\n' + \
                 '\n'.join(tracks)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=answer
        )

        return ConversationHandler.END

    async def end(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="See you next time!")
        return ConversationHandler.END

    def run(self) -> None:
        # ^ means "start of line/string"
        # $ means "end of line/string"
        # So ^ABC$ will only allow 'ABC'

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                self.INPUT_SEARCH_TYPE: [
                    CallbackQueryHandler(self.input_top_tracks, pattern="^top tracks by artist$"),
                    CallbackQueryHandler(self.input_albums, pattern="^albums by artist$"),
                    CallbackQueryHandler(self.input_tracks_from_album, pattern="^tracks from album$"),
                ],
                self.TOP_TRACKS: [
                    CallbackQueryHandler(self.start_over, pattern="^Restart$"),
                    CallbackQueryHandler(self.end, pattern="^End$"),
                    MessageHandler(filters.TEXT & ~(filters.COMMAND), self.get_top_tracks)
                ],
                self.ALBUMS: [
                    CallbackQueryHandler(self.start_over, pattern="^Restart$"),
                    CallbackQueryHandler(self.end, pattern="^End$"),
                    MessageHandler(filters.TEXT & ~(filters.COMMAND), self.get_albums)
                ],
                self.TRACKS_FROM_ALBUM: [
                    CallbackQueryHandler(self.start_over, pattern="^Restart$"),
                    CallbackQueryHandler(self.end, pattern="^End$"),
                    MessageHandler(filters.TEXT & ~(filters.COMMAND), self.get_tracks_from_album)
                ],
            },
            fallbacks=[CommandHandler("start", self.start)]
        )

        self.application.add_handler(conv_handler)
        self.application.run_polling()
