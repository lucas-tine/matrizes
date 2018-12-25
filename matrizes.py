#coding: utf8
from decimal import *
from fractions import Fraction
from random import randint

'''<<< BIBLIOTECA DA CLASSE MATRIZ >>>'''

#DEFINE 
IDENTIDADE = 'I'
RANDOM = 'R'
RANDOM_HARD = 'RH'

def dec(numero):

	return Decimal(  str(numero) )

class matrix(object):
	
	class MatrixError(Exception): # tratar erros referentes a manipulação inapropriada de objetos matriz
	
		def __init__(self,tipo,other = None ):
			self.__typ = tipo
			self.__othertype = str(type(other))[7:-1]
		def __str__(self):
			if self.__typ == 'lc':
				returned = "\033[91mMatriz não ajustada com os parametros linha e coluna"
			
			if self.__typ == 'add':
				returned = "\033[91mImpossível somar matrizes de tamanhos diferentes"
			
			if self.__typ == 'inv':
				returned = "\033[91mImpossível inverter matrizes não-quadradas"

			if self.__typ == 'notlist':
			 return \
			 "\033[91mSegundo argumento do modificador deve ser do tipo \033[33mlist\033[91m,não %s"%(self.__othertype)

			if self.__typ == 'mul':
				returned = "\033[91mImpossível multiplicar matrizes de ordens incompatíveis \033[33m(M1 != N2)"	

			if self.__typ == 'typemul':
				returned = "\033[91mClasse incompatível para multiplicação com matrizes: %s " %(self.__othertype)

			if self.__typ == 'sqr':
				returned = "\033[91mOperação impossível para matrizes não quadradas! "
			
			returned += '\033[m'

			return returned

	def __init__(self, linhas = 1,colunas = 1,tipo = 0): # inicializar matriz MxN segundo o modelo: >>> obj_matriz = matriz(M,N)  
		self.lines = linhas
		self.columns = colunas
		self.list = [] # representação em forma de lista da matriz 
		for i in range (colunas):
			self.list.append([0]*self.lines) 
		self.valid = True
		self.__tipo = tipo

		if self.__tipo in ('identidade','Identidade','IDENTIDADE','i','I') :
				
			for i in range(1, min(self.lines,self.columns)+1 ):
				self.setterm(i,i,1)

		if self.__tipo in ('random','RANDOM','Random','R','r'):
			for i in range( len(self.list) ):
				for j in range ( len(self.list[i] ) ):

					self.list[i][j] = randint (-2,2) 
	
		if self.__tipo in ('random hard','RANDOM HARD','Random Hard','RH','rh'):
			for i in range( len(self.list) ):
				for j in range ( len(self.list[i] ) ):

					self.list[i][j] = randint (-8,9) 




	def __str__(self): # gerar um modelo do objeto matriz para ser exibido ao usuário ou tratado

			self.checkDim()
			string = ""
			for i in range (self.lines):
				for j in range (self.columns):	
					num =  self.list[j][i]  
					if num % 1 != 0 and len( str( Fraction(num).limit_denominator() ) ) < 7:

						string += "{:^7}".format( str( Fraction(num).limit_denominator()) )	
		
					elif num % 1 < 0.0001:

							string += "{:^7}".format( int(self.list[j][i]) )

					else :

						string += "{:^7.3f}".format( self.list[j][i] )

				string += '\n'
				continue
			return string

	def __add__(self,other): # somar de forma simples matrizes de mesma dimensão
	
		resultado = matriz(other.linhas,self.columns)
# verificação de dimensões compativeis 		
		self.checkDim()
		other.checkDim()

		if not self.lines == other.linhas:
			raise resultado.MatrixError('add')
		if not self.columns == other.colunas:
			raise resultado.MatrixError('add')
# operação propriamente dita
		novamatriz = []
		
		for i in range (other.colunas):
			novamatriz.append([])
		for i in range (self.columns):
			for j in range(other.linhas):

				novamatriz[i].append(0)


		for i in range (self.lines):
			for j in range (self.columns):
			 novamatriz[j][i] = float( dec( self.list[j][i] ) + dec( other.lista[j][i] ) )
		resultado.lista = novamatriz

		return resultado
	
	def __mul__(self,other): # Multiplicar matrizes matematicamente

		if type(other) == matriz:

			resultado = matriz( self.lines , other.colunas )
	
			self.checkDim()
			other.checkDim()

			if not( self.columns == other.linhas ):
				raise resultado.MatrixError('mul')
					
			for i in range (self.lines): 

				linha_atual = self.getline(i+1) # *
				linha_resultante2 = matriz(1, other.colunas)
				for j in range( self.columns ):
			
					linha_resultante1 = matriz(1, other.colunas )
					linha_resultante1.setline(1, other.getline(j+1) )
					linha_resultante1 *= linha_atual[j]
					linha_resultante2 += linha_resultante1
					
				resultado.setline( i+1 , linha_resultante2.getline(1)  )

			return resultado

# * para cada linha M em self: para cada termo N na linha M, multiplica-se o termo N pela linha correspondente a N em other, ao fim
# soma-se as linhas multiplicadas. Isto corresponde a linha M da matriz resultante				

		elif type(other) in (float,int,Decimal):
			
			resultado = self.copy()
			
			for i in range (self.columns):
				for j in range(self.lines):

					resultado.lista[i][j] = float ( dec(other) * dec(resultado.lista[i][j])  )

			return resultado

		raise self.MatrixError('typemul',other)

	def __rmul__(self,rother):

		if type(rother) in (int,float,Decimal):

			return (self * rother)
		raise self.MatrixError('typemul', other = rother)	



	def __truediv__(self,other):

		if not type(other) in (int,float,Decimal):
			raise self.MatrixError('typemul', other)

		return self * ( dec(1)/dec(other) ) 		

        
        
	def fill(self, *args):

            if len(args) != (self.lines * self.columns):
                raise self.MatrixError('lc')
    
            n = 0
            for i in range (1,self.lines+1):
                for j in range (1,self.columns+1):
                    self.setterm(i, j, args[n])
                    n += 1
	
	def __abs__(self):

		self.checkDim()
		if self.columns == 1: # módulo euclidiano

			soma_total = 0
			for termo in self.getcolumn(1):
			
				soma_total += ( dec(termo) ** dec(2) )
				
			return float(dec (soma_total) ** dec(1/2))				

		if not self.lines == self.columns: # "módulo" determinante
			raise self.MatrixError('sqr')
			
		lista_linhas = self.transpose().lista
		matrizes_linha = []
		det = 1

		for linha in lista_linhas:
			
			nova_matriz_linha = matriz(self.columns).transpose()
			nova_matriz_linha.setline(1,linha)
			matrizes_linha.append( nova_matriz_linha  )
			if linha == [0] * self.columns:
				return 0	
		

		# início das combinações lineares

		estagio = 0 # contagem de linha
		numl = len(matrizes_linha)		

		while (estagio < numl ):

			for i in range (estagio + 1, numl ): # contando todas 

				if matrizes_linha[i].getterm(1, estagio + 1 ) == 0:
					continue
				else:
					if matrizes_linha[estagio].getterm(1, estagio+1) == 0:
						for i in range(estagio+1,numl):

							if matrizes_linha[i].getterm(1, estagio+1) != 0:
								aux = matrizes_linha[estagio].copy()
								matrizes_linha[estagio] = matrizes_linha[i].copy()
								matrizes_linha[i] = aux.copy()
								det *= -1
								break

					termo_original = matrizes_linha[estagio].getterm(1,estagio+1)		
					k = dec(-1) * dec (matrizes_linha[i].getterm(1,estagio + 1 ) )/ dec( termo_original)
					matrizes_linha[i] += (k* matrizes_linha[estagio] )  
					
					#for i in range (numl): # DEBUGGING, SE DESMARCADO, PRINTA O PROCESSO DE LINHA-EQUIVALENCIA

					#	print (matrizes_linha[i]) 
					#print('') # ATÉ AQUI		
	
					del termo_original
			estagio += 1

		# se tudo deu certo, temos linhas de uma matriz U em matrizes.linha

		for i in range( numl ):
			det *= matrizes_linha[i].getterm(1, i+1)		

		
		if abs(det) < 0.000000000001:
			return 0	

		return det

	def det(self):

		if self.lines == self.columns:
			return abs(self)	
		else:
			raise self.MatrixError('sqr')

	def transpose(self):
		trans = matriz(self.columns , self.lines)

		i = 1
		for coluna in self.list:
			trans.setline(i , coluna)
			i += 1

		return trans

	def inverse(self) : 
		
		if self.det() == 0:
			return None

		self.checkDim()

		if not self.lines == self.columns: # terá inverse apenas se for quadrada
			raise self.MatrixError('sqr')			

		inverse = matriz( self.lines, self.columns, IDENTIDADE )
	
		lista_linhas = self.transpose().lista
		lista_linhas_inv = inverse.transpose().lista

		matrizes_linha = []
		matrizes_linha_inv = []

		for linha in lista_linhas:
			
			nova_matriz_linha = matriz(self.columns).transpose()
			nova_matriz_linha.setline(1,linha)
			matrizes_linha.append( nova_matriz_linha  )
			if linha == [0] * self.columns:
				return 0	

		for linha in lista_linhas_inv:

			nova_matriz_linha = matriz( inverse.colunas ).transpose()
			nova_matriz_linha.setline (1,linha)
			matrizes_linha_inv.append( nova_matriz_linha )

		for sentido in range (2):  # sentido == 0 indica que estamos zerando a parte inferior da matriz
				 	   # sentido == 1, análogamente, refere-se a parte superior

			# início das combinações lineares
	
			numl = len(matrizes_linha)		
			
			if not sentido:	# sentido == 0	
				estagio = 0
			else:		# sentido == 1
				estagio = numl - 1
			
			while (estagio < numl ):

				if sentido:
					inicio = estagio - 1
					limite = 0
					passo = -1
				else:
					inicio = estagio + 1
					limite = numl
					passo = 1

				for i in range ( estagio + 1, numl): # contando todas 
							
					if matrizes_linha[i].getterm(1, estagio + 1 ) == 0:
						continue
					else:
						
						if matrizes_linha[estagio].getterm(1, estagio+1) == 0:

							for i in range(inicio,limite,passo):

								if matrizes_linha[i].getterm(1, estagio+1) != 0:

									aux = matrizes_linha[estagio].copy()
									aux_inv = matrizes_linha_inv[estagio].copy()

									matrizes_linha[estagio] = matrizes_linha[i].copy()
									matrizes_linha_inv[estagio] = matrizes_linha_inv[i].copy()

									matrizes_linha[i] = aux.copy()
									matrizes_linha_inv[i] = aux_inv.copy()

									break
						
						if estagio == i - numl :
							continue 
					
						termo_original = matrizes_linha[estagio].getterm(1,estagio+1)
			
						k = dec(-1) * dec(matrizes_linha[i].getterm(1,estagio + 1 )) / dec(termo_original)

						matrizes_linha[i] += (k * matrizes_linha[estagio] )  
						matrizes_linha_inv[i] += (k* matrizes_linha_inv[estagio])
						
						#for i in range (numl): # DEBUGGING, SE DESMARCADO, PRINTA AS OPERAÇÕES NA ORIGINAL
	
						#	print (matrizes_linha[i]) 
						#print('\n')		

						#for i in range (numl): # PRINTA AS OPERAÇÕES NA INVERSA
	
						#	print (matrizes_linha_inv[i]) 
						#print('\n') # ATÉ AQUI	

						#del termo_original

				if sentido:
					estagio -= 1
				else:
					estagio += 1
					
				if estagio == -numl:
					break

		# formar a inverse concatenando suas linhas

		inverse = matriz(self.lines,self.columns)
		for i in range( len(matrizes_linha_inv) ):
		
		# finalmente, dividir as linhas da inverse pelos termos restantes na diagonal de self
		
				matrizes_linha_inv[i] *= dec( 1/matrizes_linha[i].getterm(1,i+1))

		for i in range ( len(matrizes_linha_inv) ):
			inverse.setline( i+1 , matrizes_linha_inv[i].getline(1)  )
	
		return inverse

	def copy(self): # Copiar uma matriz para formar um objeto identico, porém desvencilhado do original

		nova_matriz = matriz(self.lines,self.columns)
		i = 0
		for coluna in self.list:
			nova_matriz.lista[i] = coluna.copy()
			i += 1
		return nova_matriz

	def checkDim(self): # Checar se a atual dimensão de self.list condiz com a especificada em __init__

		if (len(self.list) != self.columns):			
			raise self.MatrixError('lc')
		for coluna in self.list:
			if len(coluna) != self.lines: 
				raise self.MatrixError('lc')
		return True

	def setline(self,indice,nova_linha): # Substituir uma linha da matriz pela fornecida, PULANDO TERMOS 'x'

		if not type(nova_linha) in (list,tuple) :
			raise matriz().MatrixError(3)
		i = 0
		indice -= 1
		for coluna in self.list:
			if nova_linha[i] != 'x':
				coluna[indice] = nova_linha[i]
			i += 1
			
	def setcolumn(self,indice,nova_coluna): # Substituir uma linha da matriz pela fornecida, PULANDO TERMOS 'x'

		if not type(nova_coluna) in (list,tuple) :
			raise matriz().MatrixError(3)
		indice -= 1
		coluna_antiga = self.list[indice]
		for i in range ( len(nova_coluna) ):
			if nova_coluna[i] == 'x':
				nova_coluna[i] = coluna_antiga[i]
			
		self.list[indice] = nova_coluna

	def getline(self,indice): # Retornar uma lista com o conteúdo da linha especificada em índice
		indice -= 1
		linha_solicitada = [0] * self.columns
		i = 0
		for coluna in self.list:
			linha_solicitada[i] = coluna[indice]
			i += 1
		return linha_solicitada

	def getcolumn(self,indice): # Retornar uma lista com o conteúdo da coluna especificada em índice 
		indice -= 1
		return self.list[indice]

	def getterm(self,M,N): # retornar o termo indicado

		return self.getcolumn(N)[M-1]

	def setterm(self,M,N,novo_termo): # mudar o valor de apenas um termo isolado

		coluna_n = self.getcolumn(N).copy()
		coluna_n [M-1] = novo_termo
		self.setcolumn(N, coluna_n )

	def gaussianEliminiation(self) : 

		def repareDim(self):

			if (len(self.list) > self.columns):
				for i in range ( self.columns,len(self.list) ):
					self.list.pop(-1)
			elif (len(self.list) < self.columns):
				for i in range ( len(self.list),self.columns ):
					self.list.append([0]*self.lines)
			for coluna in self.list:
				if len(coluna) > self.lines:
					while len(coluna) > self.lines: 
						coluna.pop(-1)
				if len(coluna) < self.lines: 
					while len(coluna) < self.lines:
						coluna.append(0)
		m = self.lines
		n = self.columns	
	
		maior = max(self.lines,self.columns)
		self.lines , self.columns = maior,maior
		repareDim(self)	
	
		print (self)

		lista_linhas = self.transpose().lista
		matrizes_linha = []

		for linha in lista_linhas:
			
			nova_matriz_linha = matriz(self.columns).transpose()
			nova_matriz_linha.setline(1,linha)
			matrizes_linha.append( nova_matriz_linha  )

		for sentido in range (2):  # sentido == 0 indica que estamos zerando a parte inferior da matriz
				 	   # sentido == 1, análogamente, refere-se a parte superior

			# início das combinações lineares
	
			numl = len(matrizes_linha)		
			
			if not sentido:	# sentido == 0	
				estagio = 0
			else:		# sentido == 1
				estagio = numl - 1
			
			while (estagio < numl ):

				if sentido:
					inicio = estagio - 1
					limite = 0
					passo = -1
				else:
					inicio = estagio + 1
					limite = numl
					passo = 1

				for i in range ( estagio + 1, numl): # contando todas 
							
					if matrizes_linha[i].getterm(1, estagio + 1 ) == 0:
						continue
					else:
						
						if matrizes_linha[estagio].getterm(1, estagio+1) == 0:

							for i in range(inicio,limite,passo):

								if matrizes_linha[i].getterm(1, estagio+1) != 0:

									aux = matrizes_linha[estagio].copy()

									matrizes_linha[estagio] = matrizes_linha[i].copy()

									matrizes_linha[i] = aux.copy()

									break
						
						if estagio == i - numl :
							continue 
					
						termo_original = matrizes_linha[estagio].getterm(1,estagio+1)
						if termo_original == 0:
							continue	
						k = dec(-1) * dec(matrizes_linha[i].getterm(1,estagio + 1 )) / dec(termo_original)

						matrizes_linha[i] += (k * matrizes_linha[estagio] )  
						
						for i in range (numl): # DEBUGGING, SE DESMARCADO, PRINTA AS OPERAÇÕES NA ORIGINAL
	
							print (matrizes_linha[i]) 
						print('\n')		

				if sentido:
					estagio -= 1
				else:
					estagio += 1
					
				if estagio == -numl:
					break
		self = matriz( maior, maior)

		for i in range ( len(matrizes_linha) ):
			self.setline( i+1 , matrizes_linha[i].getline(1)  )
	

		self.lines = m
		self.columns = n
		repareDim(self)
		return self
