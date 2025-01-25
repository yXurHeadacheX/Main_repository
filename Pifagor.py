class Pifagor():
    def __init__(self, nums_1: float, nums_2: float):
        self.nums1 = nums_1
        self.nums2 = nums_2

    def Solution_Pifagor_catheter(self) -> float:
        from math import sqrt
        return sqrt(self.nums1**2 - self.nums2**2)

    def Solution_Pifagor_hypotenuse(self) -> float:
        from math import sqrt
        return sqrt(self.nums1**2 + self.nums2**2)

if __name__ == '__main__':
    print("Запуск...Class Pifagor")
    P = Pifagor(

        nums_1=float(input("Введите первое число(если известна гипотенуза, то сюда)\n")),
        nums_2=float(input("Введите второе число(точно катет)\n"))

                )
    print(P.Solution_Pifagor_catheter()) \
        if input("1: Если нужен КАТЕТ\n2: Если нужна ГИПОТЕНУЗА\n")=="1" else\
    print(P.Solution_Pifagor_hypotenuse())
