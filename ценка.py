class AveragesMark_plus_recommendations():
    def __init__(self, five:int, four:int, three:int, two:int):
        self.five = five
        self.four = four
        self.three = three
        self.two = two

    def Solution_Marks(self) -> str:
        all_mark = self.five + self.four + self.three + self.two
        middle_mark = (self.five * 5) + (self.four * 4) + (self.three * 3) + (self.two * 2)
        need_five = 0
        need_four = 0
        need_three = 0
        print(f"Средний балл:{round(middle_mark/all_mark, 2)}")

        ask_need = int(input('Какая оценка вас интересует?\n1) 5\n2) 4\n3) 3\n'))
        if ask_need == 1:
            while middle_mark/all_mark < 4.5:
                all_mark += 1
                middle_mark += 5
                need_five += 1
            return f'До пятерки осталось заработать ещё {need_five} пятерок(-ку).'
        if ask_need == 2:
            while middle_mark/all_mark < 3.5:
                all_mark += 1
                middle_mark += 5
                need_four += 1
            return f'До четверки осталось заработать ещё {need_five} четверок(-ку).'
        if ask_need == 3:
            while middle_mark / all_mark < 3.5:
                all_mark += 1
                middle_mark += 5
                need_three += 1
            return f'До тройки осталось заработать ещё {need_five} троек(-йку).'

if __name__ == "__main__":
    A = AveragesMark_plus_recommendations(

        five= int(input("Сколько пятерок?\n")),
        four= int(input("Сколько четверок?\n")),
        three= int(input("Сколько троек?\n")),
        two= int(input("Сколько двоек?\n"))

    )
    print(A.Solution_Marks())
