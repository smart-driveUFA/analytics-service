from aiohttp import ClientSession


async def send_result_auth(processed_data: dict):
    async with ClientSession() as session, session.post(
        "AUTH_CHECK_REQUEST_COUNT", data=processed_data
    ) as resp:
        resp.close()
