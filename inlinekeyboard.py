from aiogram.types import InlineKeyboardButton,  InlineKeyboardMarkup

mainMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍽 Taomlar", callback_data="🍽 Taomlar"),
            InlineKeyboardButton(text="🥤 Ichimliklar", callback_data="🥤 Ichimliklar")
        ],
        [
            
            InlineKeyboardButton(text="🛒 Korzinka", callback_data="Korzinka"),
            InlineKeyboardButton(text="🛒❌ Korzinkani bo'shatish", callback_data="Toza")

        ],
        [
            InlineKeyboardButton(text="🗑 Mahsulotni tanlab o'chirish", callback_data="delete"),
            InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="Tasdiqlash")
        ],
    ]
)

taomMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍔 Burger 15000", callback_data="Burger"),
            InlineKeyboardButton(text="🍔 Gamburger 18000", callback_data="Gamburger"),
            InlineKeyboardButton(text="🌭 Hotdog 10000", callback_data="Hotdog"),
        ],
        [
            InlineKeyboardButton(text="🍔 Chizburger 24000", callback_data="Chizburger"),
            InlineKeyboardButton(text="🌮 Minilavash 19000", callback_data="Minilavash"),
            InlineKeyboardButton(text="🌮 Lavash 23000", callback_data="Lavash"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga qaytish" , callback_data="Orqaga")
        ]
    ]
)
ichimlikMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍷 Pepsi 9000", callback_data="Pepsi"),
            InlineKeyboardButton(text="🧃 Sok 5000", callback_data="Sok"),
            InlineKeyboardButton(text="🍹 Coca-Cola 17000", callback_data="Coca-Cola"),
        ],
        [
            InlineKeyboardButton(text="🍾 Sprite 15000", callback_data="Sprite"),
            InlineKeyboardButton(text="☕️ Cofe 8000", callback_data="Kofe"),
            InlineKeyboardButton(text="💧 Suv 2000", callback_data="Suv"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga qaytish" , callback_data="Orqaga")
        ]
    ]
)