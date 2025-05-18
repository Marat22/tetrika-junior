import asyncio
import aiohttp
import aiofiles
import tqdm
from aiohttp import ClientSession, ClientError
from bs4 import BeautifulSoup
import string


ALL_LETTERS = (list(string.ascii_uppercase) + [chr(i) for i in range(1040, 1072)])


async def make_requests() -> None:
    async with ClientSession() as session:
        to_do = [count_one_letter(session, letter)
                 for letter in sorted(ALL_LETTERS)]
        to_do_iter = asyncio.as_completed(to_do)
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(ALL_LETTERS))
        
        async with aiofiles.open("beasts.csv", mode="w", encoding="utf-8") as file:
            for coro in to_do_iter: 
                try:
                    letter, qty = await coro
                    await file.write(f'{letter}, {qty}\n')
                except ClientError as exc:
                    break


                # if error:
                #     status = DownloadStatus.ERROR 
                #     if verbose:
                #         url = str(error.request.url) 
                #         cc = Path(url).stem.upper()  
                #         print(f'{cc} error: {error_msg}')
                # counter[status] += 1

        # try:
        #     asyncio.as_completed(*to_do, )
        # except ClientError:
        #     print("FAILED")


async def count_one_letter(
        session: ClientSession,
        letter: str,
    ) -> tuple[str, int]:
    params = dict(title= "Категория:Животные_по_алфавиту", 
                  pagefrom=letter)
    counter = 0
    while True:
        async with session.get("https://ru.wikipedia.org/w/index.php", params=params) as resp:
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


async def test_count(letter="А"):
    async with ClientSession() as session:
        print(await count_one_letter(session, "А"))


if __name__ == "__main__":
    # asyncio.run(test_count("A"))
    asyncio.run(make_requests())
    
