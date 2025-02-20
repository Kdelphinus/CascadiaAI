import cv2
from ultralytics import YOLO


class Token:
    def __init__(
        self,
        name: str,
        center: list[float],
        size: list[float],
        left_top_corner: list[float],
        right_bottom_corner: list[float],
        confidence: float,
    ):
        """
        토큰의 정보를 저장한 객체로 모든 좌표 정보는 x,y 순서로 저장
        Args:
            name: 토큰 이름
            center: 중심점
            size: 너비와 높이
            left_top_corner: 좌상단 죄표
            right_bottom_corner: 우하단 좌표
            confidence: 신뢰도
        """
        self.name: str = name
        self.center: list[float] = center
        self.size: list[float] = size
        self.left_top_corner: list[float] = left_top_corner
        self.right_bottom_corner: list[float] = right_bottom_corner
        self.confidence: float = confidence

    def __str__(self):
        return (
            f"<토큰 정보>\n"
            f"클래스: {self.name}\n"
            f"중심점: {self.center[0]:.1f}, {self.center[1]:.1f}\n"
            f"크기: {self.size[0]:.1f} x {self.size[1]:.1f}\n"
            f"박스 좌표: 좌상단({self.left_top_corner[0]}, {self.left_top_corner[1]}), 우하단({self.right_bottom_corner[0]}, {self.right_bottom_corner[1]})\n"
            f"신뢰도: {self.confidence:.2f}"
        )


class TokenClassification:
    """
    주어진 이미지에 있는 토큰을 분류하는 객체
    """

    def __init__(self):
        self.model = YOLO("../model/cascadia_token_classification.pt", task="detect")
        self.conf_value: float = 0.7

    def run(self, image_url: str) -> (dict[str, list[Token]], int):
        """
        주어진 이미지에 있는 토큰을 식별하는 함수
        Args:
            image_url (str): 이미지 경로

        Returns:
            tokens (dict[str, list[Token]]): 각 토큰 별로 정보를 저장한 딕셔너리
            pine_cone_token (int): 솔방울 토큰 개수
        """
        results = self.model(image_url, conf=self.conf_value)
        result = results[0]
        tokens: dict[str, list[Token]] = {
            "salmon_token": [],
            "elk_token": [],
            "fox_token": [],
            "bear_token": [],
            "hawk_token": [],
            "pine_cone_token": [],
        }
        pine_cone_token: int = 0

        # 각 탐지된 객체의 정보 출력
        for box in result.boxes:
            # 박스 좌표 가져오기 (xywh 형식: 중심x, 중심y, 너비, 높이)
            x_center, y_center, width, height = box.xywh[0].tolist()

            # 신뢰도와 클래스 정보 가져오기
            confidence = box.conf.item()
            class_id = int(box.cls.item())
            class_name = result.names[class_id]

            # 박스의 왼쪽 상단, 오른쪽 하단 좌표 계산
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            if class_name == "pine_cone_token":
                pine_cone_token += 1
            else:
                tokens[class_name].append(
                    Token(
                        name=class_name,
                        center=[x_center, y_center],
                        size=[width, height],
                        left_top_corner=[x1, y1],
                        right_bottom_corner=[x2, y2],
                        confidence=confidence,
                    )
                )

        return tokens, pine_cone_token

    def show_image(self, image_url: str) -> None:
        """
        모델이 토큰을 식별한 이미지를 표시
        Args:
            image_url: 이미지 경로
        """
        results = self.model(image_url, conf=self.conf_value)
        results[0].show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
