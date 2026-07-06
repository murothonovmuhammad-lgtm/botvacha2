import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from inlinekeyboard import mainMenu, taomMenu, ichimlikMenu
from state import order
from dp import add_order, init_db, get_user_order_count, clear_orders, delete_one_order

TOKEN = "8643222844:AAGrDiW9axIOXrNvnRNhn6vCL5Lo4V8xYas"
ADMIN_ID = 7038624148
dp = Dispatcher()

prices = {
    "Burger": 15000, "Gamburger": 18000, "Hotdog": 10000, "Chizburger": 24000,
    "Minilavash": 19000, "Lavash": 23000, "Pepsi": 9000, "Sok": 5000,
    "Coca-Cola": 17000, "Sprite": 15000, "Kofe": 8000, "Suv": 2000,
}

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Ro'yxatni ko'rmoqchimisiz pastga qarang", reply_markup=mainMenu)

@dp.callback_query(F.data == "🍽 Taomlar")
async def taomlar(call: CallbackQuery): 
    await call.message.edit_text("Bizda bor taomlar 👇", reply_markup=taomMenu)

@dp.callback_query(F.data == "🥤 Ichimliklar")
async def ichimliklar(call: CallbackQuery):
    await call.message.edit_text("Bizda bor ichimliklar 👇", reply_markup=ichimlikMenu)

@dp.callback_query(F.data == "Orqaga")
async def orqaga_handler(call: CallbackQuery):
    await call.message.edit_text("Asosiy menyu", reply_markup=mainMenu)

@dp.callback_query(F.data == "Korzinka")
async def show_handler(query: CallbackQuery, state: FSMContext):
    await state.clear()
    orders = get_user_order_count(tg_id=query.from_user.id)
    if orders:
        text = "Buyurtmalaringiz: \n"
        total_price = 0
        for i, (product, count) in enumerate(orders, 1):
            price = prices.get(product, 0) * count
            total_price += price
            text += f'{i}. {product} 🫴 {count} ta {price} so\'m \n'
        text += f'\n 💰 Jami summa {total_price} so\'m bo\'ldi'
    else:
        text = "Siz hali buyurtma bermadingiz"
    
    await query.message.edit_text(text, reply_markup=mainMenu)

@dp.callback_query(F.data == "Toza")
async def tozalash(query: CallbackQuery):
    clear_orders(tg_id=query.from_user.id)
    await query.message.edit_text("Korzinka tozalandi", reply_markup=mainMenu)

@dp.callback_query(F.data == "delete")
async def delete(query: CallbackQuery):  
    orders = get_user_order_count(tg_id=query.from_user.id)
    if not orders:
        await query.message.edit_text("❌ Siz hali buyurtma bermadingiz-ku ❌", reply_markup=mainMenu)
        return

    buttons = [[InlineKeyboardButton(text=f'{p} {c} ta', callback_data=f"del_{p}")] for p, c in orders]
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data="Orqaga")])    
    
    await query.message.edit_text(
        "Qaysi mahsulotni o'chirmoqchisiz ?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(F.data.startswith("del_"))
async def delete_item(query: CallbackQuery):
    product = query.data[4:]
    delete_one_order(tg_id=query.from_user.id, product=product)
    await query.answer(f"❌ {product} o'chirildi")
    await delete(query)

@dp.callback_query(F.data == "Tasdiqlash")
async def tasdiqlash(query: CallbackQuery, state: FSMContext):
    orders = get_user_order_count(tg_id=query.from_user.id)
    if not orders:
        await query.answer("❌❌ Siz xali buyurtma bermadingiz-ku ❌❌")
        return
    await query.message.answer("Telefon raqamingizni kiriting")
    await state.set_state(order.telefon)

@dp.message(order.telefon)
async def phone(msg: Message, state: FSMContext):
    await state.update_data(telefon1=msg.text)
    await msg.answer("Yaxshi, endi manzilingizni kiriting")
    await state.set_state(order.manzil)

@dp.message(order.manzil)
async def manzil(msg: Message, state: FSMContext):
    await state.update_data(manzil1=msg.text)
    data = await state.get_data()
    orders = get_user_order_count(tg_id=msg.from_user.id)
    
    text = "Buyurtmalaringiz:\n\n"
    text += f"User: @{msg.from_user.username}\n"
    text += f"Telefon: {data['telefon1']}\n"
    text += f"Manzil: {data['manzil1']}\n"
    for product, count in orders:
        text += f"\n{product} {count} ta"
    
    text += "\n\nBuyurtmalaringizni jo'natasizmi ?"
    confirmMenu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ha ✅", callback_data="Ha")],
        [InlineKeyboardButton(text="Yo'q ❌", callback_data="Yoq")]
    ])
    await msg.answer(text, reply_markup=confirmMenu)

@dp.callback_query(F.data == "Ha")
async def ha(query: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    orders = get_user_order_count(tg_id=query.from_user.id)
    
    text = "‼️‼️ Diqqat yangi buyurtma ‼️‼️\n\n"
    text += f"User: @{query.from_user.username}\n"
    text += f"Telefon: {data.get('telefon1')}\n"
    text += f"Manzil: {data.get('manzil1')}\n"
    for product, count in orders:
        text += f"\n{product} {count} ta"
    
    await bot.send_message(ADMIN_ID, text, reply_markup=admin_keyboard(query.from_user.id))
    clear_orders(tg_id=query.from_user.id)
    await query.message.edit_text("✅ Buyurtmalaringiz Adminga jo'natildi ✅", reply_markup=mainMenu)
    await state.clear()

@dp.callback_query(F.data == "Yoq")
async def yoq(query: CallbackQuery, state: FSMContext):
    await query.message.answer("❌ Buyurtmalaringiz bekor qilindi ❌", reply_markup=mainMenu)
    await state.clear()

def admin_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qabul qilish ✅", callback_data=f"accept_{user_id}"),
         InlineKeyboardButton(text="❌ Bekor qilish ❌", callback_data=f"cancel_{user_id}")]
    ])

@dp.callback_query(F.data.startswith("accept_"))
async def accept_order(query: CallbackQuery, bot: Bot):
    user_id = int(query.data.split("_")[1])
    await bot.send_message(user_id, "✅ Buyurtmalaringiz qabul qilindi ✅")
    await query.message.answer("✅ Buyurtma qabul qilindi ✅")

@dp.callback_query(F.data.startswith("cancel_"))
async def cancel_order(query: CallbackQuery, bot: Bot):
    user_id = int(query.data.split("_")[1])
    await bot.send_message(user_id, "❌ Buyurtmalaringiz qabul qilinmadi ❌")
    await query.message.answer("❌ Buyurtma bekor qilindi ❌")

@dp.callback_query()
async def process_callback_all(call: CallbackQuery):
    product = call.data
    if product in prices:
        add_order(tg_id=call.from_user.id, product_name=product)
        await call.answer(f'✅ {product} korzinkaga qo\'shildi')

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Nice try!")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())