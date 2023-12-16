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
        
    

    # cek apakah legal move
    def is_legal_move(self, x, y):
        # apakah di dalam board
        return 0 <= x < self.n and 0 <= y < self.n

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


  

    




    