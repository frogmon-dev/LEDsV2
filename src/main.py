from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
import time
from frogmon.uCommon     import COM
from frogmon.uGlobal     import GLOB

# 매트릭스 설정
options = RGBMatrixOptions()
options.rows = 32  # 패널의 행 수
options.cols = 64  # 패널의 열 수
options.chain_length = 1  # 체인으로 연결된 패널 수
options.parallel = 1  # 병렬로 연결된 체인 수
options.hardware_mapping = 'adafruit-hat'  # GPIO 매핑

# 이미지 함수
def getImage(path):
    image = Image.open(path)
    image = image.resize((16, 16))
    return image.convert('RGB')    

matrix = RGBMatrix(options=options)

# 텍스트 설정
font = graphics.Font()
font.LoadFont("/home/pi/LEDsV2/fonts/gulim_8.bdf")  # 사용할 폰트 경로

timeFont = graphics.Font()
timeFont.LoadFont("/home/pi/LEDsV2/fonts/gulim.bdf")  # 사용할 폰트 경로

temp_text_color = graphics.Color(255, 0, 0)  # 빨간색 텍스트
humi_text_color = graphics.Color(0, 0, 255)  # 파란색 텍스트

time_text_color = graphics.Color(255, 255, 0)  # 노란색 텍스트


pos = matrix.width  # 텍스트 시작 위치 (오른쪽 끝)
message = "안녕하세요!"

imgTemp  = getImage('/home/pi/LEDsV2/bin/images/temp.png')
imgHumi  = getImage('/home/pi/LEDsV2/bin/images/humi.png')
imgTimer = getImage('/home/pi/LEDsV2/bin/images/timer.png')

configFileNM = COM.gHomeDir + COM.gSetupFile
sensor_id = GLOB.readConfig(configFileNM, 'SENSOR', 'id', '0')

strTemp = '--°C'
strHumi = '--%'
try:
    while True:        
        dicData = GLOB.loadJsonFileToDic(COM.gJsonDir+sensor_id+'.json')
        if not dicData:  # 데이터가 비어 있는 경우
            print("Error: No valid data found.")
            strTemp = '--°C'
            strHumi = '--%'
        else:
            strTemp = '%2d°C' % dicData.get('out_temperature', 99)
            strHumi = '%2d%%' % dicData.get('out_humidity', 0)
                
        GLOB.setUpdateTime()
        
        matrix.SetImage(imgTimer, 0, 0)  # 이미지 위치 (0, 0)
        graphics.DrawText(matrix, font, 16, 11, time_text_color, '현재시각')  # 텍스트 출력
        graphics.DrawText(matrix, timeFont, 5, 28, temp_text_color, COM.gStrTime)  # 텍스트 출력
        
        time.sleep(4.5)  # 50ms 대기
        matrix.Clear()  # 화면 초기화
        # 온도 습도
        matrix.SetImage(imgTemp, 0, 0)  # 이미지 위치 (0, 0)
        graphics.DrawText(matrix, font, 14, 11, temp_text_color, '온도:')  # 텍스트 출력
        graphics.DrawText(matrix, font, 40, 12, temp_text_color, strTemp)  
        matrix.SetImage(imgHumi, 0, 16)  # 이미지 위치 (0, 0)
        graphics.DrawText(matrix, font, 14, 27, humi_text_color, '습도:')  # 텍스트 출력
        graphics.DrawText(matrix, font, 40, 28, humi_text_color, strHumi)  # 텍스트 출력
        
        time.sleep(4.5)  # 50ms 대기
        matrix.Clear()  # 화면 초기화
        
except KeyboardInterrupt:
    print("종료합니다.")
    matrix.Clear()

