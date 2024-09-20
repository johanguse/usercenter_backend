import asyncio


async def process_chat_message(user_id: int, bot_id: int, message: str):
    # This function would call your AI service to process the message
    # For now, it's a placeholder
    await asyncio.sleep(1)  # Simulating AI processing time
    return f'AI response to: {message}'
