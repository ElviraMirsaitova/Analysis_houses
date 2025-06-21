import csv

# import json

# OUTPUT_FILENAME = "housing_data_output.json"

def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    houses_list = []
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_ = {
                "area_id": row["area_id"],
                "house_address": str(row["house_address"]),
                "floor_count": int(row["floor_count"]),
                "heating_house_type": row["heating_house_type"],
                "heating_value": float(row["heating_value"]),
                "area_residential": float(row["area_residential"]),
                "population": int(row["population"]),
            }
            houses_list.append(row_)

    #    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
    #        json.dump(houses_list, f,ensure_ascii=False, indent=4)

    return houses_list


def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома в виде строки:
    "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int):
        raise TypeError(f"У переменной floor_count должен быть тип int, не {type(floor_count)}")
    if floor_count <= 0:
        raise ValueError("Число floor_count должно быть положительным.")

    if floor_count in range(1, 6):
        return "Малоэтажный"
    if floor_count in range(6, 17):
        return "Среднеэтажный"
    return "Многоэтажный"


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    kategorii = []
    for i in houses:
        klass_doma = classify_house(i["floor_count"])
        kategorii.append(klass_doma)
    return kategorii


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    if isinstance(categories, list):
        podschet_kategoriy = {}  # Посчитать частоту упоминаний каждой категории

        for category in categories:
            if category not in podschet_kategoriy:
                podschet_kategoriy[category] = 1
            else:
                podschet_kategoriy[category] += 1
        return podschet_kategoriy


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес дома с минимальным средним количеством жилой площади на человека.

    Функция рассчитывает среднее количество квадратных метров жилой площади,
    приходящееся на каждого зарегистрированного жильца в доме.
    Среди всех домов функция возвращает адрес того дома, где эта величина минимальна.
    Такой подход позволяет выявлять дома с высокой плотностью заселения.

    :param houses: Список словарей с данными о домах.
    :return: Адрес дома с наименьшим средним количеством
    квадратных метров жилой площади на одного жильца.
    """
    min_square = houses[0]["area_residential"] / houses[0]["population"]
    for i in houses:
        square = i["area_residential"] / i["population"]
        min_square = min(min_square, square)
    return min_square

if __name__ == "__main__":
    #  проверка списка данных - 1 функция
    houses_data = read_file("housing_data.csv")
    #    print(houses_data)

    #  проверка категории этажности - 2 функция
    #    print(classify_house(17))

    #  проверка категориальности по этажности - 3 функция
    spisok_kategoryi = get_classify_houses(houses_data)
    #    print(spisok_kategoryi)

    #  проверка классификатора по типам этажности - 4 функция
    podschet_kategoryi = get_count_house_categories(spisok_kategoryi)
    print(podschet_kategoryi)

    #  проверка классификатора по типам этажности - 5 функция
    minimalnaya_ploshad = min_area_residential(houses_data)
    print(minimalnaya_ploshad)

