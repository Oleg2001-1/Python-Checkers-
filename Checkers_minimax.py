#Aleh Iotchanka
#Warcaby za pomocą algorytmu min-max z przycinaniem alfa-beta

from copy import deepcopy   # deepcopy dla robienia kopii całego pola
import math

class Game_condition:                                    # klasa, odpowiadająca za stan pola
    def __init__(self, field, move=None, value=None):
        self.field = field
        self.value = value
        self.move = move

    def child_get(self, maximizing_player):        # funkcja, odpowiadająca za następne stany pola
        curr_state = deepcopy(self.field)
        possibilites_to_move = []
        child_states = []
        capital_let = ""
        row_of_queen = 0
        if maximizing_player is True:             # komputer powinien wygrać, jest maksymizatorem
            possibilites_to_move = Draughts.find_AI_possibilites_to_move(curr_state)
            capital_let = "C"
            row_of_queen = 7
        else:                                   #Player musi przegrać , jest minimalizatorem
            possibilites_to_move = Draughts.find_player_possibilites_to_move(curr_state)
            capital_let = "P"
            row_of_queen = 0
        for i in range(len(possibilites_to_move)):
            new_i = possibilites_to_move[i][2]
            new_j = possibilites_to_move[i][3]
            early_i = possibilites_to_move[i][0]
            early_j = possibilites_to_move[i][1]
            state = deepcopy(curr_state)       #kopiujemy stan pola
            Draughts.make_a_move(state, early_i, early_j, new_i, new_j, capital_let, row_of_queen)
            child_states.append(Game_condition(state, [early_i, early_j, new_i, new_j]))
        return child_states

    def get_value(self):           #Otrzymanie stanu pola
        return self.value

    def set_value(self, value):    #Zwrócenie wartości stanu pola
        self.value = value

    def get_field(self):           #Zwrócenie pola
        return self.field

class Draughts:                  #Klasa odpowiadająca za Warcaby
    def __init__(self):
        self.checkers_of_AI = 12
        self.checkers_of_Player = 12
        self.turn_cur = True
        self.field = [[], [], [], [], [], [], [], []]
        self.possibilites_to_move = []

        for row in self.field:  #generecja pola
            for i in range(8):
                row.append("*")

        self.AI_pos()                 #generacja pionów komputera
        self.player_pos()             #generacja pionów playera

    def AI_pos(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.field[i][j] = ("c" + str(i) + str(j))

    def player_pos(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.field[i][j] = ("p" + str(i) + str(j))

    def print_field(self):      #rysowanie pola gry
        i = 0
        print()
        for row in self.field:
            print(i, end="  ")
            i += 1
            for elem in row:
                print(elem[0], end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "   0"
            print(j, end=" ")
        print("\n")

    def get_player_input(self):                       #Funkcja otrzymuje oraz analizuje ruchy, podane przez Playera
        possibilites_to_move = Draughts.find_player_possibilites_to_move(self.field)
        if len(possibilites_to_move) == 0:
            if self.checkers_of_AI > self.checkers_of_Player:
                print( "YOU LOSE!" )
                exit()
            else:
                print( "GAME ENDED!")
                exit()
        self.checkers_of_Player = 0
        self.checkers_of_AI = 0
        while True:
            coord1 = input("Który pion wybierasz[i,j]?: ")
            if coord1 == "":
                print("GAME ENDED!")
                exit()
            coord2 = input("Idziemy do[i,j]:")
            if coord2 == "":
                print("GAME ENDED!")
                exit()
            early = coord1.split(",")
            new = coord2.split(",")
            if len(early) != 2 or len(new) != 2:
                print("Niepoprawny format")
            else:
                early_i = early[0]
                early_j = early[1]
                new_i = new[0]
                new_j = new[1]
                if not early_i.isdigit() or not early_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print("Niepoprawny format")
                else:
                    move = [int(early_i), int(early_j), int(new_i), int(new_j)]
                    if move not in possibilites_to_move:
                        print("Niepoprawny ruch")
                    else:
                        Draughts.make_a_move(self.field, int(early_i), int(early_j), int(new_i), int(new_j), "P", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.field[m][n][0] == "c" or self.field[m][n][0] == "C":
                                    self.checkers_of_AI += 1
                                elif self.field[m][n][0] == "p" or self.field[m][n][0] == "P":
                                    self.checkers_of_Player += 1
                        break

    @staticmethod
    def find_AI_possibilites_to_move(field):    #Funkcja znalezienia możliwych ruchów komputera
        possibilites_to_move = []
        possible_hits = []
        for x in range(8):
            for y in range(8):
                if field[x][y][0] == "c":            #Możliwe ruchy, jeżeli jest poprostu pionem
                    if Draughts.verify_AI_moves(field, x, y, x + 1, y + 1):
                        possibilites_to_move.append([x, y, x + 1, y + 1])
                    if Draughts.verify_AI_moves(field, x, y, x + 1, y - 1):
                        possibilites_to_move.append([x, y, x + 1, y - 1])
                    if Draughts.verify_AI_hits(field, x, y, x + 1, y - 1, x + 2, y - 2):
                        possible_hits.append([x, y, x + 2, y - 2])
                    if Draughts.verify_AI_hits(field, x, y, x + 1, y + 1, x + 2, y + 2):
                        possible_hits.append([x, y, x + 2, y + 2])
                elif field[x][y][0] == "C":      #Możliwe ruchy, jeżeli pion jest damką
                    if Draughts.verify_AI_moves(field, x, y, x + 1, y + 1):
                        possibilites_to_move.append([x, y, x + 1, y + 1])
                    if Draughts.verify_AI_moves(field, x, y, x + 1, y - 1):
                        possibilites_to_move.append([x, y, x + 1, y - 1])
                    if Draughts.verify_AI_moves(field, x, y,x - 1, y - 1):
                        possibilites_to_move.append([x, y, x - 1, y - 1])
                    if Draughts.verify_AI_moves(field, x, y, x - 1, y + 1):
                        possibilites_to_move.append([x, y, x - 1, y + 1])
                    if Draughts.verify_AI_hits(field, x, y, x + 1, y - 1, x + 2, y - 2):
                        possible_hits.append([x, y, x + 2, y - 2])
                    if Draughts.verify_AI_hits(field, x, y, x - 1, y - 1, x - 2, y - 2):
                        possible_hits.append([x, y, x - 2, y - 2])
                    if Draughts.verify_AI_hits(field, x, y, x - 1, y + 1, x - 2, y + 2):
                        possible_hits.append([x, y, x - 2, y + 2])
                    if Draughts.verify_AI_hits(field, x, y, x + 1, y + 1, x + 2, y + 2):
                        possible_hits.append([x, y, x + 2, y + 2])
        if len(possible_hits) == 0:
            return possibilites_to_move
        else:
            return possible_hits

    @staticmethod
    def find_player_possibilites_to_move(field):     #Funkcja znalezienia możliwych ruchów Playera
        possibilites_to_move = []
        possible_hits = []
        for x in range(8):
            for y in range(8):
                if field[x][y][0] == "p":                      #Możliwe ruchy, jeżeli jest poprostu pionem
                    if Draughts.verify_player_moves(field, x, y, x - 1, y - 1):
                        possibilites_to_move.append([x, y, x - 1, y - 1])
                    if Draughts.verify_player_moves(field, x, y, x - 1, y + 1):
                        possibilites_to_move.append([x, y, x - 1, y + 1])
                    if Draughts.verify_player_hits(field, x, y, x - 1, y - 1, x - 2, y - 2):
                        possible_hits.append([x, y, x - 2, y - 2])
                    if Draughts.verify_player_hits(field, x, y, x - 1, y + 1, x - 2, y + 2):
                        possible_hits.append([x, y, x - 2, y + 2])
                elif field[x][y][0] == "P":                        #Możliwe ruchy, jeżeli pion jest damką
                    if Draughts.verify_player_moves(field, x, y, x - 1, y - 1):
                        possibilites_to_move.append([x, y, x - 1, y - 1])
                    if Draughts.verify_player_moves(field, x, y, x - 1, y + 1):
                        possibilites_to_move.append([x, y, x - 1, y + 1])
                    if Draughts.verify_player_hits(field, x, y, x - 1, y - 1, x - 2, y - 2):
                        possible_hits.append([x, y, x - 2, y - 2])
                    if Draughts.verify_player_hits(field, x, y, x - 1, y + 1, x - 2, y + 2):
                        possible_hits.append([x, y, x - 2, y + 2])
                    if Draughts.verify_player_moves(field, x, y, x + 1, y - 1):
                        possibilites_to_move.append([x, y, x + 1, y - 1])
                    if Draughts.verify_player_hits(field, x, y, x + 1, y - 1, x + 2, y - 2):
                        possible_hits.append([x, y, x + 2, y - 2])
                    if Draughts.verify_player_moves(field, x, y, x + 1, y + 1):
                        possibilites_to_move.append([x, y, x + 1, y + 1])
                    if Draughts.verify_player_hits(field, x, y, x + 1, y + 1, x + 2, y + 2):
                        possible_hits.append([x, y, x + 2, y + 2])

        if len(possible_hits) == 0:
            return possibilites_to_move
        else:
            return possible_hits

    @staticmethod
    def verify_AI_hits(field, early_i, early_j, via_i, via_j, new_i, new_j):        #Funkcja znalezienia możliwych przeskakiwań komputera
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if field[via_i][via_j] == "*":
            return False
        if field[via_i][via_j][0] == "C" or field[via_i][via_j][0] == "c":
            return False
        if field[new_i][new_j] != "*":
            return False
        if field[early_i][early_j] == "*":
            return False
        if field[early_i][early_j][0] == "p" or field[early_i][early_j][0] == "P":
            return False
        return True


    @staticmethod
    def verify_player_hits(field, early_i, early_j, via_i, via_j, new_i, new_j):     #Funkcja znalezienia możliwych przeskakiwań Playera
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if field[via_i][via_j] == "*":
            return False
        if field[via_i][via_j][0] == "P" or field[via_i][via_j][0] == "p":
            return False
        if field[new_i][new_j] != "*":
            return False
        if field[early_i][early_j] == "*":
            return False
        if field[early_i][early_j][0] == "c" or field[early_i][early_j][0] == "C":
            return False
        return True
    
    @staticmethod
    def verify_AI_moves(field, early_i, early_j, new_i, new_j):         #Funkcja znalezienia możliwych ruchów komputera
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if field[early_i][early_j] == "*":
            return False
        if field[new_i][new_j] != "*":
            return False
        if field[early_i][early_j][0] == "p" or field[early_i][early_j][0] == "P":
            return False
        if field[new_i][new_j] == "*":
            return True

    @staticmethod
    def verify_player_moves(field, early_i, early_j, new_i, new_j):     #Funkcja znalezienia możliwych ruchów Playera
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if field[early_i][early_j] == "*":
            return False
        if field[new_i][new_j] != "*":
            return False
        if field[early_i][early_j][0] == "c" or field[early_i][early_j][0] == "C":
            return False
        if field[new_i][new_j] == "*":
            return True

    @staticmethod
    def Calculate_evaluation(field):           #Funkcja oceny gry
        comp, player = 0, 0
        checkers_of_comp, checkers_of_player = 0, 0 
        for x in range(8):
            for y in range(8):
                if field[x][y][0] == "c":
                    checkers_of_comp +=1
                    if y >= 0 and y <= 3:
                        comp = comp + 5
                    else:
                        comp = comp + 7
                if field[x][y][0] == "C":
                    checkers_of_comp +=1
                    comp += 10
                if field[x][y][0] == "p":
                    checkers_of_player += 1
                    if y >= 0 and y <= 3:
                        player = player + 7
                    else:
                        player = player + 5
                if field[x][y][0] == "P":
                    checkers_of_player += 1 
                    player += 10                
        return (player/checkers_of_player) - (comp/checkers_of_comp)

    def evaluate_states(self):                                   #Funkcja oceny stanu pola dla komputera
        curr_state = Game_condition(deepcopy(self.field))
        start_AI_moves = curr_state.child_get(True)
        if len(start_AI_moves) == 0:
            if self.checkers_of_Player > self.checkers_of_AI:
                print( "YOU WIN!")
                exit()
            else:
                print( "GAME ENDED!" )
                exit()
        dict = {}
        for i in range(len(start_AI_moves)):
            child = start_AI_moves[i]
            value = Draughts.minimax(child.get_field(), 4, -math.inf, math.inf, False)
            dict[value] = child
        if len(dict.keys()) == 0:
            exit()
        new_field = dict[max(dict)].get_field()
        move = dict[max(dict)].move
        self.field = new_field
        print("Komputer rusza z (" + str(move[0]) + "," + str(move[1]) + ") do (" + str(move[2]) + "," + str(move[3]) + ").")

    @staticmethod
    def minimax(field, depth, alpha, beta, maximizing_player):    # Algorytm minimaks z przycinaniem alfa - beta. To jest standardowa implementacja tego algorytmu.
        if depth == 0:
            return Draughts.Calculate_evaluation(field)
        curr_state = Game_condition(deepcopy(field))
        if maximizing_player is True:
            max_evaluate = -math.inf
            for child in curr_state.child_get(True):
                evaluate = Draughts.minimax(child.get_field(), depth - 1, alpha, beta, False)
                max_evaluate = max(max_evaluate, evaluate)
                alpha = max(alpha, evaluate)
                if beta <= alpha:
                    break
            curr_state.set_value(max_evaluate)
            return max_evaluate
        else:
            min_evaluate = math.inf
            for child in curr_state.child_get(False):
                evaluate = Draughts.minimax(child.get_field(), depth - 1, alpha, beta, True)
                min_evaluate = min(min_evaluate,evaluate)
                beta = min(beta,evaluate)
                if beta <= alpha:
                    break
            curr_state.set_value(min_evaluate)
            return min_evaluate

    @staticmethod
    def make_a_move(field, early_i, early_j, new_i, new_j, capital_let, row_of_queen):     #Funkcja robienia ruchu
        let = field[early_i][early_j][0]
        diff_i = early_i - new_i
        diff_j = early_j - new_j
        if diff_i == -2 and diff_j == 2:
            field[early_i + 1][early_j - 1] = "*"
        elif diff_i == 2 and diff_j == 2:
            field[early_i - 1][early_j - 1] = "*"
        elif diff_i == 2 and diff_j == -2:
            field[early_i - 1][early_j + 1] = "*"
        elif diff_i == -2 and diff_j == -2:
            field[early_i + 1][early_j + 1] = "*"
        if new_i == row_of_queen:
            let = capital_let
        field[early_i][early_j] = "*"
        field[new_i][new_j] = let + str(new_i) + str(new_j)

    def Play_game(self):                              #Funkcja uruchomiania gry
        print("\nReguły gry:")
        print("1.Współrzędne wpisujesz w postaci i,j( gdzie i numer wiersza, j numer kolumny).")
        print("2.Możesz wyjść z gry w dowolnym momencie, naciskając Enter")
        print("Twoje piony to 'p' , komputera 'c' ")
        while True:
            self.print_field()
            if self.turn_cur is True:
                print("\nTwoj ruch!")
                self.get_player_input()
            else:
                print("Ruch komputera")
                self.evaluate_states()
            if self.checkers_of_Player == 0:
                self.print_field()
                print("YOU LOSE!")
                exit()
            elif self.checkers_of_AI == 0:
                self.print_field()
                print("YOU WIN!")
                exit()
            self.turn_cur = not self.turn_cur

draughts = Draughts()
draughts.Play_game()
