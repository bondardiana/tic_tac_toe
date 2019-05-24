import random
from linkedbst import LinkedBST


import copy
from bstnode import BSTNode
from linkedbst import LinkedBST
import random
import sys


class Board:
    """
    Class represents a board for playing
    Tic Tac Toe Game
    Here we have basic computer intelligence based on binary tree from variants
    """

    USER_MARK = "O"
    COMPUTER_MARK = "X"

    def __init__(self):
        """
        Create new instance of Board for playing tic-tac-toe game
        """
        self._board = [[None, None, None], [
            None, None, None], [None, None, None]]
        self.lastPosition = [None, None]
        self.lastMark = None
        self.rec_cur_player = [self.USER_MARK, self.COMPUTER_MARK]

    def __str__(self):
        """
        String representation of board
        :return str:
        """
        s = ""
        for line in self._board:
            for el in line:
                if el:
                    s += el
                else:
                    s += "_"
            s += "\n"

        return s

    def check_status(self):
        """
        Check status of board. Are there winner or no?
        :param list[list] board:
        :return str: mark of winner
        """

        for i in range(3):
            if self._board[i][0] == self._board[i][1] == self._board[i][2] and self._board[i][0] is not None:
                return self._board[i][0]

            if self._board[0][i] == self._board[1][i] == self._board[2][i] and self._board[0][i] is not None:
                return self._board[0][i]

        if self._board[0][0] == self._board[1][1] == self._board[2][2] and self._board[2][2]:
            return self._board[2][2]

        if self._board[2][0] == self._board[1][1] == self._board[0][2] and self._board[0][2]:
            return self._board[0][2]

        return None

    def put(self, position, mark):
        """
        Check conditionals and put mark on the board
        :param list[int, int] position:
        :param str mark: str
        :return None:
        """
        try:
            if self._board[position[0]][position[1]] is not None:
                return False

            self._board[position[0]][position[1]] = mark
            self.lastPosition = [position[0], position[1]]
            return True
        except:
            return False

    def build_tree(self):
        """
        Build binary game tree
        :param board:
        :return: BinaryTree
        """

        tree = LinkedBST()
        tree._root = BSTNode(self)

        def process(node):
            board = node.data
            if not board or not board.is_free_cell():
                return

            if board.check_status() is not None:
                return
            list2 = [[1, 0], [1, 2], [0, 1], [2, 1]]
            list1 = [[2, 2], [0, 0], [0, 2], [2, 0], [1, 1]]
            retries = 0
            while True:

                retries += 1

                if retries > 10:
                    list2 = list1
                position = random.choice(list2)
                if not board._board[position[0]][position[1]]:
                    break
            retries = 0
            new_board = copy.deepcopy(board)
            new_board.put([position[0], position[1]],
                          self.rec_cur_player[1])
            self.rec_cur_player = [
                self.rec_cur_player[1], self.rec_cur_player[0]]
            node.left = BSTNode(new_board)

            board = node.data
            if not board or not board.is_free_cell():
                return

            if board.check_status() is not None:
                return

            while True:
                retries += 1

                if retries > 10:
                    list1 = list2
                position = random.choice(list1)
                if not board._board[position[0]][position[1]]:

                    break

            new_board = copy.deepcopy(board)
            new_board.put([position[0], position[1]],
                          self.COMPUTER_MARK)
            node.right = BSTNode(new_board)

            process(node.left)
            process(node.right)

        process(tree._root)
        return tree

    def choose_pos(self):
        """
        Choose next step by computer based on binary tree
        :return list:
        """

        tree = self.build_tree()

        def count(node):
            if node.right is None and node.left is None:
                if node.data.check_status() == self.COMPUTER_MARK:
                    return 10
                elif node.data.check_status() == self.USER_MARK:
                    return -10
                else:
                    return 0

            return count(node.left) + count(node.right)
        count_left = count(tree._root.left)
        count_right = count(tree._root.right)
        if count_right > count_left:
            return tree._root.right.data.lastPosition
        else:
            return tree._root.left.data.lastPosition

    def make_the_move(self):
        """
        Computer move
        """
        pos1, pos2 = self.choose_pos()
        self.put((pos1, pos2), "X")

    def is_free_cell(self):
        """
        Cheks whether the boad is not full
        """
        for line in self._board:
            for el in line:
                if not el:
                    return True
        return False
