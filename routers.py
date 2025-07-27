from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.formatting import as_marked_list

from database.get_towns import orm_get_town, orm_towns, orm_select_region
from kb import inline_kb
from weather import weather_town_one_day, weather_days

private_router = Router()

@private_router.message(CommandStart())
async def start_bot(message:Message):
    await message.answer("Погода на сейчас или на 5 дней вперед?",
                         reply_markup=inline_kb(
                             btns={"Погода на сейчас":"now_reg_"+str(message.message_id),"Погода на 5 дней":"5days_reg_"+str(message.message_id)},
                             sizes=(2,)))

@private_router.callback_query(F.data.startswith("restart"))
async def start_bot(query:CallbackQuery):
    t,id = query.data.split("_")
    await query.message.edit_text("Погода на сейчас или на 5 дней вперед?",
                         reply_markup=inline_kb(
                             btns={"Погода на сейчас":"now_reg_"+id,"Погода на 5 дней":"5days_reg_"+id},
                             sizes=(2,)),inline_message_id=id)


@private_router.callback_query(F.data.startswith("now_reg"))
async def now_reg_weather(query:CallbackQuery,session: AsyncSession):

    t,text, id = query.data.split("_")
    res = await orm_towns(session)
    regions = []
    for reg in res:
        regions.append(reg.region)

    btns = {region: "now_town_" + region+"_"+id for region in regions}
    await query.message.edit_text("Выберите область, в которой находиться ваш город",
                                  reply_markup=inline_kb(btns=btns,sizes=(4,)),
                                  inline_message_id=id)
    await query.answer()


@private_router.callback_query(F.data.startswith("now_town"))
async def now_town_weather(query:CallbackQuery,session: AsyncSession):
    t,text,region,id = query.data.split("_")
    res = await orm_select_region(session,region)
    towns = []
    for town in res:
        towns.append(town.name)
    btns = {town: "now_res_"+town+"_"+id for town in towns}

    await query.message.edit_text("Выберите город, в котором хотите узнать погоду",
                                  reply_markup=inline_kb(btns=btns,sizes=(4,)),
                                  inline_message_id=id)
    await  query.answer()

@private_router.callback_query(F.data.startswith("now_res"))
async def now_town_weather(query:CallbackQuery):
    t, text, town, id = query.data.split("_")
    weather = weather_town_one_day(town)
    await query.message.edit_text(weather,inline_message_id=id,
                                  reply_markup=inline_kb(btns={"Назад":"restart_"+id},sizes=(1,)))
    await query.answer()




@private_router.callback_query(F.data.startswith("5days_reg"))
async def days_reg_weather(query:CallbackQuery,session: AsyncSession):

    t,text, id = query.data.split("_")
    res = await orm_towns(session)
    regions = []
    for reg in res:
        regions.append(reg.region)

    btns = {region: "5days_town_" + region+"_"+id for region in regions}
    await query.message.edit_text("Выберите область, в которой находиться ваш город",
                                  reply_markup=inline_kb(btns=btns,sizes=(4,)),
                                  inline_message_id=id)
    await query.answer()


@private_router.callback_query(F.data.startswith("5days_town"))
async def days_town_weather(query:CallbackQuery,session: AsyncSession):
    t,text,region,id = query.data.split("_")
    res = await orm_select_region(session,region)
    towns = []
    for town in res:
        towns.append(town.name)
    btns = {town: "5days_res_"+town+"_"+id for town in towns}

    await query.message.edit_text("Выберите город, в котором хотите узнать погоду",
                                  reply_markup=inline_kb(btns=btns,sizes=(4,)),
                                  inline_message_id=id)
    await  query.answer()

@private_router.callback_query(F.data.startswith("5days_res"))
async def days_town_weather(query:CallbackQuery):
    t, text, town, id = query.data.split("_")
    weather = weather_days(town)
    text = as_marked_list(*weather,
                          marker="• ")
    await query.message.edit_text(text=text.as_html(),inline_message_id=id,
                                  reply_markup=inline_kb(btns={"Назад":"restart_"+id},sizes=(1,)))
    await query.answer()