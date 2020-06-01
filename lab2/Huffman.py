import copy # библиотека для копирования списков

"""
Объявляем структуру, которая хранит - символ, его частоту,
 и закодированное значение.
 Кроме того, структура содержит ссылки на левый и правый 
 предок, тем самым можно констурировать бинарное дерево
"""
class Node():

	def __init__(self,char, code, value, left_child, right_child):
		self.char = char
		self.code = code
		self.value = value
		self.left_child = left_child
		self.right_child = right_child


"""
Функция декодирования
"""
def huffman_decode(encoded_string, elements):
	
	code = encoded_string.split()
	
	decode = ""

	for i in code:
		for element in elements:
			if element.code == i:
				decode += element.char
	return decode 



"""
Функция кодирования
"""
def  huffman_encode(freq,codes):
	

	if len(freq) > 1: #если массив соджержит больше 1 элемента
		
		#Устанавливаем код элемента на текущей итерации 
		for i in range(len(codes)):
			if codes[i].char in freq[len(freq)-1].char:
				codes[i].code += "0"
			if codes[i].char in freq[len(freq)-2].char:
				codes[i].code += "1"


		min_freq_node_1 = freq.pop()
		min_freq_node_2 = freq.pop()
		print("current itteration values:")
		print(min_freq_node_1.value)
		print(min_freq_node_2.value)

		

		# Добавляем соответственно коды
		min_freq_node_1.code += "0"
		min_freq_node_2.code += "1"
		

		#Формируем новый узел, где его потомки будут наименьшие два узла
		#а значение узла будет сумма вероятностей его ветвей 
		new_node = Node(min_freq_node_1.char + min_freq_node_2.char,"", \
						min_freq_node_1.value + min_freq_node_2.value, min_freq_node_1, min_freq_node_2)
		
		freq.append(new_node) # Добавляем в конец текущего списка
		

		#Сортируем список, для избежания проблем с кодированием
		freq = sorted(freq, key=lambda x: x.value, reverse=True)

		#Делаем рекурсивный вызов функции
		huffman_encode(freq,codes)

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
			prev_element = Node(ch,"",s.count(ch)/len(s),"","")
			freq_list.append(prev_element)
			added_elements.append(ch)
			is_first_itteration = False
			
			continue
		if ch != prev_element.char and (ch not in added_elements):
			prev_element = Node(ch,"",s.count(ch)/len(s),"","")
			freq_list.append(prev_element)
			added_elements.append(ch)


	freq_list = sorted(freq_list, key=lambda x: x.value, reverse=True)
	for i in range(len(freq_list)):
		print(freq_list[i].value)

	
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
		freq_list[i] = Node(char_name,"", float(freq_list[i]),"","")
		print(freq_list[i].char, freq_list[i].value)
	return freq_list
	
"""
Главная функция, старт программы
"""
def main():
	
	probabilities = [] #Массив nodes
	chars = []
	codes = []
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

	codes_list = copy.deepcopy(probabilities)
	
	print("call encode function")

	data = huffman_encode(probabilities,codes_list)

	
	for i in codes_list:
		i.code = i.code[::-1] #переворачиваем строку
		print(i.char + " " + i.code)
	

	#Собираем закодированную строку
	for ch in string_from_cli:
		for i in codes_list:
			if i.char == ch:
				output_code += i.code+" "
	
	print("input string: " + string_from_cli)
	print("output code: " + output_code)
	print()
	print("decoded string:")
	print(huffman_decode(output_code, codes_list))


if __name__ == '__main__':
	main()

