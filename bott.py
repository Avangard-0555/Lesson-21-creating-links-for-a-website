from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from number_analysis import NumberAnalyzer

TOKEN = '7564372102:AAEfE-VxNcmlzrTFDQZAqHqOoLYYpVJdw4A'

class IntelligentBot:
    def __init__(self):
        self.number_analyzer = NumberAnalyzer()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            ["Ввести диапазон", "Результат"],
            ["Стоп"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        if user_input == "Ввести диапазон":
            await update.message.reply_text("Введите минимальное и максимальное число через пробел.")
            context.user_data['state'] = 'set_range'
        elif user_input == "Результат":
            if 'range' in context.user_data:
                min_num, max_num = context.user_data['range']
                predicted_number = self.number_analyzer.predict_next_number([min_num, max_num])
                await update.message.reply_text(f"Предсказанная цифра: {predicted_number:.2f}")

                keyboard = [
                    ["Далее", "Пропустить", "Стоп"]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
                await update.message.reply_text("Что делать дальше?", reply_markup=reply_markup)

                context.user_data['predicted_number'] = predicted_number
                context.user_data['state'] = 'wait_for_confirmation'
            else:
                await update.message.reply_text("Сначала нужно ввести диапазон.")

        elif user_input == "Стоп":
            await update.message.reply_text("Бот остановлен.")
            context.user_data.clear()

    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        state = context.user_data.get('state', '')

        if state == 'set_range':
            try:
                min_num, max_num = map(float, user_input.split())
                context.user_data['range'] = (min_num, max_num)
                await update.message.reply_text(f"Диапазон установлен: {min_num} - {max_num}")
                await self.start(update, context)
            except ValueError:
                await update.message.reply_text("Пожалуйста, введите два числа через пробел.")

        elif state == 'wait_for_confirmation':
            predicted_number = context.user_data['predicted_number']
            if user_input.lower() == str(predicted_number):
                # Запоминаем цифру, если она совпала
                context.user_data['memory'] = context.user_data.get('memory', []) + [predicted_number]
                await update.message.reply_text(f"Цифра {predicted_number} сохранена в памяти.")
                # Отправляем следующее предсказание
                min_num, max_num = context.user_data['range']
                predicted_number = self.number_analyzer.predict_next_number([min_num, max_num])
                await update.message.reply_text(f"Предсказанная цифра: {predicted_number:.2f}")
            elif user_input.lower() == "пропустить":
                await update.message.reply_text("Цифра пропущена.")
                min_num, max_num = context.user_data['range']
                predicted_number = self.number_analyzer.predict_next_number([min_num, max_num])
                await update.message.reply_text(f"Предсказанная цифра: {predicted_number:.2f}")

            keyboard = [
                ["Далее", "Пропустить", "Стоп"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
            await update.message.reply_text("Что делать дальше?", reply_markup=reply_markup)

        elif user_input.lower() == 'стоп':
            await update.message.reply_text("Бот остановлен.")
            context.user_data.clear()

        else:
            await update.message.reply_text("Пожалуйста, выберите одну из опций ниже.")

if __name__ == '__main__':
    intelligent_bot = IntelligentBot()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', intelligent_bot.start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, intelligent_bot.button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, intelligent_bot.message_handler))

    print("Бот запущен...")
    app.run_polling()
