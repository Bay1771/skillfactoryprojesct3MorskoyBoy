def move(self):
    while True:
        try:
            target = self.ask()
            repeat = self.enemy.shot(target)
            return repeat
        except BoardException as e:
            print(e)


class AI(Player):
    def ask(self):
        return Dot(randint(0, 5), randint(0, 5))

    def move(self):
        # ИИ перехватывает ошибки молча, чтобы не спамить в консоль
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                print(f"Ход компьютера: {target.x + 1} {target.y + 1}")
                return repeat
            except BoardException:
                pass


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход (строка столбец): ").split()
            if len(cords) != 2:
                print("Введите 2 координаты через пробел!")
                continue

            x, y = cords

            if not x.isdigit() or not y.isdigit():
                print("Координаты должны быть числами!")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


# --- Класс Игры ---
class Game:
    def init(self, size=6):
        self.size = size
        self.lens = [3, 2, 2, 1, 1, 1, 1]

        pl = self.random_board()
        co = self.random_board()
        co.hid = True  # Скрываем корабли ИИ

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветствуем вас ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)

            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1  # Если попадание, счетчик ходов не увеличивается (игрок ходит еще раз)

            if self.ai.board.count == len(self.lens):
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == len(self.lens):
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if name == "main":
    g = Game()
    g.start()