import discord
from discord.ext import commands
import generate_weather_image
from datetime import datetime

api_key = open("./src/discord_token.txt", "r").read()

bot = commands.Bot(command_prefix="=", intents=discord.Intents(messages=True, message_content=True))

beta_testers = open("./src/beta_testers.txt", "r").read().split("\n")

bot.remove_command("help")

browhat_emoji_id = open("./src/browhat_emoji_id.txt", "r").read()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.tree.command(name="4-by-3", description="Generates a 4:3 image with the current conditions at a location.")
@discord.app_commands.describe(location="Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude or city name.",
                               imperial="Use imperial measurements. (mph, miles, fahrenheit) Default: True")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.user_install()
async def make_4_3(interaction: discord.Interaction, location: str, imperial: bool = True):
    if str(interaction.user.id) in beta_testers:
        try:
            f = generate_weather_image.create_4_by_3(f"./src/generated_images/4-3_{interaction.user.id}_{int(datetime.now().timestamp())}.png", imperial, location)
        except Exception as err:
            e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
            e.description = f"```\n{err}\n```"
            await interaction.response.send_message(embed=e, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(file=f)
    else:
        await interaction.response.send_message(content="This bot is in a closed beta.", ephemeral=True)


@bot.tree.command(name="16-by-9", description="Generates a 16:9 image with the current conditions at a location.")
@discord.app_commands.describe(location="Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude or city name.",
                               imperial="Use imperial measurements. (mph, miles, fahrenheit) Default: True")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.user_install()
async def make_16_9(interaction: discord.Interaction, location: str, imperial: bool = True):
    if str(interaction.user.id) in beta_testers:
        try:
            f = generate_weather_image.create_16_by_9(f"./src/generated_images/16-9_{interaction.user.id}_{int(datetime.now().timestamp())}.png", imperial, location)
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
    if str(ctx.author.id) in beta_testers:
        f = open("./src/version.txt", "r").read
        await ctx.send(content=f)
    else:
        await ctx.send(content="This bot is in a closed beta.")


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context):
    await ctx.send(content="Syncing...")
    await bot.tree.sync()
    await ctx.send(content="Synced...")


@bot.command()
@commands.is_owner()
async def add_bt(ctx: commands.Context, uid: int):
    try:
        user = await bot.fetch_user(uid)
    except discord.NotFound as err:
        e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
        e.description = f"```\n{err}\n```"
        await ctx.send(embed=e, ephemeral=True)
        return
    except discord.HTTPException as err:
        e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
        e.description = f"```\n{err}\n```"
        await ctx.send(embed=e, ephemeral=True)
        return

    class View(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
        
        @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅")
        async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
            beta_testers.append(str(uid))
            f = open("./src/beta_testers.txt", "w")
            for tester in beta_testers:
                if beta_testers[0] == tester:
                    f.write(tester)
                else:
                    f.write(f"\n{tester}")
            f.close()

            await interaction.response.send_message(content=f"Added {user.mention} ({user.name}) to the beta tester list.", ephemeral=True)
            await self.message.edit(content=f"Added {user.mention} ({user.name}) to the beta tester list.", view=None)
        
        @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="❌")
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.message.delete()
        
        async def on_timeout(self):
            await self.message.edit(content="-# Timed out, run the command again to access the buttons.", view=None)
    if str(uid) in beta_testers:
        await ctx.send(content=f"{user.mention} ({user.name}) is already on the beta tester list.")
    else:
        view = View()
        message = await ctx.send(content=f"Are you sure you want to add {user.mention} ({user.name}) to the beta tester list?", view=view)
        view.message = message


@bot.command()
@commands.is_owner()
async def del_bt(ctx: commands.Context, uid: int):
    try:
        user = await bot.fetch_user(uid)
    except discord.NotFound as err:
        e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
        e.description = f"```\n{err}\n```"
        await ctx.send(embed=e, ephemeral=True)
        return
    except discord.HTTPException as err:
        e = discord.Embed(title="An error ocurred.", colour=discord.Colour.brand_red())
        e.description = f"```\n{err}\n```"
        await ctx.send(embed=e, ephemeral=True)
        return

    class View(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
        
        @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅")
        async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
            beta_testers.remove(str(uid))
            f = open("./src/beta_testers.txt", "w")
            for tester in beta_testers:
                if beta_testers[0] == tester:
                    f.write(tester)
                else:
                    f.write(f"\n{tester}")
            f.close()

            await interaction.response.send_message(content=f"Added {user.mention} ({user.name}) to the beta tester list.", ephemeral=True)
            await self.message.edit(content=f"Added {user.mention} ({user.name}) to the beta tester list.", view=None)
        
        @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="❌")
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.message.delete()
        
        async def on_timeout(self):
            await self.message.edit(content="-# Timed out, run the command again to access the buttons.", view=None)

    if str(uid) in beta_testers:
        view = View()
        message = await ctx.send(content=f"Are you sure you want to remove {user.mention} ({user.name}) from the beta tester list?", view=view)
        view.message = message
    else:
        await ctx.send(content=f"{user.mention} ({user.name}) is not on the beta tester list.")


@bot.command()
async def ht(ctx: commands.Context):
    await ctx.send(content=f"hawk tuah <:browhat:{browhat_emoji_id}>")

    
bot.run(api_key)