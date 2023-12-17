# Praktikum T GRAF

# Praktikum 1
Implemantasikan sebuah program untuk menyelesaikan permasalahan “Largest Monotonically Increasing Subsequence” (pada hal 3)

## Jawab
Menggunakan segment tree untuk menyelesaiakan problem

![](./img/segment%20tree.jpg)

Class segment tree beserta constructornya
```py
class SegmentTree:
    # Init
    def __init__(self, n):
        self.n = n

        # create segment tree
        # karena segment tree untuk array ukuran n adalah 2*n - 1 maka. jumlah nodenya adalah (2*n)
        self.tree = [0] * (2 * n)
```

Method untuk mengupdate tree
```py
# update Tree
    def update(self, index, value):
        # adjust index
        index += self.n

        # update value nya
        self.tree[index] = value

        # update node parent parentnya dengan max dari child
        while index > 1:
            index //= 2
            self.tree[index] = max(self.tree[2 * index], self.tree[2 * index + 1])
```

Method untuk query
```py
# cari max value dari range [left, right]
    def query(self, left, right):
        # adjust index
        left += self.n
        right += self.n

        result = 0

        # cek apakah left < right. traverse dari bawah (child) ke atas (parent)
        while left < right:
            # jika left merupakan child kanan
            if left % 2 == 1:
                # bandingkan dengan result
                result = max(result, self.tree[left])
                left += 1
            
            # jika right merupakan child kanan
            if right % 2 == 1:
                right -= 1
                # bandingkan dengan result
                result = max(result, self.tree[right])
            
            # ke node parent
            left //= 2
            right //= 2
        
        #print(result)
        return result
```

Fungsi untuk mencari longest increasing subsequence

```py
def longest_increasing_subsequence(nums):
    n = len(nums)

    # map index : sorted num
    index_map = {num: i for i, num in enumerate(sorted(set(nums)))}
    # print(index_map)
    # print(len(index_map))

    # buat segment tree
    segment_tree = SegmentTree(len(index_map))

    # track panjang lis
    lis_length = 0

    # iterates tiap nums
    for num in nums:
        # ambil index dari hasil map
        index = index_map[num]

        # gunakan segment tree untuk mendapatkan max length increasing subsequence yang berakhiran index
        # + 1 untuk menghitung nums saat ini juga
        length = segment_tree.query(0, index) + 1

        # update segment tree dengan length baru index 
        segment_tree.update(index, length)

        # bandingkan dengan lis_length
        lis_length = max(lis_length, length)

        

    return lis_length
```

Driver Code:
```py
# Driver Code
nums = [3,1,4,2,5]
result = longest_increasing_subsequence(nums)
print("Panjang LiS:", result)
```


# Praktikum 2
![](./img/Soal%202.png)

## Closed Tour (Hamiltonian Cycle)
menggunakan warnsdorf's heuristic

class current tile dan N (ukuran borad)
```py
# class untuk current_tile
class CurrentTile:
	def __init__(self, x, y):
		self.x = x
		self.y = y

# ukuran current_tile
N = 8
```

moves dari knight
```py
# moves knight
moves_x = [1, 1, 2, 2, -1, -1, -2, -2]
moves_y = [2, -2, 1, -1, 2, -2, 1, -1]
```

cek apakah moves legal (berada dalam board)
```py
# cek apakah tile masih ada didalam current_tile (legal moves)
def isLegal(x, y):
	return ((x >= 0 and y >= 0) and (x < N and y < N))
```
cek apakah tile pernah dikunjungi dan legal

```py
# Checks apakah tiles berada dalam current_tile dan kosong
def isempty(tour, x, y):
	return (isLegal(x, y)) and (tour[y * N + x] < 0)
```

cari degree dari tiles (banyaknya neighbor)
```py
# Cari jumlah tiles kosong yang adjacent (degree dari knight graph)
def getDegree(tour, x, y):
	count = 0
	for i in range(N):
		if isempty(tour, (x + moves_x[i]), (y + moves_y[i])):
			count += 1
	return count
```

Generate next move berdasarkan warnsdorff heuristic
```py
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
```

print tour
```py
# displays the chesscurrent_tile with all the isLegal knight's moves
def print_tour(tour):
	for i in range(N):
		for j in range(N):
			print("%d\t" % tour[j * N + i], end="")
		print()
```

cek apakah dua tiles merupakan neighbour (terhubung edge)
```py
# cek apakah neighbor tiles nya adalah starting_node
def neighbour(x, y, start_x, start_y):
	for i in range(N):
		if ((x + moves_x[i]) == start_x) and ((y + moves_y[i]) == start_y):
			return True
	return False
```

cari hamiltonian cycle:
```py
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
```

driver code
```py
# Driver Code

# initial position
start_x = 7
start_y = 7

## Hamiltonian Cycle
# loop sampai ketemu solusi
while not findClosedTour(start_x, start_y):
	continue
```

## Open tour (Hamiltionia Path)
menggunakan dfs

## jawab
Class knight graph dan constructor
```py
class KnightGraph:
    # init 
    def __init__(self, n):
        # jumlah board
        self.n = n

        # generate graph (vertex)
        self.graph = {i * n + j: [] for i in range(n) for j in range(n)}
        
        # definisikan moves dari knight
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                      (-2, -1), (-1, -2), (1, -2), (2, -1)]
```

cek apakah legal move
```py
# cek apakah legal move
    def is_legal_move(self, x, y):
        # apakah di dalam board
        return 0 <= x < self.n and 0 <= y < self.n
```

generate knight graph 
```py
# generate graph (edge)
    def generate_graph(self):
        # generate moves tiap node / tiles

        # iterasi tiap tiles
        for i in range(self.n):
            for j in range(self.n):
                current_node = i * self.n + j

                # iterasi moves 
                for move in self.moves:
                    x, y = i + move[0], j + move[1]
                    if self.is_legal_move(x, y):
                        next_node = x * self.n + y
                        self.graph[current_node].append(next_node)
        
        # print(self.graph)
```

method print graph dan print tour
```py
def print_graph(self):
        for node in self.graph:
            print(f"{node}: {self.graph[node]}")

    def print_tour(self, tour):
        board = [0] * 64
        i = 1
        for tiles in tour:
            board[tiles] = i
            i += 1
        
        i = 1
        for moves in board:
            print(moves, end="\t")
            if(i % 8 ==0 ):
                print()
            i += 1
```

generate tour (hamiltonian path) dengan menggunakan dfs
```py
# cari tour (hamiltonian path)
    def generate_tour(self, start_node):
        visited = set()
        tour = []

        # gunakan dfs 
        def dfs(node):
            nonlocal tour
            tour.append(node)
            visited.add(node)

            # cek apakah sudah pernah mengunjungi vertec
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        # rekursi
        dfs(start_node)

        self.print_tour(tour)
```

Driver Code
```py
# Driver Code

n = 8  # Board size

# init
knight_graph = KnightGraph(n)

# generate graph
knight_graph.generate_graph()
# knight_graph.print_graph()


# cari tour (hamiltonian path)
start_x = 0
start_y = 0

start_node = (start_y) * 8 + (start_x) 
knight_graph.generate_tour(start_node)
```