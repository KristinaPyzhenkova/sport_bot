import telebot
from telebot import types, apihelper
import os
import logging

from dotenv import load_dotenv

load_dotenv()


# apihelper.proxy = {'https':'socks5://294.154.31.136:2114'}
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def wake_up(message):
    '''Привестсвие и выбор тренировки'''
    bot.send_message(
        message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}.'
    )
    main_menu(message)


@bot.message_handler(commands=['menu'])
def main_menu(message):
    '''Выбор тренировки'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    markup.add(*button)
    bot.send_message(
        message.chat.id,
        'Выбери тренировку',
        reply_markup=markup
    )


def get_new_train(message):
    '''Тренировки и разбор упражнения'''
    dict = {
        1: [['Тренировка 1\n1. Лодочка 15 раз + Супермен 15 раз + Скалолаз 30 раз ( 4 круга )\n2. Касания плеча 30 раз + Скалолаз 30 раз + Тараканчик 30 раз( 4 круга )\n3. Присед с резинкой 30 раз + Ходьба с резинкой 50 шагов ( 4 круга )'],
            [{'Лодочка':'boat', 'Супермен':'supermen', 'Скалолаз':'climber', 'Касания плеча':'shoulder', 'Тараканчик':'cockroach', 'Присед с резинкой':'band squat', 'Ходьба с резинкой':'walking with band'}]],
        2: [['Тренировка 2\n1. Болгарские выпады 20 раз + Книжка 30 раз (3 круга )\n2. Присед с утяжелителем в руках 30 раз + Ягодичный мост с лавочки 30 раз ( 3 круга )\n3. Махи по диагонали 20 раз + Махи назад 20 раз ( 4 круга )\n4. Ходьба с резинкой 70 шагов ( 4 круга )\n5. Скалолаз 30 раз + Касание плеча 30 раз ( 4 круга )'],
            [{'Болгарские выпады':'bulgarian lunges', 'Книжка':'book', 'Присед с утяжелителем в руках':'weighted squat', 'Ягодичный мост с лавочки':'bridge with weight', 'Махи по диагонали':'diagonal', 'Махи назад':'back', 'Ходьба с резинкой':'walking with band', 'Скалолаз':'climber', 'Касание плеча':'shoulder'}]],
        3: [['Тренировка 3\n1. Ленивые Берпи 15 раз + Скалолаз 30 раз ( 4 круга )\n2. Выпады на месте по 20 раз + Подъем с планки по 10 раз на каждую руку ( 4 круга )\n3. Ягодичный мост с утяжелителем 30 раз + Махи назад и в сторону 30 раз + Разведение ног лёжа на спине 30 раз ( 4 круга )'],
            [{'Ленивые Берпи': 'lazy burpees', 'Скалолаз': 'climber', 'Выпады на месте':'lunges in place', 'Подъем с планки': 'plank lift', 'Ягодичный мост с утяжелителем':'bridge with weight', 'Махи назад и в сторону': 'back and side', 'Разведение ног лёжа на спине':'lying on back'}]],
        4: [['Тренировка 4\nКруговая тренировка \n1. Отжимания волной 15 раз\n2. Касания плеча 30 раз\n3. Скалолаз 30 раз\n4. Супермен с резинкой 20 раз на каждую сторону\n5. Повороты таза в планке 30 раз\n4 круга'],
            [{'Отжимания волной':'wave push-ups','Касания плеча':'shoulder','Скалолаз':'climber','Супермен с резинкой':'supermen with bend','Повороты таза в планке':'turn in plank'}]],
        5: [['Тренировка 5\n1. Выпады на месте с утяжелителем 20 раз на каждую ногу ( 4 круга )\n2. Отведение ноги 15 раз + добивка в верхней точке 15 раз + разгибание и сгибание в верхней точке по 15 раз ( 4 круга )\n3. Румынская тяга с резинкой и с утяжелителем- широкая постановка ног ( 4 круга )\n4. Ягодичный мост на одну ногу с лавочки по 20 раз на каждую ногу ( 4 круга )\n5. Румынская с узкой постановкой ног 30 раз + Книжка с резинкой 30 раз на каждую ногу (4 круга)'],
            [{'Выпады на месте с утяжелителем':'lunges in place','Отведение ноги + добивка в верхней точке + разгибание и сгибание в верхней точке':'complex 3','Румынская тяга':'Romanian draft','Румынская тяга с узкой постановкой ног':'Romanian draft narrow','Ягодичный мост на одну ногу с лавочки':'bridge on one leg from the bench','Книжка':'book'}]],
        6: [['Тренировка 6\nКруговая тренировка \n1. Тараканчик 40 раз\n2. Скалолаз 40 раз\n3. Повороты таза в планке 40 раз\n4. Лодочка 25 раз\n4 круга'],
            [{'Тараканчик':'cockroach','Скалолаз':'climber','Повороты таза в планке':'turn in plank','Лодочка':'boat'}]],
        7: [['Тренировка 7\n1. Приседания с 2мя гантелями 30 раз + Ягодичный мост с резинкой и утяжелителем 30 раз + Разведения 10 раз (4 круга)\n2. Выпады на месте 25 раз + отведение ноги/короткая амплитуда/сгибание (4 круга)\n3. Румынская тяга с резинкой широкая постановка ног 20 раз + узкая постановка 20 раз + книжка 40 раз (4 круга)'],
            [{'Приседания с 2мя гантелями':'weighted squat','Ягодичный мост с резинкой и утяжелителем':'bridge with weight','Разведения':'breeding','Выпады на месте':'lunges in place','Отведение ноги/короткая амплитуда/сгибание':'complex 3','Румынская тяга (широкая постановка)':'Romanian draft', 'Румынская тяга (узкая постановка)':'Romanian draft narrow', 'Книжка':'book'}]],
        8: [['Тренировка 8\nКруговая тренировка\n1. Лодочка 20 раз\n2. Отжимания волной 20 раз\n3. Подъем с планки 10 раз на каждую руку\n4. Скалолаз 30 раз\n5. Таракан 30 раз\n6. Поворот таза в планке 30 раз\n7. Обратные отжимания 20 раз'],
            [{'Лодочка': 'boat', 'Отжимания волной': 'wave push-ups', 'Подъем с планки':'plank lift', 'Скалолаз': 'climber','Таракан':'cockroach', 'Поворот таза в планке':'turn in plank', 'Обратные отжимания':'Reverse push-ups'}]],
        9: [['Тренировка 9\n1. Приседания с гантелями 30 раз + ягодичный мост с резинкой и утяжелителем 30 раз + Разведения 100 раз (4 круга)\n2. Выпады на месте 25 раз + отведение ноги / короткая амплитуда / сгибания(по 15 раз)( 4 круга )\n3. Румынская тяга с резинкой широкая постановка 20 раз + узкая постановка 20 раз + Книжка 40 раз (4 круга)'],
            [{'Приседания с гантелями':'weighted squat', 'ягодичный мост':'bridge with weight','Разведения':'breeding', 'Выпады на месте':'lunges in place','отведение ноги / короткая амплитуда / сгибания':'complex 3', 'Румынская тяга (широкая постановка)':'Romanian draft', 'Румынская тяга (узкая постановка)':'Romanian draft narrow', 'Книжка':'book'}]],
        10: [['Тренировка 10\nКруговая тренировка \n1. Лодочка 20 раз\n2. Отжимания волной 20 раз\n3. Подъем с планки 10 раз на каждую руку \n4. Скалолаз 30 раз\n5. Таракан 30 раз\n6. Поворота таза в планке 30 раз\n7. Обратные отжимания 20 раз\n8. Планка 60 секунд\n4 круга'],
             [{'Лодочка': 'boat', 'Отжимания волной': 'wave push-ups', 'Подъем с планки':'plank lift', 'Скалолаз': 'climber','Таракан':'cockroach', 'Поворот таза в планке':'turn in plank', 'Обратные отжимания':'Reverse push-ups','Планка':'plank'}]],
        11: [['Тренировка 11\n1. Болгарские выпады 20 раз + Махи по диагонали 25 раз (4 круга)\n2. Присед с утяжелителем в руках 30 раз + Ягодичный мост с пола с резинкой и с утяжелителем 30 раз + Махи назад 20 раз и махи в сторону 20 раз (4 круга)\n3. Румынская тяга с гантелями 25 раз  + Ходьба с резинкой 100 шагов + Книжка 30 раз (4 круга)'],
             [{'Болгарские выпады':'bulgarian lunges', 'Махи по диагонали':'diagonal', 'Присед с утяжелителем в руках': 'weighted squat', 'Ягодичный мост': 'bridge with weight','Махи назад и в сторону':'back and side','Румынская тяга':'Romanian draft','Ходьба с резинкой':'walking with band','Книжка':'book'}]],
        12: [['Тренировка 12\n1. Ленивые берпи 20 раз (4 круга)\n2. Выпады на месте с гантелями 20 раз (4 круга)\n3. Ягодичный мост с подъемом 30 раз (4 круга)\n4. Книжка с резинкой 30 раз (4 круга)\n5. Скалолаз 40 раз (4 круга)\n6. Разведение ног лёжа с резинкой 40 раз (4 круга)'],
             [{'Ленивые берпи':'lazy burpees','Выпады на месте':'lunges in place','Ягодичный мост':'bridge with weight','Книжка с резинкой':'book','Скалолаз':'climber','Разведение ног лёжа с резинкой':'lying on back'}]],
        13: [['Тренировка 13\nКруговая тренировка\n1. Отжимания волной 20 раз\n2. Касания плеч 30 раз\n3. Скалолаз 40 раз\n4. Супермен 20 раз на каждую руку \n5. Тараканчик 40 раз\n4 круга'],
             [{'Отжимания волной':'wave push-ups','Касания плеч':'shoulder','Скалолаз':'climber','Супермен':'supermen','Тараканчик':'cockroach'}]],
        14: [['Тренировка 14\n1. Выпады в сторону 40 раз + Махи назад и в сторону 30 раз + Скалолаз 40 раз (4 круга)\n2. Присед с утяжелителем в руках 30 раз + Разведения 100 раз (4 круга)\n3. Румынская тяга с резинкой и гантелями широкая постановка ног 25 раз + Ходьба с резинкой 100 раз (4 круга)\n4. Повороты таза в планке 40 раз + Таракан 40 раз (4 круга)'],
             [{'Выпады в сторону':'Lunges to the side','Махи назад и в сторону':'back and side','Скалолаз':'climber','Присед с утяжелителем в руках':'weighted squat', 'Разведения':'breeding','Румынская тяга':'Romanian draft','Ходьба с резинкой':'walking with band','Повороты таза в планке':'turn in plank','Таракан':'cockroach'}]]
    }
    return dict[int(message)]

@bot.message_handler(content_types='text')
def choose_train(message):
    '''При выборе тренировки - обработка значения'''
    mess = get_new_train(message.text)
    exercises = mess[0]
    markup = types.InlineKeyboardMarkup(row_width=2)
    button = []
    for i, w in mess[1][0].items():
        button.append(types.InlineKeyboardButton(text=f"{i}", callback_data=f"{w}"))
    markup.add(*button)
    bot.send_message(message.chat.id, exercises[0], reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    '''Ответ при вызове разбора упражнения'''
    if call.message:
        if call.data == 'boat':
            video = open('train/boat.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Лодочка.\nИсходная позиция - лежа на животе. Руки вытянуты вперед. Ладони направлены вниз. Ноги прямые, носки вытянутые. Одновременно совершаем следующие движения: поднимаем верхнюю часть туловища и ноги на максимально комфортную высоту. Опорой служит область таза и живота.Медленно выдыхаем и опускаемся в стартовое положение.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'supermen':
            video = open('train/supermen.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Супермен.\nИсходная позиция: на 4 четвереньках ‚ живот подтянут, позвоночник ровный .На выдохе выпрямляем параллельно полу правую ногу и левую руку ‚ на вдохе опускаем на место не касаясь пола, выпрямляем ещё 15 раз. Повторяем то же самое на левую ногу и правую руку 15 раз.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'climber':
            video = open('train/climber.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Скалолаз.\nИсходная позиция: планка на прямых руках, Копчик немного подкручен под себя, Живот подтянут , на выдохе тянем правое колено к левой груди / левое колено к правой груди.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'shoulder':
            video = open('train/shoulder.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Касания плеча.\nИсходная позиция: примите упор лёжа. Расположите ладони под плечами. Держите спину прямо. Напрягите ягодицы и мышцы живота.Избегайте прогиба в пояснице. Ваше тело должно образовать прямую линию. Далее поочерёдно касаемся рукой противоположного плеча, сохраняя при этом тело в зафиксированном положении. Выполняя упражнение, сохраняйте ровное дыхание.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'band squat':
            video = open('train/band squat.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Присед с резинкой.\nИсходная позиция: ноги на ширине плеч ‚ носки разведены в сторону. Колени и носки стоп направляйте в одну сторону. Стопы прижмите плотно к полу и не приподнимайте их на протяжении всего упражнения. Держите поясницу с легким прогибом. Старайтесь не наклоняться вперед. Следите за осанкой. Не сводите коленки внутрь и не разводите их в стороны, вставая из нижнего положения. Колени должны «смотреть» туда же, куда и стопы. Старайтесь также не выводить колени вперед за уровень носков. Сделайте вдох в начале упражнения ‚отводя таз назад присядьте до параллели с полом. Поднимаясь не нужно доходить до полного выпрямления сразу же начинайте движение вниз.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'walking with band':
            video = open('train/walk.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Ходьба с резинкой (5 шагов вправо / 5 влево).\nИсходная позиция: упор в пятку, таз оттянут назад, корпус в наклоне. Шагаем в сторону‚ так чтобы расстояние между ступнями не доходило менее чем на 50 см\nРезинка на икрах')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'bulgarian lunges':
            video = open('train/lunges.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Болгарские выпады.\nИсходная позиция: Подойди к скамье (стул) и стань к ней спиной. Сделай одной ногой широкий шаг вперед, а вторую положи на скамью на верхнюю часть стопы. Руки с гантелями опусти вдоль корпуса, либо без утяжелителей держи перед собой. Это твоё исходное положение. Сохраняя ровное положение корпуса и естественный прогиб в спине, присядь на рабочей ноге (та что на полу) так, чтобы ее бедро достигло параллели с полом. Колено этой ноги во время приседа не должно выходить за линию носка. Центр тяжести находится на пятке рабочей ноги, но носок от пола не отрывается. Колено опорной ноги свободно опускается вниз. Толкнись пяткой от пола и вернись в исходное положение')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'book':
            video = open('train/book.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Книжка.\nИсходное положение: лёжа на боку, упираемся в предплечье, резинка располагается на бёдрах. Спина ровная , колени согнуты в прямой угол. На выдохе поднимаем согнутую в колене ногу максимально высоко‚ на вдохе возвращаем на место‚ не касаясь второй ноги поднимаем заново.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'bridge with weight':
            video = open('train/bridge with weight.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Ягодичный мост с лавочки (любая высокая поверхность около 50 см, можно расположить стопы на диван).\nИсходное положение: лёжа на спине, ноги согнуты и располагаются на возвышенности упираясь в пятки, колени над стопами. Руки придерживают гантель в районе таза . В этом положении на выдохе поднимаем таз вверх до прямой линии от плеч до колен‚ выжимаем ягодицы. На вдохе опускаем таз в исходное положение, но не касаясь пола, поднимаем снова вверх. Выполняем упражнение не спеша, следим за дыханием.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'diagonal':
            video = open('train/diogonal.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Махи по диагонали.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'back':
            video = open('train/back.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Махи назад')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'back and side':
            video = open('train/back and side.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Махи назад и в сторону')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'complex 3':
            video = open('train/complex 3.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Махи + добивка в верхней точке.\nИсходное положение на четвереньках‚ (руки ( локти) под плечами , колени под бёдрами).\nРезинка на бёдрах либо под коленями - поясница зафиксирована. На выдохе поднимаем согнутую в колене (90 градусов) ногу и тянем пятку к потолку - на вдохе немного опускаем. Плотность резинки определяем индивидуально - жжение в ягодицах и бёдрах как индикатор.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'lazy burpees':
            video = open('train/lazy burpees.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Ленивые берпи.\nИсходная позиция: Встаём прямо, ноги на ширине плеч. Опускаемся на руки и «шагаем» руками вперёд‚ укладываем руки на одном уровне и ложимся волной (колени - таз -грудь), поднимаемся волной (грудь - таз - колени), возвращаясь в исходное положение.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'lunges in place':
            video = open('train/lunge in place.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Выпады на месте (можно использовать утяжелитель до 5 кг).\nТехника: встаём прямо, отводим левую ногу назад ‚ вес - тела располагается на передней ноге , она же является рабочей. На вдохе отводим таз назад, приседая до параллели с полом на выдохе давим в пятку рабочей ноги и поднимаемся в исходную позицию. Спинка ровная, поясница зафиксирована в течении всего упражнения, колени до конца не разгибаем, оставляем немного согнутыми.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'plank lift':
            video = open('train/plank lift.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Подъем с планки.\nТехника: Примите упор лёжа. Расположите локти под плечами. Держите спину прямо. Напрягите ягодицы и мышцы живота. Избегайте прогиба в пояснице. Ваше тело должно образовать прямую линию. Начинайте подъем на ладони поочерёдно ‚ сначала с правой руки ‚ затем с левой. Выполняя упражнение - сохраняйте ровное дыхание.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'bridge with weight':
            video = open('train/bridge with weight.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Ягодичный мост с утяжелителем(до 5 кг).\nИсходное положение: лёжа на спине. Ноги согнуты и давят ступнями в пол на расстоянии друг от друга - колени над стопами. Руки вдоль тела. В этом положении на выдохе поднимаем таз вверх до прямой линии от плеч до колен, выжимаем ягодицы. На вдохе опускаем таз в исходное положение, но не касаясь пола поднимаем снова вверх. Таким образом в режиме нон-стоп делаем 30-50 повторений - каждый раз зажимная ягодицы . Делаем не спеша, следим за дыханием')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'lying on back':
            video = open('train/lying on back.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Разведение ног лёжа с резинкой на бёдрах.\nИсходная позиция: лёжа на спине, прямые ноги подняты вверх‚ руки за головой и поддерживают приподнятые плечи. Живот скручен. На выдохе разводим ноги на вдохе медленно сводим.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'wave push-ups':
            video = open('train/wave.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Отжимания волной (15-20 раз).\nИсходное положение: лежа на животе, руки по обе стороны от груди, ладонями упираются в пол. На выдохе, отжимаясь от пола, мы поднимаем поочерёдно сначала грудь, затем таз, затем колени, и опускаем наоборот (колени / таз / грудь ) в исходное положение.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'supermen with bend':
            video = open('train/supermen with bend.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Супермен с резинкой.\nТехника: исходная позиция на четвереньках, резинка зафиксировать под опорное колено, живот подтянут, позвоночник ровный. На выдохе выпрямляем параллельно полу правую ногу и левую руку‚ на вдохе опускаем на место не касаясь пола.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'turn in plank':
            video = open('train/turn in plank.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Поворот таза в планке.\nТехника: стоим в классической планке с упором на предплечья. Для этого руки сгибаем в локтях, а ладошки сводим вместе. Локти под плечами и упираются в коврик совместно с предплечьями и носками ног. Скручиваем корпус в талии, отводя бедра влево, совместно с ягодицами. Стараемся опустить таз к полу, Выполняем поворот на выдохе. На следующий счет возвращаем корпус в исходное положение, без паузы на выдохе повторяем динамическое скручивание в обратную сторону.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'Romanian draft':
            video = open('train/romanian draft.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Румынская тяга с резинкой и с гантелями (широкая постановка ног).\nТехника выполнения: ноги чуть шире плеч , носочки немного разведены‚ резинка на бёдрах ‚колени постоянно удерживаем разведёнными . В руках утяжелитель Немного прогибаем поясницу, лопатки сводим вместе, не сутулимся, живот подтянут, голову держим ровно, взгляд, направлен прямо перед собой. На вдохе оттягиваем таз назад, одновременно опуская корпус вниз, сохраняем руки прямыми, на выдохе зажимая ягодицы, плавно выпрямляемся. Держим колени немного разведёнными, сопротивляемся резинке, Поясница в течении всего упражнения жесткая , движение происходит в тазобедренном и коленном суставах.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'bridge on one leg from the bench':
            video = open('train/bridge on one leg.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Ягодичный мост на одну ногу с лавочки (можно использовать утяжелитель).\nИсходное положение: лёжа на спине. Рабочая нога согнута и давит всей стопой на лавочку (любая возвышенность около полуметра) вторая нога согнута и свободно располагается на рабочей. Руки вдоль тела, поясница прижата к полу. В этом положении на выдохе поднимаем таз вверх до прямой линии - от плеч до колена, выжимаем ягодицы . На вдохе медленно опускаем таз в исходное положение‚ не касаясь пола поднимаем снова вверх. Таким образом повторяем 20 раз - каждый раз зажимая ягодицы. Повторяем на каждую ногу. Выполняем упражнение не спеша, следим за дыханием.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'Romanian draft narrow':
            video = open('train/romanian draft narrow.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Румынская тяга (узкая постановка ног).\nТехника: yзкая постановка ног, носочки смотрят прямо, в руках утяжелитель. Немного прогибаем поясницу, лопатки сводим вместе, не сутулимся, живот подтянут, голову держим ровно, взгляд, направлен прямо перед собой. На вдохе оттягиваем таз назад, одновременно опуская корпус вниз, сохраняем руки прямыми, на выдохе зажимая ягодицы плавно выпрямляемся. Поясница в течении всего упражнения жесткая, движение происходит в тазобедренном суставе')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'Reverse push-ups':
            video = open('train/reverse push-up.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Обратные отжимания.\nТехника: расположите ладони на краю горизонтальной скамьи, ноги поставьте на пол, напрягите пресс.\nНа выдохе вытолкните вес тела вверх, ощущая работу трицепса. Локти при этом смотрят назад — строго не в стороны. Отталкиваясь от скамьи как можно сильнее, раскрывая грудь — задержитесь в положении 1 сек. На вдохе медленно опуститесь вниз, держа пресс напряженным. В нижней точке движения плечи должны быть параллельны полу.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'Lunges to the side':
            video = open('train/lunge in to slide.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Выпады в сторону.\nТехника: широкая постановка ног . На вдохе переносим вес тела на правую ногу, приседая на неё ‚ левая нога сохраняется прямой ‚ на вдохе возвращаемся в исходное положение. Повторяем нужное количество и затем переходим к выполнению выпадов на левую ногу. В течении всего упражнения пятки прижаты к полу. Можно использовать утяжелитель в виде штанги на плечах, либо гири - гантели в руках.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'cockroach':
            video = open('train/cockroach.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Тараканчик.\nТехника: лягте на пол, руки заведите за голову, ноги согните в коленях. Стопы должны упираться в пол. Выполните скручивание, во время которого правый локоть тянется за левое колено к середине бедра, а колено стремится к локтю. Во время выполнения упражнения старайтесь поднять верхнюю часть тела так, чтобы лопатки оторвались от пола. Поясница должна быть прижата к полу. Не прижимайте подбородок к шее и не тяните себя вверх с помощью рук. При скручивании выполните выдох, в исходном положении — вдох.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'plank':
            video = open('train/plank.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Планка.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'weighted squat':
            video = open('train/squet.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Присед.\n Исходная позиция: ноги на ширине плеч ‚ носки разведены в сторону. Колени и носки стоп направляйте в одну сторону. Стопы прижмите плотно к полу и не приподнимайте их на протяжении всего упражнения. Держите поясницу с легким прогибом. Старайтесь не наклоняться вперед. Следите за осанкой. Не сводите коленки внутрь и не разводите их в стороны, вставая из нижнего положения. Колени должны «смотреть» туда же, куда и стопы. Старайтесь также не выводить колени вперед за уровень носков. Сделайте вдох в начале упражнения ‚отводя таз назад присядьте до параллели с полом. Поднимаясь не нужно доходить до полного выпрямления сразу же начинайте движение вниз.')
            bot.send_video(call.message.chat.id, video)
        elif call.data == 'breeding':
            video = open('train/breeding.mp4', 'rb')
            bot.send_message(call.message.chat.id, 'Разведения.')
            bot.send_video(call.message.chat.id, video)


def main():
    """Основная логика работы бота."""
    try:
        bot.polling(none_stop=True)
    except Exception as error:
        logger.error('Cбой при отправке сообщения в Telegram.')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='program.log',
        format='%(asctime)s, %(levelname)s, %(message)s'
    )
    main()



