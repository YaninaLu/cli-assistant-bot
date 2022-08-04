from typing import List, Callable, Tuple, Any
from re import match


class CliApp:
    """
    A class that is responsible for communicating with the user.

    It takes input from the user, parses it and sends it to the AssistantBot class. Also, it outputs the result that
    returns from the bot and terminates the app when the user inputs one of the stop words.
    """
    def run(self):
        """
        Waits for the user input in an infinite loop. Terminates when one of the stop words is given.

        :return: result of running the command by the bot
        """
        bot = AssistantBot()
        while True:
            command, args = self.parse_command(input().lower())
            if command in ["good bye", "close", "exit"]:
                print("Good bye!")
                break
            else:
                result = bot.handle(command, args)
                if result:
                    print(result)

    @staticmethod
    def parse_command(user_input: str) -> Tuple[str, list[str]]:
        """
        Parses the string input into a tuple of command and arguments.

        :param user_input: a string that user provides
        :return: tuple(command, *args)
        """
        user_input = user_input.split()
        if len(user_input) == 0:
            raise ValueError()
        command = user_input[0]
        args = user_input[1:]
        return command, args


class AssistantBot:
    """
    A class that is responsible for identifying and calling functions that correspond to the given command.

    It stores commands and corresponding functions in a dictionary and calls these functions with the given arguments.
    It also catches exceptions on the domain level. When the user calls commands connected with managing the phonebook,
    bot sends them to the PhoneBook class.
    """
    def __init__(self):
        self.commands = {
            "hello": self.hello,
            "add": self.add,
            "change": self.change,
            "phone": self.show,
            "show": self.show,
        }
        self.phonebook = PhoneBook()

    @staticmethod
    def input_error(func: Callable) -> Callable[[tuple[Any, ...]], str | Any]:
        """
        Catches exceptions on the domain level (i.e. mistakes that prevent functions to fulfil their promises).

        :param func: function to execute
        :return: inner function that checks for exceptions when the function to execute is run
        """

        def exception_handler(*args, **kwargs):

            try:
                result = func(*args, **kwargs)
            except TypeError as err:
                return f"Invalid input, some info is missing: {err}"
            except KeyError as err:
                return f"Sorry, no such command: {err}"
            except ValueError as err:
                return f"ValueError: {err}"
            else:
                return result

        return exception_handler

    @input_error
    def handle(self, command: str, args: List[str]) -> str:
        """
        An entry point for the commands given by the user. It takes a corresponding function from the dictionary and
        calls its instance with the given arguments.

        :param command: command given by the user
        :param args: arguments to call the function with
        :return: function call with the given arguments
        """
        handler = self.commands[command]
        return handler(*args)

    @staticmethod
    @input_error
    def hello():
        """
        Returns a greeting to the 'hello' command.

        :return: greeting string
        """
        return "How can I help you?"

    @input_error
    def add(self, name: str, phone: str) -> None:
        """
        Calls a function that adds the given phone number to the phonebook.

        :param name: name of the person to add
        :param phone: phone of the person to add
        """
        self.phonebook.add_contact(name, phone)

    @input_error
    def change(self, name: str, phone: str) -> None:
        """
        Calls a function that changes the phone number of the given person.

        :param name: name that has to be already present in the phonebook
        :param phone: new phone of this person
        """
        self.phonebook.change_contact(name, phone)

    @input_error
    def show(self, name: str) -> str:
        """
        Calls a function that shows the phone number of the given person.

        :param name: name of a person or 'all' if the user wants all the phonebook to be printed
        :return: phone number or the whole phonebook
        """
        return self.phonebook.show_phone(name)


class PhoneBook:
    """
    A class that stores a dictionary of 'name': 'phone number' pairs. It is also responsible for managing the phonebook.
    """
    def __init__(self):
        self.phones = {}

    @staticmethod
    def verify_phone(phone: str) -> None:
        """
        Checks if the phone number is valid. Throws exception if it's not valid.

        :param phone: phone number as a string
        :return: exception if it doesn't match the needed pattern
        """
        if not match(r"(\+?\d{12}|\d{10})", phone):
            raise ValueError("Invalid phone format")

    def add_contact(self, name: str, phone: str) -> None:
        """
        Adds a new entry to the dictionary. Throws exception if the person with this name already exists in the phonebook.

        :param name: name of a person to add
        :param phone: phone number of a person to add
        """
        self.verify_phone(phone)
        if name not in self.phones:
            self.phones[name] = phone
        else:
            raise ValueError(
                "This name is already in your phonebook. If you want to change the phone number, type 'change'.")

    def change_contact(self, name: str, phone: str) -> None:
        """
        Changes the phone number of a person already present in the phonebook. Throws exception if the name is not
        present in the dictionary.

        :param name: name of a person
        :param phone: new phone
        """
        self.verify_phone(phone)
        if name in self.phones:
            self.phones[name] = phone
        else:
            raise ValueError("This name is not in your phonebook. If you want to add it, type 'add'.")

    def show_phone(self, name: str) -> str:
        """
        Shows the phone number of a given person. If 'all' was given as an argument it returns the whole phonebook.

        :param name: name to show or 'all'
        :return: phone number or phonebook as a string
        """
        if name == "all":
            if self.phones:
                phonebook = ""
                for name, phone in self.phones.items():
                    phonebook += f"Name: {name}, phone: {phone}\n"
                return phonebook
            else:
                return "You do not have any contacts yet."
        else:
            return self.phones[name]


def main():
    CliApp().run()


if __name__ == "__main__":
    main()
