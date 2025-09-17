import math

convertionDic = {
'.' : 0,
1 : 1,
0 : -1
}

# def  classic_minimax(game_state : GameState, depth : int, maximizingPlayer : bool, alpha=float('-inf'), beta=float('inf')):

# 	if (depth==0) or (game_state.is_terminal()):
# 		return game_state.score(), None

# 	if maximizingPlayer:
# 		value = float('-inf')
# 		possible_moves = game_state.get_possible_moves()
# 		for move in possible_moves:
# 			child = game_state.get_new_state(move)

# 			tmp = minimax(child, depth-1, False, alpha, beta)[0]
# 			if tmp > value:
# 				value = tmp
# 				best_movement = move

# 			if value >= beta:
# 				break
# 			alpha = max(alpha, value)

# 	else:
# 		value = float('inf')
# 		possible_moves = game_state.get_possible_moves()
# 		for move in possible_moves:
# 			child = game_state.get_new_state(move)

# 			tmp = minimax(child, depth-1, True, alpha, beta)[0]
# 			if tmp < value:
# 				value = tmp
# 				best_movement = move

# 			if value <= alpha:
# 				break
# 			beta = min(beta, value)

# 	return value, best_movement
	

def checkWinCondition(map):
	a = 1
	if (map[0] + map[1] + map[2] == a * 3 or map[3] + map[4] + map[5] == a * 3 or map[6] + map[7] + map[8] == a * 3 or
		map[0] + map[3] + map[6] == a * 3 or map[1] + map[4] + map[7] == a * 3 or
		map[2] + map[5] + map[8] == a * 3 or map[0] + map[4] + map[8] == a * 3 or map[2] + map[4] + map[6] == a * 3):
		return a
	a = -1
	if (map[0] + map[1] + map[2] == a * 3 or map[3] + map[4] + map[5] == a * 3 or map[6] + map[7] + map[8] == a * 3 or
		map[0] + map[3] + map[6] == a * 3 or map[1] + map[4] + map[7] == a * 3 or
		map[2] + map[5] + map[8] == a * 3 or map[0] + map[4] + map[8] == a * 3 or map[2] + map[4] + map[6] == a * 3):
		return a
	return 0

def evaluateGame(position, currentBoard):
	evale = 0
	mainBd = []
	evaluatorMul = [1.4, 1, 1.4, 1, 1.75, 1, 1.4, 1, 1.4]
	for eh in range(9):
		evale += realEvaluateSquare(position[eh])*1.5*evaluatorMul[eh]
		if eh == currentBoard:
			evale += realEvaluateSquare(position[eh])*evaluatorMul[eh]
		tmpEv = checkWinCondition(position[eh])
		evale -= tmpEv*evaluatorMul[eh]
		mainBd.append(tmpEv)
	evale -= checkWinCondition(mainBd)*5000
	evale += realEvaluateSquare(mainBd)*150
	return evale

#minimax algorithm
def miniMax(position, boardToPlayOn, depth, alpha, beta, maximizingPlayer, ai, player):

	tmpPlay = -1

	calcEval = evaluateGame(position, boardToPlayOn)
	if depth <= 0 or abs(calcEval) > 5000:
		return {0: calcEval, 1: tmpPlay}
	#If the board to play on is -1, it means you can play on any board
	if boardToPlayOn != -1 and checkWinCondition(position[boardToPlayOn]) != 0:
		boardToPlayOn = -1
	#If a board is full (doesn't include 0), it also sets the board to play on to -1
	if boardToPlayOn != -1 and not 0 in position[boardToPlayOn]:
		boardToPlayOn = -1

	if maximizingPlayer:
		maxEval = float('-inf')
		for mm in range(9):
			evalut = float('-inf')
			#If you can play on any board, you have to go through all of them
			if boardToPlayOn == -1:
				for trr in range(9):
					#Except the ones which are won
					if checkWinCondition(position[mm]) == 0:
						if position[mm][trr] == 0:
							position[mm][trr] = ai
							#tmpPlay = pickBoard(position, True)
							evalut = miniMax(position, trr, depth-1, alpha, beta, False, ai, player)[0]
							#evalut+=150
							position[mm][trr] = 0
						if evalut > maxEval:
							maxEval = evalut
							tmpPlay = mm
						alpha = max(alpha, evalut)

				if beta <= alpha:
					break
			#If there's a specific board to play on, you just go through it's squares
			else:
				if position[boardToPlayOn][mm] == 0:
					position[boardToPlayOn][mm] = ai
					evalut = miniMax(position, mm, depth-1, alpha, beta, False, ai, player)
					position[boardToPlayOn][mm] = 0
				#Beautiful variable naming
				try :
					blop = evalut[0]
					if blop > maxEval:
						maxEval = blop
						#Saves which board you should play on, so that this can be passed on when the AI is allowed to play in any board
						tmpPlay = evalut[1]
						alpha = max(alpha, blop)
				except :
					pass
				if beta <= alpha:
					break
		return maxEval, tmpPlay
	else:
		#Same for the minimizing end
		minEval = float('inf')
		for mm in range(9):
			evalua = float('inf')
			if boardToPlayOn == -1:
				for trr in range(9):
					if checkWinCondition(position[mm]) == 0:
						if position[mm][trr] == 0:
							position[mm][trr] = player
							#tmpPlay = pickBoard(position, True)
							evalua = miniMax(position, trr, depth-1, alpha, beta, True, ai, player)[0]
							#evalua -= 150
							position[mm][trr] = 0
						if evalua < minEval:
							minEval = evalua
							tmpPlay = mm
						beta = min(beta, evalua)

				if beta <= alpha:
					break
			else:
				if position[boardToPlayOn][mm] == 0:
					position[boardToPlayOn][mm] = player
					evalua = miniMax(position, mm, depth-1, alpha, beta, True, ai, player)
					position[boardToPlayOn][mm] = 0
				try :
					blep = evalua[0]
					if blep < minEval:
						minEval = blep
						tmpPlay = evalua[1]
					beta = min(beta, blep)
				except :
					pass
				if beta <= alpha:
					break
		return minEval, tmpPlay

def evaluatePos(pos, square, ai, player):
	pos[square] = ai
	evaluation = 0
	#Prefer center over corners over edges
	#evaluation -= (pos[0]*0.2+pos[1]*0.1+pos[2]*0.2+pos[3]*0.1+pos[4]*0.25+pos[5]*0.1+pos[6]*0.2+pos[7]*0.1+pos[8]*0.2)
	points = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]

	a = 2
	evaluation+=points[square]
	#print("Eyy")
	#Prefer creating pairs
	a = -2
	if pos[0] + pos[1] + pos[2] == a or pos[3] + pos[4] + pos[5] == a or pos[6] + pos[7] + pos[8] == a or pos[0] + pos[3] + pos[6] == a or pos[1] + pos[4] + pos[7] == a or pos[2] + pos[5] + pos[8] == a or pos[0] + pos[4] + pos[8] == a or pos[2] + pos[4] + pos[6] == a:
		evaluation += 1
	#Take victories
	a = -3
	if pos[0] + pos[1] + pos[2] == a or pos[3] + pos[4] + pos[5] == a or pos[6] + pos[7] + pos[8] == a or pos[0] + pos[3] + pos[6] == a or pos[1] + pos[4] + pos[7] == a or pos[2] + pos[5] + pos[8] == a or pos[0] + pos[4] + pos[8] == a or pos[2] + pos[4] + pos[6] == a:
		evaluation += 5
	#Block a players turn if necessary
	pos[square] = player
	a = 3
	if pos[0] + pos[1] + pos[2] == a or pos[3] + pos[4] + pos[5] == a or pos[6] + pos[7] + pos[8] == a or pos[0] + pos[3] + pos[6] == a or pos[1] + pos[4] + pos[7] == a or pos[2] + pos[5] + pos[8] == a or pos[0] + pos[4] + pos[8] == a or pos[2] + pos[4] + pos[6] == a:
		evaluation += 2
	pos[square] = ai
	evaluation-=checkWinCondition(pos)*15
	pos[square] = 0
	#evaluation -= checkWinCondition(pos)*4
	return evaluation

#This function actually evaluates a board fairly, is talked about in video.
def realEvaluateSquare(pos):
	evaluation = 0
	points = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]
	for bw in pos:
		evaluation -= pos[bw]*points[bw]
	a = 2
	if pos[0] + pos[1] + pos[2] == a or pos[3] + pos[4] + pos[5] == a or pos[6] + pos[7] + pos[8] == a:
		evaluation -= 6
	if pos[0] + pos[3] + pos[6] == a or pos[1] + pos[4] + pos[7] == a or pos[2] + pos[5] + pos[8] == a:
		evaluation -= 6
	if pos[0] + pos[4] + pos[8] == a or pos[2] + pos[4] + pos[6] == a:
		evaluation -= 7
	a = -1
	if (pos[0] + pos[1] == 2*a and pos[2] == -a) or (pos[1] + pos[2] == 2*a and pos[0] == -a) or (pos[0] + pos[2] == 2*a and pos[1] == -a) or (pos[3] + pos[4] == 2*a and pos[5] == -a) or (pos[3] + pos[5] == 2*a and pos[4] == -a) or (pos[5] + pos[4] == 2*a and pos[3] == -a) or (pos[6] + pos[7] == 2*a and pos[8] == -a) or (pos[6] + pos[8] == 2*a and pos[7] == -a) or (pos[7] + pos[8] == 2*a and pos[6] == -a) or (pos[0] + pos[3] == 2*a and pos[6] == -a) or (pos[0] + pos[6] == 2*a and pos[3] == -a) or (pos[3] + pos[6] == 2*a and pos[0] == -a) or (pos[1] + pos[4] == 2*a and pos[7] == -a) or (pos[1] + pos[7] == 2*a and pos[4] == -a) or (pos[4] + pos[7] == 2*a and pos[1] == -a) or (pos[2] + pos[5] == 2*a and pos[8] == -a) or (pos[2] + pos[8] == 2*a and pos[5] == -a) or (pos[5] + pos[8] == 2*a and pos[2] == -a) or (pos[0] + pos[4] == 2*a and pos[8] == -a) or (pos[0] + pos[8] == 2*a and pos[4] == -a) or (pos[4] + pos[8] == 2*a and pos[0] == -a) or (pos[2] + pos[4] == 2*a and pos[6] == -a) or (pos[2] + pos[6] == 2*a and pos[4] == -a) or (pos[4] + pos[6] == 2*a and pos[2] == -a):
		evaluation-=9
	a = -2
	if pos[0] + pos[1] + pos[2] == a or pos[3] + pos[4] + pos[5] == a or pos[6] + pos[7] + pos[8] == a:
		evaluation += 6
	if pos[0] + pos[3] + pos[6] == a or pos[1] + pos[4] + pos[7] == a or pos[2] + pos[5] + pos[8] == a:
		evaluation += 6
	if pos[0] + pos[4] + pos[8] == a or pos[2] + pos[4] + pos[6] == a:
		evaluation += 7
	a = 1
	if (pos[0] + pos[1] == 2*a and pos[2] == -a) or (pos[1] + pos[2] == 2*a and pos[0] == -a) or (pos[0] + pos[2] == 2*a and pos[1] == -a) or (pos[3] + pos[4] == 2*a and pos[5] == -a) or (pos[3] + pos[5] == 2*a and pos[4] == -a) or (pos[5] + pos[4] == 2*a and pos[3] == -a) or (pos[6] + pos[7] == 2*a and pos[8] == -a) or (pos[6] + pos[8] == 2*a and pos[7] == -a) or (pos[7] + pos[8] == 2*a and pos[6] == -a) or (pos[0] + pos[3] == 2*a and pos[6] == -a) or (pos[0] + pos[6] == 2*a and pos[3] == -a) or (pos[3] + pos[6] == 2*a and pos[0] == -a) or (pos[1] + pos[4] == 2*a and pos[7] == -a) or (pos[1] + pos[7] == 2*a and pos[4] == -a) or (pos[4] + pos[7] == 2*a and pos[1] == -a) or (pos[2] + pos[5] == 2*a and pos[8] == -a) or (pos[2] + pos[8] == 2*a and pos[5] == -a) or (pos[5] + pos[8] == 2*a and pos[2] == -a) or (pos[0] + pos[4] == 2*a and pos[8] == -a) or (pos[0] + pos[8] == 2*a and pos[4] == -a) or (pos[4] + pos[8] == 2*a and pos[0] == -a) or (pos[2] + pos[4] == 2*a and pos[6] == -a) or (pos[2] + pos[6] == 2*a and pos[4] == -a) or (pos[4] + pos[6] == 2*a and pos[2] == -a):
		evaluation+=9
	evaluation -= checkWinCondition(pos)*12
	return evaluation

def moves(boards, player) :
	MOVES = 0
	for board in boards :
		for i in board :
			if i == player : MOVES += 1
	return MOVES


def convertformat(grid) :
	grid = [[convertionDic[i] for i in j] for j in grid]

	for i, t in enumerate(grid) :
		winning = checkWinCondition(t)
		if winning != 0 :
			grid[i] = [winning for _ in range(9)]

	return grid




def startai(boards, currentBoard, player) :

	boards = convertformat(boards)

	ai = player
	if ai == 1 : player = -1
	else : player = 1
	MOVES = moves(boards, player)
	AIACTIVE = True
	
	print("Start AI")

	bestMove = -1
	bestScore = [float("-inf"), float("-inf"), float("-inf"), float("-inf"), float("-inf"), float("-inf"), float("-inf"), float("-inf"), float("-inf")]

	# Calculates the remaining amount of empty squares
	count = 0
	for bt in range(len(boards)):
		if checkWinCondition(boards[bt]) == 0:
			count += sum(1 for v in boards[bt] if v == 0)

	if currentBoard == -1 or checkWinCondition(boards[currentBoard]) != 0:
		savedMm = None

		print("Remaining:", count)

		# This minimax doesn't actually play a move, it simply figures out which board you should play on
		if MOVES < 10:
			savedMm = miniMax(boards, -1, min(5, count), float("-inf"), float("inf"), True, ai, player)  # Putting math.min makes sure that minimax doesn't run when the board is full
		elif MOVES < 18:
			savedMm = miniMax(boards, -1, min(5, count), float("-inf"), float("inf"), True, ai, player)
		else:
			savedMm = miniMax(boards, -1, min(6, count), float("-inf"), float("inf"), True, ai, player)
		print(savedMm[1])
		currentBoard = savedMm[1]

	# Just makes a quick default move for if all else fails
	for i in range(9):
		if boards[currentBoard][i] == 0:
			bestMove = i
			break


	if bestMove != -1:  # This condition should only be false if the board is full, but it's here in case
		# Best score is an array which contains individual scores for each square, here we're just changing them based on how good the move is on that one local board
		for a in range(9):
			if boards[currentBoard][a] == 0:
				score = evaluatePos(boards[currentBoard], a, ai, player) * 45
				bestScore[a] = score

		# And here we actually run minimax and add those values to the array
		for b in range(9):
			if checkWinCondition(boards[currentBoard]) == 0:
				if boards[currentBoard][b] == 0:
					boards[currentBoard][b] = ai
					# Notice the stacking, at the beginning of the game, the depth is much lower than at the end
					if MOVES < 20:
						savedMm = miniMax(boards, b, min(5, count), float("-inf"), float("inf"), False, ai, player)
					elif MOVES < 32:
						print("DEEP SEARCH")
						savedMm = miniMax(boards, b, min(5, count), float("-inf"), float("inf"), False, ai, player)
					else:
						print("ULTRA DEEP SEARCH")
						savedMm = miniMax(boards, b, min(6, count), float("-inf"), float("inf"), False, ai, player)
					print(savedMm)
					score2 = savedMm[0]
					boards[currentBoard][b] = 0
					bestScore[b] += score2

		print(bestScore)

		# Choses to play on the square with the highest evaluation in the bestScore array
		for i in range(len(bestScore)):
			if bestScore[i] > bestScore[bestMove]:
				bestMove = i

		aiboard = currentBoard

		# Actually places the cross/nought
		# if boards[currentBoard][bestMove] == 0:
		# 	boards[currentBoard][bestMove] = ai
		# 	currentBoard = bestMove

		# print(evaluateGame(boards, currentBoard))
		# print(boards, currentBoard)
		return aiboard, bestMove


if __name__ == '__main__' :


	boards = [
	['.', '.', '.', '.', '.', '.', '.', '.', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.'],
	['.', '.', '.', '.', '.', 0, '.', '.', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.'],
	['.', '.', '.', 1, '.', '.', '.', '.', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.'],
	['.', 1, '.', '.', '.', '.', 0, '.', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.'],]

	currentBoard = 2

	player = 1

	print(startai(boards, currentBoard, player))