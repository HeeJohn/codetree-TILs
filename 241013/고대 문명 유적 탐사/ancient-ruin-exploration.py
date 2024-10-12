# [1] 탐사 진행
# 1. 3 x 3 격자 선택 (회전 중심 좌표를 선택)
# 2. 선택한 격자 회전 (90, 180, 90) -- space 회전 함수
# 목표 :
# 1. 유물 1차 획득 가치를 최대화
# 2. 회전한 각도가 가장 작은 방법을 선택
# 3. 회전 중심 좌표의 열이 가장 작은 구간
# 4. 회전 중심 좌표의 행이 가장 작은 구간 순


# [2] 유물 획득
# 1. 상하좌우로 인접한 같은 종류의 유물 조각은 서로 연결  -- space bfs 함수
# 2. 이 조각들이 3개이상 연결된 경우 유물이 됨. -- trace 담고 len()로 카운트
# 3. 유물의 가치 = 모인 조각 개수
# 4. 획득한 조간 위치 제거 (제거 시 bfs로 좌표를 수집 ) -- trace

# [3] 조각 채우기 -- wall 자료 구조
# 1. 열 번호가 작은 순으로 조각이 생김
# 2. 행 번호가 큰 순으로 조각 생김
# 3. trace를 열 순으로 먼저 asc, 행 순으로 desc -- space 정렬 함수
# 4. 벽에 있는 숫자는 큐처럼 뽑아서 쓰기 FIFO

# [4] 유물 연쇄 획득 (조각 채우기 바로 이후, 턴이 넘어가기 전)
# 1. 연결된 조각들이 있나 다시 확인 --> 3 조각 이상 연결되지 않아 유물이 될 수 없을 때까지
# 2. 연쇄 획득 반복 -- bfs 반복할 수 있도록 모듈화


# [5] 탐사 반복
# 1. 탐사 ~ 유물 연쇄까지 1턴 -> 총 K 턴 반복


# 출력 : 각 턴마다 획득한 유물의 가치의 총합을 출력하는 프로그램
# (K번의 턴을 진행하지 못했지만, 유물 획득 못하는 경우 즉시 종료 ) -- 종료되는 턴에 출력 x

# 입력
# 1. 탐사 반복 횟수 K, 벽면의 유물 조각의 수 M
# 2. 5개의 줄로 유물의 각 행의 유물 조각 번호
# 3. 벽면에 적힌 M개의 유물 조각 번호
from collections import deque

class Place :
    def __init__(self, size):
        self.cell = [[0]*size for _ in range(size)]
        self.trace = []

    ## 각도에 따른 회전 함수
    def rotate(self, center, angle):
        ## copy
        new_place = Place(len(self.cell))
        new_place.cell = [row[::] for row in self.cell]

        y, x = center
        edge_offset = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        for edge in range(4) :
            l = edge*2
            m = l + 1
            r = (m + 1) % len(edge_offset)

            gap_l = (l+(angle*2))%len(edge_offset)
            gap_m = (gap_l + 1) %len(edge_offset)
            gap_r = (gap_m + 1) % len(edge_offset)

            l_offset, nl_offset = edge_offset[l], edge_offset[gap_l]
            m_offset, nm_offset = edge_offset[m], edge_offset[gap_m]
            r_offset,nr_offset  = edge_offset[r], edge_offset[gap_r]

            new_place.cell[y+nl_offset[0]][x+nl_offset[1]] = self.cell[y+l_offset[0]][x+l_offset[1]]
            new_place.cell[y+nm_offset[0]][x+nm_offset[1]] = self.cell[y+m_offset[0]][x+m_offset[1]]
            new_place.cell[y+nr_offset[0]][x+nr_offset[1]] = self.cell[y+r_offset[0]][x+r_offset[1]]

        return new_place

    # 3. trace를 열 순으로 먼저 asc, 행 순으로 desc -- space 정렬 함수
    def prioritize_pos(self):
        self.trace.sort(key=lambda y : (y[1], -y[0]))

    def scan(self):
        for y in range(len(self.cell)) :
            for x in range(len(self.cell)) :
                if self.cell[y][x] != 0 :
                    trace = self.bfs((y,x))
                    if len(trace) >=3 :
                        for t_y,t_x in trace :
                            self.cell[t_y][t_x] =0
                            self.trace.append((t_y,t_x))
        return len(self.trace)

    def bfs(self, start):
        q = deque([start])
        visited = [[False]*len(self.cell) for _ in range(len(self.cell))]
        offset = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        trace = []
        while q :
            y,x = q.popleft()
            visited[y][x] = True
            trace.append((y,x))
            num = self.cell[y][x]
            for off_y, off_x in offset :
                new_y, new_x = y+off_y, x+off_x
                if self.is_inbound((new_y, new_x)) and self.cell[new_y][new_x] == num and not visited[new_y][new_x]:
                    q.append((new_y,new_x))

        return trace

    def is_inbound(self, pos):
        y,x = pos
        return 0<=x<len(self.cell) and 0<=y<len(self.cell)

    def display(self):
        for row in self.cell :
            for cell in row :
                print(f"{cell:<5}", end="")
            print()

        print(f"trace : {self.trace}, size : {len(self.trace)}")

def get_input() :
    return list(map(int,input().split()))

def solution() :
    max_y = 5
    min_y = 3

    # input
    [K, M] = get_input()
    space = Place(max_y)
    for i in range(max_y) :
        space.cell[i] = get_input()
    wall = deque(get_input())

    for turn in range(K) :
        max_place = None
        max_val = 0
        for rotate in range(1,4) :
            for x in range(1,1+min_y) :
                for y in range(1,1+min_y) :

                    new_space = space.rotate((y,x), rotate)
                    new_val = new_space.scan()

                    if max_val < new_val :
                        max_val= new_val
                        max_place = new_space

        if max_place is None : break
        max_place.prioritize_pos()
        turn_total = max_val

        while True :
            q = deque(max_place.trace)
            max_place.trace = []

            while q :
                y, x =  q.popleft()
                max_place.cell[y][x] = wall.popleft()

            extra_val = max_place.scan()
            max_place.prioritize_pos()

            if extra_val == 0 : break
            turn_total += extra_val

        print(turn_total, end=" ")
        space=max_place

if __name__ =="__main__" :
    solution()