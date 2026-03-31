import serial
import time
import sys


def test_com5():
    print("=" * 60)
    print("Проверка COM5 (CP210x)")
    print("=" * 60)

    port = "COM5"
    baudrates = [9600]

    for baud in baudrates:
        print(f"\n📡 Пробуем {baud} бод...")

        try:
            ser = serial.Serial(
                port=port,
                baudrate=baud,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=2
            )

            print(f"✅ Порт COM5 открыт успешно")

            ser.reset_input_buffer()
            ser.reset_output_buffer()
            # ser.write(b'AT\r\n')

            print("⏳ Ожидание данных 5 секунд...")
            received = []
            start = time.time()

            while time.time() - start < 5:
                if ser.in_waiting > 0:
                    try:
                        data = ser.readline().decode('utf-8', errors='ignore').strip()
                        if data:
                            print(f"✅ Получено: {data}")
                            received.append(data)
                    except:
                        data = ser.read(ser.in_waiting)
                        print(f"✅ RAW: {data}")
                        received.append(data)

                time.sleep(0.1)

            ser.close()

            if received:
                print(f"\n🎉 УСПЕХ! Скорость: {baud} бод")
                print(f"📊 Получено сообщений: {len(received)}")

                monitor_com5(port, baud)
                return True
            else:
                print("❌ Нет данных")

        except serial.SerialException as e:
            print(f"❌ Ошибка Serial: {e}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    return False


def monitor_com5(port, baud):
    print(f"\n" + "=" * 60)
    print(f"📊 МОНИТОРИНГ: COM5 @ {baud} бод")
    print("=" * 60)
    print("Нажмите Ctrl+C для выхода\n")

    try:
        ser = serial.Serial(port, baud, timeout=1)

        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] {data}")
                except:
                    data = ser.read(ser.in_waiting)
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] RAW: {data}")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n⏹ Остановлено пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if 'ser' in locals():
            ser.close()


def check_pyserial():
    print("\n🔧 Проверка pyserial...")
    try:
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        print(f"✅ pyserial работает. Найдено портов: {len(ports)}")

        for port in ports:
            print(f"   {port.device} - {port.description}")

        return True
    except Exception as e:
        print(f"❌ Ошибка pyserial: {e}")
        return False


if __name__ == "__main__":

    if not test_com5():
        print("\n" + "=" * 60)
        print("⚠️  STM32 НЕ ОБНАРУЖЕН")
        print("=" * 60)

    input("\nНажмите Enter для выхода...")
