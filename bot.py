import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict


TOKEN = '8375852663:AAFFCpAPGqsyFmYeud7G2Cps9SYWHmvRWms'
bot = telebot.TeleBot(TOKEN)


# Полный список вопросов
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
    'А': "У вас мышление долга и напряжения.\nДеньги связаны с «надо», а не с «можно».\nДоход растет, когда уходит внутренний контроль.",
    'Б': "Есть ресурс и потенциал,\nно доход нестабилен — деньги приходят волнами.\nНужно закрепить состояние «я выдерживаю больше».",
    'В': "Вы близки к зрелому денежному мышлению,\nно есть бессознательные блоки на «легко» и «много».",
    'Г': "Деньги для вас — зона тревоги и неопределенности.\nВы чувствуете, что причина не снаружи, а внутри — и это ключ."
}


user_states = defaultdict(lambda: {'current_question': 0, 'answers': defaultdict(int)})


def get_keyboard(q_num, options):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i, opt in enumerate(options):
        # Русские буквы А,Б,В,Г (Юникод 1040+)
        letter = chr(1040 + i)  # 'А', 'Б', 'В', 'Г'
        callback = f"ans_{q_num}_{letter}"
        # На кнопке только буква
        buttons.append(InlineKeyboardButton(letter, callback_data=callback))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = {'current_question': 0, 'answers': defaultdict(int)}
    
    welcome_text = """🌟 *Привет! Добро пожаловать в тест «Деньги и мышление»* 🌟


💰 Этот тест поможет понять ваше отношение к деньгам за 10 быстрых вопросов.


⚡ Отвечайте *первым импульсом* — он самый честный!


*Готовы узнать свое денежное мышление?*


Нажмите кнопку ниже 👇"""
    
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
    state = user_states[user_id]
    if q_num < len(questions):
        q = questions[q_num]
        # Собираем текст: вопрос + варианты по строкам
        options_text = "\n".join(q['options'])
        text = f"**Вопрос {q_num+1}:**\n\n{q['text']}\n\n{options_text}"
        markup = get_keyboard(q_num, q['options'])
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    else:
        show_result(chat_id, user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ans_'))
def handle_answer(call):
    bot.answer_callback_query(call.id)
    _, q_num_str, answer = call.data.split('_')
    q_num = int(q_num_str)
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
    
    result_text = results.get(most_common, results['А'])
    full_text = f"""🔍 *Расшифровка (очень честно)*


{result_text}


⸻


🔥 Ты чувствуешь, что можешь больше, но что-то внутри будто не отпускает? Это не случайно.

Это твоя внутренняя система держит старый сценарий.

На сессии я помогу его разорвать — мягко, но необратимо.

Если внутри щёлкнуло хоть на секунду — пиши. Это знак, что пора.
"""

    # Кнопка с ссылкой на аккаунт
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "✉️ Записаться на консультацию",
            url="https://t.me/martynova_ludmila"
        )
    )

    bot.send_message(chat_id, full_text, parse_mode='Markdown', reply_markup=markup)
    del user_states[user_id]


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
