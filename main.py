from flask import Flask, request, render_template
import time
import serial

app = Flask(__name__)

ser = serial.Serial('COM3', baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE)

@app.route('/')
def index_handler():
    return render_template('Robot-Arm.html')


@app.route('/preset-action', methods=['POST'])
def preset_action_handler():
    # 执行预设动作指令
    command1 = "AA BB 60 60 60 60 90 50 CC DD"
    # 初态
    word1 = bytes.fromhex(command1)
    ser.write(word1)
    time.sleep(1)

    for i in range(1, 60):
        tmp = int(96 + i)
        command = f"AA BB 60 {tmp:02x} {tmp:02x} {tmp:02x} 90 50 CC DD"
        word = bytes.fromhex(command)
        ser.write(word)
        time.sleep(0.01)

    # AA BB 60 9c 9c 9c 90 50 CC DD
    command_open = "AA BB 60 9c 9c 9c 30 50 CC DD"
    word_open = bytes.fromhex(command_open)
    ser.write(word_open)

    time.sleep(1.5)

    command_close = "AA BB 60 9c 9c 9c 80 50 CC DD"
    word_close = bytes.fromhex(command_close)
    ser.write(word_close)

    time.sleep(1)

    command_turn = "AA BB 90 9c 9c 9c 80 50 CC DD"
    word_turn = bytes.fromhex(command_turn)
    ser.write(word_turn)

    time.sleep(1)

    command_drop = "AA BB 90 9c 9c 9c 30 50 CC DD"
    word_drop = bytes.fromhex(command_drop)
    ser.write(word_drop)

    time.sleep(0.6)

    for i in range(1, 60):
        tmp = int(156 - i)
        command = f"AA BB 90 {tmp:02x} {tmp:02x} {tmp:02x} 90 50 CC DD"
        word = bytes.fromhex(command)
        ser.write(word)
        time.sleep(0.01)

    # for i in range(1, 48):
    #     tmp = hex(i)
    #     command = "AA BB 60 90+tmp 90+tmp 90 90 50 CC DD"
    #     word = bytes.fromhex(command)
    #     ser.write(word)


    # command2 = "AA BB 60 90 90 90 90 50 CC DD"
    # # 弯腰1
    # word2 = bytes.fromhex(command2)
    # command3 = "AA BB 60 ee a1 90 30 50 CC DD"
    # # 弯腰2
    # word3 = bytes.fromhex(command3)
    # command4 = "AA BB 60 ee a1 90 80 50 CC DD"
    # word4 = bytes.fromhex(command4)
    # # 抓取
    # command5 = "AA BB 60 80 80 80 80 50 CC DD"
    # # 回收1
    # word5 = bytes.fromhex(command5)
    # command6 = "AA BB 90 80 80 80 80 50 CC DD"
    # # 转底座
    # word6 = bytes.fromhex(command6)
    # command7 = "AA BB 90 80 80 80 30 50 CC DD"
    # # 松手
    # word7 = bytes.fromhex(command7)
    # command8 = "AA BB 60 60 60 60 90 50 CC DD"
    # # 回归初态
    # word8 = bytes.fromhex(command8)
    #
    # #for i in range(1,60):
    #  #   tmp = hex(i)
    #   #  command = "AA BB 60 60 60 60 60+tmp 50 CC DD"
    #    # word = bytes.fromhex(command)
    #     #ser.write(word)
    #
    # ser.write(word1)
    # time.sleep(1)
    # ser.write(word2)
    # time.sleep(1)
    # ser.write(word3)
    # time.sleep(1)
    # ser.write(word4)
    # time.sleep(1)
    # ser.write(word5)
    # time.sleep(1)
    # ser.write(word6)
    # time.sleep(1)
    # ser.write(word7)
    # time.sleep(1)
    # ser.write(word8)
    # time.sleep(1)
    return '预设动作执行成功'

@app.route('/control', methods=['POST'])
def control_handler():
    data = request.get_json()
    joint1 = int(data['joint1'])
    joint2 = int(data['joint2'])
    joint3 = int(data['joint3'])
    joint4 = int(data['joint4'])
    joint5 = int(data['joint5'])

    command = f"AA BB {joint1:02x} {joint2:02x} {joint3:02x} {joint4:02x} {joint5:02x} 50 CC DD"
    word = bytes.fromhex(command)
    ser.write(word)
    ser.write(word)
    return '控制指令执行成功'

if __name__ == '__main__':
    app.run()
