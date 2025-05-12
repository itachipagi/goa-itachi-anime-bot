import os
import json
import logging
import asyncio
import random

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    CallbackQueryHandler
)

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
FILTERS_FILE = 'filters.json'
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN') or ""

# Dictionary to store ad deletion state for each group
ad_deletion_states = {}

# Predefined filters
PREDEFINED_FILTERS = {
    "welcome": {
        "content": "Welcome to our Hindi Official channels group! Type 'channels' to see all our channels.",
        "use_buttons": False
    },
    "rules": {
        "content": "1. Be respectful\n2. No spam\n3. No advertising\n4. English or Hindi only",
        "use_buttons": True
    },
    "help": {
        "content": "You can use these commands:\n• 'channels' - See all our Hindi Official channels\n• 'attack on titan' - Attack On Titan channel\n• 'tokyo 24th ward' - Tokyo 24th Ward channel\n• 'naruto shippuden' - Naruto Shippuden channel\n• 'girl i hate' or 'married' - I'M Getting Married channel\n• 'wolf king' - Wolf King channel\n\nNote: Not exact command matches will work.",
        "use_buttons": False
    }
}

# Channel links
CHANNEL_LINKS = {
    "attack on titan": "https://t.me/+rIKUUyTYlo8wNGM1",
    "tokyo 24th ward": "https://t.me/+ShzCsWRvCvcwMjFl",
    "married": "https://t.me/+bEGR9J6aAFthZDU1",
    "Movie Channel": "https://t.me/andi_mandi_sandi_clicklink_again"
}

# Ensure filters file exists
def init_filters():
    """Initialize filters file with predefined filters"""
    if os.path.exists(FILTERS_FILE):
        # Load existing filters
        existing_filters = load_filters()
        # Add predefined filters (without overwriting existing ones)
        for name, data in PREDEFINED_FILTERS.items():
            if name not in existing_filters:
                existing_filters[name] = data
        save_filters(existing_filters)
    else:
        # Create new filters file with predefined filters
        with open(FILTERS_FILE, 'w') as f:
            json.dump(PREDEFINED_FILTERS, f)

def load_filters():
    """Load filters from file"""
    try:
        with open(FILTERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_filters(filters):
    """Save filters to file"""
    with open(FILTERS_FILE, 'w') as f:
        json.dump(filters, f)

def add_filter(name, content, use_buttons=None, button_links=None):
    """Add a filter programmatically

    Parameters:
    name (str): The name of the filter
    content (str): The content of the filter
    use_buttons (bool, optional): Whether to use buttons. If None, determined by newlines in content
    button_links (dict, optional): Dictionary mapping button text to URLs. Format: {"Button text": "https://example.com"}
    """
    # Determine if we should use buttons (if not specified)
    if use_buttons is None:
        use_buttons = '\n' in content

    filters = load_filters()
    filters[name.lower()] = {
        'content': content,
        'use_buttons': use_buttons,
        'button_links': button_links
    }
    save_filters(filters)
    logger.info(f"Filter '{name}' added programmatically")

def remove_filter(name):
    """Remove a filter programmatically"""
    filters = load_filters()
    if name.lower() in filters:
        del filters[name.lower()]
        save_filters(filters)
        logger.info(f"Filter '{name}' removed programmatically")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("List All Anime", callback_data="show_anime_list")],
        [InlineKeyboardButton("List All Movies", callback_data="show_anime_movie_list")],
        [InlineKeyboardButton("Popular Channels", callback_data="show_popular")],
        [InlineKeyboardButton("Help", callback_data="show_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        f"👋 Hi {user.first_name}! Welcome to the Anime Channel Finder Bot!\n\n"
        f"I can help you find Telegram anime channels for your favorite anime and manga series.\n\n"
        f"Just type the name of an anime (like 'attack on titan' or 'one piece') "
        f"and I'll give you a link to join the channel.\n\n"
        f"You can also use me in groups to help members discover anime channels!"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()

    # Handle menu buttons
    if query.data == "show_anime_list":
        await query.edit_message_text(
            text="All Anime/Manga Channels Available:\n1. Dragon Ball Diama\n2. The Angel Next Door\n3. Dandadan\n4. Code Geass\n5. Tokyo Revengers\n6. 365 Days to the Wedding\n7. Bleach\n8. Banished From Hero's Party\n9. Castlevania Nocturne\n10. Hunter X Hunter\n11. Fairy Tail\n12. Tomb Raider\n13. True Beauty\n14. Trillion Game\n15. Reincarnated as a Slime\n16. Blue Lock\n17. The Exclusive Samurai\n18. Days With My Stepsister\n19. Vinland Saga\n20. Alya Sometimes Hides Feelings\n21. Nobody Remember Me\n22. Tower of God\n23. Haikyu\n24. Bye Bye Earth\n25. Black Summoner\n26. Mushoku Tensei\n27. Strongest Magician\n28. Kaiju No. 8\n29. Iceblade Sorcerer\n30. Makeine\n31. Black Clover\n32. Red Ranger\n33. Archdemon's Dilemma\n34. Dr. Stone\n35. Berserk of Gluttony\n36. Reincarnated Aristocrat\n37. One Piece\n38. Record of Ragnarok\n39. Solo Leveling\n40. Sakamoto Days\n41. Hell's Paradise\n42. Tokyo 24th Ward\n43. Wind Breaker\n44. i parry everything\n45. naruto shippuden\n 46. devil may cry\n 47. berserk\n48.  JoJo's Bizarre Adventure \n 49. My Hero Academia \n50. lookism \n51. demon slayer \n52. my dress up darling \n53. death note\n54. I'M Getting Married to a Girl I hate\n54. masmune kun no revenge.\n55. Spy x Family.\n56. boruto."
        )
        return
    elif query.data == "show_anime_movie_list":
        await query.edit_message_text(
            text="All Anime Movies Available:\n1. Howls Moving Castle (2004)\n2. Grave of the Fireflies\n3. I want to eat your pancreas\n4. Princess Mononoke (1997)\n4. Your Name(kimi no nawa)\n5. weathering with you\n6. my neighbour totoro\n7. black clover: sword of the wizard king\n8. A Silent Voice\n9. chhota bheem movies"
        )
        return
    elif query.data == "show_popular":
        keyboard = [
            [InlineKeyboardButton("One Piece", callback_data="anime_one_piece")],
            [InlineKeyboardButton("Attack on Titan", callback_data="anime_attack_on_titan")],
            [InlineKeyboardButton("Naruto Shippuden", callback_data="anime_naruto_shippuden")],
            [InlineKeyboardButton("Solo Leveling", callback_data="anime_solo_leveling")],
            [InlineKeyboardButton("Dragon Ball", callback_data="anime_dragon_ball")],
            [InlineKeyboardButton("Back to Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose a popular anime:", reply_markup=reply_markup)
        return
    elif query.data == "show_help":
        help_text = (
            "🌟 *Anime Channel Finder Bot Help* 🌟\n\n"
            "*Commands:*\n"
            "• /start - Show the welcome message\n"
            "• /help - Show this help message\n"
            "• /anime - Show all anime channels\n"
            "• /movie - Show all anime movies\n\n"
            "*How to use:*\n"
            "Simply type the name of an anime to get its channel link. For example:\n"
            "• one piece\n"
            "• attack on titan\n"
            "• solo leveling\n\n"
            "*Note:* Type the full name exactly as shown in the anime list for best results."
        )
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=help_text, reply_markup=reply_markup, parse_mode='Markdown')
        return
    elif query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("List All Anime", callback_data="show_anime_list")],
            [InlineKeyboardButton("List All Movies", callback_data="show_anime_movie_list")],
            [InlineKeyboardButton("Popular Channels", callback_data="show_popular")],
            [InlineKeyboardButton("Help", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="I can help you find Telegram channels for your favorite anime and manga series.\n\nJust type the name of an anime to get a link!",
            reply_markup=reply_markup
        )
        return


    # Handle specific anime callbacks
    if query.data.startswith("anime_"):
        anime_name = query.data.replace("anime_", "").replace("_", " ")
        filters = load_filters()
        if anime_name in filters:
            filter_data = filters[anime_name]
            button_links = filter_data.get('button_links', None)

            if button_links:
                keyboard = []
                for title, url in button_links.items():
                    keyboard.append([InlineKeyboardButton(title, url=url)])

                # Add back button
                keyboard.append([InlineKeyboardButton("Back", callback_data="show_popular")])
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    text=f"{anime_name.title()} Channel:",
                    reply_markup=reply_markup
                )
                return

    # For channel options, maintain the buttons with links rather than just showing selection
    if query.data.startswith("option_") and "naruto shippuden" in query.message.text.lower():
        filters = load_filters()
        if "naruto shippuden" in filters:
            filter_data = filters["naruto shippuden"]
            button_links = filter_data.get('button_links', None)

            if button_links:
                keyboard = []
                for option, url in button_links.items():
                    keyboard.append([InlineKeyboardButton(option, url=url)])

                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(text="Naruto Shippuden Hindi Official Channel:", reply_markup=reply_markup)
                return

    # Just acknowledge other button presses
    if query.data.startswith("option_"):
        option_index = int(query.data.replace("option_", ""))
        await query.edit_message_text(f"You selected option {option_index+1}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    # Basic help text for all users
    help_text = (
        "🌟 *Anime Channel Finder Bot Help* 🌟\n\n"
        "*Available Commands:*\n"
        "• /start - Start the bot and see welcome message\n"
        "• /help - Show this help message\n"
        "• /anime - Show all available anime channels\n"
        "• /movie - Show all available anime movies\n"
        "• /command - Show all available commands\n"
        "• /checkall - Show all filters with links (Group admins only)\n"
        "• /ad on/off - Enable/disable ad deletion (Group admins only)\n\n"
        "*How to use:*\n"
        "Simply type the name of an anime to get a link to that channel.\n"
        "For example:\n"
        "• one piece\n"
        "• attack on titan\n"
        "• solo leveling\n\n"
        "*Note:* Type the full name exactly as shown in the anime list for best results."
    )

    await update.message.reply_text(help_text, parse_mode='Markdown')

async def command_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a detailed list of all commands when /command is issued."""
    # Basic commands for all users
    command_text = (
        "📋 *All Available Commands* 📋\n\n"
        "*General Commands:*\n"
        "• /start - Start the bot and see welcome message\n"
        "• /help - Show help information\n"
        "• /anime - Show all available anime channels\n"
        "• /movie - Show all available anime movies\n"
        "• /command - Show this command list\n\n"
        "*Group Admin Commands:*\n"
        "• /checkall - Show all filters with links\n"
        "• /ad on - Enable ad deletion\n"
        "• /ad off - Disable ad deletion\n"
    )

    await update.message.reply_text(command_text, parse_mode='Markdown')

async def anime_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the anime list when the command /anime is issued."""
    # Use the same content as the "anime list" filter
    anime_list_text = "All Anime/Manga Channels Available:\n1. Dragon Ball Diama\n2. The Angel Next Door\n3. Dandadan\n4. Code Geass\n5. Tokyo Revengers\n6. 365 Days to the Wedding\n7. Bleach\n8. Banished From Hero's Party\n9. Castlevania Nocturne\n10. Hunter X Hunter\n11. Fairy Tail\n12. Tomb Raider\n13. True Beauty\n14. Trillion Game\n15. Reincarnated as a Slime\n16. Blue Lock\n17. The Exclusive Samurai\n18. Days With My Stepsister\n19. Vinland Saga\n20. Alya Sometimes Hides Feelings\n21. Nobody Remember Me\n22. Tower of God\n23. Haikyu\n24. Bye Bye Earth\n25. Black Summoner\n26. Mushoku Tensei\n27. Strongest Magician\n28. Kaiju No. 8\n29. Iceblade Sorcerer\n30. Makeine\n31. Black Clover\n32. Red Ranger\n33. Archdemon's Dilemma\n34. Dr. Stone\n35. Berserk of Gluttony\n36. Reincarnated Aristocrat\n37. One Piece\n38. Record of Ragnarok\n39. Solo Leveling\n40. Sakamoto Days\n41. Hell's Paradise\n42. Tokyo 24th Ward\n43. Wind Breaker\n44. i parry everything\n45. naruto shippuden\n 46. devil may cry\n 47. berserk \n48.  JoJo's Bizarre Adventure \n 49. My Hero Academia \n50. lookism \n51. demon slayer \n52. my dress up darling \n53. death note\n54. I'M Getting Married to a Girl I hate"

    await update.message.reply_text(anime_list_text)

async def ad_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /ad command to toggle ad deletion"""
    # Check if command is used in a group
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in groups!")
        return

    # Get the chat member who sent the command
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, user.id)

    # Check if user is the group owner
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("Only group owners and administrators can use this command!")
        return

    # Get the command argument
    args = context.args
    if not args:
        await update.message.reply_text("Please specify 'on' or 'off' after the command!")
        return

    command = args[0].lower()
    chat_id = update.effective_chat.id

    if command == 'on':
        ad_deletion_states[chat_id] = True
        await update.message.reply_text("Ad deletion has been enabled. I will now delete promotional messages from other bots.")
    elif command == 'off':
        ad_deletion_states[chat_id] = False
        await update.message.reply_text("Ad deletion has been disabled. I will no longer delete promotional messages.")
    else:
        await update.message.reply_text("Please use '/ad on' or '/ad off'")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages"""
    # # Check for specific user ID and reply "kamine"
    # if str(update.effective_user.id) == "8114986649":
    #     await update.message.reply_text("kamine")
    #     return

    # Check for ad deletion if message is from a bot
    if update.message.from_user.is_bot and update.message.from_user.id != context.bot.id:
        chat_id = update.effective_chat.id
        if ad_deletion_states.get(chat_id, False):
            try:
                await update.message.delete()
                return
            except Exception as e:
                logger.error(f"Error deleting ad message: {e}")

    # Get original message text and lowercase version
    original_text = update.message.text
    text = original_text.lower().strip()
    filters = load_filters()

    # Check for admin/owner mentions
    if text in ["admin", "owner"]:
        await update.message.reply_text("my cute owner Lord @Saiksh_pagi 😉😉")
        return

    # Handle anime list separately
    if text == "anime list":
        try:
            await update.message.reply_text("All Anime/Manga Channels Available:\n1. Dragon Ball Diama\n2. The Angel Next Door\n3. Dandadan\n4. Code Geass\n5. Tokyo Revengers\n6. 365 Days to the Wedding\n7. Bleach\n8. Banished From Hero's Party\n9. Castlevania Nocturne\n10. Hunter X Hunter\n11. Fairy Tail\n12. Tomb Raider\n13. True Beauty\n14. Trillion Game\n15. Reincarnated as a Slime\n16. Blue Lock\n17. The Exclusive Samurai\n18. Days With My Stepsister\n19. Vinland Saga\n20. Alya Sometimes Hides Feelings\n21. Nobody Remember Me\n22. Tower of God\n23. Haikyu\n24. Bye Bye Earth\n25. Black Summoner\n26. Mushoku Tensei\n27. Strongest Magician\n28. Kaiju No. 8\n29. Iceblade Sorcerer\n30. Makeine\n31. Black Clover\n32. Red Ranger\n33. Archdemon's Dilemma\n34. Dr. Stone\n35. Berserk of Gluttony\n36. Reincarnated Aristocrat\n37. One Piece\n38. Record of Ragnarok\n39. Solo Leveling\n40. Sakamoto Days\n41. Hell's Paradise\n42. Tokyo 24th Ward\n43. Wind Breaker\n44. i parry everything\n45. naruto shippuden\n 46. devil may cry\n 47. berserk \n48.  JoJo's Bizarre Adventure \n 49. My Hero Academia \n50. lookism \n51. demon slayer \n52. my dress up darling \n53. death note\n54. I'M Getting Married to a Girl I hate")
            return
        except Exception as e:
            logger.error(f"Error sending anime list: {e}")

    # ============ CONVERSATION HANDLING SECTION ============

    # List of all anime filter names for matching in conversational messages
    anime_filter_names = list(filters.keys())

    # Sort by length (descending) to match longer titles first
    anime_filter_names.sort(key=len, reverse=True)

    # Check if any anime name appears in the message
    found_anime = None

    # Common request patterns before anime name
    request_prefixes = [
        "i want", "give me", "looking for", "search for",
        "can i get", "please give", "need", "where is",
        "how to watch", "link for", "link to"
    ]

    # Common patterns after anime name
    request_suffixes = [
        "anime", "channel", "please", "link", "group",
        "telegram", "hindi", "english", "episode", "episodes"
    ]

    # First check for exact matches of anime names in the text
    for anime_name in anime_filter_names:
        if anime_name in text:
            found_anime = anime_name
            logger.info(f"Found anime name '{anime_name}' in conversational message")
            break

    # If no match yet, look for anime name with request patterns
    if not found_anime:
        for anime_name in anime_filter_names:
            # Check for patterns like "I want [anime_name]" or "give me [anime_name]"
            for prefix in request_prefixes:
                pattern = f"{prefix} {anime_name}"
                if pattern in text:
                    found_anime = anime_name
                    logger.info(f"Found request pattern '{pattern}' in message")
                    break

            # Check for patterns like "[anime_name] anime" or "[anime_name] channel"
            if not found_anime:
                for suffix in request_suffixes:
                    pattern = f"{anime_name} {suffix}"
                    if pattern in text:
                        found_anime = anime_name
                        logger.info(f"Found request pattern '{pattern}' in message")
                        break

            if found_anime:
                break

    # If we found an anime name in the conversation, use that filter
    if found_anime and found_anime in filters:
        filter_data = filters[found_anime]
        button_links = filter_data.get('button_links', None)

        if button_links:
            keyboard = []
            for title, url in button_links.items():
                keyboard.append([InlineKeyboardButton(title, url=url)])

            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                await update.message.reply_text(
                    f"Found '{found_anime}' channel for you:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e:
                logger.error(f"Error replying to message with anime match: {e}")
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Found '{found_anime}' channel for you:",
                        reply_markup=reply_markup
                    )
                    return
                except Exception as e2:
                    logger.error(f"Failed to send message even with fallback: {e2}")

    # ============ KEYWORD DETECTION SECTION ============

    # Extract potential keywords from the message

    # Check for common keywords within messages
    keywords = {
        "pfp": "pfp",
        "profile": "pfp",
        "pic": "pfp",
        "masamune": "masamune kun no revemge",
        "aot": "attack on titan",
        "titan": "attack on titan",
        "naruto": "naruto shippuden",
        "solo": "solo leveling",
        "dragon": "dragon ball",
        "piece": "one piece",
        "one": "one piece",
        "samurai": "the exclusive samurai",
        "angel": "the angel next door",
        "next": "the angel next door",
        "slime": "reincarnated as a slime",
        "stone": "dr. stone",
        "dr.": "dr. stone",
        "clover": "black clover",
        "black": "black clover",
        "spy": "spy x family",
        "family": "spy x family",
        "tokyo 24th ward": "tokyo 24th ward",
        "tokyo revengers": "tokyo revengers",
        "married": "i'm getting married to a girl i hate in my class",
        "girl": "i'm getting married to a girl i hate in my class",
        "hate": "i'm getting married to a girl i hate in my class",
        "hunter": "hunter x hunter",
        "vinland": "vinland saga",
        "bleach": "bleach",
        "sakamoto": "sakamoto days",
        "bye": "bye bye earth",
        "wind": "wind breaker",
        "breaker": "wind breaker",
        "parry": "i parry everything",
        "everything": "i parry everything",
        "devil": "devil may cry",
        "moving": "Howls Moving Castle",
        "i want": "i want to eat your pancreas",
        "grave": "grave of the fireflies",
        "fireflies": "grave of the fireflies",
        "fire": "grave of the fireflies",
        "princess": "Princess Mononoke",
        "Mononoke": "Princess Mononoke",
        }

    # Check if any keyword is in the message
    detected_filter = None
    for word in text.split():
        for keyword, filter_name in keywords.items():
            if keyword in word:  # This allows partial matches
                detected_filter = filter_name
                logger.info(f"Detected keyword '{keyword}' in message, showing filter '{filter_name}'")
                break
        if detected_filter:
            break

    # If we found a keyword match, use that filter
    if detected_filter and detected_filter in filters:
        filter_data = filters[detected_filter]
        content = filter_data['content']
        button_links = filter_data.get('button_links', None)

        if button_links:
            keyboard = []
            for title, url in button_links.items():
                keyboard.append([InlineKeyboardButton(title, url=url)])

            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                await update.message.reply_text(
                    f"Found '{detected_filter}' channel for you:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e:
                logger.error(f"Error replying to message with keyword match: {e}")
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Found '{detected_filter}' channel for you:",
                        reply_markup=reply_markup
                    )
                    return
                except Exception as e2:
                    logger.error(f"Failed to send message even with fallback: {e2}")

    # ============ DIRECT HANDLERS SECTION ============

    # Direct handler for "naruto shippuden" with channel link
    if text == "naruto shippuden":
        keyboard = [[InlineKeyboardButton("Join Naruto Shippuden Hindi Official Channel", url="https://t.me/naruto_shippuden_hindi_by_itachi")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await update.message.reply_text("Naruto Shippuden Hindi Official Channel:", reply_markup=reply_markup)
            return
        except Exception as e:
            logger.error(f"Error replying to message: {e}")
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Naruto Shippuden Hindi Official Channel:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e2:
                logger.error(f"Failed to send message even with fallback: {e2}")

    # Direct handler for "married" filter with channel link
    if text == "married" or text == "girl i hate":
        keyboard = [[InlineKeyboardButton("Join I'M Getting Married to a Girl I hate channel", url="https://t.me/+bEGR9J6aAFthZDU1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await update.message.reply_text("I'M Getting Married to a Girl I hate in my class Hindi Official:", reply_markup=reply_markup)
            return
        except Exception as e:
            logger.error(f"Error replying to message: {e}")
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="I'M Getting Married to a Girl I hate in my class Hindi Official:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e2:
                logger.error(f"Failed to send message even with fallback: {e2}")

    # Direct handler for "wolf king" with channel link
    if text == "wolf king":
        keyboard = [[InlineKeyboardButton("Join Wolf King Hindi Official Channel", url="https://t.me/+LSkILVJlHh0zZDdl")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await update.message.reply_text("Wolf King Hindi Official Channel:", reply_markup=reply_markup)
            return
        except Exception as e:
            logger.error(f"Error replying to message: {e}")
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Wolf King Hindi Official Channel:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e2:
                logger.error(f"Failed to send message even with fallback: {e2}")

    # Direct handler for "solo leveling" with channel link
    if text == "solo leveling":
        keyboard = [[InlineKeyboardButton("Join Solo Leveling Channel", url="https://t.me/+hrOLw2weDKY2YzE1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await update.message.reply_text("Solo Leveling Channel:", reply_markup=reply_markup)
            return
        except Exception as e:
            logger.error(f"Error replying to message: {e}")
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Solo Leveling Channel:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e2:
                logger.error(f"Failed to send message even with fallback: {e2}")

    # Direct handler for "wind breaker" with channel link
    if text == "wind breaker":
        keyboard = [[InlineKeyboardButton("Join Wind Breaker Channel", url="https://t.me/+CJBqVPIb7sdhNWJl")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await update.message.reply_text("Wind Breaker Channel:", reply_markup=reply_markup)
            return
        except Exception as e:
            logger.error(f"Error replying to message: {e}")
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Wind Breaker Channel:",
                    reply_markup=reply_markup
                )
                return
            except Exception as e2:
                logger.error(f"Failed to send message even with fallback: {e2}")

    # ============ POPULAR ANIME FILTERS SECTION ============

    # Direct handler for popular anime filters
    if text in ["one piece", "naruto shippuden", "masamune kun no revenge", "One punch man", "attack on titan", "Lookism", "solo leveling"]:
        # Get URLs from filters
        if text in filters:
            filter_data = filters[text]
            button_links = filter_data.get('button_links', None)
            if button_links:
                for title, url in button_links.items():
                    keyboard = [[InlineKeyboardButton(title, url=url)]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    try:
                        await update.message.reply_text(f"{title.replace('Join our', '').replace('channel!', '').strip()} Channel:", reply_markup=reply_markup)
                        return
                    except Exception as e:
                        logger.error(f"Error replying to message: {e}")
                        try:
                            await context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                text=f"{title.replace('Join our', '').replace('channel!', '').strip()} Channel:",
                                reply_markup=reply_markup
                            )
                            return
                        except Exception as e2:
                            logger.error(f"Failed to send message even with fallback: {e2}")

    # ============ EXACT MATCH FILTERS SECTION ============

    # Check for exact match in other filters
    if text in filters:
        # Skip if the filter name is a single word and less than 2 characters
        if len(text.split()) <= 1 and len(text) < 2:
            return

        filter_data = filters[text]
        content = filter_data['content']
        use_buttons = filter_data.get('use_buttons', False)
        button_links = filter_data.get('button_links', None)

        if use_buttons:
            # Split content by lines and create buttons
            options = [line.strip() for line in content.split('\n') if line.strip()]
            keyboard = []
            row = []

            # If we have button links, use them
            if button_links:
                for option in options:
                    if option in button_links:
                        row.append(InlineKeyboardButton(option, url=button_links[option]))
                    else:
                        row.append(InlineKeyboardButton(option, callback_data=f"option_{options.index(option)}"))

                    # Create rows with 2 buttons each
                    if len(row) == 2:
                        keyboard.append(row)
                        row = []

                # Add any remaining buttons
                if row:
                    keyboard.append(row)
            else:
                # Original button creation logic without URLs
                for i, option in enumerate(options):
                    row.append(InlineKeyboardButton(option, callback_data=f"option_{i}"))

                    # Create rows with 2 buttons each
                    if len(row) == 2 or i == len(options) - 1:
                        keyboard.append(row)
                        row = []

            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                await update.message.reply_text(f"Options for '{original_text}':", reply_markup=reply_markup)
            except Exception as e:
                logger.error(f"Error replying to message: {e}")
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Options for '{original_text}':",
                        reply_markup=reply_markup
                    )
                except Exception as e2:
                    logger.error(f"Failed to send message even with fallback: {e2}")
        else:
            # Just send the content as text
            try:
                await update.message.reply_text(content)
            except Exception as e:
                logger.error(f"Error replying with text: {e}")
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=content
                    )
                except Exception as e2:
                    logger.error(f"Failed to send text even with fallback: {e2}")
        return

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot."""
    logger.error(f"Exception while handling an update: {context.error}")

    # Log the error before we do anything else, so we can see it even if something breaks
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # Try to notify the user that something went wrong
    if update and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, something went wrong. Please try again later."
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle new member joins"""
    for new_member in update.message.new_chat_members:
        if new_member.id == context.bot.id:
            # Bot was added to a group
            welcome_text = (
                "👋 Hello everyone! I'm your Anime Channel Finder Bot!\n\n"
                "To see all available anime channels, type:\n"
                "• /anime - Shows all anime channels\n"
                "• /start - Shows welcome message\n"
                "• /help - Shows help information\n\n"
                "You can also type any anime name (like 'solo leveling' or 'attack on titan') "
                "to get a direct link to that channel!"
            )
            await update.message.reply_text(welcome_text)
        else:
            # New user joined the group
            welcome_text = (
                f"👋 Welcome {new_member.first_name}!\n\n"
                f"To see all available anime channels, type:\n"
                f"• /anime - Shows all anime channels\n"
                f"• /start - Shows welcome message\n"
                f"• /help - Shows help information\n\n"
                f"You can also type any anime name (like 'solo leveling' or 'attack on titan') "
                f"to get a direct link to that channel!"
            )
            await update.message.reply_text(welcome_text)

async def checkall_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /checkall command - shows all filters with links"""
    # Check if command is used in a group
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in groups!")
        return

    # Get the chat member who sent the command
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, user.id)

    # Check if user is the group owner
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("Only group owners and administrators can use this command!")
        return

    # Get all filters
    filters = load_filters()

    # Create message with all filters and their links
    message = "📋 All Available Filters and Links:\n\n"

    # Add each filter with its link
    for filter_name, filter_data in filters.items():
        if filter_data.get('button_links'):
            for title, url in filter_data['button_links'].items():
                message += f"• {filter_name.title()}\n  Link: {url}\n\n"

    # Split message into chunks if it's too long
    max_length = 4000
    if len(message) > max_length:
        chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(message)

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle sticker messages"""
    # Function disabled - no longer checking channel membership for stickers
    pass

async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the anime movie list when the command /movie is issued."""
    movie_list_text = "All Anime Movies Available:\n1. Howls Moving Castle (2004)\n2. Grave of the Fireflies\n3. I want to eat your pancreas\n4. Princess Mononoke (1997)\n5. black clover: sword of the wizard king\n6. your name(kimi no nawa)\n7. weathering with you\n8. A Silent Voice\n9. Over The Sky\n10. 5cm per second\n11. suzume no tojimari"

    await update.message.reply_text(movie_list_text)

async def main() -> None:
    """Start the bot."""
    # Initialize filters
    init_filters()

    # Create all channel filters
    create_all_filters()

    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("anime", anime_list_command))
    application.add_handler(CommandHandler("movie", movie_command))  # Add the new movie command handler
    application.add_handler(CommandHandler("checkall", checkall_command))
    application.add_handler(CommandHandler("ad", ad_command))
    application.add_handler(CommandHandler("command", command_command))

    # Callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Register new member handler
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # Sticker handler removed
    # application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    # Add error handler
    application.add_error_handler(error_handler)

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    logger.info("Bot started.")

    # Run indefinitely until interrupted
    try:
        while True:
            await asyncio.sleep(3600)  # Check every hour
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopping...")
    finally:
        # Clean shutdown
        await application.stop()

def create_all_filters():
    """Create all channel filters in a separate function for better organization.

    Filters are organized alphabetically (A-Z) for easier maintenance.
    Each filter has a comment describing what anime/manga it's for.
    """
    # ================= MAIN FILTER COLLECTIONS =================

    # Anime list - Shows all available anime channels
    add_filter(
        "anime list",
        "All Anime/Manga Channels Available:\n1. Dragon Ball Diama\n2. The Angel Next Door\n3. Dandadan\n4. Code Geass\n5. Tokyo Revengers\n6. 365 Days to the Wedding\n7. Bleach\n8. Banished From Hero's Party\n9. Castlevania Nocturne\n10. Hunter X Hunter\n11. Fairy Tail\n12. Tomb Raider\n13. True Beauty\n14. Trillion Game\n15. Reincarnated as a Slime\n16. Blue Lock\n17. The Exclusive Samurai\n18. Days With My Stepsister\n19. Vinland Saga\n20. Alya Sometimes Hides Feelings\n21. Nobody Remember Me\n22. Tower of God\n23. Haikyuu\n24. Bye Bye Earth\n25. Black Summoner\n26. Mushoku Tensei\n27. Strongest Magician\n28. Kaiju No. 8\n29. Iceblade Sorcerer\n30. Makeine\n31. Black Clover\n32. Red Ranger\n33. Archdemon's Dilemma\n34. Dr. Stone\n35. Berserk of Gluttony\n36. Reincarnated Aristocrat\n37. One Piece\n38. Record of Ragnarok\n39. Solo Leveling\n40. Sakamoto Days\n41. Hell's Paradise\n42. Tokyo 24th Ward\n43. Wind Breaker\n44. i parry everything\n45. naruto shippuden\n46. devil may cry\n47. berserk\n48.  JoJo's Bizarre Adventure \n49. My Hero Academia \n50. lookism \n51. demon slayer \n52. my dress up darling \n53. death note\n54. I'M Getting Married to a Girl I hate",
        use_buttons=False
    )

    # Channels - Shows all main Hindi Official channels
    add_filter(
        "channels",
        "Join our Hindi Official channels!\n1. Attack On Titan Hindi Official\n2. Tokyo 24th Ward Hindi Official\n3. I'M Getting Married to a Girl I hate in my class Hindi Official\n4. Naruto Shippuden Hindi Official\n5. Wolf King\n6. Dragon Ball Diama",
        use_buttons=True,
        button_links={
            "1. Attack On Titan Hindi Official": "https://t.me/+rIKUUyTYlo8wNGM1",
            "2. Lookism Hindi Official": "https://t.me/lookismhindidubofficial",
            "3. Masamune kun no revenge Hindi Official": "https://t.me/masamune_kuns_revenge_hindi_01",
            "4. Naruto Shippuden Hindi Official": "https://t.me/naruto_shippuden_hindi_by_itachi",
            "5. The angel next door": "https://t.me/+MY2RlYAOSJ41NmJl",
            "6. Dragon Ball Diama": "https://t.me/+1gh_jaECTH0zMGZl"
        }
    )

    # ================= ALPHABETICAL ANIME FILTERS =================

    # 365 Days to the Wedding
    add_filter(
        "365 days to the wedding",
        "Join our 365 Days to the Wedding channel!",
        use_buttons=True,
        button_links={
            "Join our 365 Days to the Wedding channel!": "https://t.me/+yMsIsFN_LhFkNzhl"
        }
    )

    # Alya Sometimes Hides Her Feelings in Russian (with alternative name)
    add_filter(
        "alya sometimes hides her feelings in russian",
        "Join our Alya Sometimes Hides Her Feelings in Russian channel!",
        use_buttons=True,
        button_links={
            "Join our Alya Sometimes Hides Her Feelings in Russian channel!": "https://t.me/+tHv3vabltudkNzU9"
        }
    )

    add_filter(
        "alya sometimes hides her feelings",
        "Join our Alya Sometimes Hides Her Feelings in Russian channel!",
        use_buttons=True,
        button_links={
            "Join our Alya Sometimes Hides Her Feelings in Russian channel!": "https://t.me/+tHv3vabltudkNzU9"
        }
    )

    # masamune kun no revenge
    add_filter(
        "masamune kun no revenge",
        "Join our Masamune kun no revenge Hindi Official channel!",
        use_buttons=True,
        button_links={
            "⚜️Masamune kun no revenge Hindi⚜️": "https://t.me/masamune_kuns_revenge_hindi_01"
        }
    )

    # masamune kun no revenge (other worda)
    add_filter(
        "masamune",
        "Join our Masamune kun no revenge Hindi Official channel!",
        use_buttons=True,
        button_links={
            "⚜️Masamune kun no revenge Hindi⚜️": "https://t.me/masamune_kuns_revenge_hindi_01"
        }
    )

    # The Gorilla God’s Go-To Girl
    add_filter(
        "The Gorilla God’s Go-To Girl",
        "The Gorilla God’s Go-To Girl!",
        use_buttons=True,
        button_links={
            "The Gorilla God’s Go-To Girl": "https://t.me/+L_QlfKP7FWdiNTll"
        }
    )

    # The Gorilla God’s Go-To Girl
    add_filter(
        "The Gorilla God",
        "The Gorilla God’s Go-To Girl!",
        use_buttons=True,
        button_links={
            "The Gorilla God’s Go-To Girl": "https://t.me/+L_QlfKP7FWdiNTll"
        }
    )

    #Lookism
    add_filter(
        "Lookism",
        "Join our Lookism Hindi channel!",
        use_buttons=True,
        button_links={
            "⚜️Lookism Hindi⚜️": "https://t.me/lookismhindidubofficial"
        }
    )

    #Spy X Family
    add_filter(
        "Spy x family",
        "Join our Spy X Family Hindi channel!",
        use_buttons=True,
        button_links={
            "⚜️Spy X Family Hindi⚜️": "https://t.me/+VdKezSBeWlhiOTZl"
        }
    )

    #Spy X Family (other worda)
    add_filter(
        "Spy",
        "Join our Spy X Family Hindi channel!",
        use_buttons=True,
        button_links={
            "⚜️Spy X Family Hindi⚜️": "https://t.me/+VdKezSBeWlhiOTZl"
        }
    )

    #Spy X Family (other words)
    add_filter(
        "family",
        "Join our Spy X Family Hindi channel!",
        use_buttons=True,
        button_links={
            "⚜️Spy X Family Hindi⚜️": "https://t.me/+VdKezSBeWlhiOTZl"
        }
    )

     #naruto
    add_filter(
        "naruto",
        "Join our Naruto Hindi channel!\n⚜️Naruto Classic Hindi⚜️\n⚜️Naruto Classic English⚜️",
        use_buttons=True,
        button_links={
            "⚜️Naruto Classic Hindi⚜️": "https://t.me/goan_anime_boy",
            "⚜️Naruto Classic English⚜️": "https://t.me/+jQFbVIW0JksyM2Y1"
        }
    )

    # Attack on Titan
    add_filter(
        "attack on titan",
        "Join our Attack On Titan Hindi Official channel!",
        use_buttons=True,
        button_links={
            "⚜️Attack On Titan Hindi⚜️": "https://t.me/+rIKUUyTYlo8wNGM1"
        }
    )

    # Banished From Hero's Party
    add_filter(
        "banished from the hero's party",
        "Join our Banished From The Hero's Party channel!",
        use_buttons=True,
        button_links={
            "Join our Banished From The Hero's Party channel!": "https://t.me/+9r-mcECjMkU4M2M1"
        }
    )

    # Berserk of Gluttony
    add_filter(
        "berserk of gluttony",
        "Join our Berserk of Gluttony channel!",
        use_buttons=True,
        button_links={
            "Join our Berserk of Gluttony channel!": "https://t.me/+6PovWxfhmr80MGRl"
        }
    )

    add_filter(
        "berserk",
        "Join our Berserk channel!",
        use_buttons=True,
        button_links={
            "Join our Berserk channel!": "https://t.me/+6PovWxfhmr80MGRl"
        }
    )

    # Black Clover
    add_filter(
        "black clover",
        "Join our Black Clover channel!\n⚜️Black Clover Hindi⚜️\n⚜️Black Clover English⚜️",
        use_buttons=True,
        button_links={
            "⚜️Black Clover Hindi⚜️": "https://t.me/+ebqfkhHMwKZhZjY1",
            "⚜️Black Clover English⚜️": "https://t.me/+PQTUS0aP67czMzA1"
        }
    )

    #Boruto
    add_filter(
        "boruto",
        "Join our Lookism Hindi channel!",
        use_buttons=True,
        button_links={
            "⚜️Boruto English⚜️": "https://t.me/+72_6hOFG9_s4MWJl"
        }
    )

    # Black Summoner
    add_filter(
        "black summoner",
        "Join our Black Summoner channel!",
        use_buttons=True,
        button_links={
            "⚜️Black Summoner⚜️": "https://t.me/+Dxi8FhL7OWM0YzQ1"
        }
    )

    # Bleach
    add_filter(
        "bleach",
        "Join our Bleach channel!",
        use_buttons=True,
        button_links={
            "Join our Bleach channel!": "https://t.me/+cbkoLK1BMXllODg1"
        }
    )

    # Blue Lock
    add_filter(
        "blue lock",
        "Join our Blue Lock channel!",
        use_buttons=True,
        button_links={
            "Join our Blue Lock channel!": "https://t.me/+mlb_OIhPtj40ODc9"
        }
    )

    # Bye Bye Earth
    add_filter(
        "bye bye earth",
        "Join our Bye Bye Earth channel!",
        use_buttons=True,
        button_links={
            "Join our Bye Bye Earth channel!": "https://t.me/+Dxi8FhL7OWM0YzQ1"
        }
    )

    # Castlevania Nocturne
    add_filter(
        "castlevania nocturne",
        "Join our Castlevania Nocturne channel!",
        use_buttons=True,
        button_links={
            "Join our Castlevania Nocturne channel!": "https://t.me/+jxms8T753JgzNzRl"
        }
    )

    # Code Geass
    add_filter(
        "code geass",
        "Join our Code Geass channel!",
        use_buttons=True,
        button_links={
            "Join our Code Geass channel!": "https://t.me/+kVBhy_IRNVBjZjRl"
        }
    )

    # Dandadan
    add_filter(
        "dandadan",
        "Join our Dandadan channel!",
        use_buttons=True,
        button_links={
            "Join our Dandadan channel!": "https://t.me/+ilLS_2IHOsplZTll"
        }
    )

    # Days With My Stepsister
    add_filter(
        "days with my stepsister",
        "Join our Days With My Stepsister channel!",
        use_buttons=True,
        button_links={
            "Join our Days With My Stepsister channel!": "https://t.me/+uzmJv4FcKXI2MWQ1"
        }
    )

    # Death Note
    add_filter(
        "Death Note",
        "Join our Death Note!",
        use_buttons=True,
        button_links={
            "Join our Death Note!": "https://t.me/+yk39P6z_ejE3NWY1"
        }
    )

    # Demon Slayer
    add_filter(
        "Demon Slayer",
        "Join our Demon Slayer!",
        use_buttons=True,
        button_links={
            "Join our Demon Slayer!": "https://t.me/demon_slayer_by_itachi"
        }
    )

    # Dr. Stone (with alternative name)
    add_filter(
        "dr. stone",
        "Join our Dr. Stone channel!",
        use_buttons=True,
        button_links={
            "Join our Dr. Stone channel!": "https://t.me/+to7vXXj2seJkNzA1"
        }
    )

    add_filter(
        "dr stone",
        "Join our Dr. Stone channel!",
        use_buttons=True,
        button_links={
            "Join our Dr. Stone channel!": "https://t.me/+to7vXXj2seJkNzA1"
        }
    )

    # Dragon Ball (with alternative name)
    add_filter(
        "dragon ball",
        "Join our Dragon Ball Diama channel!",
        use_buttons=True,
        button_links={
            "Join our Dragon Ball Diama channel!": "https://t.me/+1gh_jaECTH0zMGZl"
        }
    )

    add_filter(
        "dragon ball diama",
        "Join our Dragon Ball Diama channel!",
        use_buttons=True,
        button_links={
            "Join our Dragon Ball Diama channel!": "https://t.me/+1gh_jaECTH0zMGZl"
        }
    )

    # devil may cry
    add_filter(
        "Devil may cry",
        "Join our Devil may cry!",
        use_buttons=True,
        button_links={
            "Join Devil may cry channel!": "https://t.me/+1hsuaPkU0R4xNzll"
        }
    )

    # Fairy Tail
    add_filter(
        "fairy tail",
        "Join our Fairy Tail channel!",
        use_buttons=True,
        button_links={
            "Join our Fairy Tail channel!": "https://t.me/+PQuJwoIu5FtjZDBl"
        }
    )

    # Haikyuu
    add_filter(
        "haikyuu",
        "Join our Haikyuu channels!\n⚜️Haikyuu Hindi⚜️\n⚜️Haikyuu English⚜️",
        use_buttons=True,
        button_links={
            "⚜️Haikyuu Hindi⚜️": "https://t.me/+R71oa-rUAfpkMTc1",
            "⚜️Haikyuu English⚜️": "https://t.me/+j0vfD_JJ5ZhjOGQ9"
        }
    )

    # Hell's Paradise
    add_filter(
        "Hell's Paradise",
        "Join our Hell's Paradise channel!",
        use_buttons=True,
        button_links={
            "Join our Hell's Paradise channel!": "https://t.me/+ZFrN0l7LWxZiZjI1"
        }
    )


    # Hunter X Hunter (with alternative name)
    add_filter(
        "hunter x hunter",
        "Join our Hunter X Hunter channel!",
        use_buttons=True,
        button_links={
            "Join our Hunter X Hunter channel!": "https://t.me/+zYqe7HbwomNhN2Jl"
        }
    )

    add_filter(
        "hunter hunter",
        "Join our Hunter X Hunter channel!",
        use_buttons=True,
        button_links={
            "Join our Hunter X Hunter channel!": "https://t.me/+zYqe7HbwomNhN2Jl"
        }
    )

    # i parry everything
    add_filter(
        "i parry everything",
        "Join our i parry everything!",
        use_buttons=True,
        button_links={
            "Join our i parry everything": "https://t.me/+3TLW2IsnkoUxZjRl"
        }
    )

    # I'M Getting Married to a Girl I hate (with multiple alternative names)
    add_filter(
        "i'm getting married to a girl i hate in my class",
        "Join our I'M Getting Married to a Girl I hate in my class Hindi Official channel!",
        use_buttons=True,
        button_links={
            "⚜️I'M Getting Married to a Girl I hate in my class⚜️": "https://t.me/+bEGR9J6aAFthZDU1"
        }
    )

    add_filter(
        "married",
        "Join our I'M Getting Married to a Girl I hate in my class Hindi Official channel!",
        use_buttons=True,
        button_links={
            "⚜️I'M Getting Married to a Girl I hate in my class⚜️": "https://t.me/+bEGR9J6aAFthZDU1"
        }
    )

    add_filter(
        "girl i hate",
        "Join our I'M Getting Married to a Girl I hate in my class Hindi Official channel!",
        use_buttons=True,
        button_links={
            "⚜️I'M Getting Married to a Girl I hate in my class⚜️": "https://t.me/+bEGR9J6aAFthZDU1"
        }
    )

# JoJo's Bizarre Adventure
    add_filter(
        "JoJo's Bizarre Adventure",
        "Join our JoJo's Bizarre Adventure!",
        use_buttons=True,
        button_links={
            "Join our JoJo's Bizarre Adventure!": "https://t.me/+CDIm-d1NgzoxYzE1"
        }
    )

    # Iceblade Sorcerer (with alternative name)
    add_filter(
        "the iceblade sorcerer",
        "Join our The Iceblade Sorcerer Shall Rule the World channel!",
        use_buttons=True,
        button_links={
            "Join our The Iceblade Sorcerer Shall Rule the World channel!": "https://t.me/+vdcSA2aiEsw1ZmM9"
        }
    )

    add_filter(
        "iceblade sorcerer",
        "Join our The Iceblade Sorcerer Shall Rule the World channel!",
        use_buttons=True,
        button_links={
            "Join our The Iceblade Sorcerer Shall Rule the World channel!": "https://t.me/+vdcSA2aiEsw1ZmM9"
        }
    )

    # Kaiju No. 8 (with alternative spelling)
    add_filter(
        "kaiju no 8",
        "Join our Kaiju No. 8 channel!",
        use_buttons=True,
        button_links={
            "Join our Kaiju No. 8 channel!": "https://t.me/+xSWUiodOBN0zYTE1"
        }
    )

    add_filter(
        "kaiju no. 8",
        "Join our Kaiju No. 8 channel!",
        use_buttons=True,
        button_links={
            "Join our Kaiju No. 8 channel!": "https://t.me/+xSWUiodOBN0zYTE1"
        }
    )

    # Lookism
    add_filter(
        "Lookism",
        "Lookism!",
        use_buttons=True,
        button_links={
            "Join our Lookism!": "https://t.me/lookismhindidubofficial"
        }
    )

    # Makeine
    add_filter(
        "makeine",
        "Join our Makeine: Too Many Losing Heroines channel!",
        use_buttons=True,
        button_links={
            "Join our Makeine: Too Many Losing Heroines channel!": "https://t.me/+kpkv8_eHksE4NTA1"
        }
    )

# My Hero Academia
    add_filter(
        "My Hero Academia",
        "Join our My Hero Academia!",
        use_buttons=True,
        button_links={
            "Join our My Hero Academia!": "https://t.me/+XvXvc1zUBYY2ZmU1"
        }
    )
    # My Dress Up Darling
    add_filter(
        "My Dress Up Darling",
        "Join our My Dress Up Darling!",
        use_buttons=True,
        button_links={
            "Join our My Dress Up Darling!": "https://t.me/+tUqeksNR6jRkOWI1"
        }
    )

    # Mushoku Tensei
    add_filter(
        "mushoku tensei",
        "Join our Mushoku Tensei Jobless Reincarnation channel!",
        use_buttons=True,
        button_links={
            "Join our Mushoku Tensei Jobless Reincarnation channel!": "https://t.me/+kuLg8hDnGjxkYTFl"
        }
    )

    # Naruto Shippuden
    add_filter(
        "naruto shippuden",
        "Naruto Shippuden Hindi Official Channel",
        use_buttons=True,
        button_links={
            "Join Naruto Shippuden Hindi Official Channel": "https://t.me/naruto_shippuden_hindi_by_itachi"
        }
    )

    # Nobody Remember Me (with alternative name)
    add_filter(
        "why does nobody remember me in this world",
        "Join our Why Does Nobody Remember Me in This World channel!",
        use_buttons=True,
        button_links={
            "Join our Why Does Nobody Remember Me in This World channel!": "https://t.me/+fQZWeXpsm5wxODJl"
        }
    )

    add_filter(
        "nobody remember me",
        "Join our Why Does Nobody Remember Me in This World channel!",
        use_buttons=True,
        button_links={
            "Join our Why Does Nobody Remember Me in This World channel!": "https://t.me/+fQZWeXpsm5wxODJl"
        }
    )

    # One Piece
    add_filter(
        "one piece",
        "Join our One Piece channel!",
        use_buttons=True,
        button_links={
            "Join our One Piece channel!": "https://t.me/+lSCWH3o7N181MWU1"
        }
    )

    #pfp comples
    add_filter(
        "pfp",
        "Join our pfp channel!",
        use_buttons=True,
        button_links={
            "Join our pfp channel!": "https://t.me/+DY5UnChCRiE3MDNl"
        }
    )

    # Record of Ragnarok
    add_filter(
        "record of ragnarok",
        "Join our Record of Ragnarok channel!",
        use_buttons=True,
        button_links={
            "Join our Record of Ragnarok channel!": "https://t.me/+lrHocYkUDRA1ZmQ9"
        }
    )

    # Reincarnated Aristocrat
    add_filter(
        "reincarnated aristocrat",
        "Join our As a Reincarnated Aristocrat, I'll Use My Appraisal Skill to Rise in the World channel!",
        use_buttons=True,
        button_links={
            "Join our Reincarnated Aristocrat channel!": "https://t.me/+_xR_UDiTR-hkNjNl"
        }
    )

    # Reincarnated as a Slime (with alternative name)
    add_filter(
        "that time i got reincarnated as a slime",
        "Join our That Time I Got Reincarnated as a Slime channel!",
        use_buttons=True,
        button_links={
            "Join our That Time I Got Reincarnated as a Slime channel!": "https://t.me/+ktyGhQqUEbA2MzY1"
        }
    )

    add_filter(
        "reincarnated as a slime",
        "Join our That Time I Got Reincarnated as a Slime channel!",
        use_buttons=True,
        button_links={
            "Join our That Time I Got Reincarnated as a Slime channel!": "https://t.me/+ktyGhQqUEbA2MzY1"
        }
    )

    # Red Ranger (with alternative name)
    add_filter(
        "the red ranger",
        "Join our The Red Ranger Becomes an Adventurer in Another World channel!",
        use_buttons=True,
        button_links={
            "Join our The Red Ranger Becomes an Adventurer in Another World channel!": "https://t.me/+vLnY2TPESNpjYjU1"
        }
    )

    add_filter(
        "red ranger",
        "Join our The Red Ranger Becomes an Adventurer in Another World channel!",
        use_buttons=True,
        button_links={
            "Join our The Red Ranger Becomes an Adventurer in Another World channel!": "https://t.me/+vLnY2TPESNpjYjU1"
        }
    )

    # Solo Leveling (with alternative names)
    add_filter(
        "solo leveling",
        "Join our Solo Leveling channel!\n⚜️Solo Leveling Hindi⚜️\n⚜️Solo Leveling Englsih sub⚜️",
        use_buttons=True,
        button_links={
            "⚜️Solo Leveling Hindi⚜️": "https://t.me/+hrOLw2weDKY2YzE1",
            "⚜️Solo Leveling English sub⚜️": "https://t.me/Solo_leveling_english_sub_itachi"
        }
    )

    add_filter(
        "solo",
        "Join our Solo Leveling channel!!\n⚜️Solo Leveling Hindi⚜️\n⚜️Solo Leveling Englsih sub⚜️",
        use_buttons=True,
        button_links={
            "⚜️Solo Leveling Hindi⚜️": "https://t.me/+hrOLw2weDKY2YzE1",
            "⚜️Solo Leveling English sub⚜️": "https://t.me/Solo_leveling_english_sub_itachi"
        }
    )

    add_filter(
        "sung jinwoo",  # Main character's name
        "Join our Solo Leveling channel!!\n⚜️Solo Leveling Hindi⚜️\n⚜️Solo Leveling English sub⚜️",
        use_buttons=True,
        button_links={
            "⚜️Solo Leveling Hindi⚜️": "https://t.me/+hrOLw2weDKY2YzE1",
            "⚜️Solo Leveling English sub⚜️": "https://t.me/Solo_leveling_english_sub_itachi"
        }
    )

    # sakamoto days
    add_filter(
        "sakamoto days",
        "Join our sakamoto days!",
        use_buttons=True,
        button_links={
            "Join our sakamoto days!": "https://t.me/+pzbmkUAsJ3NkYzdl"
        }
    )

    # sakamoto days
    add_filter(
        "horimiya",
        "Join our horimiya!",
        use_buttons=True,
        button_links={
            "⚜️Horimiya⚜️": "https://t.me/+eGAtcRyUyIhmNTY1"
        }
    )

    # Strongest Magician (with alternative name)
    add_filter(
        "the strongest magician in the demon lord's army",
        "Join our The Strongest Magician in the Demon Lord's Army Was a Human channel!",
        use_buttons=True,
        button_links={
            "Join our The Strongest Magician in the Demon Lord's Army Was a Human channel!": "https://t.me/+3XsNQbIQn7ViN2Nl"
        }
    )

    add_filter(
        "strongest magician",
        "Join our The Strongest Magician in the Demon Lord's Army Was a Human channel!",
        use_buttons=True,
        button_links={
            "Join our The Strongest Magician in the Demon Lord's Army Was a Human channel!": "https://t.me/+3XsNQbIQn7ViN2Nl"
        }
    )

    # The Angel Next Door
    add_filter(
        "the angel next door",
        "Join The Angel Next Door Spoils Me Rotten channel!",
        use_buttons=True,
        button_links={
            "Join The Angel Next Door Spoils Me Rotten channel!": "https://t.me/+MY2RlYAOSJ41NmJl"
        }
    )

    # The Exclusive Samurai
    add_filter(
        "the exclusive samurai",
        "Join our The Exclusive Samurai channel!",
        use_buttons=True,
        button_links={
            "Join our The Exclusive Samurai channel!": "https://t.me/+cOWAompwXTc3ZGU1"
        }
    )

    # Tokyo 24th Ward
    add_filter(
        "tokyo 24th ward",
        "Join our Tokyo 24th Ward Hindi Official channel!",
        use_buttons=True,
        button_links={
            "Join our Tokyo 24th Ward Hindi Official channel!": "https://t.me/+ShzCsWRvCvcwMjFl"
        }
    )

    # Tokyo Revengers
    add_filter(
        "tokyo revengers",
        "Join our Tokyo Revengers channel!",
        use_buttons=True,
        button_links={
            "Join our Tokyo Revengers channel!": "https://t.me/+DlAvoUkq-fc1NjZl"
        }
    )

    # Tomb Raider
    add_filter(
        "tomb raider",
        "Join our Tomb Raider channel!",
        use_buttons=True,
        button_links={
            "Join our Tomb Raider channel!": "https://t.me/+8Uk6uI1ALpU5ZWJl"
        }
    )

    # Tower of God
    add_filter(
        "tower of god",
        "Join our Tower of God channel!",
        use_buttons=True,
        button_links={
            "Join our Tower of God channel!": "https://t.me/+L8xLBF_ld7BlZTM1"
        }
    )

    # Trillion Game
    add_filter(
        "trillion game",
        "Join our Trillion Game channel!",
        use_buttons=True,
        button_links={
            "Join our Trillion Game channel!": "https://t.me/+0BhCMko4oGg0ZmFl"
        }
    )

    # True Beauty
    add_filter(
        "true beauty",
        "Join our True Beauty channel!",
        use_buttons=True,
        button_links={
            "Join our True Beauty channel!": "https://t.me/+8RT0IpMY7p5mOWE1"
        }
    )

    # Vinland Saga
    add_filter(
        "vinland saga",
        "Join our Vinland Saga channel!",
        use_buttons=True,
        button_links={
            "Join our Vinland Saga channel!": "https://t.me/+tXDuwMgFK-RmOGFl"
        }
    )

    # wind breaker

    add_filter(
        "wind breaker",
        "Join our wind breaker channel!",
        use_buttons=True,
        button_links={
            "Join our wind breaker channel!": "https://t.me/+CJBqVPIb7sdhNWJl"
        }
    )

    # Wolf King
    add_filter(
        "wolf king",
        "Join our Wolf King channel!",
        use_buttons=True,
        button_links={
            "Join our Wolf King channel!": "https://t.me/+LSkILVJlHh0zZDdl"
        }
    )

#classroom of the elite
    add_filter(
        "classroom of the elite",
        "classroom of the elite",
        use_buttons=True,
        button_links={
            "⚜️classroom of the elite⚜️": "https://t.me/+k6-pC-WerIpjYTM9"
        }
    )

    add_filter(
        "classroom",
        "classroom of the elite",
        use_buttons=True,
        button_links={
            "⚜️classroom of the elite⚜️": "https://t.me/+k6-pC-WerIpjYTM9"
        }
    )

# Kaguya-sama: Love Is War
    add_filter(
        "Kaguya-sama: Love Is War",
        "Kaguya-sama: Love Is War",
        use_buttons=True,
        button_links={
            "⚜️Kaguya-sama: Love Is War⚜️": "https://t.me/+sKiOZDL1aGo1YjA1"
        }
    )

    add_filter(
        "Love Is War",
        "Kaguya-sama: Love Is War",
        use_buttons=True,
        button_links={
            "⚜️Kaguya-sama: Love Is War⚜️": "https://t.me/+sKiOZDL1aGo1YjA1"
        }
    )

    add_filter(
        "Kaguya sama",
        "Kaguya-sama: Love Is War",
        use_buttons=True,
        button_links={
            "⚜️Kaguya-sama: Love Is War⚜️": "https://t.me/+sKiOZDL1aGo1YjA1"
        }
    )

# mob psycho 100
    add_filter(
        "mob psycho 100",
        "mob psycho 100",
        use_buttons=True,
        button_links={
            "⚜️mob psycho 100⚜️": "https://t.me/+_h43S2hlfO1jMjQ9"
        }
    )

    add_filter(
        "mob psycho",
        "mob psycho 100",
        use_buttons=True,
        button_links={
            "⚜️mob psycho 100⚜️": "https://t.me/+_h43S2hlfO1jMjQ9"
        }
    )

    add_filter(
        "mob",
        "mob psycho 100",
        use_buttons=True,
        button_links={
            "⚜️mob psycho 100⚜️": "https://t.me/+_h43S2hlfO1jMjQ9"
        }
    )

    # anime movies filters start here

    # howls moving castle
    add_filter(
        "Howls Moving Castle",
        "Join our Howls Moving Castle",
        use_buttons=True,
        button_links={
            "Join our Howls Moving Castle!": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/67"
        }
    )

    # grave of thr fireflies
    add_filter(
        "grave of thr fireflies",
        "Join our grave of thr fireflies",
        use_buttons=True,
        button_links={
           "Join our grave of thr fireflies!": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/72"
        }
    )

    # I want to eat your pancreas
    add_filter(
        "I want to eat your pancreas",
        "Join our I want to eat your pancreas",
        use_buttons=True,
        button_links={
            "Join our I want to eat your pancreas!": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/27"
        }
    )

    # Princess Mononoke
    add_filter(
        "Princess Mononoke",
        "Join our Princess Mononoke",
        use_buttons=True,
        button_links={
            "Join our Princess Mononoke!": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/70"
        }
    )

    # Your name
    add_filter(
        "your Name",
        "Join our your name",
        use_buttons=True,
        button_links={
            "Join our your name!": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/3"
        }
    )

    # Chhota bheem all movies
    add_filter(
        "chhota bheem",
        "watch chhota bheem movies\nwatch: chhota bheem master of sholin\nwatch: chhota bheem and the shinobi secret\nwatch: chhota bheem and the rise of kirmada",
        use_buttons=True,
        button_links={
            "watch: chhota bheem master of sholin": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/4",
            "watch: chhota bheem and the shinobi secret": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/5",
            "watch: chhota bheem and the rise of kirmada": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/6"
        }
    )

# suzume
    add_filter(
        "suzume",
        "watch suzume no tojimari",
        use_buttons=True,
        button_links={
            "watch suzume no tojimari": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/7"
        }
    )

# weathering with you
    add_filter(
        "weathering with you",
        "watch weathering with you",
        use_buttons=True,
        button_links={
            "⚜️weathering with you⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/9"
        }
    )

    add_filter(
        "weathering",
        "watch weathering with you",
        use_buttons=True,
        button_links={
            "⚜️weathering with you⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/9"
        }
    )

# spirited away
    add_filter(
        "spirited away",
        "watch spirited away",
        use_buttons=True,
        button_links={
            "⚜️spirited away⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/10"
        }
    )

# bubble
    add_filter(
        "bubble",
        "watch bubble",
        use_buttons=True,
        button_links={
            "⚜️bubble⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/13"
        }
    )

# my neighbor totoro
    add_filter(
        "my neighbor totoro",
        "watch my neighbor totoro",
        use_buttons=True,
        button_links={
            "⚜️my neighbor totoro⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/15"
        }
    )

    add_filter(
        "totoro",
        "watch my neighbor totoro",
        use_buttons=True,
        button_links={
            "⚜️my neighbor totoro⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/15"
        }
    )

# over the sky
    add_filter(
        "over the sky",
        "watch over the sky",
        use_buttons=True,
        button_links={
            "⚜️over the sky⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/17"
        }
    )

# a silent voice
    add_filter(
        "a silent voice",
        "watch a silent voice",
        use_buttons=True,
        button_links={
            "⚜️a silent voice⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/20"
        }
    )

    add_filter(
        "silent",
        "watch a silent voice",
        use_buttons=True,
        button_links={ "⚜️a silent voice⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/20"
        }
    )

# 5 cm per second
    add_filter(
        "5 cm per second",
        "watch 5 cm per second",
        use_buttons=True,
        button_links={ "⚜️5 cm per second⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/24"
        }
    )

    add_filter(
        "per second",
        "watch 5 cm per second",
        use_buttons=True,
        button_links={ "⚜️5 cm per second⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/24"
        }
    )
#hello world
    add_filter(
        "hello world",
        "watch hello world",
        use_buttons=True,
        button_links={ "⚜️hello world⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/25"
        }
    )

#i want to eat your pancreas
    add_filter(
        "i want to eat your pancreas",
        "watch i want to eat your pancreas",
        use_buttons=True,
        button_links={ "⚜️i want to eat your pancreas⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/27"
        }
    )

    add_filter(
        "pancreas",
        "watch i want to eat your pancreas",
        use_buttons=True,
        button_links={ "⚜️i want to eat your pancreas⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/27"
        }
    )

    add_filter(
        "i want to eat",
        "watch i want to eat your pancreas",
        use_buttons=True,
        button_links={ "⚜️i want to eat your pancreas⚜️": "https://t.me/ANIMEMOVIEHINDIDUBHINDISUB/27"
        }
    )

if __name__ == '__main__':
    # Check for existing instances
    try:
        import sys
        import psutil
        
        current_process = psutil.Process()
        # Check if any other python process is running this script
        for process in psutil.process_iter():
            if process.pid != current_process.pid:
                try:
                    if process.name().lower() == "python.exe" and any("bot.py" in cmd.lower() for cmd in process.cmdline()):
                        print("Another instance of the bot is already running. Exiting...")
                        sys.exit(1)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
    except ImportError:
        # If psutil is not installed, skip the check
        pass
    
    
    # Run the bot
    asyncio.run(main())
 
