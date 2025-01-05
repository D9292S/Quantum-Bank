import asyncio

def test_ping_command(self):
    asyncio.run(self._async_test_ping_command())

async def _async_test_ping_command(self):
    ctx = AsyncMock()
    await self.bot.ping(ctx)
    self.bot.send_message.assert_called_with(ctx, "Pong!")

