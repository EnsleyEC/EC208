# encoding: utf-8

''' valores padrao para soma e subtracao '''
op_soma = 1
op_sub = 2

def inicializa():
	nome_arquivo = 'ensley.txt'
	write_arquivo(nome_arquivo)
	tag = [' ',' ',' ',' ',' ',' ',' ',' ']
	validade = [0,0,0,0,0,0,0,0]
	pc = 0

	return nome_arquivo, tag, validade, pc

def binario_para_decimal(valor_binario, tamanho_valor):

	valor_decimal = 0
	cont = tamanho_valor - 1
	inicio = 0

	if tamanho_valor > 30:
		inicio = 1
		cont = cont - 2

	# range(0,5) - 0 ate 4
	for i in range(inicio,tamanho_valor):

		if valor_binario[i] == '1' or valor_binario[i] == 1:
			valor_decimal = valor_decimal + pow(2,cont)


		cont = cont - 1

	return valor_decimal

def decimal_para_binario(n):
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

def write_cache(novo_dado,posicao_para_atualizar_dado):
	'''Se deu miss, escrevo o novo dado na cache'''
	dados = open('cache.txt','r')
	dados_cache = dados.readlines()
	escreve = open('cache.txt','w')
	for linha in dados_cache:
		if linha is dados_cache[posicao_para_atualizar_dado]:
			escreve.write(novo_dado)
		elif linha != '\n':
			escreve.write(linha)

	dados.close()
	escreve.close()

def cache(registro,tag,validade):

	m_cache = open('cache.txt','r')
	dados = m_cache.readlines()
	peguei_valor_da_cache = False
	valor_da_cache = 0
	registro_tag = registro[3]+registro[4]
	'''
	Exemplo:
	Registro = 111-00

	111 = posição da cache de 0 a 8
	00 = TAG
	'''

	# pegando a posição da cache
	posicao_cache = binario_para_decimal(registro,3)

	'''
	HIT, se:
	* validade[posicao_cache] == 1
	* tag[posicao_cache] == tag do registro

	se nao:
	* miss

	se for miss:
	* validade[posicao_cache] = 1
	* tag[posicao_cache] = tag do registro
	* escrever o dado na memoria cache
	'''
	print('')
	'''
	print('Pos cache = ',posicao_cache)
	print('Registro tag = ',registro_tag)
	print('Tag = ',tag[posicao_cache])
	'''
	if validade[posicao_cache] == 1:

		if registro_tag == tag[posicao_cache]:
			peguei_valor_da_cache = True
			valor_da_cache = dados[posicao_cache]
			print("Hit")
		else:
			tag[posicao_cache] = registro_tag
			peguei_valor_da_cache = False
			print("Miss")
	else:
		validade[posicao_cache] = 1
		tag[posicao_cache] = registro_tag
		peguei_valor_da_cache = False
		print("Miss")

	print('TAG = ',tag)
	print('Validade = ',validade)

	return tag,validade,valor_da_cache,peguei_valor_da_cache

def registros(instrucao):
	'''Pegando o primeiro e o segundo valor da memoria'''

	rs = [' ',' ',' ',' ',' ']
	rt = [' ',' ',' ',' ',' ']
	rd = [' ',' ',' ',' ',' ']
	j = 0

	for i in range(6,11):
		rs[j] = str(instrucao[i])
		j = j + 1

	j = 0

	for i in range(11,16):
		rt[j] = str(instrucao[i])
		j = j + 1

	j = 0

	for i in range(16,21):
		rd[j] = str(instrucao[i])
		j = j + 1

	return rs,rt,rd

def write_arquivo(nome_arquivo):
	'''escrevendo as instrucoes na memoria de programa'''
	novo_fila = open(nome_arquivo,'w')
	novo_fila.write('00000000101000100001101100000001\n')
	novo_fila.write('00000000010000100010001100000010\n')
	novo_fila.close()

def executar(rs,rt,funct):
	''' executando as operacoes'''

	resultado = 0

	if funct is op_soma:
		resultado = rs + rt
		print('A = ',rs)
		print('B = ',rt)
		print('SOMA -> A + B = ',resultado)
	elif funct is op_sub:
		resultado = rs - rt
		print('A = ',rs)
		print('B = ',rt)
		print('SUB -> A - B = ',resultado)
	else:
		print('Nao fez nada!')

	return resultado

def load(rs,rt,tag,validade):

	'''
	A = true ----- RS existe na cache
	B = true ----- RT existe na cache
	'''
	tag, validade , rs_cache, a = cache(rs,tag,validade)
	tag, validade , rt_cache, b = cache(rt,tag,validade)

	m_dados = open('dados.txt','r')
	dados_memoria_principal = m_dados.readlines()

	if a == True and b == True:

		rs_decimal = binario_para_decimal(rs_cache,len(rs_cache))
		rt_decimal = binario_para_decimal(rt_cache,len(rt_cache))

		if rs_cache[0] is '1':
			rs_decimal = rs_decimal*(-1)
		if rt_cache[0] is '1':
			rt_decimal = rt_decimal*(-1)

		return rs_decimal,rt_decimal,tag,validade

	elif a == True:

		rs_decimal = binario_para_decimal(rs_cache,len(rs_cache))

		rt_pos_memoria_principal = binario_para_decimal(rt,len(rt))
		rt_binario = dados_memoria_principal[rt_pos_memoria_principal]
		rt_decimal = binario_para_decimal(rt_binario,len(rt_binario))

		# atualizando os dados na m_cache
		posicao_cache = binario_para_decimal(rt,len(rt)-2)
		write_cache(rt_binario,posicao_cache)

		m_dados.close()

		if rs_cache[0] is '1':
			rs_decimal = rs_decimal*(-1)
		if rt_binario[0] is '1':
			rt_decimal = rt_decimal*(-1)

		return rs_decimal,rt_decimal,tag,validade

	elif b == True:

		rt_decimal = binario_para_decimal(rt_cache,len(rt_cache))
		rs_pos_memoria_principal = binario_para_decimal(rs,len(rs))
		rs_binario = dados_memoria_principal[rs_pos_memoria_principal]
		rs_decimal = binario_para_decimal(rs_binario,len(rs_binario))

		# atualizando os dados na m_cache
		posicao_cache = binario_para_decimal(rs,len(rs)-2)
		write_cache(rs_binario,posicao_cache)

		m_dados.close()

		if rs_binario[0] is '1':
			rs_decimal = rs_decimal*(-1)
		if rt_cache[0] is '1':
			rt_decimal = rt_decimal*(-1)

		return rs_decimal,rt_decimal,tag,validade

	else:

		rt_pos_memoria_principal = binario_para_decimal(rt,len(rt)) -1
		rt_binario = dados_memoria_principal[rt_pos_memoria_principal]
		rt_decimal = binario_para_decimal(rt_binario,len(rt_binario))

		rs_pos_memoria_principal = binario_para_decimal(rs,len(rs)) -1
		rs_binario = dados_memoria_principal[rs_pos_memoria_principal]
		rs_decimal = binario_para_decimal(rs_binario,len(rs_binario))

		# atualizando os dados na m_cache
		posicao_cache = binario_para_decimal(rt,len(rt)-2)
		write_cache(rt_binario,posicao_cache)

		posicao_cache = binario_para_decimal(rs,len(rs)-2)
		write_cache(rs_binario,posicao_cache)

		m_dados.close()

		if rs_binario[0] is '1':
			rs_decimal = rs_decimal*(-1)
		if rt_binario[0] is '1':
			rt_decimal = rt_decimal*(-1)

		return rs_decimal,rt_decimal,tag,validade

def store(resultado,rd,sinal):
	'''funcao que salva os dados na memoria de dados'''
	txt = open('dados.txt','r')
	texto = txt.readlines()
	txt.close()
	escrever = open('dados.txt','w')
	rd = binario_para_decimal(rd,len(rd))

	for linha in texto:

		'''converter rd '''
		if linha is texto[rd]:
			resp = decimal_para_binario(resultado)

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

	escrever.close()

def tamanho_pc(nome_arquivo):
	''' Função que retorna o numero de instrucoes na memoria principal '''
	with open(nome_arquivo,'r') as line:
		tamanho = len(line.readlines())
		line.close()
		return tamanho

def main():
	'''funcao principal'''

	nome_arquivo, tag , validade, pc = inicializa()
	pc_max = tamanho_pc(nome_arquivo)

	while pc != pc_max:

		# instru é a instrucao completa da memoria RAM de 32 bits
		instru = readArquivo(pc)
		# da instrucao de 32 bits, pegando qual operação será realizada(add,sub...)
		instrucao = obter_instrucao(instru)
		'''
		Exemplo: C = A + B
		RS = registro do A
		RT = registro do B
		RD = registro do C
		'''
		rs,rt,rd = registros(instru)
		# buscando os valores de contidos nos registradores RS e RT
		_rs,_rt,tag,validade = load(rs,rt,tag,validade)
		# com os valores de A e B, executo a instrução e retorno a resposta
		resultado = executar(_rs,_rt,instrucao)
		# 1 - negativo, 0 - positivo
		if resultado >= 0:
			store(resultado,rd,0)
		else:
			store(abs(resultado),rd,1)
		pc = pc + 1

if __name__ == '__main__':
	main()
