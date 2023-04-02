import os
import requests
import json
import discord
import datetime as dt
from discord.ext import commands


intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

def getDateTimeString(time):
    d_t = dt.datetime.fromtimestamp(time)
    return d_t.strftime('%Y-%m-%d %H:%M:%S')

def playtime(time):
    d_t = dt.datetime.fromtimestamp(time)
    return d_t.strftime('%H:%M:%S')

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Ready!")

@client.slash_command(name='player', description='Введите никнейм игрока, "паспорт" которого вы хотите увидеть.')
async def _player(ctx, *, nickname):
    ins = 'Да'
    await ctx.delete()
    if nickname is None:
        await ctx.send(embed = discord.Embed(
                title = ":warning: **ВНИМАНИЕ!!!** :warning:",
                description = f"{ctx.author.mention}, вы не указали пользователя."
            ))
    else:
        resp = requests.get("https://api.reworlds.net/player/" + nickname)
        if resp.status_code == 404:
            await ctx.send(embed = discord.Embed(
                title = ":warning: **ВНИМАНИЕ!!!** :warning:",
                description = f"{ctx.author.mention}, ошибка, вы указали неверный/несуществующий никнейм."
            ))
        else:
            if resp.status_code == 200:
                data = resp.json()
                if data['online'] == True:
                    ins = 'Да'
                    await ctx.send(embed = discord.Embed(
                        title = f"**{data['name']}**",
                        description = f"*ID игрока: {data['id']}\nDiscord-ID: <@{data['discord-id']}>\nИгровое время: {playtime(int(data['play-time'])/1000)}\nПервый вход: {getDateTimeString(int(data['first-seen'])/1000)}\nПоследний вход: {getDateTimeString(int(data['last-seen'])/1000)}\nОнлайн: {ins}*",
                        colour = 0x00FF00
                    ))
                else:
                    ins = 'Нет'
                    await ctx.send(embed = discord.Embed(
                        title = f"**{data['name']}**",
                        description = f"*ID игрока: {data['id']}\nDiscord-ID: <@{data['discord-id']}>\nИгровое время: {playtime(int(data['play-time'])/1000)}\nПервый вход: {getDateTimeString(int(data['first-seen'])/1000)}\nПоследний вход: {getDateTimeString(int(data['last-seen'])/1000)}\nОнлайн: {ins}*",
                        colour = 0xFF0000
                    ))

@client.slash_command(name='server', description='Информация о состоянии сервера.')
async def _server(ctx):
    await ctx.delete()
    resp = requests.get("https://api.reworlds.net/server")
    if resp.status_code == 200:
        data = resp.json()
        await ctx.send(embed = discord.Embed(
                title = f"**Revolution Worlds**",
                description = f"*Сервер сейчас работает.\nОнлайн: {data['online']}\nTPS: {round(data['tps'][0])}\nПервый игрок в табе: {data['players'][0]}*",
                colour = 0x00FF00
            ))

    else:
        if resp.status_code == 404:
            await ctx.send(embed = discord.Embed(
                title = ":warning: **ВНИМАНИЕ!!!** :warning:",
                description = f"{ctx.author.mention}, ошибка, попробуйте использовать команду позже.",
                colour = discord.Color.white
            ))
        if resp.status_code == 500:
            await ctx.send(embed = discord.Embed(
            title = ":warning: **ВНИМАНИЕ!!!** :warning:",
            description = f"{ctx.author.mention}, ошибка, внутренняя ошибка на сервере.",
            colour = discord.Color.white
        ))
        if resp.status_code == 503:
            await ctx.send(embed = discord.Embed(
            title = ":warning: **ВНИМАНИЕ!!!** :warning:",
            description = f"{ctx.author.mention}, ошибка, сервер не доступен.",
            colour = discord.Color.white
        ))
    


client.run(os.environ["DISCORD_TOKEN"])
