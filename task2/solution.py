import asyncio
import aiofiles
import os
import string
import tqdm

from aiohttp import ClientSession, ClientError
from bs4 import BeautifulSoup
from pathlib import Path


ALL_LETTERS = (list(string.ascii_uppercase) + [chr(i) for i in range(1040, 1072)])


async def write_animals_letters(output_file: Path, ordered: bool = False, write_zero: bool = True) -> None:
    """Записывает количество животных на каждую букву алфавита на русскоязычной википедии.
    
    Args:
        output_file: Путь к файлу, в которой будет записан результат.
        ordered: True - записывать буквы в алфавитном порядке. 
            False - записывать буквы в порядке их парсинга (так быстрее).
        write_zero: True - записывать буквы число которых равно 0.
            False - записывать только те буквы, по которым есть более одного животного.
    """
    if ordered:
        ordered_results = []
    async with ClientSession() as session:
        to_do = [asyncio.create_task(count_one_letter(session, letter))
                 for letter in sorted(ALL_LETTERS)]
        to_do_iter = asyncio.as_completed(to_do)
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(ALL_LETTERS))
        
        if not ordered:
            async with aiofiles.open(output_file, mode="w", encoding="utf-8") as file:
                for coro in to_do_iter:
                    try:
                        letter, qty = await coro
                        await write_result(file, letter, qty, write_zero)
                    except ClientError as exc:
                        for task in to_do:
                            task.cancel()
                        await asyncio.gather(*to_do, return_exceptions=True)
                        raise exc
        if ordered:
            for coro in to_do_iter:
                ordered_results.append(await coro)
    if ordered:
        async with aiofiles.open(output_file, mode="w", encoding="utf-8") as file:
            for res in sorted(ordered_results, key=lambda x: x[0]):
                letter, qty = res
                await write_result(file, letter, qty, write_zero)


async def write_result(file, letter: str, qty: int, write_zero: bool):
    """Записывает количество повторений буквы в файл.
    
    Args:
        file: Файл для записи.
        letter: Буква.
        qty: Количество животных.
        write_zero: True - записывать буквы, по которым `qty` = 0.
            False - НЕ записывать буквы, по которым `qty` = 0.

    """
    if not write_zero and not qty:
        return
    await file.write(f'{letter}, {qty}\n')


async def count_one_letter(
        session: ClientSession,
        letter: str,
    ) -> tuple[str, int]:
    """Возвращает количество животных по одной букве.
    
    Args:
        session: Сессия для запросов.
        letter: Буква, по которой требуется получить кол-во животных.
    
    Returns:
        буква, количество животных
    """
    params = dict(title= "Категория:Животные_по_алфавиту", 
                  pagefrom=letter)
    counter = 0
    while True:
        async with session.get("https://ru.wikipedia.org/w/index.php", params=params, timeout=10) as resp:
            html = await resp.text()

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(attrs={"class": "mw-category mw-category-columns"})

        if title is None:
            return letter, counter

        animals_on_page = title.find_all("li")


        if not animals_on_page:
            return letter, counter

        for i in animals_on_page:
            last_added_animal = i.string
            if not last_added_animal.startswith(letter):
                return letter, counter
            counter += 1

        params["pagefrom"] = last_added_animal + ' '


if __name__ == "__main__":
    # ПРИМЕЧАНИЕ
    # 1. Я не был уверен, нужно ли записывать данные алфавитном порядке, поэтому добавил в функцию флаг параметр `ordered`
    # 2. Я не был уверен, нужно ли записывать буквы, по которым количество животных равно нулю, поэтому добавил флаг параметр `write_zero`
    asyncio.run(
        write_animals_letters(
            output_file=Path(os.path.realpath(__file__)) / "beasts.csv"
        )
    )
