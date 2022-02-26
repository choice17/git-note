import numpy as np
from typing import List

class Matches(object):
    """
    Graph matching  Gale–Shapley algorithm
    """
    def __init__(self, N : int):
        self.N = N
        self.boy_scores = []
        self.girl_scores = []

    def build_pairs(self) -> List[int]:

        def ind_search(arr : List[int], v : int) -> int:
            for ind, i in enumerate(arr):
                if i == v:
                    return ind
            return -1

        m_list = list(range(self.N))

        # init with val
        m_matches = [-1 for _ in range(self.N)]
        f_matches = [-1 for _ in range(self.N)]
        boy = -1
        next_man_choice = [0] * self.N

        # iter util the end
        while len(m_list):

            # pick one boy
            boy = m_list[0]
            his_score = self.boy_scores[boy]

            # pick the one girl such that
            # 1. he like the most
            # 2. he never paired with before
            girl = his_score[next_man_choice[boy]]
            her_score = self.girl_scores[girl]

            # check her current match
            cur_partner = f_matches[girl]

            # apply the match for vacancy
            if cur_partner == -1:
                f_matches[girl] = boy
                m_matches[boy] = girl
                m_list.pop(0)
            else: # replace the match for priority
                cur_partner_ind = ind_search(her_score, cur_partner)
                boy_ind = ind_search(her_score, boy)
                if cur_partner_ind > boy_ind:
                    m_list.pop(0)
                    m_list.insert(0, f_matches[girl])
                    f_matches[girl] = boy
                    m_matches[boy] = girl

            # switch to next unpaired girl
            next_man_choice[boy] = next_man_choice[boy] + 1

        return [i+1 for i in m_matches]

def read_score(string):
    a = string.split(" ")
    return [int(i)-1 for i in a]


""" test case 0
3
1 2 3
1 2 3
2 1 3
3 2 1
3 1 2
2 1 3
->
3 1 2
"""

""" test case 1
2
1 2
2 1
2 1
1 2
->
1 2
"""

""" test case 2
5
5 1 2 3 4
1 2 5 3 4
1 5 2 3 4
2 5 3 1 4
3 2 5 1 4
5 2 3 4 1
5 1 3 4 2
2 1 5 3 4
2 1 5 3 4
5 1 2 4 3
->
5 1 2 4 3
"""

if __name__ == "__main__":
    n = int(input())
    matches = Matches(n)

    for _ in range(n):
        scores = read_score(input())
        matches.boy_scores.append(scores)

    for _ in range(n):
        scores = read_score(input())
        matches.girl_scores.append(scores)

    pairs = matches.build_pairs()
    for i in pairs:
    	print(i)
