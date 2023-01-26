"""
An app that does a bunch of cool stuffs
"""
import toga
from toga import TextInput, Box, Button, MainWindow, Label
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Any, List


class MultiApp(toga.App):
    def __init__(
            self,
            formal_name=None,
            app_id=None,
            app_name=None,
            id=None,
            icon=None,
            author=None,
            version=None,
            home_page=None,
            description=None,
            startup=None,
            windows=None,
            on_exit=None,
            factory=None,
    ):
        super().__init__(formal_name, app_id, app_name, id, icon, author, version, home_page, description, startup,
                         windows, on_exit, factory)

        self.anagram_user_input0 = None
        self.anagram_user_input1 = None
        self.input_text = None

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # MAIN BOX
        main_box: Box = toga.Box(style=Pack(background_color='blue', direction=COLUMN))

        # NAME LABEL SECTION
        name_label: Label = toga.Label("Enter name", style=Pack(direction=ROW, padding=(0, 5)))
        anagram_name_label: Label = toga.Label("Check Anagram", style=Pack(direction=ROW, padding=(5, 0)))

        # USER TEXT INPUT SECTION
        self.input_text: TextInput = toga.TextInput(placeholder="Enter your name here",
                                                    style=Pack(flex=1))
        self.anagram_user_input0: TextInput = toga.TextInput(placeholder="Enter word here",
                                                             style=Pack(flex=10, padding=5))
        self.anagram_user_input1: TextInput = toga.TextInput(placeholder=" Enter another word here",
                                                             style=Pack(flex=10, padding=5))

        # ENCAPSULATION BOX SECTION
        name_box: Box = toga.Box(id='grey')
        anagram_box: Box = toga.Box(id='green')

        name_box.add(name_label)
        name_box.add(self.input_text)

        anagram_box.add(anagram_name_label)
        anagram_box.add(self.anagram_user_input0)
        anagram_box.add(self.anagram_user_input1)

        # BUTTON SECTION
        greet_button: Button = toga.Button("greet", id='green', on_press=self.say_hello,
                                           style=Pack(flex=20, padding=5),
                                           )
        anagram_button: Button = toga.Button("Check", id='blue', on_press=self.anagram_solution,
                                             style=Pack(flex=30, padding=5),
                                             )

        # BOX INTO MAIN-BOX SECTION
        main_box.add(name_box)
        main_box.add(greet_button)
        main_box.add(anagram_box)
        main_box.add(anagram_button)

        # MAIN BOX INTO MAIN WINDOW SECTION
        self.main_window: MainWindow = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    # HANDLER SECTION
    async def say_hello(self, widget: Any) -> Any:
        if self.input_text.value:
            user_name: str = self.input_text.value
        else:
            user_name = "Stranger"

        # Using a context manager
        async with httpx.AsyncClient() as client:
            response: Any = await client.get("https://jsonplaceholder.typicode.com/posts/42")
            u_response = response.json()

        self.main_window.info_dialog(
            F"Hello {user_name}", u_response['body'],
        )

    def anagram_solution(self, widget) -> None:
        """Takes two words, returns True if anagram, False otherwise
        """

        s1: List[int] = [0] * 26
        s2: List[int] = [0] * 26

        for s1_var in range(0, len(self.anagram_user_input0.value), 1):
            pos: int = ord(self.anagram_user_input0.value[s1_var]) - ord('a')
            s1[pos] += 1
        for s2_var in range(0, len(self.anagram_user_input1.value), 1):
            pos: int = ord(self.anagram_user_input1.value[s2_var]) - ord('a')
            s2[pos] += 1

        found: bool = True
        j: int = 0
        while j < 26 and found:
            if s1[j] == s2[j]:
                found = True
                j += 1
            else:
                found = False
        if found:
            self.main_window.info_dialog(
                F"Yippi!", F"you found an anagram"
            )
        else:
            self.main_window.info_dialog(
                F"Sorry", F"Words are not anagrams, try again"
            )


def main() -> Any:
    return MultiApp()
