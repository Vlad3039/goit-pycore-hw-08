
import pickle
import os
from pathlib import Path
from typing import Optional
from models import AddressBook


class AddressBookStorage:
    """Клас для управління збереженням та завантаженням адресної книги."""
    
    def __init__(self, filename: str = "addressbook.pkl"):
        """
        Ініціалізує зберігальище.
        
        Args:
            filename: Назва файлу для збереження (за замовчуванням: addressbook.pkl)
        """
        self.filename = filename
        self.filepath = Path(filename)
    
    def save(self, book: AddressBook) -> bool:
        """
        Зберігає адресну книгу у файл.
        
        Args:
            book: Об'єкт AddressBook для збереження
            
        Returns:
            True якщо збереження успішне, False в іншому випадку
        """
        try:
            with open(self.filepath, "wb") as f:
                pickle.dump(book, f)
            print(f"✓ Адресна книга збережена у файл '{self.filename}'")
            return True
        except Exception as e:
            print(f"✗ Помилка при збереженні: {e}")
            return False
    
    def load(self) -> AddressBook:
        """
        Завантажує адресну книгу з файлу.
        
        Returns:
            Об'єкт AddressBook. Якщо файл не існує, повертає нову адресну книгу.
        """
        try:
            if self.filepath.exists():
                with open(self.filepath, "rb") as f:
                    book = pickle.load(f)
                print(f"✓ Адресна книга завантажена з файлу '{self.filename}'")
                return book
            else:
                print(f"ℹ Файл '{self.filename}' не знайдено. Створюється нова адресна книга.")
                return AddressBook()
        except Exception as e:
            print(f"✗ Помилка при завантаженні: {e}")
            print("ℹ Створюється нова адресна книга.")
            return AddressBook()
    
    def file_exists(self) -> bool:
        """Перевіряє, чи існує файл адресної книги."""
        return self.filepath.exists()
    
    def get_file_size(self) -> str:
        """Повертає розмір файлу в читаному форматі."""
        if self.filepath.exists():
            size_bytes = self.filepath.stat().st_size
            
            for unit in ['B', 'KB', 'MB']:
                if size_bytes < 1024:
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024
            
            return f"{size_bytes:.2f} GB"
        return "Файл не існує"
    
    def delete_file(self) -> bool:
        """Видаляє файл адресної книги."""
        try:
            if self.filepath.exists():
                self.filepath.unlink()
                print(f"✓ Файл '{self.filename}' видалено.")
                return True
            else:
                print(f"ℹ Файл '{self.filename}' не існує.")
                return False
        except Exception as e:
            print(f"✗ Помилка при видаленні файлу: {e}")
            return False