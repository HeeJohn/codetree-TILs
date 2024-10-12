# 입력 

# 입력
# 1. 숲의 크기 R, C, 정령 수 K
# 2. 골렘 출발 열(중심) C, 골렘의 방향 정보 d [0,1,2,3](북,동,남,서)
# k-1.

# 출력 첫번째 줄에 각 정령들이 최종적으로 위치한 행의 총합을 출력하세요.

# 특이사항
# 골렘이 최대한 남쪽으로 이동해도 맵을 벗어나는 경우 맵 초기화, 해당 정령 카운트 x

# 처리
# 입력 받는 함수
# 맵의 크기, 골렘 개수 저장
# 골렘 생성, 맵 생성 함수

# 맵 생성 객체 2차원 배열
# 1. 생성자(맵 초기화)
# 2. 정렬 위치 기록

# 3. 출구가 다른 골렘에 연결되어 있는 경우 타고 가되, visited 골렘 설정. (루프 방지)
# 4. 현재 골렘의 가장 아랫 부분과 탐색을 건너간 골렘의 하단 부분을 그래프로 비교, 탐색
# 5. 골렘의 중심점이 2행보다 작으면 1 호출.

# 골렘 구조 생성
#  1. (객체화) 중심, 방향
#  2. 움직일 수 있는지 판단하는 메소드
#  3. 출구를 회전하는 메소드
from enum import Enum
from collections import deque

class Map :
    def __init__(self, R, C, answer = 0):
        self.map = [[0]*C for _ in range(R)] # 위로 3칸 여유
        self.answer = answer
        self.offset = {
            "N" : (-1,0), "E" :  (0,1), "S" : (1, 0), "W" :(0,-1)
        }

    def is_inbound(self, pos) :
        y,x = len(self.map)-1, len(self.map[0])-1
        if y >= pos[0] >= 0 and x >= pos[1] >= 0 : return True
        return False

    def is_pos_empty(self, pos) -> bool:
        pos_y, pos_x = pos
        for y,x in self.offset.values() :
            new_y, new_x = pos_y+y, pos_x+x
            if not self.is_inbound((new_y, new_x)) or  self.map[new_y][new_x] > 0 : return False
        return True

    def mark_golam(self, pos, gate) -> None:
        y, x = pos
        if y-1 < 3 :
            # print("\n\n\n\n\n =======reset=========")
            self.__init__(len(self.map), len(self.map[0]),self.answer)
            return

        for dir in self.offset :
            off_y, off_x = self.offset[dir]
            if dir == gate : self.map[y+off_y][x+off_x] = 2
            else : self.map[y+off_y][x+off_x] = 1

        self.map[y][x] = 3
        self.answer += self.bfs(pos)

    def mark_golam_t(self, pos, gate) -> None:
        y, x = pos

        for dir in self.offset:
            off_y, off_x = self.offset[dir]
            if dir == gate:
                self.map[y + off_y][x + off_x] = 2
            else:
                self.map[y + off_y][x + off_x] = 1
        self.map[y][x] = 3


    def bfs(self, start):
        y,x = start
        deepest = 1
        visited = [[False] * len(self.map[0]) for _ in range(len(self.map))]
        q = deque([(y,x)])

        while q :
            curr_y, curr_x = q.popleft()

            for off_y, off_x in self.offset.values() :
                new_y, new_x = curr_y + off_y, curr_x + off_x

                # 맵에서 벗어나는지
                # 방문한 곳인지
                # 출구가 맞는지 -> 다른 골렘으로 갈 수 있음
                # 골렘 내부인지 -> 내부로는 이동 가능
                # 1- > 3 : o
                # 1 -> 1 : x
                # 2,3은 아무 데나 o
                if new_y > 2 and self.is_inbound((new_y, new_x)) and not visited[new_y][new_x]   :

                    if self.map[curr_y][curr_x]  == 1 :
                        if self.map[new_y][new_x] == 3:
                            visited[new_y][new_x] = True
                            deepest = max(deepest, new_y)
                            # print(f"x,y : {x},{y}")
                            q.append((new_y, new_x))
                    elif self.map[curr_y][curr_x]  > 1 :
                        visited[new_y][new_x] = True
                        deepest = max(deepest, new_y)
                        # print(f"x,y : {x},{y}")
                        q.append((new_y, new_x))

        # print(deepest-2)
        return deepest -2 # 첫 행이 1이고, +3 했던 것을 고려


    def show_map(self):
        for i, row in enumerate(self.map) :
            if i == 3 : print("--------------------------")
            for col in row :
                print(f"{col:>5}", end="")
            print()

# 골렘 구조 생성
#  1. (객체화) 중심, 방향
#  2. 움직일 수 있는지 판단하는 메소드
#  3. 출구를 회전하는 메소드
class Golam :
    class Gate(Enum):
        N = 0
        E = 1
        S = 2
        W = 3

    def __init__(self, center, dir : Gate):
        self.center = (0, center)
        self.dir = dir
        self.temp_center = (0,0)

    def spin(self, clockwise):
        if clockwise : self.dir = self.Gate((self.dir.value + 1)%4)
        else : self.dir = self.Gate((self.dir.value -1) % 4)

    def move_if_possible(self, map) -> bool:
        gate = Golam.Gate
        actions = {
            self.Gate.E: lambda: self.w_or_e_action(map, map.offset["E"]),
            self.Gate.S: lambda: self.south_action(map, False),
            self.Gate.W: lambda: self.w_or_e_action(map, map.offset["W"]),
        }

        for d in [gate.S, gate.W, gate.E] :
            if actions[d]()  :
                # self.show_golam(map)
                if d == gate.W : self.spin(False)
                elif d == gate.E : self.spin(True)

                return True
        # self.show_golam(map)
        return False

    def w_or_e_action(self, map : Map, offset):
        y, x = self.center
        off_y, off_x = offset
        new_pos = [y+off_y, off_x+x]

        if not map.is_pos_empty(new_pos) : return False
        self.temp_center = new_pos
        return self.south_action(map,True)

    def south_action(self, map :Map, after : bool):
        y, x = self.center
        if after : y, x = self.temp_center
        off_y, off_x = map.offset['S']
        south_pos = [y + off_y, x+ off_x]
        if not map.is_pos_empty(south_pos):
            return False
        self.center = (south_pos[0], south_pos[1])
        return True

    def show_golam(self, map):
        print("\n\n")
        temp_map = Map(len(map.map), len(map.map[0]))

        for i, row in enumerate(map.map) :
            for j, col in enumerate(row) :
                temp_map.map[i][j] = col

        temp_map.mark_golam_t(self.center,self.dir.name)
        temp_map.show_map()

        # print(f"center : {self.center}, gate : {self.dir}\n\n\n\n\n")

    def set_golam(self, map) :
        map.mark_golam(self.center, self.dir.name)

def solution() :
    [R, C, K] = list(map(int, input().split())) # 입력 함수

    m = Map(R+3,C)

    for k in range(K) :
        [c, d] = list(map(int, input().split()))
        golam = Golam(c-1, Golam.Gate(d))
        while golam.move_if_possible(m): pass
        golam.set_golam(m)
        # m.show_map()
    print(m.answer)

if __name__ =="__main__" :
    solution()