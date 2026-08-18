# ESP32_Dumper
ESP32_Dumper
A simple tool that converts your ESP32 into an SPI flash reader.<br>

Hello! 👋

**Introduction**<br>
If you do not have a dedicated hardware programmer like the CH341A and you need to read an SPI flash memory chip, you can use this project instead!

**Requirements** <br>
- ESP32 development board.<br>
- Python 3.x installed on your PC.<br>
- pyserial library installed. <br>

You can install it using:<br>
```
pip install pyserial
```
**How to Use Step-by-Step** <br>
1. **Flash the ESP32**

- Open the Arduino IDE.
- Load the sketch from ESP32_Dumper/ESP32/dumper_client/dumper_client.ino.
- Adjust the #define FLASH_SIZE_BYTES at the top of the file to match the size of your SPI flash chip.
- Upload the code to your ESP32.
<br>

2. **Connect the Hardware**<br>

Connect your ESP32 to the target SPI flash chip using jumper wires. You can choose any GPIO pins you want.


|   SPI Flash Pin   |   ESP32 GPIO Pin   |
| ----------------- | ------------------ |
| MISO (DO)	    | Your chosen MISO Pin   |
| MOSI (DI)	    | Your chosen MOSI Pin   |
| CLK (SCK)	    | Your chosen CLK Pin    |
| CS (CS)	      | Your chosen CS Pin     |
| VCC           |	3.3V                   |
| GND	          | GND                    |

<br>

<img width="224" height="119" alt="components_8pin_spi" src="https://github.com/user-attachments/assets/ede52172-4e94-4c04-ac10-dcfe113525b1" />
**standard SPI Flash Pinout**

>[!WARNING]
>Make sure the SPI flash chip is powered with 3.3V, not 5V!

<br>

**3. Run the Python Host Script**<br>

- Open your terminal or command prompt.
- Navigate to the folder containing your Python script (ESP32_Dumper/PC).
- Run the host script:
```
python dumper_host.py
```
<br>

**4. Provide the Inputs**<br>

The script will ask you for configuration step-by-step. Enter the values and press Enter:
```
enter serial port>> "/dev/ttyUSB0" or if you are using windows write "COMX" like COM1
Connected to /dev/ttyUSB0 
MISO_Pin>> 19
MOSI_Pin>> 23
CLK(SCK)_Pin>> 18
CS_Pin>> 5
Enter output filename>> flash_dump.bin

Waiting for DUMP_START signal...

DUMP_START

Receiving data -> flash_dump.bin...
Received: 4194304 bytes

Dump complete! Saved 4194304 bytes.
Serial port closed.
```
<br>

**5. Done!**<br>
The script will communicate with the ESP32, start the dump, and save the binary data directly to your specified output file.
<br>
**Tadaaa!** 👍 Your SPI flash is now dumped and ready for analysis!
