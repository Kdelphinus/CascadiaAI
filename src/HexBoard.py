from collections import defaultdict, deque
from math import sqrt

from Token import Token


class HexBoard:
    def __init__(self, tokens: dict[str, list[Token]], threshold: float = 150.0):
        """
        육각형 격자에서 토큰들의 위치를 저장하고, 탐색이 가능하도록 인접 리스트 생성.

        Args:
            tokens (dict[str, list[Token]]): 토큰 분류 결과
            threshold (float): 인접 판별 거리 기준 (기본값: 150)
        """
        self.tokens = {}  # (q, r) 좌표를 key로 사용
        self.adjacency_list = defaultdict(list)  # 인접 리스트 저장
        self.threshold = threshold  # 거리 기준

        # 토큰을 (q, r) 좌표로 변환하여 저장
        self._map_tokens(tokens)
        self._build_graph()

    def _map_tokens(self, tokens: dict[str, list[Token]]):
        """토큰의 중심점을 기반으로 육각형 좌표 시스템 (q, r) 을 할당"""
        for category in tokens.values():
            for token in category:
                q, r = self._convert_to_hex_coord(
                    token.center
                )  # 중심점을 육각형 좌표로 변환
                self.tokens[(q, r)] = token

    @staticmethod
    def _convert_to_hex_coord(center: list[float]) -> tuple[int, int]:
        """토큰의 중심점을 기반으로 (q, r) 육각형 격자 좌표를 계산"""
        x, y = center
        q = round(x / 150)  # 대략적인 x 위치를 q로 변환
        r = round(y / 130)  # 대략적인 y 위치를 r로 변환
        return q, r

    @staticmethod
    def _calculate_distance(token1: Token, token2: Token) -> float:
        """두 토큰의 중심점 간의 거리 계산"""
        x1, y1 = token1.center
        x2, y2 = token2.center
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _build_graph(self):
        """인접한 토큰들끼리 그래프 연결"""
        directions = [
            (1, 0),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (0, -1),
            (1, -1),
        ]  # 육각형의 6방향

        for (q, r), token in self.tokens.items():
            for dq, dr in directions:
                neighbor_q, neighbor_r = q + dq, r + dr
                neighbor = self.tokens.get((neighbor_q, neighbor_r))

                if (
                    neighbor
                    and self._calculate_distance(token, neighbor) <= self.threshold
                ):
                    self.adjacency_list[(q, r)].append((neighbor_q, neighbor_r))

    def get_neighbors(self, q: int, r: int) -> list[tuple[int, int]]:
        """특정 토큰의 (q, r) 좌표를 기반으로 이웃 토큰 목록 반환"""
        return self.adjacency_list.get((q, r), [])

    def display_graph(self):
        """토큰 간 인접 관계 출력"""
        for (q, r), neighbors in self.adjacency_list.items():
            token = self.tokens[(q, r)]
            neighbor_coords = [(nq, nr) for nq, nr in neighbors]
            print(f"{token.name} ({q}, {r}) -> {neighbor_coords}")

    class HexBoard:
        def __init__(self):
            self.tokens = {}  # (q, r) 좌표를 키로 하고 Token 객체를 값으로 저장

    def add_token(self, q: int, r: int, token: Token):
        """보드에 토큰 추가"""
        self.tokens[(q, r)] = token

    def __str__(self):
        """육각형 그리드 형태로 보드를 문자열로 변환"""
        if not self.tokens:
            return "Empty HexBoard"

        # q, r 좌표의 최소/최대값 구하기
        min_q = min(q for q, _ in self.tokens)
        max_q = max(q for q, _ in self.tokens)
        min_r = min(r for _, r in self.tokens)
        max_r = max(r for _, r in self.tokens)

        # 보드 출력 문자열 만들기
        board_str = ""
        for r in range(min_r, max_r + 1):
            row_str = " " * abs(r - min_r)  # r 값에 따라 들여쓰기 조절
            for q in range(min_q, max_q + 1):
                if (q, r) in self.tokens:
                    token = self.tokens[(q, r)]
                    row_str += token.name[0].upper() + " "  # 토큰의 첫 글자만 출력
                else:
                    row_str += ". "  # 빈 자리
            board_str += row_str.rstrip() + "\n"  # 오른쪽 공백 제거 후 줄 바꿈

        return board_str.strip()
