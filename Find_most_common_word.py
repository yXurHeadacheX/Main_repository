import re
from collections import Counter

def most_common_word(text):
    words = re.findall(r'\b\w+\b', text.lower())
    counter = Counter(words)
    print(counter.most_common(3)[0][1])
    return counter.most_common(1)[0]

    # Пример использования:
if __name__ == "_main__":
    text = "Привет, мы виделись? Мы знакомы? Мы в целом кто? Кто мы? Кто? Кто? КТО?"
    result = most_common_word(text)
    print(result)
