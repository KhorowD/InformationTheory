"""
Объявляем структуру, которая хранит - символ, его частоту, и закодированное значение
"""
class Element():
	
	def __init__(self,char, code, value):
		self.char = char
		self.code = code
		self.value = value
		
"""
Функция декодирования
"""
def shannon_fano_decode(encoded_string, elements):

	code = encoded_string.split()
	print(code)
	decode = ""

	for i in code:
		for element in elements:
			if element.code == i:
				decode += element.char
	return decode 


"""
Функция кодирования
"""
def  shannon_fano_encode(freq):
	
	summ = 0
	for i in freq:
		summ += i.value

	middle = summ/2 # Ищем середину
	current_value = 0

	top = []
	bottom = [] 

	# В зависимости от частоты добавляем элементы в два новых массива,
	# которые передаем в рекурсивную функцию.
	# одновременно формируем и вторичный код
	for i in freq:
		if current_value < middle:
			i.code += "0"
			bottom.append(i)
			current_value += i.value
		else:
			i.code += "1"
			top.append(i)
			
	# если длина массива больше 1, то вызываем еще раз функцию
	if len(top) != 1:
		shannon_fano_encode(top)
	if len(bottom) != 1:
		shannon_fano_encode(bottom)

	return freq
	
"""
Функция, которая обрабатывает поданную на вход строку для кодирования
"""
def input_string():
	s = input()
	freq_list = []
	is_first_itteration = True
	prev_element = 0
	added_elements = []

	for ch in s:
		if is_first_itteration:
			prev_element = Element(ch,"",s.count(ch)/len(s))
			freq_list.append(prev_element)
			added_elements.append(ch)
			is_first_itteration = False
			print("first")
			continue
		if ch != prev_element.char and (ch not in added_elements):
			prev_element = Element(ch,"",s.count(ch)/len(s))
			freq_list.append(prev_element)
			added_elements.append(ch)
	
	print(added_elements)	
	print(len(freq_list))

	freq_list = sorted(freq_list, key=lambda x: x.value, reverse=True)
	for i in range(len(freq_list)):
		print(freq_list[i].value)

	print(freq_list)	
	return freq_list, s


"""
Функция, которая обрабатывает поданные на вход вероятности
"""
def input_probabilities():
	freq_list = input()
	freq_list = freq_list.split(" ")
	freq_list.sort(reverse=True)
	
	print(freq_list)
	position = 0
	for i in range(len(freq_list)):
		position += 1
		char_name = "a"+str(position)
		freq_list[i] = Element(char_name,"", float(freq_list[i]))
		print(freq_list[i].char, freq_list[i].value)
	return freq_list
	
"""
Главная функция, старт программы
"""
def main():
	
	probabilities = []
	chars = []
	answer = ""
	string_from_cli = "" #Строка входных данных
	output_code = ""
	

	while answer != "correct":
		print()
		print("chose the way to input data:")
		print("1. String")
		print("2. Probability list")
		
		answer = input("Enter number 1 or 2: ")
		
		if answer == "1":
			print(string_from_cli)
			probabilities, string_from_cli = input_string()
			answer = "correct"
		
		elif answer == "2":
			
			probabilities = input_probabilities()

			print(probabilities)

			answer = "correct"

		else: 
			print("Try again")

	data = shannon_fano_encode(probabilities)
	
	for i in data:
		print(i.char +" "+  i.code)
	#Собираем закодированную строку
	for ch in string_from_cli:
		for i in data:
			if i.char == ch:
				output_code += i.code+" "
	
	print(string_from_cli)

	print("encoded string:")
	print()
	print(output_code)
	print()
	print(shannon_fano_decode(output_code, data))


if __name__ == '__main__':
	main()

