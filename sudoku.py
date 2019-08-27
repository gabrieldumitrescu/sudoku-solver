import logging

class Sudoku:
	def __init__(self,strPz):
		self.strInPz=strPz
		self.pz=[int(x) for x in strPz]

	def getCurrentPrintablePuzzle(self):
		result=' '+'_'*17 + '\n'
		for i in range(0,len(self.pz)):
			delim=' '
			digit=str(self.pz[i])
			if digit == '0':
				digit='_'
			if(i%3 == 0):
				delim='|'
			if(i%27 == 0 and i!=0):
				result = result + ' '+'\u203e'*17 + '\n'
				result= result + ' '+'_'*17+ '\n'
			result= result + delim + digit
			if ((i+1)%9)==0:
				result= result + '|\n'
		result= result + ' '+'\u203e'*17 + '\n'
		return result

	def getCurrentStrPuzzle(self):
		result=''
		for d in self.pz:
			result= result + str(d)
		return result

	def getInitialStrPuzzle(self):
		return self.strInPz

	def printPuzzle(self):
		print(self.getCurrentPrintablePuzzle())

	def posInRow(self,r):
		possibilities=set(range(1,10))
		for j in range(0,9):
			idx=r*9+j
			if self.pz[idx]!=0:
				possibilities.discard(self.pz[idx])
		return possibilities

	def posInCol(self,c):
		possibilities=set(range(1,10))
		for i in range(0,9):
			idx=i*9+c
			if self.pz[idx]!=0:
				possibilities.discard(self.pz[idx])
		return possibilities

	def posInRegion(self,r,c):
		possibilities=set(range(1,10))
		startI=int(r/3)*3
		startJ=int(c/3)*3
		for i in range(startI,startI+3):
			for j in range(startJ,startJ+3):
				idx=i*9+j
				if self.pz[idx]!=0:
					possibilities.discard(self.pz[idx])
		return possibilities

	def getPosValSets(self):
		res=[]
		for i in range(0,9):
			for j in range(0,9):
				idx=i*9 + j
				if self.pz[idx]==0:
					rowPos=self.posInRow(i)
					colPos=self.posInCol(j)
					regPos=self.posInRegion(i,j)
					cPosVal=rowPos.intersection(colPos,regPos)
					res.append(cPosVal)
					logging.debug(f'Possible values at [{i},{j}]:{cPosVal}')
				else:
					res.append({})
		return res

	def tryDerrivedRules(self,r,c,posValues):
		"""Takes the set of possible values at position [r,c] and removes
		the possible values for the other cells in the same column. If only
		one value remains in the set then that value is only possible on that cell
		so it is return as the correct value.
		If no or multiple values remain it does the same algorithm for the corresponding
		row and region.
		Returns 0 if it can't discover any value. 
		"""
		idx=r*9+c
		remVals=posValues[idx]
		for row in range(0,9):
			if row!=r:
				cIdx=row*9+c
				if self.pz[cIdx]==0:
					remVals=remVals.difference(posValues[cIdx])
		if len(remVals)==1:
			v=remVals.pop()
			logging.debug(f'Possible only here in column discovered value {v} at [{r},{c}]')
			return v
		remVals=posValues[idx]
		for col in range(0,9):
			if col!=c:
				cIdx=r*9+col
				if self.pz[cIdx]==0:
					remVals=remVals.difference(posValues[cIdx])
		if len(remVals)==1:
			v=remVals.pop()
			logging.debug(f'Possible only here in row discovered value {v} at [{r},{c}]')
			return v
		startI=int(r/3)*3
		startJ=int(c/3)*3
		#logging.debug(f'For position [{r},{c}] region starts at [{startI},{startJ}]')
		remVals=posValues[idx]
		#logging.debug(f'Posible values:{remVals}')
		for i in range(startI,startI+3):
			for j in range(startJ,startJ+3):
				if i!=r or j!=c:
					cIdx=i*9+j
					if self.pz[cIdx]==0:
						remVals=remVals.difference(posValues[cIdx])
		if len(remVals)==1:
			v=remVals.pop()
			logging.debug(f'Possible only here in region discovered value {v} at [{r},{c}]')
			return v
		return 0

	def placeSoleValues(self):
		posValues=self.getPosValSets()
		cellsSolved=0
		for i in range(0,len(self.pz)):
			if len(posValues[i])==1:
				val=posValues[i].pop()
				self.pz[i]=val
				r=int(i/9)
				c=i-r*9
				logging.debug(f'Placing:{val} at [{r},{c}]')		
				cellsSolved+=1
		return cellsSolved

	def placeDerrivedRuleCells(self):
		posValues=self.getPosValSets()
		cellsSolved=0
		for i in range(0,len(self.pz)):
			cellV=self.pz[i]
			if cellV==0:
				r=int(i/9)
				c=i-r*9
				derrivedValue=self.tryDerrivedRules(r,c,posValues)
				if derrivedValue!=0:
					logging.debug(f'Derrived rules got value {derrivedValue} at position[{r},{c}]')
					self.pz[i]=derrivedValue
					posValues=self.getPosValSets()
					cellsSolved+=1
		return cellsSolved

	def isValid(self):
		posValues=self.getPosValSets()
		for i in range(0,len(posValues)):
			if self.pz[i]==0 and len(posValues[i])==0:
				r=int(i/9)
				c=i-r*9
				logging.debug(f'No values possible at position[{r},{c}]')
				return False
		return True

	def getCandidates(self):
		posValues=self.getPosValSets()
		candidates=[]
		for minNumCand in range(2,10):
			candidatesCreated=False
			for i in range(0,len(posValues)):
				if len(posValues[i])==minNumCand:
					while len(posValues[i])>0:
						v=posValues[i].pop()
						self.pz[i]=v
						candidates.append(Sudoku(self.getCurrentStrPuzzle()))
					candidatesCreated=True
					break
			if candidatesCreated:
				break
		return candidates

	def isSolved(self):
		for cell in self.pz:
			if cell==0:
				return False
		logging.debug(f'Solved puzzle:\n{self.getCurrentPrintablePuzzle()}')
		return True

	def solvePuzzle(self):
		while(True):
			cellsSolved=self.placeSoleValues() + self.placeDerrivedRuleCells()
			if not self.isValid():
				logging.debug(f'Puzzle validation failed!!!!\n Current state: \n{self.getCurrentPrintablePuzzle()}')
				return False
			if self.isSolved():
				return True
			if cellsSolved==0:
				logging.debug('Smart solve fail, must revert to brute force!!!')
				pzCandidates=self.getCandidates()
				logging.debug(f'{len(pzCandidates)} puzzle candidates')
				for s in pzCandidates:
					logging.debug(f'First candidate:\n{s.getCurrentPrintablePuzzle()}')
					if s.solvePuzzle():
						self.pz=s.pz
						return True
		return False
	
	def reset(self):
		self.pz=[int(x) for x in self.strInPz]
