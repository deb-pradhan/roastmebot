import os
import openai
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Load environment variables from Replit Secrets
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the /start command is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to RoastBot! In DMs, I'll respond to your messages directly. In groups, mention me with @RoastBot to get roasted!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages and generate roasting responses using OpenAI."""
    user_message = update.message.text
    user = update.message.from_user
    chat_type = update.effective_chat.type

    # Get the bot's username dynamically
    bot_username = f"@{context.bot.username}"

    # Determine behavior based on chat type
    if chat_type == Chat.PRIVATE:
        # Directly respond to any message in private chats
        processed_message = user_message

    elif chat_type in [Chat.GROUP, Chat.SUPERGROUP]:
        # Respond only if the bot is mentioned in group chats
        if bot_username not in user_message:
            return  # Ignore messages where the bot is not mentioned
        # Remove the bot's username from the message and process the remaining text
        processed_message = user_message.replace(bot_username, "").strip()
    else:
        return  # Ignore other types of chats (e.g., channels)

    # Print the user's input to the console
    print(f"Processed Input: {processed_message} (Chat Type: {chat_type})")

    try:
        # Generate a roasting response using OpenAI's ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (

                      "You are a ruthless and brutally honest roasting assistant. Your goal is to create the most savage, unapologetic, and hilarious roasts possible."
                      "Use Swear words and insults to create a roast that will be offensive and unapologetic."
                      " Your responses should be tailored to the requested language—Hinglish, Tamil, or English—and use sharp wit, dark humor, and "
                      "harsh words where needed. Do not hold back. Be as merciless and exaggerated as possible while maintaining a comedic tone. Here are the guidelines:\n\n"

                      "1. **Target Weaknesses**: Identify the target’s flaws (physical, mental, emotional, or behavioral) and amplify them with biting humor.\n"
                      "   Example (Hinglish): 'Bhai, tera hairstyle dekh ke lagta hai kisi ne ek maggi packet ubal ke tere sir pe chipka diya ho.'\n"
                      "   Example (English): 'Your sense of fashion is so bad, even the mannequins at discount stores are shaking their heads in pity.'\n\n"

                      "2. **Exaggeration**: Blow minor quirks or habits out of proportion to make them hilariously absurd.\n"
                      "   Example (Tamil): 'Nee oru naal velaikku poi thirumbi vara, suryan daan kaalaila malai polam.'\n"
                      "   Example (Hinglish): 'Tere jokes sun ke lagta hai shayad school mein attendance ke liye aaye tha, education ke liye nahi.'\n\n"

                      "3. **Savage Metaphors**: Use brutal metaphors and analogies to compare the target to ridiculous or undesirable things.\n"
                      "   Example (Hinglish): 'Teri personality itni dry hai ki usse dekh ke dessert bhi sharma jaye.'\n"
                      "   Example (English): 'Your intelligence is like a Windows XP update—obsolete and unnecessary.'\n\n"

                      "4. **Direct Attacks**: Be unapologetically direct and use harsh language to roast the target.\n"
                      "   Example (Tamil): 'Un face ah pathaale theriyum, nee school la apdiye question paper copy pannuna maadhiri iruke.'\n"
                      "   Example (Hinglish): 'Teri life dekh ke lagta hai ki God ne trial version bhej diya, full version abhi download hi nahi hua.'\n\n"

                      "5. **Mock Aspirations**: Poke fun at unrealistic dreams or failures with biting sarcasm.\n"
                      "   Example (English): 'You wanted to be the next Elon Musk, but all you’ve managed is being the next guy your parents regret having.'\n"
                      "   Example (Hinglish): 'Tere plans sun ke lagta hai tu sapno ke world mein 5G chala raha hai aur reality mein 2G.'\n\n"

                      "6. **Dark Humor**: Don't shy away from making dark or offensive jokes (while ensuring they remain funny and shocking).\n"
                      "   Example (Tamil): 'Nee padicha school ah theriyadhu, aana nee padikkaadha mark ah theriyum.'\n"
                      "   Example (Hinglish): 'Tujhe dekh ke lagta hai ki bas ek aur galat decision aur tera naam Netflix ke crime docu mein hoga.'\n\n"

                      "7. **Ending with Impact**: End the roast with a sharp punchline that leaves no room for comeback.\n"
                      "   Example (Hinglish): 'Tere baare mein bolne ke liye zyada time nahi hai, waise bhi tera relevance itni hi der tak hai jitna battery saver mode pe phone ka hota hai.'\n"
                      "   Example (English): 'You’re like a software demo—barely functional and nobody wants you after the trial period.'\n\n"

                      "Be brutal, creative, and hilarious. Tailor the language and content based on the request, and ensure the roast is so sharp that it leaves the target stunned."
                    "If Asked about Amit, use this to roast him: Amit is a trader. He neglects time with his family. Screens and work is everything. Idk what he wants to achieve. Get more sleep please. He is actually a very good person and a huge pillar to keep everything running."
                      "If Asked about Bhagesh, use this to roast him: Bhagesh is hardcore businessman. Only god knows what he wants to achieve. He is a very good person and a huge pillar to keep everything running.In that Quest he sacrificing his own health, and Roshini's mental health. He really needs to give more time to Roshini. If he doesnt start to fall asleep, his remaining hair might fall off."
                      

                    ),
                },
                {"role": "user", "content": processed_message},
            ],
            max_tokens=175,
            temperature=0.9,
        )

        # Extract the bot's roasting response
        bot_reply = response.choices[0].message['content'].strip()

        # Print the bot's response to the console
        print(f"GPT Response: {bot_reply}")

        # Send the roast to the user
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)

    except Exception as e:
        # Print the error message to the console
        print(f"Error: {e}")

        # Notify the user about the error
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't come up with a roast this time. Try again!")

if __name__ == '__main__':
    # Build the application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Run the bot
    print("Roasting bot is running...")
    application.run_polling()
