import os
from typing import Optional


class Url:
    def __init__(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        count: Optional[int] = 1,
    ):
        self.weather = (
            f"https://api.weather.yandex.ru/v2/forecast?"
            f"lat={lat}"
            f"&lon={lon}"
            f"&lang=ru_RU"
            f"&limit={count}"
            f"&hours=False"
            f"&extra=False"
        )
        self.open_ai = "https://api.openai.com/v1/chat/completions"
        self.to_gis = f"http://routing.api.2gis.com/routing/7.0.0/global?key={os.getenv('KEY_2GIS')}"


city_russian_set = {
    "Любим",
    "Морозовск",
    "Кыштым",
    "Нюрба",
    "Минусинск",
    "Семёнов",
    "Порхов",
    "Ессентуки",
    "Ишимбай",
    "Выкса",
    "Макушино",
    "Тара",
    "Александровск-Сахалинский",
    "Сурск",
    "Звенигово",
    "Иннополис",
    "Светлый",
    "Черняховск",
    "Холм",
    "Алагир",
    "Мышкин",
    "Багратионовск",
    "Анапа",
    "Островной",
    "Рязань",
    "Белёв",
    "Серафимович",
    "Юрюзань",
    "Николаевск",
    "Гулькевичи",
    "Удачный",
    "Камышин",
    "Йошкар-Ола",
    "Луга",
    "Саранск",
    "Медынь",
    "Железногорск",
    "Златоуст",
    "Приволжск",
    "Анадырь",
    "Нижние Серги",
    "Орёл",
    "Старый Крым",
    "Чёрмоз",
    "Кашин",
    "Ангарск",
    "Черноголовка",
    "Полысаево",
    "Раменское",
    "Одинцово",
    "Новочеркасск",
    "Гороховец",
    "Новоржев",
    "Сасово",
    "Хилок",
    "Кызыл",
    "Новосиль",
    "Магас",
    "Бугуруслан",
    "Заводоуковск",
    "Кинешма",
    "Зеленогорск",
    "Талдом",
    "Далматово",
    "Когалым",
    "Заволжье",
    "Королёв",
    "Лебедянь",
    "Мончегорск",
    "Елец",
    "Верхоянск",
    "Емва",
    "Киселёвск",
    "Весьегонск",
    "Лукоянов",
    "Бузулук",
    "Армянск",
    "Химки",
    "Вязьма",
    "Озёры",
    "Волгореченск",
    "Шимановск",
    "Покров",
    "Велиж",
    "Аксай",
    "Кирсанов",
    "Новошахтинск",
    "Асино",
    "Жиздра",
    "Новоаннинский",
    "Северобайкальск",
    "Судак",
    "Хасавюрт",
    "Новый Оскол",
    "Байкальск",
    "Орехово-Зуево",
    "Боровичи",
    "Гдов",
    "Бородино",
    "Пущино",
    "Берёзовский",
    "Бирюч",
    "Вихоревка",
    "Гремячинск",
    "Почеп",
    "Кольчугино",
    "Саратов",
    "Пенза",
    "Городище",
    "Заполярный",
    "Новоузенск",
    "Малоархангельск",
    "Псков",
    "Балабаново",
    "Грозный",
    "Астрахань",
    "Волчанск",
    "Ростов",
    "Называевск",
    "Петровск",
    "Богучар",
    "Малая Вишера",
    "Старая Русса",
    "Печоры",
    "Кемь",
    "Кропоткин",
    "Курчатов",
    "Невьянск",
    "Тула",
    "Кировск",
    "Осташков",
    "Уяр",
    "Азнакаево",
    "Электроугли",
    "Краснокаменск",
    "Хабаровск",
    "Лысьва",
    "Ейск",
    "Магнитогорск",
    "Гусь-Хрустальный",
    "Жуков",
    "Краснослободск",
    "Сарапул",
    "Белогорск",
    "Унеча",
    "Верхняя Пышма",
    "Лакинск",
    "Сольвычегодск",
    "Назарово",
    "Кстово",
    "Сургут",
    "Дзержинский",
    "Петушки",
    "Азов",
    "Воскресенск",
    "Бабушкин",
    "Лаишево",
    "Тимашёвск",
    "Усть-Лабинск",
    "Вытегра",
    "Лагань",
    "Медвежьегорск",
    "Пугачёв",
    "Ишим",
    "Липецк",
    "Новокузнецк",
    "Сосновоборск",
    "Калининск",
    "Тавда",
    "Демидов",
    "Новоульяновск",
    "Котельнич",
    "Талица",
    "Урень",
    "Очёр",
    "Нижнекамск",
    "Улан-Удэ",
    "Рассказово",
    "Шарья",
    "Устюжна",
    "Курлово",
    "Пролетарск",
    "Голицыно",
    "Жуковский",
    "Закаменск",
    "Севск",
    "Микунь",
    "Терек",
    "Шадринск",
    "Махачкала",
    "Северо-Курильск",
    "Волгодонск",
    "Сорочинск",
    "Кувшиново",
    "Сатка",
    "Лахденпохья",
    "Абинск",
    "Мичуринск",
    "Тетюши",
    "Беслан",
    "Поворино",
    "Пятигорск",
    "Карабаш",
    "Спасск",
    "Судогда",
    "Барыш",
    "Тобольск",
    "Кандалакша",
    "Сокол",
    "Верхняя Салда",
    "Белинский",
    "Новоуральск",
    "Кириши",
    "Каменск-Уральский",
    "Старица",
    "Чадан",
    "Красноуральск",
    "Славянск-на-Кубани",
    "Балашиха",
    "Белово",
    "Алдан",
    "Новокуйбышевск",
    "Моздок",
    "Слободской",
    "Миллерово",
    "Агрыз",
    "Евпатория",
    "Нововоронеж",
    "Стерлитамак",
    "Донской",
    "Тарко-Сале",
    "Сыктывкар",
    "Клин",
    "Оса",
    "Канаш",
    "Бокситогорск",
    "Усинск",
    "Ленинск-Кузнецкий",
    "Касимов",
    "Выборг",
    "Сельцо",
    "Павловский Посад",
    "Касли",
    "Бийск",
    "Баймак",
    "Октябрьский",
    "Цивильск",
    "Рузаевка",
    "Бугульма",
    "Нижний Ломов",
    "Юхнов",
    "Реж",
    "Энгельс",
    "Томмот",
    "Урус-Мартан",
    "Дмитровск",
    "Ардон",
    "Плёс",
    "Лабытнанги",
    "Коряжма",
    "Любань",
    "Вилючинск",
    "Пушкино",
    "Аткарск",
    "Канск",
    "Баксан",
    "Нижняя Тура",
    "Плавск",
    "Карачев",
    "Уссурийск",
    "Муравленко",
    "Торопец",
    "Свирск",
    "Советский",
    "Джанкой",
    "Питкяранта",
    "Чебоксары",
    "Боровск",
    "Печора",
    "Болгар",
    "Лосино-Петровский",
    "Козловка",
    "Белая Холуница",
    "Богородск",
    "Дубовка",
    "Москва",
    "Сибай",
    "Артёмовский",
    "Жигулёвск",
    "Карасук",
    "Дрезна",
    "Курган",
    "Оханск",
    "Сызрань",
    "Светлоград",
    "Губкин",
    "Сафоново",
    "Волгоград",
    "Среднеколымск",
    "Струнино",
    "Усолье-Сибирское",
    "Конаково",
    "Чухлома",
    "Изобильный",
    "Кедровый",
    "Кизел",
    "Кингисепп",
    "Слюдянка",
    "Апшеронск",
    "Североуральск",
    "Щигры",
    "Андреаполь",
    "Новокубанск",
    "Учалы",
    "Волоколамск",
    "Сегежа",
    "Наволоки",
    "Павловск",
    "Жердевка",
    "Зубцов",
    "Костерёво",
    "Вышний Волочёк",
    "Починок",
    "Пыталово",
    "Севастополь",
    "Кадников",
    "Гай",
    "Волжский",
    "Кунгур",
    "Сим",
    "Суоярви",
    "Кострома",
    "Краснокамск",
    "Подольск",
    "Арсеньев",
    "Самара",
    "Славгород",
    "Тихвин",
    "Вуктыл",
    "Колтуши",
    "Константиновск",
    "Бор",
    "Воронеж",
    "Салават",
    "Духовщина",
    "Нолинск",
    "Калач-на-Дону",
    "Новосокольники",
    "Полевской",
    "Лодейное Поле",
    "Находка",
    "Сольцы",
    "Ясногорск",
    "Острогожск",
    "Зерноград",
    "Харабали",
    "Иваново",
    "Галич",
    "Гусев",
    "Змеиногорск",
    "Алапаевск",
    "Лангепас",
    "Вилюйск",
    "Алексин",
    "Зарайск",
    "Краснодар",
    "Остров",
    "Сорск",
    "Усть-Илимск",
    "Ханты-Мансийск",
    "Каменск-Шахтинский",
    "Катайск",
    "Удомля",
    "Большой Камень",
    "Луховицы",
    "Ярцево",
    "Тогучин",
    "Бахчисарай",
    "Зеленодольск",
    "Тотьма",
    "Шилка",
    "Опочка",
    "Сосновый Бор",
    "Коломна",
    "Тюмень",
    "Бологое",
    "Камень-на-Оби",
    "Михайлов",
    "Алейск",
    "Барнаул",
    "Протвино",
    "Нижневартовск",
    "Шумиха",
    "Донецк",
    "Никольское",
    "Вятские Поляны",
    "Белозерск",
    "Болохово",
    "Покачи",
    "Тайшет",
    "Уржум",
    "Спас-Клепики",
    "Беломорск",
    "Клинцы",
    "Ртищево",
    "Сланцы",
    "Можга",
    "Дзержинск",
    "Калтан",
    "Артём",
    "Меленки",
    "Набережные Челны",
    "Перевоз",
    "Новоалександровск",
    "Верхотурье",
    "Бодайбо",
    "Кулебаки",
    "Избербаш",
    "Усмань",
    "Зима",
    "Арамиль",
    "Городовиковск",
    "Харовск",
    "Санкт-Петербург",
    "Дно",
    "Маркс",
    "Великий Новгород",
    "Кириллов",
    "Руза",
    "Топки",
    "Новая Ляля",
    "Иланский",
    "Алатырь",
    "Киржач",
    "Гусиноозёрск",
    "Верхний Уфалей",
    "Алексеевка",
    "Барабинск",
    "Майский",
    "Первомайск",
    "Ревда",
    "Свободный",
    "Мирный",
    "Чудово",
    "Новохопёрск",
    "Десногорск",
    "Буйнакск",
    "Вологда",
    "Луза",
    "Новодвинск",
    "Приморско-Ахтарск",
    "Шумерля",
    "Ельня",
    "Кировград",
    "Благодарный",
    "Колпашево",
    "Среднеуральск",
    "Реутов",
    "Глазов",
    "Егорьевск",
    "Корсаков",
    "Семикаракорск",
    "Троицк",
    "Михайловка",
    "Щёлкино",
    "Димитровград",
    "Челябинск",
    "Дивногорск",
    "Горбатов",
    "Заречный",
    "Череповец",
    "Балахна",
    "Заволжск",
    "Сальск",
    "Юрьевец",
    "Прохладный",
    "Заозёрск",
    "Чита",
    "Чаплыгин",
    "Тюкалинск",
    "Вельск",
    "Мамоново",
    "Ногинск",
    "Куйбышев",
    "Липки",
    "Неман",
    "Ухта",
    "Рославль",
    "Сосенский",
    "Гагарин",
    "Каменногорск",
    "Саянск",
    "Дудинка",
    "Полярные Зори",
    "Торжок",
    "Сертолово",
    "Эртиль",
    "Бабаево",
    "Городец",
    "Губаха",
    "Мамадыш",
    "Бирск",
    "Комсомольск-на-Амуре",
    "Новомичуринск",
    "Белая Калитва",
    "Бутурлиновка",
    "Лыткарино",
    "Правдинск",
    "Ярославль",
    "Ковров",
    "Петропавловск-Камчатский",
    "Красавино",
    "Балашов",
    "Бикин",
    "Батайск",
    "Великий Устюг",
    "Фатеж",
    "Муром",
    "Короча",
    "Ленинск",
    "Высоковск",
    "Северодвинск",
    "Суворов",
    "Данилов",
    "Мглин",
    "Белебей",
    "Новоалтайск",
    "Приозерск",
    "Сосновка",
    "Дмитриев",
    "Рыбное",
    "Углегорск",
    "Горнозаводск",
    "Ковылкино",
    "Междуреченск",
    "Данков",
    "Дмитров",
    "Катав-Ивановск",
    "Николаевск-на-Амуре",
    "Владимир",
    "Покровск",
    "Серов",
    "Геленджик",
    "Качканар",
    "Ядрин",
    "Дорогобуж",
    "Пучеж",
    "Кизляр",
    "Домодедово",
    "Краснотурьинск",
    "Гаджиево",
    "Нерюнгри",
    "Южноуральск",
    "Чернушка",
    "Кузнецк",
    "Владикавказ",
    "Рошаль",
    "Нягань",
    "Надым",
    "Лобня",
    "Новосибирск",
    "Верхний Тагил",
    "Ермолино",
    "Холмск",
    "Малгобек",
    "Сортавала",
    "Балаково",
    "Камышлов",
    "Нерехта",
    "Снежногорск",
    "Кондопога",
    "Борисоглебск",
    "Полярный",
    "Котельниково",
    "Нязепетровск",
    "Тайга",
    "Волхов",
    "Россошь",
    "Новотроицк",
    "Белорецк",
    "Мосальск",
    "Нефтегорск",
    "Мурманск",
    "Кологрив",
    "Видное",
    "Камешково",
    "Ивангород",
    "Межгорье",
    "Инза",
    "Куровское",
    "Дальнереченск",
    "Ипатово",
    "Адыгейск",
    "Давлеканово",
    "Туран",
    "Чегем",
    "Усть-Катав",
    "Фролово",
    "Салаир",
    "Электросталь",
    "Ковдор",
    "Фокино",
    "Бежецк",
    "Моршанск",
    "Белокуриха",
    "Светлогорск",
    "Полесск",
    "Грязовец",
    "Красногорск",
    "Козельск",
    "Лиски",
    "Пыть-Ях",
    "Сухиничи",
    "Ахтубинск",
    "Горячий Ключ",
    "Грайворон",
    "Наро-Фоминск",
    "Долгопрудный",
    "Крымск",
    "Архангельск",
    "Стародуб",
    "Гвардейск",
    "Арзамас",
    "Гуково",
    "Дятьково",
    "Звенигород",
    "Коркино",
    "Тихорецк",
    "Арск",
    "Белореченск",
    "Княгинино",
    "Райчихинск",
    "Спас-Деменск",
    "Сусуман",
    "Кирс",
    "Советск",
    "Борзя",
    "Шлиссельбург",
    "Ак-Довурак",
    "Североморск",
    "Сердобск",
    "Балей",
    "Верхняя Тура",
    "Яхрома",
    "Каргополь",
    "Сергач",
    "Красноярск",
    "Уфа",
    "Карпинск",
    "Куртамыш",
    "Ноябрьск",
    "Чапаевск",
    "Купино",
    "Кимры",
    "Кимовск",
    "Оха",
    "Дегтярск",
    "Похвистнево",
    "Нестеров",
    "Болхов",
    "Нерчинск",
    "Приморск",
    "Березники",
    "Железногорск-Илимский",
    "Минеральные Воды",
    "Певек",
    "Сунжа",
    "Менделеевск",
    "Осинники",
    "Курчалой",
    "Ирбит",
    "Ладушкин",
    "Альметьевск",
    "Норильск",
    "Иркутск",
    "Семилуки",
    "Дубна",
    "Верхнеуральск",
    "Каменка",
    "Пошехонье",
    "Карабулак",
    "Рудня",
    "Обоянь",
    "Усть-Джегута",
    "Никольск",
    "Сенгилей",
    "Красный Сулин",
    "Солнечногорск",
    "Пестово",
    "Черногорск",
    "Боготол",
    "Ликино-Дулёво",
    "Гурьевск",
    "Черкесск",
    "Аргун",
    "Абакан",
    "Гаврилов-Ям",
    "Калининград",
    "Долинск",
    "Лесной",
    "Ливны",
    "Сычёвка",
    "Тырныауз",
    "Южно-Сахалинск",
    "Цимлянск",
    "Симферополь",
    "Нальчик",
    "Прокопьевск",
    "Невельск",
    "Новозыбков",
    "Хвалынск",
    "Сковородино",
    "Навашино",
    "Апрелевка",
    "Мариинский Посад",
    "Скопин",
    "Темников",
    "Усть-Кут",
    "Пудож",
    "Лесозаводск",
    "Миасс",
    "Туймазы",
    "Фурманов",
    "Обь",
    "Чехов",
    "Кумертау",
    "Кудрово",
    "Соль-Илецк",
    "Суздаль",
    "Красноперекопск",
    "Шагонар",
    "Ялуторовск",
    "Славск",
    "Новомосковск",
    "Трёхгорный",
    "Красноармейск",
    "Старый Оскол",
    "Инта",
    "Жирновск",
    "Высоцк",
    "Лабинск",
    "Тулун",
    "Ивдель",
    "Петров Вал",
    "Биробиджан",
    "Онега",
    "Оренбург",
    "Родники",
    "Урай",
    "Трубчевск",
    "Нытва",
    "Рыбинск",
    "Майкоп",
    "Пустошка",
    "Кизилюрт",
    "Дербент",
    "Тейково",
    "Чердынь",
    "Всеволожск",
    "Благовещенск",
    "Чекалин",
    "Билибино",
    "Грязи",
    "Котельники",
    "Саяногорск",
    "Южно-Сухокумск",
    "Ижевск",
    "Волжск",
    "Еманжелинск",
    "Нефтекамск",
    "Мелеуз",
    "Белый",
    "Мензелинск",
    "Зеленокумск",
    "Казань",
    "Фрязино",
    "Анжеро-Судженск",
    "Алзамай",
    "Невинномысск",
    "Мураши",
    "Суджа",
    "Олонец",
    "Аша",
    "Старая Купавна",
    "Карабаново",
    "Ступино",
    "Людиново",
    "Новороссийск",
    "Кохма",
    "Кирово-Чепецк",
    "Агидель",
    "Чебаркуль",
    "Георгиевск",
    "Мантурово",
    "Спасск-Рязанский",
    "Назрань",
    "Новопавловск",
    "Киреевск",
    "Кукмор",
    "Мещовск",
    "Западная Двина",
    "Ставрополь",
    "Лянтор",
    "Мценск",
    "Кола",
    "Верещагино",
    "Красный Кут",
    "Черепаново",
    "Будённовск",
    "Буинск",
    "Горно-Алтайск",
    "Копейск",
    "Кубинка",
    "Бобров",
    "Поронайск",
    "Ардатов",
    "Себеж",
    "Армавир",
    "Енисейск",
    "Сосногорск",
    "Строитель",
    "Невель",
    "Суровикино",
    "Облучье",
    "Каргат",
    "Чистополь",
    "Электрогорск",
    "Кисловодск",
    "Дюртюли",
    "Орск",
    "Тамбов",
    "Елизово",
    "Ефремов",
    "Тверь",
    "Артёмовск",
    "Горняк",
    "Железноводск",
    "Котлас",
    "Калязин",
    "Волосово",
    "Шебекино",
    "Коммунар",
    "Ачхой-Мартан",
    "Кораблино",
    "Кувандык",
    "Каспийск",
    "Пересвет",
    "Уварово",
    "Шиханы",
    "Тында",
    "Камызяк",
    "Нефтекумск",
    "Миньяр",
    "Пикалёво",
    "Сураж",
    "Щёлково",
    "Костомукша",
    "Аркадак",
    "Алушта",
    "Бирюсинск",
    "Воткинск",
    "Валдай",
    "Зея",
    "Котовск",
    "Красный Холм",
    "Ворсма",
    "Собинка",
    "Ржев",
    "Таштагол",
    "Яранск",
    "Рыльск",
    "Олёкминск",
    "Белоозёрский",
    "Бронницы",
    "Венёв",
    "Гаврилов Посад",
    "Белоусово",
    "Озёрск",
    "Петухово",
    "Шахты",
    "Ужур",
    "Шелехов",
    "Сысерть",
    "Абаза",
    "Новочебоксарск",
    "Можайск",
    "Заринск",
    "Губкинский",
    "Александровск",
    "Югорск",
    "Сергиев Посад",
    "Юрьев-Польский",
    "Дедовск",
    "Ивантеевка",
    "Хотьково",
    "Смоленск",
    "Красновишерск",
    "Нижний Тагил",
    "Отрадный",
    "Петрозаводск",
    "Чайковский",
    "Светогорск",
    "Зверево",
    "Нарткала",
    "Завитинск",
    "Зеленоградск",
    "Кемерово",
    "Новая Ладога",
    "Партизанск",
    "Сясьстрой",
    "Кремёнки",
    "Нелидово",
    "Саров",
    "Урюпинск",
    "Таруса",
    "Петровск-Забайкальский",
    "Дигора",
    "Болотное",
    "Пионерский",
    "Богданович",
    "Подпорожье",
    "Ясный",
    "Гудермес",
    "Чулым",
    "Комсомольск",
    "Вяземский",
    "Мезень",
    "Янаул",
    "Пермь",
    "Яровое",
    "Шенкурск",
    "Шатура",
    "Вольск",
    "Истра",
    "Тольятти",
    "Ростов-на-Дону",
    "Котово",
    "Вичуга",
    "Жуковка",
    "Нефтеюганск",
    "Северск",
    "Лысково",
    "Абдулино",
    "Мытищи",
    "Спасск-Дальний",
    "Буй",
    "Чкаловск",
    "Переславль-Залесский",
    "Лихославль",
    "Окуловка",
    "Инсар",
    "Кяхта",
    "Нижняя Салда",
    "Воркута",
    "Снежинск",
    "Исилькуль",
    "Элиста",
    "Кушва",
    "Омск",
    "Усолье",
    "Соликамск",
    "Феодосия",
    "Саки",
    "Рубцовск",
    "Туапсе",
    "Козьмодемьянск",
    "Шуя",
    "Дальнегорск",
    "Кореновск",
    "Заозёрный",
    "Нурлат",
    "Щёкино",
    "Омутнинск",
    "Белоярский",
    "Юрга",
    "Брянск",
    "Лениногорск",
    "Курск",
    "Александров",
    "Калачинск",
    "Володарск",
    "Братск",
    "Лермонтов",
    "Малмыж",
    "Анива",
    "Первоуральск",
    "Ряжск",
    "Елабуга",
    "Шарыпово",
    "Апатиты",
    "Темрюк",
    "Томск",
    "Амурск",
    "Краснознаменск",
    "Киренск",
    "Ачинск",
    "Добрянка",
    "Мурино",
    "Углич",
    "Сухой Лог",
    "Циолковский",
    "Люберцы",
    "Куса",
    "Льгов",
    "Керчь",
    "Богородицк",
    "Карачаевск",
    "Нея",
    "Обнинск",
    "Искитим",
    "Чусовой",
    "Оленегорск",
    "Нарьян-Мар",
    "Верея",
    "Ветлуга",
    "Киров",
    "Мегион",
    "Няндома",
    "Отрадное",
    "Белгород",
    "Сочи",
    "Балтийск",
    "Макаров",
    "Дагестанские Огни",
    "Задонск",
    "Могоча",
    "Узловая",
    "Лесосибирск",
    "Ялта",
    "Тутаев",
    "Ульяновск",
    "Владивосток",
    "Новый Уренгой",
    "Тосно",
    "Шали",
    "Ершов",
    "Пласт",
    "Михайловск",
    "Щучье",
    "Алупка",
    "Хадыженск",
    "Курганинск",
    "Орлов",
    "Макарьев",
    "Стрежевой",
    "Южа",
    "Палласовка",
    "Магадан",
    "Радужный",
    "Кудымкар",
    "Калач",
    "Курильск",
    "Нариманов",
    "Томари",
    "Нижний Новгород",
    "Гатчина",
    "Бакал",
    "Кондрово",
    "Татарск",
    "Шацк",
    "Асбест",
    "Зуевка",
    "Кодинск",
    "Нижнеудинск",
    "Якутск",
    "Павлово",
    "Бавлы",
    "Ленск",
    "Знаменск",
    "Теберда",
    "Камбарка",
    "Кинель",
    "Вязники",
    "Валуйки",
    "Серпухов",
    "Салехард",
    "Краснозаводск",
    "Таганрог",
    "Злынка",
    "Сретенск",
    "Советская Гавань",
    "Октябрьск",
    "Калуга",
    "Бердск",
    "Кашира",
    "Мариинск",
    "Красноуфимск",
    "Медногорск",
    "Солигалич",
    "Екатеринбург",
    "Шахунья",
    "Карталы",
    "Заинск",
    "Игарка",
    "Черемхово",
    "Малоярославец",
    "Великие Луки",
    "Мыски",
    "Туринск",
}
