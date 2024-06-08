import discord
from discord.ext import commands
import requests
from datetime import datetime
import credits

# Настройки
token = credits.bot_token

language = 'en'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

rep_question = None
repeat = False

corr_article = 0

last_art = 5

@bot.command(name="start")
async def start(ctx):
    await ctx.send("Добро пожаловать! Я вам подберу свежие новости. Для этого напишите команду !news {ВОПРОС} {YYYY-MM-DD} {YYYY-MM-DD}")

@bot.command(name="news")
async def news(ctx, question: str, date: str = None, snd_date = None):
    global last_art, rep_question, repeat
    # Если дата не указана, используем сегодня
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    if snd_date is None:
        link = f"https://newsapi.org/v2/everything?q={question}&from={date}&sortBy=publishedAt&language={language}&apiKey={credits.api}"
    else:
        link = f"https://newsapi.org/v2/everything?q={question}&from={date}&to={snd_date}&sortBy=publishedAt&language={language}&apiKey={credits.api}"
    if rep_question == question:
        repeat = True
        last_art += 5
    else:
        repeat = False
        last_art = 5
    response = requests.get(link)
    result = response.json()

    if result['status'] == "ok":
        articles = result['articles']
        if articles:
            if not repeat:
                for article in articles[:last_art]:  # Показываем первые 5 новостей
                    title = article.get('title', 'No Title')
                    description = article.get('description', 'No Description')
                    url = article.get('url', 'No URL')
                    await ctx.send(f"**{title}**\n{description}\nRead more: {url}\n")
                rep_question = question
            else:
                for article in articles[last_art-4:last_art+1]:  # Показываем первые 5 новостей
                    title = article.get('title', 'No Title')
                    description = article.get('description', 'No Description')
                    url = article.get('url', 'No URL')
                    await ctx.send(f"**{title}**\n{description}\nRead more: {url}\n")
        else:
            await ctx.send("По вашему запросу новостей не найдено.")
    else:
        await ctx.send(result['message'])



@bot.command(name="set_language")
async def set_language(ctx, sellected_language):
    global language
    language = sellected_language
    await ctx.send(f"Язык успешно сохранен на {sellected_language}")

@bot.command(name="commands")
async def commands(ctx):
    await ctx.send(
        "!news <вопрос> <первая дата> <конечная дата> - просмотр новостей\n" + 
        "!set_language <язык> - смена языка\n" +
        "При повторном запросе, вы получите следующие 5 статьей"
                   )

bot.run(token)