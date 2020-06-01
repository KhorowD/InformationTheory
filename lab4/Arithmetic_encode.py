class Element():
    """
    Структура которая хранит символ и его частоту
    """

    def __init__(self, value, char):
        self.value = value
        self.char = char
    def __str__(self):
        return self.char + ": " + str(self.value)

class Segment():
    """
    Структура которая хранит символ и его границы
    """
    RightBorder = 0.0
    LeftBorder = 0.0
    char = ""

    def __init__(self, right, left, char):
        self.RightBorder = right
        self.LeftBorder = left
        self.char = char
    def __str__(self):
        return self.char + ": " + str(self.LeftBorder) + " " + str(self.RightBorder)

"""
Функция, которая обрабатывает поданную на вход строку для кодирования
"""
def input_string():
    s = input("Введите строку для кодирования: ")
    freq_list = []
    is_first_itteration = True
    prev_element = 0
    added_elements = []

    for ch in s:
        if is_first_itteration:
            prev_element = Element(s.count(ch)/len(s),ch)
            freq_list.append(prev_element)
            added_elements.append(ch)
            is_first_itteration = False
            # print("first")
            continue
        if ch != prev_element.char and (ch not in added_elements):
            prev_element = Element(s.count(ch)/len(s),ch)
            freq_list.append(prev_element)
            added_elements.append(ch)
    
    # print(added_elements)   
    # print(len(freq_list))

    freq_list = sorted(freq_list, key=lambda x: x.value, reverse=True)
    for i in range(len(freq_list)):
        print(freq_list[i].char, freq_list[i].value)

    # print(freq_list)    
    return freq_list, s

"""
Функция которая из входных вероятностей делает отрезки(сегменты)
"""
def makeSegments(probs):
    top = 1.0 #Верхняя граница
    bottom = 0.0 #Нижняя граница
    segment_list = [] #Список сформированнызх интервалов

    for i in probs:
        top_segment = top
        bottom_segment = top - i.value
        segment_list.append(Segment(top_segment, bottom_segment, i.char))
        top = bottom_segment

    return segment_list


"""
Функция кодирования
"""
def arithmetic_encode(segments, inputStr):
    top = float(1)
    bottom = float(0)

    for i in range(len(inputStr)):
        for j in segments:
            if j.char == inputStr[i]:
                new_top = recalculation(bottom, top-bottom, j.RightBorder)
                new_bottom = recalculation(bottom, top-bottom, j.LeftBorder)
                top, bottom = new_top,new_bottom

    print("Итоговый интервал: ")
    print(bottom,top)

    return (top+bottom)/2
    

"""
Функция декодирования
"""
def ariarithmetic_decode(segments, code, inputStr):
    decoded = ""
    for i in range(len(inputStr)):
        for j in segments:
            if j.LeftBorder <= code < j.RightBorder:
                decoded += j.char
                code = (code - j.LeftBorder)/ (j.RightBorder-j.LeftBorder)
                break
    return decoded


"""
функция для перерасчета
"""
def recalculation(oldLow, old_range, Symbol_segment_range):
    return oldLow+old_range*Symbol_segment_range



"""
Главная функция, старт программы
"""
def main():
    
    probabilities = [] #Массив elemnts
    segments = [] #Массив segments
    answer = ""
    string_from_cli = "" #Строка входных данных
    output_code = ""
    

    #получаем входную строку и список вероятностей
    probabilities, string_from_cli = input_string()
    
    #делаем из списка вероятностей список сегментов
    segments = makeSegments(probabilities)
    print("Сформированные сегменты:\n")
    for segment in segments:
    	print(str(segment))
    
    #Кодируем текущую строку
    code = arithmetic_encode(segments, string_from_cli)
    
    print("Закодированная строка: " + str(code))


    #Декодируем текущую строку
    decoded_string = ariarithmetic_decode(segments, code, string_from_cli)

    print("Декодированная строка: " + decoded_string)



if __name__ == '__main__':
    main()




