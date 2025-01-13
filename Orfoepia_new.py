import random

nums_all = list(range(0, 87))
nums = set()

def GetRandomCnt(filename):
    num = random.choice(nums_all)
    if num not in nums:
        nums.add(num)
        return FindCntInFile(filename, num)
    else: pass

def FindCntInFile(filename, num):
    f = open(filename, "r", encoding="utf_8").read().splitlines()
    print(f[num].lower())
    return CorrectAnswer(f[num],\
                            ans = input('Введите слово с правильной постановкой ударения:\n---'))
cnt = 0
def CorrectAnswer(sentence, ans):
    global cnt
    if sentence == ans:
        print("Верно!\n\
----------------------------")
        cnt += 1
    else:  print(f"Неверно!\n\
Верно: {sentence}\n\
----------------------------")

if __name__ == '__main__':
    while len(nums)!=len(nums_all):
        GetRandomCnt(filename="list_orfoepy.txt")
    if len(nums) == len(nums_all):
        print("Слова закончились:)\n\
Счетчик верных слов:", cnt, f"\n\
Процент верных слов: {round((cnt/87)*100, 2)}%")
