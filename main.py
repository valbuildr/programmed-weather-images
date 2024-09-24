import discord
from discord.ext import commands
import generate_weather_image
from datetime import datetime

api_key = open("./discord_token.txt", "r").read()

bot = commands.Bot(command_prefix="+", intents=discord.Intents(messages=True, message_content=True))

beta_testers = open("./beta_testers.txt", "r").read().split("\n")

bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.tree.command(name="4-by-3", description="Generates a 4:3 image with the current conditions at a location.")
@discord.app_commands.describe(location="Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude or city name.",
                               imperial="Use imperial measurements. (mph, miles, fahrenheit) Default: True")
async def make_4_3(interaction: discord.Interaction, location: str, imperial: bool = True):
    if interaction.user.id in beta_testers:
        try:
            f = await generate_weather_image.create_4_by_3(f"./generated_images/{interaction.user.id}_{int(datetime.now().timestamp())}.png", imperial, location)
        except Exception as err:
            e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
            e.description = f"```\n{err}\n```"
            await interaction.response.send_message(embed=e, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(file=f)
    else:
        await interaction.response.send_message(content="This bot is in a closed beta.", ephemeral=True)

@bot.command()
async def version(ctx: commands.Context):
    if ctx.author.id in beta_testers:
        f = open("./version.txt", "r").read
        await ctx.send(content=f)
    else:
        await ctx.send(content="This bot is in a closed beta.")

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context):
    await ctx.send(content="Syncing...")
    await bot.tree.sync()
    await ctx.send(content="Synced...")
    
bot.run(api_key)