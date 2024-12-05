import requests
from bs4 import BeautifulSoup


class UrlAnalyzer:
    def __init__(self):
        pass

    def analyze_url(self, url):
        """Анализирует URL и извлекает информацию."""
        try:
            response = requests.get(url)
            from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
            from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, \
                ContextTypes, filters

            from number_analysis import NumberAnalyzer
            from url_analysis import UrlAnalyzer

            # Ваш токен Telegram-бота
            TOKEN = '7564372102:AAEfE-VxNcmlzrTFDQZAqHqOoLYYpVJdw4A'

            class IntelligentBot:
                def __init__(self):
                    self.number_analyzer = NumberAnalyzer()
                    self.url_analyzer = UrlAnalyzer()

                async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    # Главное меню с кнопками
                    keyboard = [
                        ["Анализировать числа", "Анализировать URL"]
                    ]
                    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
                    await update.message.reply_text('Что хотите проанализировать?', reply_markup=reply_markup)

                async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    # Обрабатываем кнопки с выбранными действиями
                    user_input = update.message.text
                    if user_input == 'Анализировать числа':
                        await update.message.reply_text("Введите числа для анализа:")
                        context.user_data['state'] = 'numbers'
                    elif user_input == 'Анализировать URL':
                        await update.message.reply_text("Введите URL для анализа:")
                        context.user_data['state'] = 'url'

                async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    user_input = update.message.text
                    state = context.user_data.get('state', '')

                    if state == 'numbers':
                        # Обрабатываем ввод чисел для анализа
                        numbers = self.number_analyzer.extract_numbers(user_input)
                        if numbers:
                            await update.message.reply_text(f"Извлечённые числа: {numbers}")
                            await update.message.reply_text("Нажмите 'Результат' для анализа последовательности.")

                            # Кнопки для следующих действий
                            keyboard = [
                                ["Результат", "Стоп"]
                            ]
                            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
                            await update.message.reply_text("Что хотите сделать?", reply_markup=reply_markup)

                            context.user_data['numbers'] = numbers
                            context.user_data['state'] = 'analyze_numbers'
                        else:
                            await update.message.reply_text("Не удалось найти числа в сообщении. Попробуйте ещё раз.")

                    elif state == 'url':
                        # Анализируем URL
                        result = self.url_analyzer.analyze_url(user_input)
                        await update.message.reply_text(result)

                        # Возвращаем к главному меню
                        await self.start(update, context)
                        context.user_data.clear()

                    elif state == 'analyze_numbers':
                        if user_input.lower() == 'результат':
                            # Предсказание следующей цифры
                            numbers = context.user_data['numbers']
                            predicted_number = self.number_analyzer.predict_next_number(numbers)
                            await update.message.reply_text(
                                f"Предсказанная цифра: {predicted_number}\nВведите следующую цифру или нажмите 'Далее'.")

                            # Кнопки для следующих действий
                            keyboard = [
                                ["Далее", "Главная", "Стоп"]
                            ]
                            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
                            await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

                            context.user_data['predicted_number'] = predicted_number
                            context.user_data['state'] = 'next_step'

                        else:
                            await update.message.reply_text("Нажмите 'Результат' для анализа последовательности.")

                    elif state == 'next_step':
                        # Пользователь вводит цифры или нажимает "Далее"
                        predicted_number = context.user_data.get('predicted_number')
                        if user_input == str(predicted_number):
                            await update.message.reply_text(f"Правильный ответ: {predicted_number}!")
                        else:
                            await update.message.reply_text(
                                f"Ошибка! Ожидалась цифра {predicted_number}, попробуйте снова.")

                        # Кнопки для следующих действий
                        keyboard = [
                            ["Далее", "Главная", "Стоп"]
                        ]
                        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
                        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

                    elif user_input.lower() == 'главная':
                        await self.start(update, context)
                        context.user_data.clear()

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
            oup = BeautifulSoup(response.content, 'html.parser')

            title = soup.find('title').text.strip()
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description['content'].strip() if meta_description else ""
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            keyword_list = keywords['content'].split(',') if keywords else []

            return f"Текст заголовка страницы: {title}\nМета описание: {description}\nКлючевые слова: {keyword_list}"
        except Exception as e:
            return f"Ошибка анализа URL: {e}"