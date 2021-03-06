from math import log2

def hartli_formula(N):
	return log2(N)

def shennon_formula(N, p):
	i = 0
	H = 0 
	while i < N:
		H += p[i]*log2(p[i])
		i += 1
	return -H

def redundancy(N, p):
	H_max = hartli_formula(N)
	H = shennon_formula(N,p)
	return (H_max-H)*100/H_max

# first task:
# Какое количество состояний может принимать 
# источник информации, если все состояния равновероятны,
# а энтропия источника составляет 6 бит?
print("вариант 6.")
print("Задание 1.")
print("Используем формулу Хартли (H = log2(N))")
H = int(input("H = "))
N = 2**H
print("Количество состояний N = " + str(N))
print()
# Чему равна энтропия и избыточность алфавита из 8 букв,
# если известно, что половина из них встречается с 
# вероятностью 0,15, а остальные буквы также имеют 
# равную между собой вероятность?
print("Задание 2.")
N1 = 8
p1 = [0.15, 0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1]
print("Средняя энтропия на символ = " + str(shennon_formula(N1, p1)))
print("Избыточность = " + str(redundancy(N1, p1)))
#Энтропия некоторого алфавита равна  2,64  бит/симв., 
# а избыточность составляет  12  %.  Передаваемое
# сообщение несет  66  бит информации. Какой минимальный
# объем информации нужен для передачи этого сообщения
# в равномерном двоичном коде?
print("Задание 3.")
I = float(input("Кол-во информации = "))
H_avg = float(input("Энтропия алфавита = "))
D = float(input("Избыточность = ")) 
r = float(input("Разрядность кодового алфавита = "))
D = D/100
Q = - I * r / (D - 1)
print("минимальный объем информации Q = " + str(Q))
