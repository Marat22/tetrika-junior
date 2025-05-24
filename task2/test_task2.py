from aiohttp import ClientSession
import unittest
from unittest.mock import AsyncMock
from aiohttp import ClientSession

try:
    from solution import count_one_letter
except ModuleNotFoundError:
    from task2.solution import count_one_letter


class TestCountOneLetter(unittest.IsolatedAsyncioTestCase):
    async def test_count_one_letter_normal_case(self):
        """Проверяет случай, когда достаточно одного запроса для получения всех животных по букве."""
        mock_responses = [
            """
            <div class="mw-category mw-category-columns">
                <li>Аардоникс</li>
                <li>Абботины</li>
                <li>Бабакотии</li>
            </div>
            """,
            """
            <div class="mw-category mw-category-columns">
                <li>ZebЗабайкальский солонгойra</li>
            </div>
            """
        ]
        
        # Мокаем сессию
        mock_session = AsyncMock(ClientSession)
        mock_session.get.return_value.__aenter__.return_value.text.side_effect = mock_responses
        
        letter, count = await count_one_letter(mock_session, "А")
        
        self.assertEqual(letter, "А")
        self.assertEqual(count, 2)

        # Проверяем, что запрос был сделан только один раз
        self.assertEqual(mock_session.get.call_count, 1)
    
        mock_session.get.assert_called_once_with(
            "https://ru.wikipedia.org/w/index.php",
            params={
                "title": "Категория:Животные_по_алфавиту",
                "pagefrom": "А"
            },
            timeout=10
        )


    async def test_count_one_letter_multiple_pages(self):
        """Проверяет случай, когда животные находятся на нескольких страницах."""
        mock_responses = [
            """
            <div class="mw-category mw-category-columns">
                <li>А1</li>
                <li>А2</li>
                <li>А3</li>
                <li>А4</li>  # Должен быть последним на странице
            </div>
            """,
            """
            <div class="mw-category mw-category-columns">
                <li>А5</li>
                <li>А6</li>
                <li>Б</li>  # Должен остановить подсчет
            </div>
            """,
            """
            <div class="mw-category mw-category-columns">
                <li>В</li>  # Не должно учитываться
            </div>
            """
        ]
        
        mock_session = AsyncMock(ClientSession)
        mock_session.get.return_value.__aenter__.return_value.text.side_effect = mock_responses
        
        letter, count = await count_one_letter(mock_session, "А")
        
        self.assertEqual(letter, "А")
        self.assertEqual(count, 6)
        
        
    async def test_count_one_letter_no_animals(self):
        """Проверяет случай, когда нету животных на заданную букву."""
        mock_response = """
            <div class="mw-category mw-category-columns">
                <li>Bear</li>
                <li>Cat</li>
            </div>
        """
        
        mock_session = AsyncMock(ClientSession)
        mock_session.get.return_value.__aenter__.return_value.text.return_value = mock_response
        
        letter, count = await count_one_letter(mock_session, "A")
        
        self.assertEqual(letter, "A")
        self.assertEqual(count, 0)
        
    async def test_count_one_letter_empty_response(self):
        """Проверяет случай, когда в ответ на запрос не пришло никаких животных."""
        mock_response = "<html></html>"
        
        mock_session = AsyncMock(ClientSession)
        mock_session.get.return_value.__aenter__.return_value.text.return_value = mock_response
        
        letter, count = await count_one_letter(mock_session, "A")
        
        self.assertEqual(letter, "A")
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
