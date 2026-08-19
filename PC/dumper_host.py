import serial
import time
import sys

TOTAL_SIZE = 2 * 1024 * 1024  # 2MB Flash
BAUD_RATE = 921600

def wait_for_prompt(ser, prompt_text):
    """منتظر دریافت متن پرامپت از سمت میکرو می‌ماند"""
    buffer = b""
    target = prompt_text.encode('utf-8')
    while target not in buffer:
        ch = ser.read(1)
        if not ch:
            raise TimeoutError(f"Timeout waiting for: {prompt_text}")
        buffer += ch
    # چاپ آنچه تا کنون دریافت شده
    print(buffer.decode(errors='ignore'), end="")
    sys.stdout.flush()

def main():
    port = input("Enter serial port (e.g. COM3 or /dev/ttyUSB0): ").strip()
    miso = input("MISO Pin: ").strip()
    mosi = input("MOSI Pin: ").strip()
    clk  = input("CLK (SCK) Pin: ").strip()
    cs   = input("CS Pin: ").strip()
    filename = input("Enter output filename (e.g. flash_dump.bin): ").strip()

    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=5)
        print(f"Connecting to {port}...")
        
        # تاخیر برای ریست شدن میکرو و پاک‌سازی بافر ورودی
        time.sleep(1.5)
        ser.reset_input_buffer()
        
        # اگر هنوز پرامپت نیامده یک اینتر بفرستیم تا میکرو تحریک شود
        ser.write(b"\n")
        
        # مراحل ارسال تنظیمات پین‌ها
        wait_for_prompt(ser, "Enter MISO pin: ")
        ser.write(f"{miso}\n".encode())
        
        wait_for_prompt(ser, "Enter MOSI pin: ")
        ser.write(f"{mosi}\n".encode())
        
        wait_for_prompt(ser, "Enter CLK pin: ")
        ser.write(f"{clk}\n".encode())
        
        wait_for_prompt(ser, "Enter CS pin: ")
        ser.write(f"{cs}\n".encode())
        
        wait_for_prompt(ser, "Send 'DUMP' to start: ")
        ser.write(b"DUMP\n")
        
        print("\nWaiting for dump stream to begin...")
        
        # منتظر سیگنال شروع استریم
        line = ser.readline()
        while b"READY_FOR_STREAM" not in line:
            if not line:
                raise TimeoutError("Device did not respond with READY_FOR_STREAM")
            line = ser.readline()
            
        print("Receiving binary data...")
        received_bytes = 0
        
        with open(filename, 'wb') as f:
            while received_bytes < TOTAL_SIZE:
                chunk_to_read = min(4096, TOTAL_SIZE - received_bytes)
                data = ser.read(chunk_to_read)
                
                if not data:
                    print("\nWarning: Read timeout occurred before full dump!")
                    break
                    
                f.write(data)
                received_bytes += len(data)
                
                percent = (received_bytes / TOTAL_SIZE) * 100
                print(f"\rProgress: {received_bytes}/{TOTAL_SIZE} bytes ({percent:.1f}%)", end="")
                sys.stdout.flush()

        print(f"\n\nDump successfully completed! Saved {received_bytes} bytes to '{filename}'.")

    except serial.SerialException as e:
        print(f"\nSerial Error: {e}")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
