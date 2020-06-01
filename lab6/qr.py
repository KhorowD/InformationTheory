import const
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

"""
Функция проверки маски
"""
def is_mask_true(row,col):
    return (row+col)%2 == 1 # если маска равна единице не инвертируем бит

"""
Функция отрисовки данных
"""

def draw_data(pixels, data):
    size = len(pixels)
    str_bits = "" #.join(data)
    for k in data:
        str_bits += k #(bin(k)[2:]).rjust(8, '0')
    print(str_bits)
    print(len(str_bits))


    # print(np.count_nonzero(pixels ==-1))
    i = size - 1
    j = size - 1
    place = 0
    try:
        up_forw_module = True
        while j > 0: # идём по столбацам справа на лево и отнимаем 2 - типо один модуль
            if up_forw_module:
                for i in range(size-1,-1,-1):
                    if pixels[i][j]==-1: #правый
                        pixels[i][j] = (int(str_bits[place]) ^ 1) if is_mask_true(i,j) else int(str_bits[place])
                        place +=1
                    if pixels[i][j-1] == -1: #левый
                        pixels[i][j-1] = (int(str_bits[place]) ^ 1) if is_mask_true(i,j-1) else int(str_bits[place])
                        place += 1
                up_forw_module = False # следующий модуль вниз идёт
            else:
                for i in range(0,size,1):
                    if pixels[i][j]==-1: #правый
                        pixels[i][j] = (int(str_bits[place])^1) if is_mask_true(i,j) else int(str_bits[place])
                        place +=1
                    if pixels[i][j-1] == -1: #левый
                        pixels[i][j-1] = (int(str_bits[place])^1) if is_mask_true(i,j-1) else int(str_bits[place])
                        place += 1
                up_forw_module = True # следующий модуль вверх идёт
            j -=2
            if j == 6: # левая полоса синхронизации
                j -= 1
        return pixels
    except IndexError as e: # потому что кол-ва бит данных мб меньше свободного места и вылетет прога ( маску не наложил на последок, но и так работает)
        return pixels

    return pixels



"""
Функция отрисовки кода маски и уровня коррекции
"""
def draw_code_mask_and_correct_level(pixels):
    code = "101010000010010" # нулевая маска и уровень корекции М (15%)
    #code = "111111111111111"
    # заполняем вокруг левого верхнего
    # 0-7 биты
    place = 0
    for j in range(0,8):
        if pixels[8][j] ==-1:
            pixels[8][j] = int(code[place]) ^ 1
            place +=1

    i = 8

    while i >=0:
        if pixels[i][8] ==-1:
            pixels[i][8] = int(code[place])^1
            place +=1
        i -=1
    place = 0
    j = len(pixels)-1
    while j > len(pixels)-8:
        if pixels[j][8] ==-1:
            pixels[j][8] = int(code[place])^1
            place +=1
        j -=1
    pixels[len(pixels)-8][8] = 0 # ставим черный статичный модуль
    j = len(pixels)-8
    while j < len(pixels):
        if pixels[8][j] ==-1:
            pixels[8][j] = int(code[place])^1
            place +=1
        j +=1

    return pixels

"""
Функция отрисовки версии кода
"""
def draw_code_version(pixels,ver):
	# только для версий 7,8,9
    if ver < 6:
        return pixels
    vers = const.CODE_VERSIONS[ver-6] # т.к. только с 7ой версии
    # размер картинки
    size = const.ALIGNMENT_PATTERN_LOCATION[ver][len(const.ALIGNMENT_PATTERN_LOCATION[ver])-1] + 7
    i = size - 11
    j = 0
    place = 0
    for i in range(i,i+3):
        for j in range(0,6):
            pixels[i][j] = int(vers[place])^1 # - черный = 0 , белый = 1
            pixels[j][i] = int(vers[place])^1
            place += 1

    return pixels

"""
Функция отрисовки полос синхронизации
"""
def draw_timing_strip(pixels):
    # здесь полосы синхронизации (черно-бел черед)
    start = 8
    for i in range(start, len(pixels)-8):
        if i % 2 != 0:
            pixels[6][ i] = 1
            pixels[i][6] = 1
            continue
        pixels[6][i] = 0
        pixels[i][6] = 0
    return pixels

"""
Функция отрисовки выравнивающих узоров
"""
def draw_alignment_patterns(pixels,ver):

    # Есть одно важное условие: выравнивающие узоры не должны наслаиваться на поисковые узоры.
    # То есть, когда версия больше 6, в точках (первая, первая),
    # (первая, последняя) и (последняя, первая) выравнивающих узоров не должно быть

    if ver == 0:
        return
    coordinates  = []
    if ver < 6:
    	# берем координаты выравнивающих узоров
        temp = []
        temp.append(const.ALIGNMENT_PATTERN_LOCATION[ver][0])
        temp.append(const.ALIGNMENT_PATTERN_LOCATION[ver][0])
        # coordinates.append(temp)
        coordinates.append(temp)
        # вызываем функцию рисования выр. узора
        return draw_one_alignment(pixels,coordinates)

    # здесь статикой с 7ой версии фармируются вырав узоры
    patterns = const.ALIGNMENT_PATTERN_LOCATION[ver]
    temp = []
    temp2 = []
    temp3 = []
    temp4 = []
    temp.append(patterns[0])
    temp.append(patterns[1])
    coordinates.append(temp) # первый второй
    coordinates.append(temp[::-1]) # второй первый
    temp2.append(patterns[1])
    temp2.append(patterns[1])
    coordinates.append(temp2) # второй второй
    temp4.append(patterns[1])
    temp4.append(patterns[2])# вторйо третий
    coordinates.append(temp4)
    coordinates.append(temp4[::-1]) # третий второй
    temp3.append(patterns[2])
    temp3.append(patterns[2])
    coordinates.append(temp3)
    # вызываем функцию рисования выр. узора
    return draw_one_alignment(pixels,coordinates)

"""
Функция отрисовки одного выравнивающего узора
"""
def draw_one_alignment(pixels, coordinates):
    # рисуем каждый выравнивающий узор
    for k in coordinates:
        i = k[0]-2
        j = k[1]-2
        m = 0
        for i in range(i, k[0]+3):
            n = 0
            for j in range(j,k[1]+3):
                pixels[i][j] = const.ONE_ALIGNMENT[m][n]
                n+=1
            m +=1
            j = k[1] - 2
    return pixels

"""
Функция создающая пиксели поисковых узоров (3 шт.) 
"""
def draw_search_pattern(pixels):
    # 3 поисковых узора
    for i in range(len(const.SEARCH_ELEMENT)-1):
        for j in range(len(const.SEARCH_ELEMENT)-1):
            pixels[i][ j] = const.SEARCH_ELEMENT[i+1][j+1]  # левый верхний +-1 -это белая полоса
            pixels[i][ len(pixels) - 8 + j] = const.SEARCH_ELEMENT[i+1][j]  # левый нижний
            pixels[len(pixels) - 8 + i][ j] = const.SEARCH_ELEMENT[i][j+1]  # правый верхний
    return pixels

"""
Функция объединения блоков в один поток данных
"""
def makeDataStream(blocks, correct_blocks):
	stream = []
	# приведем исходные блоки к тому же формату, что и блоки коррекции
	for i in range(len(blocks)):
		list_bytes = [blocks[i][x:x+8] for x in range (0, len(blocks[i]), 8)]
		blocks[i] = list_bytes
	
	print("Исходные данне")
	print(blocks)
	print(len(blocks[0]))
	print(correct_blocks)
	print(len(correct_blocks[0]))

	#Добавляем в поток блоки данных
	isEnd = True
	while isEnd:
		for i in range(len(blocks)):
			if i == len(blocks)-1 and len(blocks[i])==0:
				isEnd = False
				break
			if len(blocks[i]) != 0:
				stream.append(blocks[i].pop(0))

	#Добавляем в поток блоки коррекции
	isEnd = True
	while isEnd:
		for i in range(len(correct_blocks)):
			if i == len(correct_blocks)-1 and len(correct_blocks[i])==0:
				isEnd = False
				break
			if len(correct_blocks[i]) != 0:
				stream.append(correct_blocks[i].pop(0))
		
	print("Поток данных")
	print(stream)
	print(len(stream))

	return stream


"""
Функция создающая байты коррекции
"""
def makeCorrectionBytes(blocks, ver):
	# определяем число байт коррекции
	number_of_bytes_corr = const.NUMBER_OF_CORRECTION_BYTES[ver]
	print("число байт коррекции: ", number_of_bytes_corr)
	# определяем генерирующий многочлен
	gener_polynom = const.GENERATING_POLYNOMS[ver]
	print("генерирующий многочлен: ")
	print(gener_polynom)


	# для каждого блока данных
	for i in range(len(blocks)):
		# делим блок на байты и переводим их в 10-ный формат
		list_bytes = [int(blocks[i][x:x+8],2) for x in range (0, len(blocks[i]), 8)]
		# запоминаем число бай
		len_data_bytes = len(list_bytes)
		# print(list_bytes)
		# Если число байт меньше числа байт коррекции, то в конце блока добавляем нули
		while len(list_bytes) < number_of_bytes_corr:
			list_bytes.append(0)
		# для каждого байта в текущем блоке
		for j in range(len_data_bytes):
			# берем первый элемент и удаляем его из блока добавляя в конец 0
			first_elem = list_bytes.pop(0)
			list_bytes.append(0)
			# Если элемент равен нулю пропускаем иттерацию
			if first_elem == 0:
				continue
			# находим значение в обратной таблице Галуа соответ. текущему элементу
			table_value = const.REV_GALOIS_FIELD[first_elem]
			# затем суммируем это значение по модулю 255 с коэф генер. мн-на
			for k in range(len(gener_polynom)):
				temp_mod_value = (table_value + gener_polynom[k]) % 255
				# ищем соответствие в таблице Галуа
				temp_mod_value = const.GALOIS_FIELD[temp_mod_value]
				# производим операцию xor 
				list_bytes[k] = list_bytes[k] ^ temp_mod_value
		# print(list_bytes)
		for j in range(len(list_bytes)):
			temp = bin(list_bytes[j])[2:].rjust(8,"0")
			list_bytes[j] = temp

		blocks[i] = list_bytes
	print("блоки для объединения: ")
	print(blocks)

	return blocks

"""
Функция разделения на блоки строки байтов в зависимости от версии
"""
def div_into_blocks(binStr, ver):
	blocks = []
	if const.NUMBER_OF_BLOCKS[ver] == 1:
		blocks.append(binStr)
		return blocks
	else:
		# число байт
		number_of_bytes = len(binStr)//8
		# число байт в одном блоке
		bytes_in_one_block = number_of_bytes// const.NUMBER_OF_BLOCKS[ver]
		# Число остаточных байт
		remaining_bytes = number_of_bytes % const.NUMBER_OF_BLOCKS[ver]
		print("отстаточные байты: ",remaining_bytes)
		
		# если остаточных байтов нет, заполняем блоки одинаковым числом битов
		if remaining_bytes == 0:
			blocks = [binStr[i:i+bytes_in_one_block*8] for i in range(0,len(binStr)-remaining_bytes*8,bytes_in_one_block*8)]
			# print("blocks")
			# print(blocks)
			return blocks
		# Если есть отстаточные байты тогда заполняем разным числом битов с конца распределя по одному биту в каждый блок
		else:
			i = 0
			position = 0
			lenght = 0
			while i < const.NUMBER_OF_BLOCKS[ver]:
				if i < remaining_bytes:
					blocks.append(binStr[position:position + bytes_in_one_block*8])
					position += bytes_in_one_block*8
				else:
					blocks.append(binStr[position:position + bytes_in_one_block*8+8])
					position += bytes_in_one_block*8 + 8
				i += 1
			# print("blocks")
			# print(blocks)
			return blocks


"""
функция дополнения кода нулями и чередующимися байтами 11101100 и 00010001
"""
def fillByBites(binStr):

	ver = 0
	if len(binStr)%8 != 0:
		while len(binStr)%8 != 0:
			binStr = binStr + "0"
			
	print(len(binStr))
	
	for i in range(len(const.VERSIES)-1):
		# если первая версия т.е. < 80
		if const.VERSIES[i] >= len(binStr):
			isFirst = True
			print(const.VERSIES[i])
			# Указываем версию кода
			ver = const.VERSIES.index(const.VERSIES[i])
			while len(binStr) < const.VERSIES[i]:

				if isFirst:
					binStr = binStr + "11101100"
					isFirst = False
				else:
					binStr = binStr + "00010001"
					isFirst = True
			break
		# остальные случаи
		if const.VERSIES[i] <= len(binStr) and const.VERSIES[i+1] >= len(binStr):
			isFirst = True
			print(const.VERSIES[i+1])
			# Указываем версию кода
			ver = const.VERSIES.index(const.VERSIES[i+1])
			while len(binStr) < const.VERSIES[i+1]:

				if isFirst:
					binStr = binStr + "11101100"
					isFirst = False
				else:
					binStr = binStr + "00010001"
					isFirst = True
			break
	# print(binStr)
	return binStr,ver		

"""
Функция выбора версии кодирования и добавления служебной информации
"""
def versionChoose(mode,binStr,number_of_symbols):

	if mode:
		information_and_bin = "0010"+ (bin(number_of_symbols)[2:]).rjust(9,"0") + binStr
		#Если объем данных с служеб. инф. больше, чем максимальное для
		# 9 версии с сжатием М(15%), то выходим
		
		if len(information_and_bin) > max(const.VERSIES):
			print("Слишком большой объем данных!")
			exit()
		return information_and_bin
	else:
		information_and_bin = "0001"+ (bin(number_of_symbols)[2:]).rjust(10,"0") + binStr
		#Аналогично для цифр. режима
		if len(information_and_bin) > max(const.VERSIES):
			print("Слишком большой объем данных!")
			exit()
		return information_and_bin

"""
Функция перевода Цифр данных в бинарный вид
"""
def NumbersToBinaries(data_to_bin):

	list_of_three_numbers = [bin(int(data_to_bin[i:i+3])) for i in range(0,len(data_to_bin),3)]
	
	list_of_str_binaries = []
	for i in range(len(list_of_three_numbers)):
		# Обработка последнего символа
		if i == len(list_of_three_numbers)-1:
			temp_str = list_of_three_numbers[i][2:]
			if len(temp_str) < 4:
				temp_str = temp_str.rjust(4, "0")
			elif (len(temp_str) > 4) and (len(temp_str) < 7):
				temp_str = temp_str.rjust(7, "0")
			elif (len(temp_str) > 7) and (len(temp_str) < 10):
				temp_str = temp_str.rjust(10, "0")
			print(temp_str)
			list_of_str_binaries.append(temp_str)
			break

		# Обработка всех символов
		temp_str = list_of_three_numbers[i][2:]
		while len(temp_str) < 10:
			temp_str = "0" + temp_str
			
		print(temp_str)
		list_of_str_binaries.append(temp_str)

	# print(list_of_str_binaries)
	# Возвращаем объединеные в один поток элементы
	return ''.join(list_of_str_binaries)
"""
Функция перевода БуквЦифр данных в бинарный вид
"""
def AlphanumToBinaries(data_to_bin):
	

	list_of_two_symbols = [data_to_bin[i:i+2] for i in range(0,len(data_to_bin),2)]
	
	list_of_str_binaries = []
	
	for i in range(len(list_of_two_symbols)):
		
		if len(list_of_two_symbols[i]) == 2:
			tmp_value1 = const.alphanumericList.index(list_of_two_symbols[i][0])
			tmp_value2 = const.alphanumericList.index(list_of_two_symbols[i][1])
			tmp_binary = bin(int(tmp_value1)*45+int(tmp_value2))[2:]
			tmp_binary = tmp_binary.rjust(11,"0")
			print(tmp_binary)
			list_of_str_binaries.append(tmp_binary)
		else:
			tmp_value1 = const.alphanumericList.index(list_of_two_symbols[i])
			tmp_binary = bin(int(tmp_value1))[2:]
			tmp_binary = tmp_binary.rjust(6,"0")
			print(tmp_binary)
			list_of_str_binaries.append(tmp_binary)
	
	# print(list_of_str_binaries)
	# Возвращаем объединеные в один поток элементы
	return ''.join(list_of_str_binaries)

"""
Функция, которая определяет вид данных
"""
def modeChoose(inputData):

	print(inputData)
	try:
		isAlphanumericMode = False
		for i in inputData:
			if const.alphanumericList.index(i) > 9:
				isAlphanumericMode = True
				break
	except ValueError:
			print("Встретился не поддерживаемый символ!")
			exit()


	return isAlphanumericMode


	pass
"""
Функция кодирования
"""
def encode(type_of_data, inputString):

	binaries = ""
	version = 0
	# list_of_blocks = []
	if type_of_data:
		binaries = AlphanumToBinaries(inputString)
		binaries = versionChoose(type_of_data,binaries,len(inputString))
	else:
		binaries = NumbersToBinaries(inputString)
		binaries = versionChoose(type_of_data,binaries,len(inputString))
	
	binaries, version = fillByBites(binaries)

	list_of_blocks = div_into_blocks(binaries, version)
	print("список блоков")
	print(list_of_blocks)
	blocks_copy = copy.deepcopy(list_of_blocks)
	prepared_blocks = makeCorrectionBytes(blocks_copy,version)

	merged_blocks = makeDataStream(list_of_blocks,prepared_blocks)
	# print(binaries)
	print("версия:", version+1)

	border_size = 8 #указываем размер границы qr


	if version + 1 == 1:
		#если первая версия, создаем картинку 29х29 (21+8 - с учетом границ по 4 пикселя с каждой стороны)
		# которая имеет два цвета - ч\б и заполняем ее белым 
		qr = Image.new("1",(21+border_size,21+border_size), "white")
		# создаем массив пикселей, который будем заполнять
		pixels = np.full((21,21),-1)
	else:
		# для остальных версий
		# определяем размеры изображения
		qr_size = const.ALIGNMENT_PATTERN_LOCATION[version][len(const.ALIGNMENT_PATTERN_LOCATION[version])-1] + 7
		qr = Image.new("1",(qr_size+border_size,qr_size+border_size), "white")
		pixels = np.full((qr_size,qr_size), -1)

	# переводим созданную картинку в пиксели
	img_pixels = qr.load()

	# поисковые узоры
	draw_search_pattern(pixels)
	# выравнивающие узоры
	draw_alignment_patterns(pixels,version)
	# полосы синхронизации
	draw_timing_strip(pixels)
	# версия кода
	draw_code_version(pixels,version)
	# код маски и уровня коррекции
	draw_code_mask_and_correct_level(pixels)
	# блоки данных
	draw_data(pixels,merged_blocks)


	# заполняем картинку готовыми модулями
	for i in range(qr.size[0]-8):
		for j in range(qr.size[0]-8):
			if(pixels[i][j] != -1):
				img_pixels[j+4, i+4] = int(pixels[i][j])

	plt.imshow(np.asarray(qr), cmap="gray")
	# убираем оси
	plt.axis("off")
	plt.show()
"""
Главная функция
"""
def main():

	string_from_cli = input("Введите, что желаете закодировать? \n").upper()
	# Выбираем режим работы: True - БуквЦифр, False - Цифр
	mode = modeChoose(string_from_cli)
	if mode:
		print("Режим: Буквенно-Цифровой \n")
	else:
		print("Режим: Цифровой \n")
	encode(mode, string_from_cli)


if __name__ == '__main__':
	main()