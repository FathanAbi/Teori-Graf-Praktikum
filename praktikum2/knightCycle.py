import random

# class untuk current_tile
class CurrentTile:
	def __init__(self, x, y):
		self.x = x
		self.y = y

# ukuran board
N = 8

# moves knight
moves_x = [1, 1, 2, 2, -1, -1, -2, -2]
moves_y = [2, -2, 1, -1, 2, -2, 1, -1]

# cek apakah tile masih ada didalam current_tile (legal moves)
def isLegal(x, y):
	return ((x >= 0 and y >= 0) and (x < N and y < N))

# Checks apakah tiles berada dalam current_tile dan kosong
def isempty(tour, x, y):
	return (isLegal(x, y)) and (tour[y * N + x] < 0)

# Cari jumlah tiles kosong yang adjacent (degree dari knight graph)
def getDegree(tour, x, y):
	count = 0
	for i in range(N):
		if isempty(tour, (x + moves_x[i]), (y + moves_y[i])):
			count += 1
	return count

# pilih next move berdasarkan Warnsdorff's heuristic
# return false jika tidak bisa memilih
def nextMove(tour, CurrentTile):
	min_degree_index = -1 # untuk menyimpan index dengan minimum degree
	degree = 0
	min_degree = (N + 1)  # minimum degree
	next_moves_x = 0
	next_moves_y = 0

	# randomize moves
	# cari degree next moves hasil randomize
	# lakukan 8 kali dan dapatkan next moves dengan minimum degree
	start = random.randint(0, 1000) % N
	for count in range(0, N):
		i = (start + count) % N
		next_moves_x = CurrentTile.x + moves_x[i]
		next_moves_y = CurrentTile.y + moves_y[i]
		degree = getDegree(tour, next_moves_x, next_moves_y)
		if ((isempty(tour, next_moves_x, next_moves_y)) and degree < min_degree):
			min_degree_index = i
			min_degree = degree

	# Jika tidak ditemukan next moves
	if (min_degree_index == -1):
		return None

	# tiles next_moves
	next_moves_x = CurrentTile.x + moves_x[min_degree_index]
	next_moves_y = CurrentTile.y + moves_y[min_degree_index]

	# Masukkan next moves ke tiles
	tour[next_moves_y * N + next_moves_x] = tour[(CurrentTile.y) * N + (CurrentTile.x)] + 1

	# Update currentTile
	CurrentTile.x = next_moves_x
	CurrentTile.y = next_moves_y

	return CurrentTile

# displays the chesscurrent_tile with all the isLegal knight's moves
def print_tour(tour):
	for i in range(N):
		for j in range(N):
			print("%d\t" % tour[j * N + i], end="")
		print()

# cek apakah neighbor node nya adalah starting_node
def neighbour(x, y, start_x, start_y):
	for i in range(N):
		if ((x + moves_x[i]) == start_x) and ((y + moves_y[i]) == start_y):
			return True
	return False

# Generates the isLegal moves using warnsdorff's heuristics. Returns false if not possible
def findClosedTour(start_x, start_y):
	# Tour array
	tour = [-1] * N * N

	# buat current_tile
	current_tile = CurrentTile(start_x, start_y)

	tour[current_tile.y * N + current_tile.x] = 1 # First move

    # Cari next move dengan menggunakan Warnsdorff's heuristik
	next_tile = None
	for i in range(N * N - 1):
		next_tile = nextMove(tour, current_tile)
		if next_tile == None:
			return False

	# cek apakah tour closed (neighbor node dari next-tile adalah starting node)
	if not neighbour(next_tile.x, next_tile.y, start_x, start_y):
		return False
	
	print_tour(tour)
	return True


# Driver Code

# initial position
start_x = 7
start_y = 7

## Hamiltonian Cycle
# loop sampai ketemu solusi
while not findClosedTour(start_x, start_y):
	continue
		
		
            
		
    




