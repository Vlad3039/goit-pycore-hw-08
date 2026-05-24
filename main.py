

from models import AddressBook, Record
from storage import AddressBookStorage
from typing import Optional


class AddressBookApp:
    """Основний клас для управління командною лінією адресної книги."""
    
    def __init__(self, storage_file: str = "addressbook.pkl"):
        """Ініціалізує застосунок."""
        self.storage = AddressBookStorage(storage_file)
        self.book = self.storage.load()
        self.running = True
    
    def display_menu(self):
        """Виводить головне меню."""
        print("\n" + "=" * 60)
        print("📇 АДРЕСНА КНИГА".center(60))
        print("=" * 60)
        print(
            """
1. ➕ Додати контакт
2. 🔍 Знайти контакт
3. 📝 Редагувати контакт
4. ❌ Видалити контакт
5. 📋 Показати всі контакти
6. 🔎 Пошук контакту
7. 📊 Статистика
8. 💾 Інформація про файл
9. ❌ Вихід
"""
        )
    
    def add_contact(self):
        """Додає новий контакт."""
        print("\n--- Додавання нового контакту ---")
        
        try:
            name = input("Введіть ім'я контакту: ").strip()
            if not name:
                print("✗ Ім'я не може бути порожним.")
                return
            
            if self.book.find(name):
                print(f"✗ Контакт '{name}' вже існує.")
                return
            
            record = Record(name)
            
            # Додавання телефонів
            while True:
                phone = input("Введіть телефон (формат: 0501234567) або натисніть Enter для пропуску: ").strip()
                if not phone:
                    break
                try:
                    record.add_phone(phone)
                    print("✓ Телефон додано.")
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            # Додавання email
            while True:
                email = input("Введіть email або натисніть Enter для пропуску: ").strip()
                if not email:
                    break
                try:
                    record.add_email(email)
                    print("✓ Email додано.")
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            # Додавання дати народження
            birthday = input("Введіть дату народження (DD.MM.YYYY) або натисніть Enter для пропуску: ").strip()
            if birthday:
                try:
                    record.set_birthday(birthday)
                    print("✓ День народження встановлено.")
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            # Додавання адреси
            address = input("Введіть адресу або натисніть Enter для пропуску: ").strip()
            if address:
                try:
                    record.set_address(address)
                    print("✓ Адреса встановлена.")
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            self.book.add_record(record)
            print(f"✓ Контакт '{name}' успішно додано.")
        
        except KeyboardInterrupt:
            print("\n✗ Операція скасована.")
        except Exception as e:
            print(f"✗ Помилка: {e}")
    
    def find_contact(self):
        """Знаходить контакт за іменем."""
        print("\n--- Пошук контакту ---")
        name = input("Введіть ім'я контакту для пошуку: ").strip()
        
        record = self.book.find(name)
        if record:
            print("\n" + str(record))
        else:
            print(f"✗ Контакт '{name}' не знайдено.")
    
    def edit_contact(self):
        """Редагує існуючий контакт."""
        print("\n--- Редагування контакту ---")
        name = input("Введіть ім'я контакту для редагування: ").strip()
        
        record = self.book.find(name)
        if not record:
            print(f"✗ Контакт '{name}' не знайдено.")
            return
        
        print("\n" + str(record))
        print("\nОпції редагування:")
        print("1. Додати телефон")
        print("2. Видалити телефон")
        print("3. Змінити телефон")
        print("4. Додати email")
        print("5. Видалити email")
        print("6. Встановити день народження")
        print("7. Встановити адресу")
        print("0. Скасувати")
        
        try:
            choice = input("Виберіть дію: ").strip()
            
            if choice == "1":
                phone = input("Введіть телефон: ").strip()
                try:
                    print(record.add_phone(phone))
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            elif choice == "2":
                phone = input("Введіть телефон для видалення: ").strip()
                print(record.remove_phone(phone))
            
            elif choice == "3":
                old_phone = input("Введіть старий телефон: ").strip()
                new_phone = input("Введіть новий телефон: ").strip()
                try:
                    print(record.edit_phone(old_phone, new_phone))
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            elif choice == "4":
                email = input("Введіть email: ").strip()
                try:
                    print(record.add_email(email))
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            elif choice == "5":
                email = input("Введіть email для видалення: ").strip()
                print(record.remove_email(email))
            
            elif choice == "6":
                birthday = input("Введіть дату народження (DD.MM.YYYY): ").strip()
                try:
                    print(record.set_birthday(birthday))
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            elif choice == "7":
                address = input("Введіть адресу: ").strip()
                try:
                    print(record.set_address(address))
                except ValueError as e:
                    print(f"✗ Помилка: {e}")
            
            elif choice == "0":
                print("✓ Редагування скасовано.")
                return
            
            else:
                print("✗ Невідома дія.")
                return
            
            print(f"\n✓ Контакт '{name}' оновлено.")
        
        except KeyboardInterrupt:
            print("\n✗ Операція скасована.")
    
    def delete_contact(self):
        """Видаляє контакт."""
        print("\n--- Видалення контакту ---")
        name = input("Введіть ім'я контакту для видалення: ").strip()
        
        record = self.book.find(name)
        if not record:
            print(f"✗ Контакт '{name}' не знайдено.")
            return
        
        confirm = input(f"Ви впевнені, що хочете видалити '{name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            print(self.book.delete(name))
        else:
            print("✓ Видалення скасовано.")
    
    def show_all_contacts(self):
        """Показує всі контакти."""
        print("\n" + "=" * 60)
        print("📋 ВСІ КОНТАКТИ".center(60))
        print("=" * 60)
        
        if not self.book.contacts:
            print("Адресна книга порожня.")
        else:
            print(self.book)
    
    def search_contacts(self):
        """Пошук контактів за запитом."""
        print("\n--- Пошук контакту ---")
        query = input("Введіть ім'я, телефон або email для пошуку: ").strip()
        
        results = self.book.search(query)
        
        if results:
            print(f"\n✓ Знайдено {len(results)} контакт(ів):\n")
            for record in results:
                print(str(record))
                print("-" * 60)
        else:
            print(f"✗ Контактів за запитом '{query}' не знайдено.")
    
    def show_statistics(self):
        """Показує статистику адресної книги."""
        print("\n" + "=" * 60)
        print("📊 СТАТИСТИКА".center(60))
        print("=" * 60)
        
        total_contacts = len(self.book.contacts)
        total_phones = sum(len(r.phones) for r in self.book.contacts.values())
        total_emails = sum(len(r.emails) for r in self.book.contacts.values())
        contacts_with_birthday = sum(1 for r in self.book.contacts.values() if r.birthday)
        contacts_with_address = sum(1 for r in self.book.contacts.values() if r.address)
        
        print(f"Всього контактів: {total_contacts}")
        print(f"Всього телефонів: {total_phones}")
        print(f"Всього email адрес: {total_emails}")
        print(f"Контактів з днем народження: {contacts_with_birthday}")
        print(f"Контактів з адресою: {contacts_with_address}")
        
        if total_contacts > 0:
            print(f"\nСередньо телефонів на контакт: {total_phones / total_contacts:.2f}")
            print(f"Середньо email на контакт: {total_emails / total_contacts:.2f}")
    
    def show_file_info(self):
        """Показує інформацію про файл збереження."""
        print("\n" + "=" * 60)
        print("💾 ІНФОРМАЦІЯ ПРО ФАЙЛ".center(60))
        print("=" * 60)
        print(f"Назва файлу: {self.storage.filename}")
        print(f"Файл існує: {'✓ Так' if self.storage.file_exists() else '✗ Ні'}")
        print(f"Розмір файлу: {self.storage.get_file_size()}")
    
    def save_and_exit(self):
        """Зберігає дані та виходить із застосунку."""
        print("\n--- Вихід ---")
        self.storage.save(self.book)
        print("✓ До побачення!")
        self.running = False
    
    def run(self):
        """Запускає головний цикл застосунку."""
        print("\n🎉 Ласкаво просимо до Адресної Книги!")
        print(f"Контактів завантажено: {len(self.book.contacts)}")
        
        while self.running:
            try:
                self.display_menu()
                choice = input("Виберіть дію (1-9): ").strip()
                
                if choice == "1":
                    self.add_contact()
                elif choice == "2":
                    self.find_contact()
                elif choice == "3":
                    self.edit_contact()
                elif choice == "4":
                    self.delete_contact()
                elif choice == "5":
                    self.show_all_contacts()
                elif choice == "6":
                    self.search_contacts()
                elif choice == "7":
                    self.show_statistics()
                elif choice == "8":
                    self.show_file_info()
                elif choice == "9":
                    self.save_and_exit()
                else:
                    print("✗ Невідома команда. Спробуйте ще раз.")
            
            except KeyboardInterrupt:
                print("\n\n--- Програма переривається ---")
                confirm = input("Зберегти дані перед виходом? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.storage.save(self.book)
                print("✓ До побачення!")
                break
            except Exception as e:
                print(f"✗ Виникла помилка: {e}")


def main():
    """Точка входу в програму."""
    app = AddressBookApp("addressbook.pkl")
    app.run()


if __name__ == "__main__":
    main()