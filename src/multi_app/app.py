"""
An app that does a bunch of cool stuffs
"""
import httpx
import toga
from toga import TextInput, Box, Button, MainWindow, Label
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Any


class MultiApp(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # Styling the main box
        main_box: Box = toga.Box(style=Pack(direction=COLUMN))  # Box to be placed inside main window

        # Create a name_label with the label widget
        name_label: Label = toga.Label("Enter name", style=Pack(direction=ROW, padding=(0, 5)))
        # Create text input field to be place beside name label
        # noinspection PyAttributeOutsideInit
        self.input_text: TextInput = toga.TextInput(style=Pack(flex=1))

        # Create box for the above widgets
        name_box: Box = toga.Box()
        name_box.add(name_label)
        name_box.add(self.input_text)

        # Create a button with a button widget
        button: Button = toga.Button("greet", on_press=self.say_hello,
                                     style=Pack(padding=5),
                                     )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window: MainWindow = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    # noinspection PyUnusedLocal
    async def say_hello(self, widget) -> None:
        if self.input_text.value:
            user_name: str = self.input_text.value
        else:
            user_name = "Stranger"

        # Using a context
        async with httpx.AsyncClient() as client:
            response: Any = await client.get("https://jsonplaceholder.typicode.com/posts/42")
            u_response = response.json()

        self.main_window.info_dialog(
            F"Hello {user_name}", u_response['body'],
        )


def main() -> Any:
    return MultiApp()
