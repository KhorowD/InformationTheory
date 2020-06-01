'''
Данная программа реализует сжатие LZ77. Входные данные: строка для сжатия, размер скользящего
окна (буфера). Отличительная особенность программы в том, что при поиске очередной подстроки используется цикличный
буфер, позволяющий оптимальнее сжимать текст.

Выходные данные, закодированная строка содержацая структуры следующего вида <offset, Lenght, char>

'''
class Node():

	'''
	структура которая содержит в себе следующие данные для кодирования
	'''
	offset = None	#смещение от текущего символа
	lenght = None	#Длина совпадающей подстроки
	char = None		#следующий (первый) символ после совпадающей подстроки


	def __init__(self, offset, lenght, char):
		self.offset = offset
		self.lenght = lenght
		self.char = char

	def __str__(self):
		return "<"+str(self.offset)+","+str(self.lenght)+","+self.char+">"


def findWordInDictionary(buffer, currentPosition, inputStr):

	'''
	функция, которая ищет подстроку максимальной длины, при этом учитывает цикличный буфер
	'''
	max_substring_lenght = 0 #длина максимальной подстроки
	max_substring_pos = 0 #индекс указывающий на позицию в буффере,с которой начинается максимальная подстрока
	count = 0 #счетчик совпавших символов
	positions_list = [] # список индексов элемнтов в буфере, в котором встречается первый символ после окна


	# Для начала ищем все места в буфере, в которых встречается первый символ подстроки
	for i in range(len(buffer)):
		if  inputStr[currentPosition] == buffer[i]:
			positions_list.append(i)

	#флаг для выхода из цикла поиска максимальной подстроки
	isEndSearching = False

	for i in range(len(positions_list)): # Для каждого найденного индекса в буфере
		buff_position = positions_list[i]
		curr_pos = currentPosition
		count = 0
		while not isEndSearching:
			# Если мы не дошли до конца строки и значения буффера и подстроки совпадают
			if (curr_pos < len(inputStr)) and (buffer[buff_position] == inputStr[curr_pos]): 
				count += 1
				buff_position += 1
				curr_pos += 1
				# трюк, позволяющий нам зациклить буффер в момент поиска максимальной подстроки
				if buff_position % len(buffer) == 0:
					buff_position = 0
			else:
				isEndSearching = True

		# если нашли строку большей длины
		if count > max_substring_lenght:
			max_substring_lenght = count
			max_substring_pos = positions_list[i]
		
	# если строка в буфере не найдена, тогда добавляем просто символ
	# иначе, находим значение offset
	if max_substring_lenght == 0:
		max_substring_pos = 0
	else:
		max_substring_pos = len(buffer) - max_substring_pos 
	
	return max_substring_pos, max_substring_lenght


def moveBuffer(buffer, nextSymbolPosition, inputStr, buff_size):

	'''
	Сдвиг буфера работает след. образом: пока размер буфера меньше размера заданного пользователем
	то мы увеличиваем буфер на число lenght + 1, иначе также сдвигаемся на lenght + 1, но копируем 
	только пять символов от новой позиции в направлении движения текста. 
	'''

	copied_buffer = ""
	if len(buffer) < buff_size and nextSymbolPosition <= buff_size:
		copied_buffer = inputStr[0:nextSymbolPosition]
	else:
		copied_buffer = inputStr[nextSymbolPosition-buff_size:nextSymbolPosition]


	return copied_buffer


def LZ77_encode(inputString, window_size):

	'''
	Функция кодирования
	'''

	list_of_nodes = []
	position = 0
	new_symbol_pointer = 0  
	buff = ""
	char_to_add = ""
	while position < len(inputString):
		offset, lenght = findWordInDictionary(buff, position, inputString)

		# увеличиваем указатель на следующий символ
		position += lenght + 1
		
		#обработка конца файла
		# if position >= len(inputString):
		# 	char_to_add = "eof"
		# else:
		# 	char_to_add = inputString[position-1]

		if position > len(inputString):
			char_to_add = "eof"
		else:
			char_to_add = inputString[position-1]
		
		# добавляем новый код 
		list_of_nodes.append(Node(offset, lenght, char_to_add))
		# двигаем окно
		buff = moveBuffer(buff, position, inputString, window_size)
		
			
	return list_of_nodes


def LZ77_decode(encoded_list):

	'''
	Функция декодирования

	просто проходим по коду и выполняем обратное преобразование
	'''

	answer = ""
	for i in encoded_list:
		if i.lenght > 0:
			start = len(answer) - i.offset
			for j in range(0,i.lenght):
				answer += answer[start+j]
		answer += i.char
	return answer

def main():
	print("LZ77 algorithm realization\n")
	string_for_encode = input("Введите строчку для сжатия:")
	buffer_size = int(input("введите размер буффера:"))
	encoded_list = LZ77_encode(string_for_encode,buffer_size)

	print("Encoded list")
	for i in encoded_list:
		print(i)
	


	print("decoded string: "+LZ77_decode(encoded_list))
	print("decoded string: "+LZ77_decode(encoded_list)[:-3])

if __name__ == '__main__':
	main()