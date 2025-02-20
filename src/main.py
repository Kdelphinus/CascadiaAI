from HexBoard import HexBoard
from Token import TokenClassification


def bfs_find_pattern(
    board: HexBoard, start: tuple[int, int], pattern: list[tuple[int, int]]
) -> bool:
    """
    BFS를 사용해 주어진 시작점에서 같은 종류의 토큰이 특정 패턴을 이루는지 확인.

    Args:
        board (HexBoard): 육각형 보드
        start (tuple[int, int]): 시작할 토큰의 (q, r) 좌표
        pattern (list[tuple[int, int]]): 찾고 싶은 패턴 (상대 좌표)

    Returns:
        bool: 패턴이 존재하면 True, 아니면 False
    """
    if start not in board.tokens:
        return False

    start_token = board.tokens[start]
    target_class = start_token.name  # 시작 토큰의 종류

    # 패턴이 성립하는지 확인
    for dq, dr in pattern:
        neighbor_pos = (start[0] + dq, start[1] + dr)
        if (
            neighbor_pos not in board.tokens
            or board.tokens[neighbor_pos].name != target_class
        ):
            return False

    return True  # 패턴이 존재함


def find_diamond_patterns(board: HexBoard):
    """
    전체 보드를 순회하면서 마름모 패턴이 존재하는지 확인.
    """
    diamond_pattern = [(0, 0), (1, -1), (1, 0), (0, 1)]
    found_patterns = []

    for token_pos in board.tokens.keys():
        if bfs_find_pattern(board, token_pos, diamond_pattern):
            found_patterns.append((token_pos, board.tokens[token_pos].name))

    if found_patterns:
        print("🔹 마름모 패턴 발견! 🔹")
        for pos, token_class in found_patterns:
            print(f"- {token_class} 토큰이 ({pos[0]}, {pos[1]}) 위치에서 패턴을 형성함")
    else:
        print("❌ 마름모 패턴이 없습니다.")


if __name__ == "__main__":
    classifier = TokenClassification()
    classifier.show_image("../image/test3.jpeg", 0.7)

    # tokens, pine_cone_token = classifier.run("../image/test3.jpeg")
    #
    # # 육각형 보드 생성
    # board = HexBoard(tokens, threshold=150)
    # print(board)
    # print(f"솔방울 토큰 개수: {pine_cone_token}")
    #
    # # 실행
    # find_diamond_patterns(board)
