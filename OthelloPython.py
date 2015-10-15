import pygame, sys
from pygame.locals import *

			###########
			#CONSTANTS#
			###########
FPS = 30 # frames per second setting
BGCOLOR = (15,110,15) #Background color constant
BOARDSIZE = 8 #number of cases in othello board
CASESIZE = 60 #size of each cases
WINDOWHEIGHT = 600 # height of window
WINDOWWIDTH = 600 # width of window
BLACK = (0,0,0) # black color
WHITE = (255,255,255) #white color
LIGHTGREEN = (15,200,15)
# vertical and horizontal margins so the game is centered
MARGINV = (WINDOWHEIGHT - BOARDSIZE*CASESIZE)/2
MARGINH = (WINDOWWIDTH - BOARDSIZE*CASESIZE)/2

assert WINDOWHEIGHT > BOARDSIZE*CASESIZE and WINDOWWIDTH > BOARDSIZE*CASESIZE, "The board is too big to fit in the window." # keep the program from crashing if bad values are entered.

def main():
	"""
	This is the main function of the program
	"""
	global FPSCLOCK, DISPLAYSURF, BASICFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	# set up the window
	BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
	pygame.display.set_caption('Othello')
	DISPLAYSURF.fill(BGCOLOR)
	#Initialization of the variable
	###############################
	testg = 0 #variable to contain result of testwinner
	board = init_board() #variable to contain the board
	turn = 1 # whose turn is it {1: black, 2: white}
	drawBoard()
	while True:
		clicked_box = () #init
		legals = possible(board,turn)
		for e in pygame.event.get():
			if e.type == QUIT: #handling quitting
				pygame.quit()
				sys.exit()
			elif e.type == MOUSEBUTTONUP: #handling click
				mousex,mousey = e.pos #record a click and its position
				clicked_box = isInBoard(mousex,mousey)
		if clicked_box != () and clicked_box in legals:
			#if it the clicked box is a legal move, make the move
			player_move = Move(clicked_box,turn, board)
			player_move.make(board)
			winner = test_winner(board)
			if winner: #if true : game is not done
				#tests the winner if the game is done
				if winner == 1:
					print "Black player winns"
				elif winner == 2:
					print "White player wins."
				elif winner == 3:
					print "This is a tie game !"
				else:
					turn = 2/(winner-3) # if res= 4 it is black's turn if it is 5 it is white's turn'
			turn = 2/turn
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def drawBoard():
	"""
	This is the method that draws the game board
	"""	
	#draw 64 Rectangles from (MARGINH,MARGINV) with CASESIZE sizes
	for i in range(BOARDSIZE):
		for j in range(BOARDSIZE):
			pygame.draw.rect(DISPLAYSURF, BLACK, [MARGINH + (i)*CASESIZE, MARGINV + (j)*CASESIZE, CASESIZE, CASESIZE], 1)
	
def drawPiece(pos,color):
	"""
	This method draws a piece of the right
	color at the right position.
	"""
	if color == 0:
		color_piece = BGCOLOR
	elif color == 1:
		color_piece = BLACK
	elif color == 2:
		color_piece = WHITE
	elif color == 3:
		color_piece = LIGHTGREEN
	#draws a circle of the right color on the board
	pygame.draw.ellipse(DISPLAYSURF, color_piece, [MARGINH + (pos[0]-1)*CASESIZE+4, MARGINV + (pos[1]-1)*CASESIZE+4, CASESIZE-8, CASESIZE-8])

def isInBoard(posx, posy):
	"""
	This function takes a mouse position and returns the position of the box
	the click is in or an empty tuple if it is not in the board
	"""
	#is pos in the board
	if posx >= MARGINH and posx <= MARGINH + (BOARDSIZE)*CASESIZE and posy >= MARGINV and posy <= MARGINV + (BOARDSIZE)*CASESIZE:
		#transform it in case coordinates
		casex = int((posx - MARGINH)/CASESIZE) + 1
		casey = int((posy - MARGINV)/CASESIZE) + 1
		return (casex,casey)
	else:
		# return emptyu tuple because pos is not in board
		return ()

class Move:
	"""
	This is the class for a move on the board
	"""
	def __init__(self, init_pos, init_coul,state_board):
		# this is the constructor of the class
		self.column = init_pos[0]
		self.line = init_pos[1]
		self.couleur = init_coul
		self.flips = flipper(init_pos,init_coul,state_board)
	
	def make(self,state_board):
		"""
		This function makes the move on the state_board
		"""
		state_board[self.column][self.line] = self.couleur #place the piece
		drawPiece((self.column,self.line),self.couleur) #draws it on the board
		for pos in self.flips: #flips all the pieces in flips
			state_board[pos[0]][pos[1]] = self.couleur
			drawPiece(pos,self.couleur) #draws it on the board

def init_board():
	"""
	This function defines the inital board of the game
	"""
	# Generates a table 10*10 of 0s with -1 around and the initial state
	# of the board with 2 whites and 2 blacks in the middle
	table = [[0 if i != 0 and i != 9 else -1 for i in range(10)] if j != 0 and j != 9 else [-1 for i in range(10)] for j in range(10)] #leaves a -1 line around the whole table of 0s
	#initial state is drawn and recorded
	table[4][4] = 2
	table[5][5] = 2
	table[4][5] = 1
	table[5][4] = 1
	drawPiece((4,4),2)
	drawPiece((5,5),2)
	drawPiece((4,5),1)
	drawPiece((5,4),1)
	return table

def possible(state_board,turn):
	"""
	This function finds possibilities for a player on a board
	"""
	legal_moves = [] # list of legal moves as Move objects
	for i in range(1,9):
		for j in range(1,9):
			if state_board[i][j] == 0:
				if flipper([i,j],turn,state_board) != []:
					# if there are flipped pieces, it appends this move to
					# the legal moves and draws it in light greens
					legal_moves.append((i,j))
					drawPiece((i,j),3)
				else:
					# if it is 0 and is not legal, make sure it is of bgcolor
					drawPiece((i,j),0)
	
	return legal_moves

def flipper(pos, coul, state_board):
	"""
	This function finds the flipped pieces and returns them
	"""
	tflips = []
	for i in range(-1,2): # -1 to 1
		for j in range(-1,2): #-1 to 1
			for k in range(1,9): # 1 to 8
				if state_board[pos[0]+i*k][pos[1]+j*k] == 0 or state_board[pos[0]+i*k][pos[1]+j*k] == -1: # if the case is empty or out of bounds
					break;
				elif state_board[pos[0]+i*k][pos[1]+j*k] == coul: # if it is the same color
					if k > 1: # if it is not directly next to pos
						for h in range(1,k): # add all the pieces in between to tflips
							if not [pos[0]+i*h,pos[1]+j*h] in tflips: #get rid of duplicates
								tflips.append([pos[0]+i*h,pos[1]+j*h])
					else:
						break;
	return tflips

def test_winner(state_board):
	"""
	This function tests a board for a winner and returns
	a value between 0 and 5
	0: game is not done
	1: p1 wins
	2: p2 wins
	3: tie game
	"""
	res = 3 #default value is tie game
	ptsb = 0 #points for the black
	ptsw = 0 #points for the white
	
	#looks in the board if there is an empty case while
	# counting the number of points for each player
	for i in state_board:
		for j in i:
			if j == 0:
				res = 0
			elif j == 1:
				ptsb += 1
			elif j == 2:
				ptsw += 1
	
	#if there is an empty case, looks for possibilities
	# for the other player, if no possibility test for the points
	#if no empty case
	# test for points
	#else return 0
	if res == 0:
		if possible(state_board,1) == []:
			if possible(state_board,2) == []:
				res = count_points(ptsb,ptsw)
			else:
				res = 5
		elif possible(state_board,2) == []:
			res = 4
	else:
		res = count_points(ptsb,ptsw)
	return res

def count_points(p1,p2):
	"""
	This function counts the points and returns
	1 : p1 wins
	2 : p2 wins
	3 : tie game
	"""
	if p1 > p2:
		drawWinner(1)
		return 1
	elif p2 > p1:
		drawWinner(2)
		return 2
	else:
		drawWinner(3)
		return 3

def drawWinner(result):
	"""
	This method says who is the winner on top of the board
	"""
	# determines who is the winner from the result
	if result == 1:
		text = "Black player is the winner !"
	elif result == 2:
		text = "White player is the winner !"
	else:
		text = "Tie Game !"
		
	#draws the text as in a surface
	winner_surf = BASICFONT.render(text, True, BLACK)
	winner_rect = winner_surf.get_rect()
	winner_rect.topleft = ((WINDOWWIDTH - winner_rect.width)/2, 20)
	DISPLAYSURF.blit(winner_surf, winner_rect)

if __name__ == '__main__': #start of the program by calling the main function
    main()
