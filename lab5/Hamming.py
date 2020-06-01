"""
Реализация алгоритма Хемминга
"""
from math import log2
from random import randint
"""
Функция замены некоректного бита в строке 
"""
def changeBit(code,bit_number):
	bit_value = "0"
	if code[bit_number] == bit_value:
		return code[:bit_number] + "1" + code[bit_number+1:]
	else:
		return code[:bit_number] + "0" + code[bit_number+1:]

"""
Функция деления строки на подстроки и поиск суммы для контрольных битов
"""
def makeSubStrSumm(code, step, check_bit_pos, isEncode):
	sub_str = [code[i:i+step] for i in range(check_bit_pos, len(code), step)]
	sub_str = sub_str[::2]
	concatenated_str = ""

	for i in sub_str:
		concatenated_str += i
				
	summ = 0

	if isEncode==True:
		for ch in concatenated_str:
			summ += int(ch) 
	else:
		for i in range(1,len(concatenated_str)):
			summ += int(concatenated_str[i])
		

	return summ % 2

def inputBytes():
	return input("Введите последовательность бит для кодирования: ")
"""
Функция проверки строки на ошибки
"""
def Hemming_code_check(string_for_check):
	number_chk_bits = int(log2(len(string_for_check))) + 1
	print("Число контрольных бит: "+ str(number_chk_bits))
	error_list = []
	encode_flag = False

	for i in range(number_chk_bits):
		
		chk_bit_value = makeSubStrSumm(string_for_check,2**i,(2**i)-1,encode_flag)
		if chk_bit_value != int(string_for_check[2**i-1]):
			
			error_list.append(2**i)
	
	# print(error_list)	
	error_place = 0
	if len(error_list) > 0 :
		for i in error_list:
			error_place += i
		print("Error in "+str(error_place-1)+" position")
		return changeBit(string_for_check,error_place-1)
	else:
		print("Errors not detected")
		return string_for_check

"""
Функция кодирования
"""
def Hemming_encode(inputStr, number_of_positions):
	result_str = ""
	power = 0
	position_in_inpStr = 0
	encode_flag = True
	# Собираем строку с проверочными битами
	for i in range(1, number_of_positions+len(inputStr)+1):
		if i == 2**power:
			result_str += "0"
			power += 1
		else:
			result_str += inputStr[position_in_inpStr]
			position_in_inpStr += 1
		

	print("Макет для заполнения: " + result_str)


	# Устанавливаем значения
	
	for i in range(number_of_positions):
		
		chk_bit_value = makeSubStrSumm(result_str,2**i,(2**i)-1,encode_flag)
		
		result_str = result_str[:(2**i)-1]+str(chk_bit_value)+result_str[(2**i):]
		

	return result_str
"""
Функция декодирования
"""
def Hemming_decode(str_for_decode):
	
	checked_str = Hemming_code_check(str_for_decode)
	
	number_chk_bits = int(log2(len(checked_str))) + 1
	
	result_str = ""
	power = 0

	for i in range(len(checked_str)):
		
		if i != 2**power-1:
			result_str += checked_str[i]
			
		else:
			power += 1
		
	return result_str



"""
Функция которая считает кол-во проверочных бит
Для входной последовательности бит 
"""
def numberCheckBits(lenght):
	for i in range(lenght):
		if (lenght + i + 1 <= 2**i):
			return i



"""
Главная функция
"""
def main():
	# Вводим последовательность бит
	string_from_cli = inputBytes()
	# Находим число бит для проверки
	number_chk_bits = numberCheckBits(len(string_from_cli))
	#Выполняем кодирование
	encoded_string = Hemming_encode(string_from_cli, number_chk_bits)

	print("Encoded string: " + encoded_string+"\n")
	print("Проверочные биты выделены [ ]\n")
	perfect_output = ""
	power = 0
	for i in range(1, len(encoded_string)+1):
		if i == 2**power:
			perfect_output += ("["+encoded_string[i-1]+"]")
			power += 1
		else:
			perfect_output += encoded_string[i-1]
	print(perfect_output+"\n")
	
	
	#сгенерируем ошибку в любой позиции закодированной строки
	randomError = randint(0,len(encoded_string)-1)

	print("Ошибка в позиции: ", randomError)

	if encoded_string[randomError] == "1":
		encoded_string = encoded_string[:randomError] + "0" + encoded_string[randomError+1:] 
	else:
		encoded_string = encoded_string[:randomError] + "1" + encoded_string[randomError+1:] 

	print("Декодируем строку с ошибкой:", encoded_string)
	decoded_string = Hemming_decode(encoded_string)
	print("Decoded string: " + decoded_string)


if __name__ == '__main__':
	main()