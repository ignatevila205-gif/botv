import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict

TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

questions = [
    {
        "text": "🧠 Тест «Деньги и мышление»\n\nОтвечайте быстро. Первый импульс — самый честный.\n\n1. Когда вы думаете о больших деньгах, в теле скорее:",
        "options": [
            "А. Напряжение",
            "Б. Интерес и азарт",
            "В. Спокойствие",
            "Г. Сомнение и усталость"
        ]
    },
    {
        "text": "2. Деньги чаще всего приходят к тем, кто:",
        "options": [
            "А. Много работает",
            "Б. Рискует",
            "В. Разрешил себе иметь",
            "Г. Родился в правильной семье"
        ]
    },
    {
        "text": "3. Если деньги «застревают», вы скорее думаете:",
        "options": [
            "А. Сейчас не время",
            "Б. Надо еще учиться",
            "В. Что-то во мне мешает",
            "Г. В стране/мире сложная ситуация"
        ]
    },
    {
        "text": "4. Большая сумма для вас — это:",
        "options": [
            "А. Ответственность",
            "Б. Свобода",
            "В. Опасность",
            "Г. Мечта, но далекая"
        ]
    },
    {
        "text": "5. Когда деньги приходят легко, внутри:",
        "options": [
            "А. Радость",
            "Б. Недоверие",
            "В. Чувство вины",
            "Г. Желание быстрее потратить"
        ]
    },
    {
        "text": "6. Если вам предложат доход «выше вашего уровня», первая мысль:",
        "options": [
            "А. «Я еще не готова»",
            "Б. «Интересно»",
            "В. «Это случайность»",
            "Г. «А вдруг не справлюсь»"
        ]
    },
    {
        "text": "7. Деньги — это про:",
        "options": [
            "А. Безопасность",
            "Б. Власть",
            "В. Энергию",
            "Г. Постоянную борьбу"
        ]
    },
    {
        "text": "8. Когда вы платите за себя (обучение, сессии), вы:",
        "options": [
            "А. Долго сомневаетесь",
            "Б. Чувствуете внутренний рост",
            "В. Жалеете после",
            "Г. Сначала покупаете, потом думаете"
        ]
    },
    {
        "text": "9. Ваш реальный доход сейчас:",
        "options": [
            "А. Ниже потенциала",
            "Б. Соответствует этапу",
            "В. Выше ожиданий",
            "Г. Сложно определить"
        ]
    },
    {
        "text": "10. Фраза, которая откликается сильнее всего:",
        "options": [
            "А. «Мне нужно разрешить себе больше»",
            "Б. «Я зарабатываю через усилие»",
            "В. «Деньги любят спокойствие»",
            "Г. «Со мной что-то не так»"
        ]
    }
]

results = {
    "А": {
        "text": "У вас мышление долга и напряжения.\nДеньги связаны с «надо», а не с «можно».\nДоход растет, когда уходит внутренний контроль.",
        "photo_url": "https://example.com/photo_a.jpg"
    },
    "Б": {
        "text": "Есть ресурс и потенциал,\nно доход нестабилен — деньги приходят волнами.\nНужно закрепить состояние «я выдерживаю больше».",
        "photo_url": "https://example.com/photo_b.jpg"
    },
    "В": {
        "text": "Вы близки к зрелому денежному мышлению,\nно есть бессознательные блоки на «легко» и «много».",
        "photo_url": "https://example.com/photo_v.jpg"
    },
    "Г": {
        "text": "Деньги для вас — зона тревоги и неопределенности.\nВы чувствуете, что причина не снаружи, а внутри — и это ключ.",
        "photo_url": "https://example.com/photo_g.jpg"
    }
}

user_states = defaultdict(lambda: {'current_question': 0, 'answers': defaultdict(int)})

CONSULT_URL = "https://t.me/martynova_ludmila"

def get_keyboard(q_num, options):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i, _ in enumerate(options):
        letter = chr(1040 + i)
        callback = f"ans_{q_num}_{letter}"
        buttons.append(InlineKeyboardButton(letter, callback_data=callback))
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'current_question': 0, 'answers': defaultdict(int)}

    welcome_text = (
        "🌟 *Привет! Добро пожаловать в тест «Деньги и мышление»* 🌟\n\n"
        "💰 Этот тест поможет понять ваше отношение к деньгам за 10 быстрых вопросов.\n\n"
        "⚡ Отвечайте *первым импульсом* — он самый честный!\n\n"
        "*Готовы узнать свое денежное мышление?*\n\n"
        "Нажмите кнопку ниже 👇"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Начать тест", callback_data="start_test"))
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'start_test')
def start_test(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    send_question(call.message.chat.id, user_id, 0)
    bot.delete_message(call.message.chat.id, call.message.message_id)

def send_question(chat_id, user_id, q_num):
    if q_num < len(questions):
        q = questions[q_num]
        options_text = "\n".join(q['options'])
        text = f"*Вопрос {q_num + 1}:*\n\n{q['text']}\n\n{options_text}"
        markup = get_keyboard(q_num, q['options'])
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    else:
        show_result(chat_id, user_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ans_'))
def handle_answer(call):
    bot.answer_callback_query(call.id)
    _, q_num_str, answer = call.data.split('_')
    user_id = call.from_user.id

    state = user_states[user_id]
    state['answers'][answer] += 1
    state['current_question'] += 1

    send_question(call.message.chat.id, user_id, state['current_question'])

def show_result(chat_id, user_id):
    state = user_states[user_id]

    max_count = 0
    most_common = 'А'
    for ans, count in state['answers'].items():
        if count > max_count:
            max_count = count
            most_common = ans

    result = results.get(most_common, results['А'])
    result_text = result["text"]
    photo_url = result.get("photo_url")

    full_text = f"""🔍 *Расшифровка (очень честно)*

{result_text}
"""

    try:
        if photo_url:
            bot.send_photo(
                chat_id,
                photo=photo_url,
                caption=full_text,
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                chat_id,
                full_text,
                parse_mode='Markdown'
            )
    except Exception:
        bot.send_message(
            chat_id,
            full_text,
            parse_mode='Markdown'
        )

    consult_markup = InlineKeyboardMarkup()
    consult_markup.add(
        InlineKeyboardButton("Записаться на консультацию", url=CONSULT_URL)
    )

    bot.send_message(
        chat_id,
        "Ты можешь записаться на бесплатную 15 минутную консультацию 👇",
        reply_markup=consult_markup
    )

    del user_states[user_id]

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()