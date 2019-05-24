from board import Board

if __name__ == "__main__":

    board = Board()
    turns = ["computer", "player"]
    while True:

        print(board)
        if board.check_status() is not None:
            if board.check_status() == "X":
                print("WIN COMPUTER")
            else:
                print("WIN PLAYER")
            break

        if board.is_free_cell():

            if turns[0] == "computer":
                board.make_the_move()

            else:
                pos1 = int(
                    input("Enter the x position (1, 2 ,3) : "))-1
                pos2 = int(
                    input("Enter the y position (1, 2 ,3) : "))-1
                while not board.put((pos1, pos2), "O"):
                    print("Reinput!!!")
                    pos1 = int(
                        input("Enter the x position (1, 2 ,3) : "))-1
                    pos2 = int(
                        input("Enter the y position (1, 2 ,3) : "))-1
            turns.reverse()

        else:
            print("50-50")
            break
