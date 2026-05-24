from datetime import datetime, date
from typing import List, Optional
import re


class Field:
    """Базовий клас для полів контакту."""
    
    def __init__(self, value: str):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.value}')"


class Name(Field):
    """Клас для представлення імені контакту."""
    
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Ім'я не може бути порожнім.")
        super().__init__(value.strip())


class Phone(Field):
    """Клас для представлення телефонного номера."""
    
    def __init__(self, value: str):
        # Телефон повинен містити 10 цифр
        cleaned = re.sub(r'\D', '', value)
        if len(cleaned) != 10:
            raise ValueError("Телефонний номер повинен містити 10 цифр.")
        super().__init__(value)
    
    @property
    def number(self):
        """Повертає номер без зайвих символів."""
        return re.sub(r'\D', '', self.value)


class Email(Field):
    """Клас для представлення email адреси."""
    
    def __init__(self, value: str):
        # Простої валідація email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Невірний формат email адреси.")
        super().__init__(value)


class Birthday(Field):
    """Клас для представлення дати народження."""
    
    def __init__(self, value: str):
        try:
            # Очікуємо формат DD.MM.YYYY
            self.date_obj = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Невірний формат дати. Очікується DD.MM.YYYY")
    
    def get_days_to_birthday(self) -> int:
        """Обчислює кількість днів до наступного дня народження."""
        today = date.today()
        next_birthday = self.date_obj.replace(year=today.year)
        
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        
        return (next_birthday - today).days


class Address(Field):
    """Клас для представлення адреси."""
    
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Адреса не може бути порожною.")
        super().__init__(value.strip())


class Record:
    """Клас для представлення контакту в адресній книзі."""
    
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.emails: List[Email] = []
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None
    
    def add_phone(self, phone: str) -> str:
        """Додає телефонний номер до контакту."""
        self.phones.append(Phone(phone))
        return f"Телефон {phone} додано."
    
    def remove_phone(self, phone: str) -> str:
        """Видаляє телефонний номер з контакту."""
        for p in self.phones:
            if p.number == re.sub(r'\D', '', phone):
                self.phones.remove(p)
                return f"Телефон {phone} видалено."
        return "Телефон не знайдено."
    
    def edit_phone(self, old_phone: str, new_phone: str) -> str:
        """Редагує телефонний номер."""
        for i, p in enumerate(self.phones):
            if p.number == re.sub(r'\D', '', old_phone):
                self.phones[i] = Phone(new_phone)
                return f"Телефон змінено з {old_phone} на {new_phone}."
        return "Старий телефон не знайдено."
    
    def find_phone(self, phone: str) -> Optional[Phone]:
        """Знаходить телефонний номер у контакті."""
        phone_digits = re.sub(r'\D', '', phone)
        for p in self.phones:
            if p.number == phone_digits:
                return p
        return None
    
    def add_email(self, email: str) -> str:
        """Додає email адресу до контакту."""
        self.emails.append(Email(email))
        return f"Email {email} додано."
    
    def remove_email(self, email: str) -> str:
        """Видаляє email адресу з контакту."""
        for e in self.emails:
            if e.value == email:
                self.emails.remove(e)
                return f"Email {email} видалено."
        return "Email не знайдено."
    
    def set_birthday(self, birthday: str) -> str:
        """Встановлює дату народження контакту."""
        self.birthday = Birthday(birthday)
        return f"День народження встановлено на {birthday}."
    
    def set_address(self, address: str) -> str:
        """Встановлює адресу контакту."""
        self.address = Address(address)
        return f"Адреса встановлена: {address}."
    
    def __str__(self):
        """Повертає рядкове представлення контакту."""
        result = f"Ім'я: {self.name.value}"
        
        if self.phones:
            phones_str = ", ".join(str(p) for p in self.phones)
            result += f"\nТелефони: {phones_str}"
        
        if self.emails:
            emails_str = ", ".join(str(e) for e in self.emails)
            result += f"\nEmails: {emails_str}"
        
        if self.birthday:
            days_to = self.birthday.get_days_to_birthday()
            result += f"\nДень народження: {self.birthday.value} ({days_to} днів до дня народження)"
        
        if self.address:
            result += f"\nАдреса: {self.address.value}"
        
        return result


class AddressBook:
    """Клас для управління адресною книгою."""
    
    def __init__(self):
        self.contacts: dict[str, Record] = {}
    
    def add_record(self, record: Record) -> str:
        """Додає контакт до адресної книги."""
        self.contacts[record.name.value] = record
        return f"Контакт {record.name.value} додано."
    
    def find(self, name: str) -> Optional[Record]:
        """Знаходить контакт за іменем."""
        return self.contacts.get(name)
    
    def delete(self, name: str) -> str:
        """Видаляє контакт за іменем."""
        if name in self.contacts:
            del self.contacts[name]
            return f"Контакт {name} видалено."
        return "Контакт не знайдено."
    
    def get_all_contacts(self) -> List[Record]:
        """Повертає список всіх контактів."""
        return list(self.contacts.values())
    
    def search(self, query: str) -> List[Record]:
        """Пошук контактів за іменем, телефоном або email."""
        query_lower = query.lower()
        results = []
        
        for record in self.contacts.values():
            # Пошук за іменем
            if query_lower in record.name.value.lower():
                results.append(record)
                continue
            
            # Пошук за телефоном
            query_digits = re.sub(r'\D', '', query)
            if query_digits and any(p.number == query_digits for p in record.phones):
                results.append(record)
                continue
            
            # Пошук за email
            if any(query_lower in e.value.lower() for e in record.emails):
                results.append(record)
        
        return results
    
    def __str__(self):
        """Повертає рядкове представлення адресної книги."""
        if not self.contacts:
            return "Адресна книга порожня."
        
        result = f"Всього контактів: {len(self.contacts)}\n"
        result += "=" * 50 + "\n"
        
        for record in sorted(self.contacts.values(), key=lambda r: r.name.value):
            result += str(record) + "\n" + "-" * 50 + "\n"
        
        return result