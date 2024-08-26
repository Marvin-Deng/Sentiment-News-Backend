import asyncio
from typing import Callable, Any, Tuple


async def async_wrap_sync(func: Callable, *args: Tuple[Any], **kwargs: dict) -> Any:
    """
    Wraps a synchronous function in an asynchronous context.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)
