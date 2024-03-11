from collections import UserDict
from datetime import datetime


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            # return "No or incorrect name. Give me name please."
            return "KeyError: no contact."
        except IndexError:
            return "IndexError: no contact."
        # except Exception as e:
        #     return f"Error: {str(e)}"
    return inner

class Birthday():
    """
    Клас для представлення дня народження користувача.
    """
    def __init__(self, value):
        self.value = value
    
    def validate(self):
        """
        Перевіряє правильність формату дати народження.
        """
        try:
            datetime.strptime(self.value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Incorrect date format, should be DD.MM.YYYY")

class Name():
    """
    Клас для представлення імені користувача.
    """
    def __init__(self, value):
        self.value = value

class Phone():
    """
    Клас для представлення телефонного номера користувача.
    """
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"Phone: {self.value}"
    
    def validate(self):
        """
        Перевіряє правильність формату телефонного номера.
        """
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits.")

class Record:
    """
    Клас для представлення контакту в адресній книзі.
    """
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        """
        Додає новий телефонний номер до контакту.
        """
        phone = Phone(phone_number)
        phone.validate()
        self.phones.append(phone)

    def add_birthday(self, birthday):
        """
        Додає день народження до контакту.
        """
        if self.birthday is None:
            self.birthday = Birthday(birthday)

    def remove_phone(self, phone_number):
        """
        Видаляє телефонний номер з контакту.
        """
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        """
        Змінює телефонний номер контакту.
        """
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                phone.validate()
                return
        raise ValueError("Phone number not found.")

    def find_phone(self, phone_number):
        """
        Знаходить телефонний номер контакту за заданим номером.
        """
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        raise ValueError("Phone number not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    """
    Клас для представлення адресної книги.
    """
    def add_record(self, record):
        """
        Додає новий запис до адресної книги.
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Знаходить контакт за заданим ім'ям.
        """
        if name in self.data:
            return self.data[name]
        else:
            raise KeyError("Record not found.")

    def delete(self, name):
        """
        Видаляє контакт за заданим ім'ям.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Record not found.")

    def add_birthday(self, name, birthday):
        """
        Додає день народження до контакту за заданим ім'ям.
        """
        if name in self.data:
            record = self.data[name]
            try:
                birthday = Birthday(birthday)  # Перетворення рядка у об'єкт Birthday
                birthday.validate()  # Перевірка формату дати
                record.add_birthday(birthday)
                return True
            except ValueError as e:
                print(e)
        else:
            print("Contact not found.")
    
    def show_birthday(self, name):
        """
        Виводить день народження контакту за заданим ім'ям.
        """
        if name in self.data:
            birthday = self.data[name].birthday.value
            if birthday:
                print(f"{name}'s birthday: {birthday.value}")
                # print(f"{name}'s birthday: {birthday}")

        else:
            print("Contact not found.")

    def birthdays(self):
        """
        Виводить список користувачів, яких потрібно привітати за день народження протягом наступного тижня.
        """
        birt_dict = {}
        formatted_output = ""
        curr_data = datetime.today().date()
        curr_year = datetime.today().year

        for contact in self.data.values():
            usr_name = contact.name.value
            birt_data = contact.birthday.value.value
            # birt_in_this_year = birt_data.replace(year=curr_year)
            birt_in_this_year = datetime.strptime(birt_data, '%d.%m.%Y').replace(year=curr_year).date()
            birt_in_this_year_of_week = birt_in_this_year.strftime('%A')

            if birt_in_this_year < curr_data:                               # д.р. в этом году уже был
                birt_in_this_year = birt_data.replace(year=curr_year+1)
                # birt_in_this_year = datetime.strptime(birt_data, '%d.%m.%Y').replace(year=curr_year+1)
            delta_days = (birt_in_this_year - curr_data).days
            if delta_days < 7:                                              # д.р. на текущей неделе
                if birt_in_this_year.weekday() < 5:                         # не попадает на выходные
                    if birt_in_this_year_of_week not in birt_dict:
                        birt_dict[birt_in_this_year_of_week] = []
                    birt_dict[birt_in_this_year_of_week].append(usr_name)                   
                else:                                                       # попадает на выходные, поздравить в понедельник
                    if "Monday" not in birt_dict:
                        birt_dict["Monday"] = []
                    birt_dict["Monday"].append(usr_name)

        for day, names in sorted(birt_dict.items(), key=lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(x[0])):
            formatted_output += f"{day}: {', '.join(names)}\n"
        
        print(formatted_output)


def parse_input(user_input):
    """
    Розбиває введену команду користувача на команду та аргументи.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    """
    Головна функція програми.
    """
    address_book = AddressBook()  # Ініціалізація адресної книги
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:                            # close exit
            print("Good bye!")
            break
        elif command == "hello":                                    # hello
            print("How can I help you?")
        elif command == "add":                                      # add John 1234567890
            name, phone = args
            record = Record(name)
            record.add_phone(phone)
            address_book.add_record(record)
            print("Contact added.")
        elif command == "change":                                   # change John 0987654321
            name, phone = args
            record = address_book.find(name)
            record.edit_phone(record.phones[0].value, phone)
            print("Contact updated.")
        elif command == "phone":                                    # phone John
            name = args[0]
            record = address_book.find(name)
            print(record.phones[0])
        elif command == "all":                                      # all
            for record in address_book.data.values():
                print(record)
        elif command == "add-birthday":                             # add-birthday John 1970.11.14   add-birthday John 14.11.1970
            name, birthday = args
            if address_book.add_birthday(name, birthday):
                print("Birthday added.")
        elif command == "show-birthday":                            # show-birthday John
            name = args[0]
            address_book.show_birthday(name)                        # birthdays
        elif command == "birthdays":
            address_book.birthdays()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
