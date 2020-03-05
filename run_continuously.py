import sched
import discord_bot
ONE_HOUR = 60*60
ONE_MINUTE = 60

scheduler = sched.scheduler()

scheduler.enter(0, 1, discord_bot.run)
while True:
    scheduler.enter(ONE_HOUR, 1, discord_bot.run)
    scheduler.run()
