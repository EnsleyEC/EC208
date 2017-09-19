op_soma = 1
op_sub = 2

def readArquivo(pc):
	'''lendo a instrucao do pc'''
	novo_fila = open('ensley.txt','r')
	variavel = novo_fila.readlines()
	tamanho = len(variavel)
	instrucao = variavel[pc]
	novo_fila.close()

	return instrucao

def obter_instrucao(instrucao):
	'''Tipo de instrucao'''
	cont = 5
	soma = 0
	for i in range(26,32):
		if(instrucao[i] == '1'):
			soma = soma + pow(2,cont)
		cont = cont - 1

	return soma

def obter_dados(instrucao):
	'''Pegando o primeiro e o segundo valor da memoria'''
	cont = 4
	rs = rt = rd = 0

	for i in range(6,11):
		if(instrucao[i] == '1'):
			rs = rs + pow(2,cont)
		cont = cont - 1
	cont = 4

	for i in range(11,16):
		if(instrucao[i] == '1'):
			rt = rt + pow(2,cont)
		cont = cont - 1

	cont = 4
	for i in range(16,21):
		if(instrucao[i] == '1'):
			rd = rd + pow(2,cont)
		cont = cont - 1


	return rs,rt,rd

def write_arquivo(nome_arquivo):
	'''escrevendo as instrucoes na memoria de programa'''
	novo_fila = open(nome_arquivo,'w')
	novo_fila.write('00000000001000100001101100000001\n')
	novo_fila.write('00000000001000100010001100000010\n')
	novo_fila.close()

def executar(rs,rt,funct):
	''' executando as operacoes'''

	resultado = 0

	if funct is op_soma:
		resultado = rs + rt
	elif funct is op_sub:
		resultado = rs - rt
	else:
		print('Nao fez nada!')


	print('Resultado = %d\n',resultado)

	return resultado

def buscar_memoria(rs,rt):

	''' pegando o valor em binario contigo em rt e rs, e passando pra decimal'''

	m_dados = open('dados.txt','r')
	dados = m_dados.readlines()

	_rs = dados[rs-1]
	_rt = dados[rt-1]

	rs_decimal = 0
	rt_decimal = 0

	cont = 31

	for i in range(1,len(_rs)):
		if(_rs[i] == '1'):
			rs_decimal = rs_decimal + pow(2,cont)
		cont = cont - 1

	cont = 31

	for i in range(1,len(_rt)):
		if(_rt[i] == '1'):
			rt_decimal = rt_decimal + pow(2,cont)
		cont = cont - 1

	m_dados.close()

	if _rs[0] is '1':
		rs_decimal = rs_decimal*(-1)
	if _rt[0] is '1':
		rt_decimal = rt_decimal*(-1)	

	return rs_decimal,rt_decimal

def converterd_b(n):
    '''funcao para converter decimal em binario'''

    binario = ""
    while(True):
        binario = binario + str(n%2)
        n = n//2
        if n == 0:
            break
    binario = binario[::-1]
    binario = int(binario)
    return binario

def salvar_dados(resultado,rd,sinal):
	'''funcao que salva os dados na memoria de dados'''

	text_arquivo = open('dados.txt','r')
	texto = text_arquivo.readlines()
	escrever = open('dados.txt','w')

	for linha in texto:

		if linha is texto[rd-1]:
			resp = converterd_b(resultado)

			tam_resp = len(str(resp))

			if sinal is 0:
				escrever.write(str(sinal))
			else:
				escrever.write(str(sinal))

			for i in range(2,34-tam_resp):
					escrever.write('0')

			escrever.write(str(resp)+'\n')
		else:
			escrever.write(linha)

	text_arquivo.close()
	escrever.close()

def tamanho_pc(nome_arquivo):

	with open(nome_arquivo,'r') as line:
		tamanho = len(line.readlines())
		line.close()
		return tamanho

def main():
	'''funcao principal'''

	nome_arquivo = 'ensley.txt'

	write_arquivo(nome_arquivo)

	pc_max = tamanho_pc(nome_arquivo)

	pc = 0;

	while pc != pc_max:
		instru = readArquivo(pc)
		instrucao = obter_instrucao(instru)
		rs,rt,rd = obter_dados(instru)
		_rs,_rt = buscar_memoria(rs,rt)
		resultado = executar(_rs,_rt,instrucao)
		# 1 - negativo, 0 - positivo
		if resultado >= 0:
			salvar_dados(resultado,rd,0)
		else:
			salvar_dados(abs(resultado),rd,1)
		pc = pc + 1

if __name__ == '__main__':
	main()
