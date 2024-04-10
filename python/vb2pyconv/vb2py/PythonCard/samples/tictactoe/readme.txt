tictactoe shows off using a background image, the ImageButton widget and
background handlers.

Francois Granger sent the email below which you can adapt to the tictactoe
sample if you want a better computer opponent than Mr. Gumby.


-----Original Message-----
From: Francois Granger [mailto:fgranger@altern.org]
Sent: Tuesday, January 01, 2002 1:50 PM
To: Kevin Altis
Subject: TicTacToe



You published a TicTacToe game developped with PythonCard recently 
with some questions about a winning algorythm. Since I worked on the 
same subject for some time, I got a working brute force one. It needs 
cleaning. See below.

seq is the previous sequence of turns in the form [(i, j), (i, j), ...]
turn is the current turn numbered from 0

======================================
class ComputerAnal(Player):
	"""
	The computer analyse the board
	"""
	def move(self, seq, turn, warn = ""):
		"""
		Analytical seek for solution
		seq is a sequence of tuples representing previous moves.
		return a tuple i, j representing the next move.
		"""
		prompt = warn + "Player " + str(self.token) + " : "
		print prompt
		if turn == 0:
			i,j = 1,1
		elif turn == 1 and seq[0] != (1,1):
			i,j = 1,1
		elif turn == 1:
			i, j = 0,0
		else:
			b = [[0,0,0],[0,0,0],[0,0,0]]
			x = 0
			for move in seq:
				i, j = move
				if x == self.play:
					b[i][j] = 1
				else:
					b[i][j] = -1
				x = not x
			row = [0,0,0]
			col = [0,0,0]
			diag =[0,0]
			"""
			find any line where there are two similar 
                        tokens and third is empty.
			first for me so I play and win
			then for the other so I play and he can't win
			other wise at random.
			"""
			for i in range(3):
				row[i] = b[i][0] + b[i][1] + b[i][2]
			for j in range(3):
				col[j] = b[0][j] + b[1][j] + b[2][j]
			diag[0] = b[0][0] + b[1][1] + b[2][2]
			diag[1] = b[0][2] + b[1][1] + b[2][0]
			pass
			if diag[0] == 2:
				for i in range(3):
					if not b[i][i]:
						return i,i
			if diag[1] == 2:
				for i in range(3):
					if not b[i][2-i]:
						return i,2-i
			for i in range(3):
				if row[i] == 2:
					for j in range(3):
						if not b[i][j]:
							return i,j
			for j in range(3):
				if col[j] == 2:
					for i in range(3):
						if not b[i][j]:
							return i,j

			if diag[0] == -2:
				for i in range(3):
					if not b[i][i]:
						return i,i
			if diag[1] == -2:
				for i in range(3):
					if not b[i][2-i]:
						return i,2-i
			for i in range(3):
				if row[i] == -2:
					for j in range(3):
						if not b[i][j]:
							return i,j
			for j in range(3):
				if col[j] == -2:
					for i in range(3):
						if not b[i][j]:
							return i,j
			pass
			i,j = rand.randint(0, 2), rand.randint(0, 2)
		print i,j
		return i, j

======================================

