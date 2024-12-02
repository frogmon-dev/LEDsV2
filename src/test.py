from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
import time

# 매트릭스 설정
options = RGBMatrixOptions()
options.rows = 32  # 패널의 행 수
options.cols = 64  # 패널의 열 수
options.chain_length = 1  # 체인으로 연결된 패널 수
options.parallel = 1  # 병렬로 연결된 체인 수
options.hardware_mapping = 'adafruit-hat'  # GPIO 매핑

matrix = RGBMatrix(options=options)

# 텍스트 설정
font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/gulim.bdf")  # 사용할 폰트 경로
text_color = graphics.Color(255, 0, 0)  # 빨간색 텍스트

pos = matrix.width  # 텍스트 시작 위치 (오른쪽 끝)
message = "안녕하세요!"

# PNG 이미지 불러오기
image_path = "/home/pi/LEDsV2/bin/images/humi.png"  # 사용할 이미지 경로
image = Image.open(image_path)
# 이미지 크기를 매트릭스 크기에 맞춤
image = image.resize((64, 32))  # 매트릭스 크기에 맞게 조정
# 이미지를 RGB 모드로 변환
image = image.convert('RGB')

try:
    while True:
        #matrix.Clear()  # 화면 초기화
        # 이미지를 매트릭스에 출력
        matrix.SetImage(image, 0, 0)  # 이미지 위치 (0, 0)
        
        len = graphics.DrawText(matrix, font, pos, 16, text_color, message)  # 텍스트 출력
        pos -= 1  # 텍스트 이동 (왼쪽으로 스크롤)
        
        if pos + len < 0:  # 텍스트가 화면에서 완전히 사라지면
            pos = matrix.width  # 다시 오른쪽 끝으로 이동
        
        time.sleep(0.05)  # 50ms 대기
except KeyboardInterrupt:
    print("종료합니다.")
    matrix.Clear()

