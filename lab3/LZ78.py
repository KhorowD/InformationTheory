
'''
Данная программа реализует сжатие LZ78. Входные данные: строка для сжатия

Выходные данные, закодированная строка содержацая структуры следующего вида <position, char>

'''

class Node():

	position = None	#смещение от текущего символа
	char = None		#следующий (первый) символ после совпадающей подстроки


	def __init__(self, position, char):
		self.position = position
		self.char = char

	def __str__(self):
		return "<"+str(self.position)+","+self.char+">"


def LZ78_encode(inputString):


	'''
	Функция кодирования
	'''

	list_of_nodes = []
	buff = ""
	char_to_add = ""
	dict = {}

	for i in range(len(inputString)):
		#если в словаре есть строка
		if dict.get(buff + inputString[i]):
			buff += inputString[i] #тогда добавляем новый символ в буфер
		#Иначе добавляем новую строку в словарь и очищаем буфер
		else: 
			list_of_nodes.append(Node(0 if (dict.get(buff) is None) else dict.get(buff),inputString[i]))
			dict[buff + inputString[i]] = len(dict) + 1
			buff = "" 
	# Если буфер не пустой, то добавляем последний символ
	if not (buff == ""):
		last_char = buff[:-1]
		buff = buff[:len(buff)]
		list_of_nodes.append(Node(0 if (dict.get(buff) is None) else dict.get(buff) ,last_char))

	print(dict)
		
	return list_of_nodes
	


def LZ78_decode(encoded_list):

	'''
	Функция декодирования
	'''

	answer = ""
	dict_list = [""]
	for i in encoded_list:
		word = dict_list[i.position] + i.char
		answer += word
		dict_list.append(word)

	return answer

def main():
	print("LZ78 algorithm realization\n")
	string_for_encode = input("Введите строчку для сжатия:")
	encoded_list = LZ78_encode(string_for_encode)


	for i in encoded_list:
		print(i)



	print(LZ78_decode(encoded_list))



if __name__ == '__main__':
	main()