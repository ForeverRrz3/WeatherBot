from sqlalchemy.ext.asyncio import AsyncSession
from requests import *
from bs4 import BeautifulSoup
from database.model import Base_town
from sqlalchemy import select,update,delete

async def orm_get_town(session: AsyncSession):
    headers = {"User-Agent":
                   "mozilla/5.0 (Windows; U; Windows NT 6.1; en-Us; rv:1.9.1.5"}

    url = "https://ru.m.wikipedia.org/wiki/Список_городов_России"
    res = get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    town = {}
    data = soup.find_all("tr")

    for i in data[1:]:
        try:
            info = i.find_all("td")
            town[info[-6].text] = town.get(info[-6].text, []) + [info[-7].text]
            obj = Base_town(name=info[-7].text,region=info[-6].text)
            session.add(obj)
        except IndexError:
            break

    await session.commit()

async def orm_towns(session:AsyncSession):
    query = select(Base_town)
    result = await session.execute(query)
    return result.scalars().all()



async def orm_select_region(session:AsyncSession,region:str):
    query = select(Base_town).where(Base_town.region == region)
    result = await session.execute(query)
    return result.scalars().all()