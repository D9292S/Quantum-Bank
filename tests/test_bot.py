import unittest
import asyncio
from unittest.mock import AsyncMock, patch


class TestMyBot(unittest.TestCase):
    def setUp(self):
        self.bot = AsyncMock()

    def tearDown(self):
        from db import client
        client.close()

    def test_ping_command(self):
        asyncio.run(self._async_test_ping_command())

    async def _async_test_ping_command(self):
        ctx = AsyncMock()
        await self.bot.ping(ctx)
        self.bot.ping.assert_called_once_with(ctx)


    # Add more test methods here as needed

if __name__ == '__main__':
    unittest.main()
