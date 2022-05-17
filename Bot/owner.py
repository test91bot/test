import asyncio



async def OwnerDashboard(event, sender):
    loading = await event.client.send_message(sender.id, '⏳')
