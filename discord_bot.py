import asyncio
import time

import discord

from mml import get_assignments

token = 'NjgxOTI3NTE0OTM5MDY0MzY1.Xlrb3A.UqAfjD3vFWtTFyDwVFCrKg0UJUI'
channel_name = 'auto-reminders'

ONE_DAY = 60 * 60 * 24

NEW_MESSAGE = '**Available**: *{name}* - __{due}__'
WARNING_MESSAGE = '**24 hour warning!** *{name}* - __{due}__'
CLOSED_MESSAGE = '**Closed**: *{name}* - __{due}__'


def run():
    client = discord.Client()

    async def get_messages_hashes(channel):
        messages = {}
        async for message in channel.history(limit=None):
            if message.author == client.user:
                messages[hash(message.content)] = message
        return messages

    async def delete_all(channel):
        async for message in channel.history(limit=None):
            if message.author == client.user:
                await message.delete()

    @client.event
    async def on_ready():
        try:
            channel = [channel for channel in client.get_all_channels() if channel.name == channel_name][0]
            assignments = await client.loop.run_in_executor(None, get_assignments)
            messages = await get_messages_hashes(channel)
            for assign_due_int, assign_name, assign_due in assignments:
                available = NEW_MESSAGE.format(due=assign_due, name=assign_name)
                warning = WARNING_MESSAGE.format(due=assign_due, name=assign_name)
                closed = CLOSED_MESSAGE.format(due=assign_due, name=assign_name)

                if assign_due_int < time.time():
                    # closed
                    avail = messages.get(hash(available))
                    if avail:
                        await avail.edit(content=closed)
                    elif hash(closed) not in messages:
                        await channel.send(closed)
                    warn = messages.get(hash(warning))
                    if warn:
                        await warn.delete()
                    continue

                if hash(available) not in messages:
                    await channel.send(available)
                    await asyncio.sleep(1)  # delay in between messages
                if hash(warning) not in messages and ONE_DAY > assign_due_int:
                    await channel.send(warning)
                    await asyncio.sleep(2)  # delay in between messages
            await client.close()
        finally:
            await client.close()

    client.run(token)
    asyncio.set_event_loop(asyncio.new_event_loop())


if __name__ == '__main__':
    run()
