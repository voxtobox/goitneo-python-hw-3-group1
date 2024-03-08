from models import AddressBook, Record
from models import ContactNotFoundError, IncorrectFormatException


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return 'Incorrect data'
        except IncorrectFormatException as error:
            return str(error.args[0])
        except ContactNotFoundError:
            return 'Contact not found'
        except KeyError:
            return 'Enter user name'
        except IndexError:
            return 'Invalid number of arguments'

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    contact = Record(name)
    contact.add_phone(phone)
    book.add_record(contact)
    return 'Contact added.'


@input_error
def change_contact(args, book: AddressBook):
    name, new_phone = args
    if name in book:
        book[name].change_phone(new_phone)
        return 'Contact updated.'
    else:
        raise ContactNotFoundError


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    if name in book:
        return book[name].all_phones()
    else:
        raise ContactNotFoundError


def show_all(book):
    return str(book)


@input_error
def add_contact_birthday(args, book: AddressBook):
    name, birthday = args
    if name in book:
        book[name].add_birthday(birthday)
        return 'Birthday added.'
    else:
        raise ContactNotFoundError


@input_error
def show_contact_birthday(args, book: AddressBook):
    name = args[0]
    if name in book:
        return str(book[name].birthday)
    else:
        raise ContactNotFoundError


def show_birthdays_this_week(book: AddressBook):
    return book.get_birthdays_per_week()


def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            print('Good bye!')
            break
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all(book))
        elif command == 'add-birthday':
            print(add_contact_birthday(args, book))
        elif command == 'show-birthday':
            print(show_contact_birthday(args, book))
        elif command == 'birthdays':
            print(show_birthdays_this_week(book))
        else:
            print('Invalid command.')


if __name__ == '__main__':
    main()
