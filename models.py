from collections import UserDict, defaultdict
from datetime import datetime, timedelta

class IncorrectFormatException(Exception):
    pass

class ContactNotFoundError(Exception):
    pass

class PhoneNotFoundError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
      
    def __eq__(self, other):
        return self.value == other

class Name(Field):
    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def __init__(self, phone):
        if phone.isdigit() and len(phone) == 10:
            super().__init__(phone)
        else:
            raise IncorrectFormatException('Incorrect phone format, should be 10 digit')
        
        
class Birthday(Field):
    def __init__(self, birthday):
        try:
            dataObj = datetime.strptime(birthday, '%d.%m.%Y')
            super().__init__(dataObj)
        except ValueError:
            raise IncorrectFormatException('Incorrect birthday format, should be DD.MM.YYYY')
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
        
    def add_phone(self, phone):
        newPhone = Phone(phone)
        self.phones.append(newPhone)
        

    def delete_phone(self, phone):
      self.phones = list(filter(lambda p: p != phone, self.phones))

      
    def edit_phone(self, oldPhone, newPhone):
        try:
            phoneIndex = self.phones.index(oldPhone)
            self.phones[phoneIndex] = Phone(newPhone)
        except ValueError:
            PhoneNotFoundError(oldPhone)
            
    def change_phone(self, phone):
        self.phones = [Phone(phone)]

    def find_phone(self, phone):
        if phone in self.phones:
            return phone
        else: 
            raise PhoneNotFoundError(phone)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        
    def all_phones(self):
        return '; '.join([str(p) for p in self.phones])
        

    def __str__(self):
        result = f"Contact name: {self.name}, phones: {self.all_phones()}"
        if self.birthday:
            result = result + f', birthday: {self.birthday}'
        return result
    
    
    def __hash__(self):
        return hash(self.name)
    

class AddressBook(UserDict[Name, Record]):
    def add_record(self, contact):
        self.data[contact.name] = contact
        
        
    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise ContactNotFoundError
        
    def delete(self, name):
        try:
            del self.data[name]
        except KeyError:
            raise ContactNotFoundError
        
        
    def __str__(self):
        return '\n'.join([f'{r}' for r in self.data.values()])
    
    
    def __get_norm_weekday_user_birthday(self, birthday):
        weekday = birthday.weekday()
        if (weekday >= 5):
            birthday = birthday + timedelta(days=(7 - weekday))
        return birthday


    def __get_user_birthday_this_year(self, user_birthday, today):
        birthday = user_birthday.date()
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        return birthday_this_year


    def __get_formatted_birthdays_per_week_result(self, result):
        result_string = ''
        for day_name, names in result.items():
            names_string = ', '.join(names)
            result_string = result_string + f'{day_name}: {names_string}\n'
        return result_string


    def get_birthdays_per_week(self):
        result = defaultdict(list)
        today = datetime.today().date()
        for contact in self.data.values():
            if not contact.birthday:
                continue
            name = contact.name.value
            birthday = contact.birthday.value
            birthday_this_year = self.__get_user_birthday_this_year(birthday, today)
            birthday_this_year = self.__get_norm_weekday_user_birthday(birthday_this_year)
            delta_days = (birthday_this_year - today).days
            if delta_days > 7:
                continue
            result[birthday_this_year.strftime("%A")].append(name)
        return self.__get_formatted_birthdays_per_week_result(result)
