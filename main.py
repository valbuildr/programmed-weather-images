import discord
from discord.ext import commands
import generate_weather_image
from datetime import datetime

api_key = open("./discord_token.txt", "r").read()

bot = commands.Bot(command_prefix="+", intents=discord.Intents(messages=True, message_content=True))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.tree.command(name="4-by-3", description="Generates a 4:3 image with the current conditions at a location.")
@discord.app_commands.describe(location="Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude or city name.",
                               imperial="Use imperial measurements. (mph, miles, fahrenheit) Default: True")
async def make_4_3(interaction: discord.Interaction, location: str, imperial: bool = True):
    try:
        f = await generate_weather_image.create_4_by_3(f"./generated_images/{interaction.user.id}_{int(datetime.now().timestamp())}.png", imperial, location)
    except Exception as err:
        e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
        e.description = f"```\n{err}\n```"
        await interaction.response.send_message(embed=e, ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=False)
    await interaction.followup.send(file=f)

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context):
    await ctx.send(content="Syncing...")
    await bot.tree.sync()
    await ctx.send(content="Synced...")
    
bot.run(api_key)