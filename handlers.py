import datetime
import json

from ru.travelfood.simple_ui import NoSQL as noClass


db_all_birds = noClass("birds_2212")
db_birds_which_i_saw = noClass("birds_which_i_saw")


class hashMap:
    def get(self, key: str) -> str:
        """
        Получение значения из hashMap
        """

        pass

    def put(self, key: str, value: str):
        """
        Внесение значения в hashMap
        """

        pass

    def containsKey(self, key: str) -> bool:
        """
        Проверка на вхождение ключа в словарь
        """

        pass

    def remove(self, key: str):
        """
        Удаление ключа из словаря
        """

        pass

#################################################
# -------------- Процесс "Птицы" -------------- #


# ////// Экраны ////// #


def show_birds(hashMap: hashMap, _files=None, _data=None):
    """
    Экран, который запускается при запуске процесса "Птицы"
    """

    birds_cards = {"customcards": {
        "options": {
          "search_enabled": True,
          "save_position": True
        },

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {
                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@bird_picture",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "match_parent",
                            "height": "wrap_content",
                            "weight": 2
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@bird_name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@bird_color",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                            ]
                        },
                    ]
                },
            ]
         }
        }
    }

    birds_cards["customcards"]["cardsdata"] = []

    keys_str = db_all_birds.getallkeys()
    keys = json.loads(str(keys_str).encode("utf-8"))
    for key in keys:
        bird_data_str = db_all_birds.get(key)
        bird_data = json.loads(bird_data_str)
        obj = {
            "key": key,
            "bird_name": key,
            "bird_color": bird_data.get("bird_color"),
            "bird_picture": bird_data.get("bird_picture"),
        }
        birds_cards["customcards"]["cardsdata"].append(obj)
    hashMap.put("cards", json.dumps(birds_cards, ensure_ascii=False).encode('utf8').decode())
    return hashMap


# ////// Обработчики кнопок ////// #


def show_add_bird_screen(hashMap, _files=None, _data=None):
    """
    Запуск экрана с добавление птицы
    """

    hashMap.put("ShowScreen", "Добавление птицы")
    return hashMap


def create_bird(hashMap: hashMap, _files=None, _data=None):
    """
    Создание птицы
    """

    bird_name = hashMap.get("bird_name")

    # проверка на уникальность...

    bird_color = hashMap.get("bird_color")

    bird_data = {
        "bird_color": bird_color,
        "bird_picture": None,
    }
    db_all_birds.put(bird_name, json.dumps(bird_data, ensure_ascii=False), True)

    hashMap.put("toast", f"Птица успешно создана. {bird_name.upper()}")

    return hashMap


def show_bird_screen(hashMap: hashMap, _files=None, _data=None):
    """
    Показать конкретную птицу из списка
    """

    hashMap.put("ShowScreen", "Птица")
    bird_name = hashMap.get("selected_card_key")
    # повтор
    bird_data_str = db_all_birds.get(bird_name)
    bird_data = json.loads(bird_data_str)
    bird_color = bird_data.get("bird_color")
    bird_picture = bird_data.get("bird_picture")

    hashMap.put("bird_name", str(bird_name))
    hashMap.put("bird_color", str(bird_color))
    return hashMap


def destroy_all_keys(hashMap: hashMap, _files=None, _data=None):
    """
    Удаление всех птиц из базы данных "db_all_birds"
    """

    db_all_birds.destroy()
    hashMap.put("FinishProcess", "Птицы")
    hashMap.put("toast", "Все ключи базы данных удалены.")
    return hashMap


def add_bird_which_i_saw_in_hashMap(hashMap: hashMap, _files=None, _data=None):
    """
    Добавление птицы, которую "я" видел в хешмапу
    """

    if hashMap.containsKey("_birds_which_i_saw"):
        birds_which_i_saw = hashMap.get("_birds_which_i_saw")
        birds_which_i_saw += "," + hashMap.get("selected_card_key")
        hashMap.put("_birds_which_i_saw", birds_which_i_saw)
    else:
        hashMap.put("_birds_which_i_saw", hashMap.get("selected_card_key"))
    hashMap.put("toast", f"Птица: {hashMap.get('selected_card_key')} добавлена в список")
    return hashMap

# -------------------------------------------- #
################################################


######################################################
# -------- Процесс "Птицы, которых я видел" -------- #


# ////// Экраны ////// #


def show_birds_which_i_see_screen(hashMap: hashMap, _files=None, _data=None):
    """
    Экран, который запускается при запуске процесса "Птицы которых я видел"
    """

    birds_cards = {"customcards": {
        "options": {
          "search_enabled": True,
          "save_position": True
        },

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {
                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@bird_picture",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "match_parent",
                            "height": "wrap_content",
                            "weight": 2
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@bird_name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@count_saw",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@updated_date",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@created_date",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                            ]
                        },
                    ]
                },
            ]
         }
        }
    }

    birds_cards["customcards"]["cardsdata"] = []

    keys_str = db_birds_which_i_saw.getallkeys()
    keys = json.loads(str(keys_str).encode("utf-8"))
    for key in keys:
        bird_data_str = db_birds_which_i_saw.get(key)
        bird_data = json.loads(bird_data_str)
        obj = {
            "key": key,
            "bird_name": key,
            "bird_picture": bird_data.get("bird_picture"),
            "count_saw": bird_data.get("count_saw"),
            "updated_date": bird_data.get("updated_date"),
            "created_date": bird_data.get("created_date"),
        }
        birds_cards["customcards"]["cardsdata"].append(obj)
    hashMap.put("cards", json.dumps(birds_cards, ensure_ascii=False).encode('utf8').decode())
    return hashMap


# ////// Обработчики кнопок ////// #


def create_birds_which_i_saw(hashMap: hashMap, _files=None, _data=None):
    """
    Внесение птицы, которую(-ых) я видел в БД "db_birds_which_i_saw"
    """

    if hashMap.containsKey("_birds_which_i_saw") and hashMap.get("_birds_which_i_saw") is not None:
        birds_which_i_saw = hashMap.get("_birds_which_i_saw").split(",")
    else:
        hashMap.put("toast", "Список птиц на добавление пуст")
        return hashMap

    for bird in birds_which_i_saw:
        bird_data_str = db_birds_which_i_saw.get(bird)
        if bird_data_str:
            bird_data = json.loads(bird_data_str)
            new_bird_data = {
                "updated_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                "created_date": bird_data.get("created_date"),
                "bird_name": bird,
                "bird_picture": bird_data.get("bird_picture"),
                "count_saw": int(bird_data.get("count_saw")) + 1
            }
        else:
            bird_data_str = db_all_birds.get(bird)
            bird_data = json.loads(bird_data_str)
            bird_picture = bird_data.get("bird_picture")

            new_bird_data = {
               "updated_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
               "created_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
               "bird_name": bird,
               "bird_picture": bird_picture,
               "count_saw": 1,
            }
        db_birds_which_i_saw.put(bird, json.dumps(new_bird_data, ensure_ascii=False), True)
    hashMap.put("toast", hashMap.get("_birds_which_i_saw"))
    # удалить из hashMap remove не работает??? можно указать значение None = костыль
    hashMap.put("_birds_which_i_saw", None)

    return hashMap

# -------------------------------------------------- #
######################################################
