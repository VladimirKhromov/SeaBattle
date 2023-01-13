from __future__ import annotations

from random import randint, shuffle
from time import sleep
from typing import Optional


class Ship:
    """ Класс для представления кораблей """

    def __init__(self, length: int, tp: int = 1,
                 x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Инициализация корабля.

        x, y - координаты начала расположения корабля (целые числа);
        length - длина корабля (число палуб);
        tp - ориентация корабля (1 - горизонтальная; 2 - вертикальная);
        is_move - может ли корабль совершать движения.
        _cells - изначально список длиной length, состоящий из единиц
        Список _cells будет сигнализировать о попадании соперником в какую-либо палубу корабля.
        Если стоит 1, то попадания не было, а если стоит значение 2, то произошло попадание в соответствующую палубу.
        """
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * self._length

    def set_start_coords(self, x: int, y: int) -> None:
        """ Установка начальных координат. """
        self._x, self._y = x, y

    def get_start_coords(self) -> tuple:
        """ Получение начальных координат корабля в виде кортежа x, y. """
        return self._x, self._y

    def _check_coords(self) -> None:
        """ Проверка наличия координат у коробля. """
        if self._x is None or self._y is None:
            raise ValueError("Для получения кортежа координат коробля нужно задать начальные значения")

    def get_ship_coords(self) -> tuple:
        """ Возвращает кортеж координат корабля. """
        self._check_coords()  # проверяем установленны ли начальные координаты
        # Создаем лист коорданат х и y
        if self._tp == 1:
            x = [self._x + i for i in range(0, self._length)]
            y = [self._y] * self._length
        elif self._tp == 2:
            x = [self._x] * self._length
            y = [self._y + i for i in range(0, self._length)]
        else:
            raise ValueError("Неверно задано расположение корабля")
        # Создаем кортеж координат из координат х и y
        coords = tuple(zip(x, y))
        return coords

    def get_ship_coords_with_pole(self) -> tuple:
        """ Возвращает кортеж кортежей координат, на котором находится корабль, а также его окружение. """
        self._check_coords()  # проверяем установленны ли начальные координаты
        # Создаем лист коорданат х и y
        if self._tp == 1:
            x = [self._x + i for i in range(-1, self._length + 1) if self._x + i >= 0]
            y = [self._y + i for i in (-1, 0, 1) if self._y + i >= 0]
        elif self._tp == 2:
            x = [self._x + i for i in (-1, 0, 1) if self._x + i >= 0]
            y = [self._y + i for i in range(-1, self._length + 1) if self._y + i >= 0]
        else:
            raise ValueError("Неверно задано расположение корабля")
        # Создаем кортеж координат из координат х и y
        coords = tuple([(i, j) for i in x for j in y])
        return coords

    @property
    def is_move(self):
        return self._is_move

    def move(self, step: int = 1) -> None:
        """ Перемещение корабля в направлении его ориентации на step клеток. """
        if self._is_move:
            if self._tp == 1:
                self._x += step
            elif self._tp == 2:
                self._y += step

    def take_damage(self, coord: tuple) -> None:
        """ Получение урона по координатам coord корабля. """
        ship_coords = self.get_ship_coords()
        for indx, value in enumerate(ship_coords):
            if coord == value:
                self._cells[indx] = 2
                self._is_move = False

    def is_collide(self, ship: Ship) -> bool:
        """
        Проверка на столкновение с другим кораблем ship.
        Метод возвращает True, если столкновение есть и False - в противном случае.
        """
        main_ship = self.get_ship_coords_with_pole()
        other_ship = ship.get_ship_coords()
        lst_general_coords = (set(main_ship) & set(other_ship))
        if lst_general_coords:
            return True
        return False

    def is_out_pole(self, size: int) -> bool:
        """
        Проверка на выход корабля за пределы игрового поля.
        Возвращается True, если корабль вышел из игрового поля
        и False - в противном случае.
        """
        self._check_coords()
        for x, y in self.get_ship_coords():
            if x < 0 or x > size - 1 or y < 0 or y > size - 1:
                return True
        return False

    def __repr__(self):
        return f"Ship coor:{self._x}-{self._y}, tp:{self._tp}, len:{self._length}\n"

    def __getitem__(self, indx):
        if 0 <= indx < self._length:
            return self._cells[indx]

    def __setitem__(self, indx, value):
        self._cells[indx] = value

    def __len__(self):
        return len(self._cells)

    @property
    def cells(self):
        return self._cells


class GamePole:
    """ Класс для работы с игровым полем. """

    def __init__(self, size: int = 10) -> None:
        """
        Инициализация поля.

        Значения:
        _size - Размер игрового поля.
        _ships - Список кораблей на поле.
        """
        self._size = size
        self._ships = []

    def init(self) -> None:
        """ Начальная инициализация игрового поля. """
        # Создаем список кораблей
        self._ships.clear()
        for i in (4, 3, 3, 2, 2, 2, 1, 1, 1, 1):
            self._ships.append(Ship(i, tp=randint(1, 2)))

        # Расставляем координаты кораблей и проверяем на столкновение и выход за поле.
        other_ships = []
        for ship in self._ships:
            while True:
                # Задаем координаты
                x = randint(0, self._size - 1)
                y = randint(0, self._size - 1)
                ship.set_start_coords(x, y)
                if ship.is_out_pole(self._size):
                    continue

                # Проверяем на столкновение
                result = []
                for other_ship in other_ships:
                    result.append(ship.is_collide(other_ship))
                if any(result):
                    continue
                other_ships.append(ship)
                break

    def get_ships(self) -> list[Ship]:
        """ Возвращает список кораблей. """
        return self._ships

    def move_ships(self) -> None:
        """
        Перемещает каждый корабль из коллекции _ships на одну клетку (случайным образом вперед или назад)
        в направлении ориентации корабля; если перемещение в выбранную сторону невозможно
        (другой корабль или пределы игрового поля), то попытаться переместиться в противоположную сторону,
        иначе (если перемещения невозможны), оставаться на месте.
        """
        move_list = [1, -1]
        shuffle(move_list)
        for ship in self._ships:
            if not ship.is_move:
                continue

            origin_coords = ship.get_start_coords()
            ship.move(move_list[0])

            result = [ship.is_collide(other_ship) for other_ship in self._ships if ship != other_ship]
            if not any(result) and not ship.is_out_pole(self._size):
                continue

            ship.set_start_coords(*origin_coords)
            ship.move(move_list[1])

            result = [ship.is_collide(other_ship) for other_ship in self._ships if ship != other_ship]
            if not any(result) and not ship.is_out_pole(self._size):
                continue

            ship.set_start_coords(*origin_coords)

    def show(self) -> None:
        """
        Отображение игрового поля в консоли.
        Корабли отображаются значениями из коллекции _cells каждого корабля, вода - значением 0.
        """

        for row in self.get_pole():
            for i in row:
                print(i, end=' ')
            print()

    def get_pole(self) -> tuple:
        """
        Получение текущего игрового поля в виде двумерного кортежа размером size x size элементов.
        """
        game_pole = [["-" for _ in range(self._size)] for _ in range(self._size)]

        for ship in self._ships:
            result = ship.get_ship_coords()
            for i in range(len(result)):
                x, y = result[i][0], result[i][1]
                game_pole[x][y] = ship[i]

        gp = []
        for row in game_pole:
            gp.append(tuple(row))

        gp = tuple(gp)
        return gp

    def get_secret_pole(self, is_secret: bool = True) -> tuple:
        """
        Получение игрового поля в виде двумерного кортежа размером size x size элементов.
        В поле отображаются только подбитые корабли, остальное поле скрыто.
        """
        game_pole = [["-" for _ in range(self._size)] for _ in range(self._size)]
        secret = "-" if is_secret else "□"

        for ship in self._ships:
            if sum(ship.cells) == len(ship) * 2:  # если корабль полностью утонул
                result_pole = ship.get_ship_coords_with_pole()
                for i in range(len(result_pole)):
                    x, y = result_pole[i][0], result_pole[i][1]
                    if 0 <= x < self._size and 0 <= y < self._size:
                        game_pole[x][y] = "+"
                result = ship.get_ship_coords()
                for i in range(len(result)):
                    x, y = result[i][0], result[i][1]
                    game_pole[x][y] = secret if ship[i] == 1 else "■"

            else:  # если корабль ранен
                result = ship.get_ship_coords()
                for i in range(len(result)):
                    x, y = result[i][0], result[i][1]
                    game_pole[x][y] = secret if ship[i] == 1 else "■"

        gp = tuple(game_pole)
        return gp

    def is_all_ships_sank(self):
        """ Проверка что все коробли затонуты. """
        result = 0
        for ship in self._ships:
            result += sum(ship.cells)
        return False if result != 40 else True


class SeaBattle:
    """ Класс управления игровым процессом. """

    def __init__(self, size: int = 10) -> None:
        """
        Инициализация поля.

        Значения:
        _size - Размер игрового поля. """
        self.size = size
        self.people_pole: Optional[GamePole] = None
        self.computer_pole: Optional[GamePole] = None

    def init(self) -> None:
        """ Инициализирует игровые поля. """
        self.people_pole = GamePole(self.size)
        self.people_pole.init()
        self.computer_pole = GamePole(self.size)
        self.computer_pole.init()

    def show(self) -> None:
        """ Отображает поле игрока и поле компьютера."""
        areas = [self.people_pole.get_secret_pole(False), self.computer_pole.get_secret_pole()]
        first_part_str = ' ' * 4 if self.size < 10 else ' ' * 5
        second_part_str = 'You' + ' ' * 25 + 'Computer'
        print(first_part_str, second_part_str, sep='')
        for i in range(self.size):
            if i == 0:
                print(first_part_str[:-1], *range(1, self.size + 1), ' ' * 6, *range(1, self.size + 1))
                print()
            print(f'{str(i + 1):2} =', *areas[0][i], f' = {str(i + 1):2}= ', *areas[1][i])
            
    @staticmethod
    def _hit(pole: GamePole, coord: tuple) -> bool:
        """
        Производит проверку координат удара coord по кораблям расставленым на поле pole,
        и если попадание есть расставляет его на корабль.
        Возвращает False если удар не удачный, True - если корабль ранен.
        """
        aim = pole.get_pole()[coord[0]][coord[1]]
        if aim == "-":
            print("Промах!")
            return False
        elif aim == 2:
            print("Эта часть коробля уже подстрелена")
            return False
        elif aim == 1:
            print("Попадание!")
            for ship in pole.get_ships():
                if coord in ship.get_ship_coords():
                    ship.take_damage(coord)
                    break
            return True

    def _get_people_coord(self) -> tuple:
        """ Получение кортежа координат выстрела игрока. """
        error_message = f'Нужно ввести 2 координаты, в пределах от 1 до {self.size}, попробуйте еще'

        try:
            hit = tuple([i - 1 for i in list(map(int, input("Введите две координаты удара: ").split()))][::-1])
            assert len(hit) == 2
            assert 0 <= hit[0] < self.size
            assert 0 <= hit[1] < self.size
        except (ValueError, AssertionError):
            print(error_message)
            hit = self._get_people_coord()

        return hit

    def _get_comp_coord(self, pole: GamePole) -> tuple:
        """ Получение координат выстрела компьютера. """
        while True:
            coord = (randint(0, self.size - 1), randint(0, self.size - 1))

            if pole.get_secret_pole()[coord[0]][coord[1]] == "-":
                print(f"Компьютер бъет в координаты {coord[1] + 1} {coord[0] + 1}")
                break

        return coord

    def start_game(self) -> None:
        """ Игровой процесс. """
        self.init()
        print('*' * 5, "Добро пожаловать!", '*' * 5)

        while not self.people_pole.is_all_ships_sank() and not self.computer_pole.is_all_ships_sank():
            self.show()
            people_hits, comp_hits = True, True
            while people_hits:
                # Получаем координаты удара от игрока.
                hit = self._get_people_coord()

                # Проверяем нанесен ли удар по кораблю,
                # если да - поздравляем игрока, изменяем параметры корабля, повторяем удар
                people_hits = self._hit(self.computer_pole, hit)

                # Если все корабли затоплены - выходим
                if self.computer_pole.is_all_ships_sank():
                    break

                # Если попадание было цикл проходит еще раз
                if people_hits:
                    print("Попробуйте еще раз!")
                    self.show()

            print("** Ход компьютера. **")
            while comp_hits:
                # Получаем координаты удара компьютера
                hit = self._get_comp_coord(self.people_pole)

                comp_hits = self._hit(self.people_pole, hit)

                # Если все корабли затоплены - выходим
                if self.people_pole.is_all_ships_sank():
                    break

                # Если попадание было цикл проходит еще раз
                if people_hits:
                    print("Компьютер бъет еще раз!")

            # Корабли совершают маневр.
            self.people_pole.move_ships()
            self.computer_pole.move_ships()
            print('Корабли сменили местоположение')

        self.show()
        if self.people_pole.is_all_ships_sank():
            print('Ваша флотилия потерпела неудачу. Попробуйте еще раз!')
        elif self.computer_pole.is_all_ships_sank():
            print('Вы отличный капитан и потопили все вражеские корабли! Поздравляем!')

        sleep(1)


if __name__ == "__main__":
    battle = SeaBattle()
    battle.start_game()
