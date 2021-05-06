import asyncio
import ctypes
import ctypes.wintypes

import wizwalker
from wizwalker import user32


class MouseHandler:
    """
    Handles clicking/moving the mouse position
    """

    def __init__(self, client: "wizwalker.client"):
        self.client = client
        self.click_lock = None

    async def activate_mouseless(self):
        """
        Activates the mousless hook
        """
        # this will error if already active for us
        await self.client.hook_handler.activate_mouseless_cursor_hook()

    async def click_window(self, window: "wizwalker.memory.window.DynamicWindow"):
        """
        Clicks a Window
        """
        raise NotImplementedError("method has not yet been implimented")

    # TODO: add errors (HookNotActive)
    async def click(
        self,
        x: int,
        y: int,
        *,
        right_click: bool = False,
        sleep_duration: float = 0.0,
        use_post: bool = False,
    ):
        """
        Send a click to a certain x and y
        x and y positions are relative to the top left corner of the screen

        Args:
            x: x to click at
            y: y to click at
            right_click: If the click should be a right click
            sleep_duration: How long to sleep between messages
            use_post: If PostMessage should be used instead of SendMessage
        """
        # We don't have to check if the hook is active since it will just error
        if right_click:
            button_down_message = 0x204
        else:
            button_down_message = 0x201

        if use_post:
            send_method = user32.PostMessageW
        else:
            send_method = user32.SendMessageW

        if self.click_lock is None:
            self.click_lock = asyncio.Lock()

        # prevent multiple clicks from happening at the same time
        async with self.click_lock:
            # TODO: test passing use_post
            await self.set_mouse_position(x, y)
            # mouse button down
            send_method(self.client.window_handle, button_down_message, 1, 0)
            if sleep_duration > 0:
                await asyncio.sleep(sleep_duration)
            # mouse button up
            send_method(self.client.window_handle, button_down_message + 1, 0, 0)

    async def set_mouse_position(
        self,
        x: int,
        y: int,
        *,
        convert_from_client: bool = True,
        use_post: bool = False,
    ):
        """
        Set's the mouse position to a certain x y relative to the
        top left corner of the client

        Args:
            x: x to set
            y: y to set
            convert_from_client: If the position should be converted from client to screen
            use_post: If PostMessage should be used instead of SendMessage
        """
        if use_post:
            send_method = user32.PostMessageW
        else:
            send_method = user32.SendMessageW

        if convert_from_client:
            point = ctypes.wintypes.tagPOINT(x, y)

            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-clienttoscreen
            if (
                user32.ClientToScreen(self.client.window_handle, ctypes.byref(point))
                == 0
            ):
                raise RuntimeError("Client to screen conversion failed")

            # same point structure is overwritten by ClientToScreen; these are also ints and not
            # c_longs for some reason?
            x = point.x
            y = point.y

        res = await self.client.hook_handler.write_mouse_position(x, y)
        # position doesn't matter here; sending mouse move
        # mouse move is here so that items are highlighted
        send_method(self.client.window_handle, 0x200, 0, 0)
        return res