import unittest

from typing import Callable
from functools import wraps
import inspect


def strict(func: Callable):
    sig = inspect.signature(func)
    annotations = func.__annotations__
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)

        for name, value in bound_args.arguments.items():
            if name in annotations and not isinstance(value, annotations[name]):
                raise TypeError
        
        return func(*args, **kwargs)
    
    return wrapper


class TestStrictDecorator(unittest.TestCase):
    """Набор тестов для декоратора @strict, проверяющего типы аргументов."""
    
    def test_correct_positional_args(self):
        """Проверка корректной работы с правильными позиционными аргументами.
        
        Тест проверяет, что функция с аннотациями типов:
        - int
        - str 
        - bool
        корректно работает при передаче аргументов правильных типов.
        """
        @strict
        def func(a: int, b: str, c: bool) -> float:
            return 3.14
            
        result = func(1, "hello", True)
        self.assertEqual(result, 3.14, 
                       "Функция должна вернуть 3.14 при корректных аргументах")
    
    def test_incorrect_positional_args_raises_typeerror(self):
        """Проверка вызова TypeError при несоответствии типов позиционных аргументов.
        
        Тест проверяет, что:
        1. При передаче float вместо int для первого аргумента
        2. Возбуждается исключение TypeError
        """
        @strict
        def func(a: int, b: str):
            pass
            
        with self.assertRaises(TypeError, 
                             msg="Должен быть TypeError при неправильном типе позиционного аргумента"):
            func(1.0, "hello")
    
    def test_correct_kwargs(self):
        """Проверка корректной работы с именованными аргументами.
        
        Тест проверяет:
        - Работу функции при передаче именованных аргументов
        - Корректность возвращаемого значения
        """
        @strict
        def func(a: int, b: str):
            return f"{a}{b}"
            
        result = func(a=1, b="2")
        self.assertEqual(result, "12", 
                       "Функция должна вернуть '12' при корректных именованных аргументах")
    
    def test_incorrect_kwargs_raises_typeerror(self):
        """Проверка вызова TypeError при несоответствии типов именованных аргументов.
        
        Тест проверяет:
        1. При передаче int вместо str для параметра b
        2. Возбуждается исключение TypeError
        """
        @strict
        def func(a: int, b: str):
            pass
            
        with self.assertRaises(TypeError,
                             msg="Должен быть TypeError при неправильном типе именованного аргумента"):
            func(a=1, b=2)
    
    def test_mixed_args_kwargs_correct(self):
        """Проверка работы при смешанной передаче позиционных и именованных аргументов.
        
        Тест проверяет:
        - Корректную обработку позиционного первого аргумента
        - Корректную обработку именованных аргументов (b и c)
        - Правильный порядок подстановки аргументов
        """
        @strict
        def func(a: int, b: str, c: float):
            return f"{a}{b}{c}"
            
        result = func(1, c=3.14, b="2")
        self.assertEqual(result, "123.14",
                        "Функция должна корректно обрабатывать смешанные аргументы")
    
    def test_all_guaranteed_types_correct(self):
        """Проверка всех гарантированных типов (bool, int, float, str).
        
        Тест проверяет работу функции с аннотациями всех гарантированных типов:
        - bool
        - int
        - float
        - str
        при передаче корректных аргументов.
        """
        @strict
        def func(a: bool, b: int, c: float, d: str):
            return f"{a}{b}{c}{d}"
            
        result = func(True, 2, 3.14, "4")
        self.assertEqual(result, "True23.144",
                       "Функция должна корректно обрабатывать все гарантированные типы")
        
    def test_all_guaranteed_types_incorrect(self):
        """Проверка всех гарантированных типов с неправильными аргументами.
        
        Тест проверяет:
        1. Передачу аргументов с полностью перепутанными типами
        2. Возникновение TypeError в таком случае
        """
        @strict
        def func(a: bool, b: int, c: float, d: str):
            pass
            
        with self.assertRaises(TypeError,
                             msg="Должен быть TypeError при полном несоответствии типов"):
            func(1, 2.0, "3", True)  # все типы перепутаны

    def test_function_metadata_preserved(self):
        """Проверка сохранения метаданных исходной функции.
        
        Тест проверяет, что декоратор сохраняет:
        - Имя функции
        - Документацию
        - Аннотации
        """
        @strict
        def sample_func(a: int, b: str) -> bool:
            """Тестовая функция для проверки метаданных."""
            return True
            
        self.assertEqual(sample_func.__name__, "sample_func",
                        "Декоратор должен сохранять имя функции")
        self.assertEqual(sample_func.__doc__, "Тестовая функция для проверки метаданных.",
                        "Декоратор должен сохранять документацию")
        self.assertEqual(sample_func.__annotations__, {'a': int, 'b': str, 'return': bool},
                        "Декоратор должен сохранять аннотации")


if __name__ == "__main__":
    unittest.main(verbosity=2)
