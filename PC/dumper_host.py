import serial
import time
import sys

SERIAL_PORT = input("enter serial port>>")
BAUD_RATE = 921600

def wait_for_prompt(ser, prompt):
    response = ser.read_until(prompt)
    print(response.decode(errors='ignore'), end="")
    sys.stdout.flush()

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    print(f"Connected to {SERIAL_PORT}")
    
    miso = input("MISO_Pin>>")
    mosi = input("MOSI_Pin>>")
    clk = input("CLK(SCK)_Pin>>")
    cs = input("CS_Pin>>")
    filename = input("Enter output filename>> ")
    
    wait_for_prompt(ser, b'MISO pin: ')
    ser.write(f"{miso}\n".encode())
    
    wait_for_prompt(ser, b'MOSI pin: ')
    ser.write(f"{mosi}\n".encode())
    
    wait_for_prompt(ser, b'CLK pin: ')
    ser.write(f"{clk}\n".encode())
    
    wait_for_prompt(ser, b'CS pin: ')
    ser.write(f"{cs}\n".encode())
    
    wait_for_prompt(ser, b"'DUMP' to start: ")
    ser.write(b"DUMP\n")
    print("DUMP")
    
    print("\nWaiting for DUMP_START signal...")
    header = ser.read_until(b'DUMP_START\n')
    print(header.decode(errors='ignore'))
    
    if b'DUMP_START' not in header:
        print("Error: Did not receive DUMP_START signal. Aborting.")
        sys.exit()

    with open(filename, 'wb') as f:
        print(f"Receiving data -> {filename}...")
        received_bytes = 0
        while True:
            chunk = ser.read(2048)
            if not chunk or b'DUMP_END' in chunk:
                if chunk:
                    final_data = chunk.split(b'DUMP_END')[0]
                    f.write(final_data)
                    received_bytes += len(final_data)
                break
            else:
                f.write(chunk)
                received_bytes += len(chunk)
                print(f"\rReceived: {received_bytes} bytes", end="")

    print(f"\n\nDump complete! Saved {received_bytes} bytes.")

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
