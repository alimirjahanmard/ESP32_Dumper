#include <SPI.h>

#define FLASH_SIZE_BYTES (64 * 1024) 
#define SPI_SPEED 1000000                   
#define BUFFER_SIZE 1024
uint8_t buffer[BUFFER_SIZE];

enum State {
  WAIT_FOR_MISO,
  WAIT_FOR_MOSI,
  WAIT_FOR_CLK,
  WAIT_FOR_CS,
  WAIT_FOR_COMMAND,
  IDLE
};

State currentState = IDLE;
int pins[4];

void startNewSession() {
  Serial.println();
  Serial.println("=== Universal SPI Dumper Ready ===");
  Serial.print("Enter MISO pin: ");
  currentState = WAIT_FOR_MISO;
}

void dumpExternalFlash(int miso_pin, int mosi_pin, int sck_pin, int cs_pin) {
  SPI.end();
  SPI.begin(sck_pin, miso_pin, mosi_pin, -1);
  
  pinMode(cs_pin, OUTPUT);
  digitalWrite(cs_pin, HIGH);
  
  SPI.beginTransaction(SPISettings(SPI_SPEED, MSBFIRST, SPI_MODE0));
  
  Serial.println("READY_FOR_STREAM");
  
  for (uint32_t addr = 0; addr < FLASH_SIZE_BYTES; addr += BUFFER_SIZE) {
    digitalWrite(cs_pin, LOW);
    SPI.transfer(0x03); 
    SPI.transfer((addr >> 16) & 0xFF);
    SPI.transfer((addr >> 8) & 0xFF);
    SPI.transfer(addr & 0xFF);
    SPI.transferBytes(NULL, buffer, BUFFER_SIZE);
    digitalWrite(cs_pin, HIGH);
    
   
    Serial.write(buffer, BUFFER_SIZE);
    Serial.flush(); 
  }
  
  SPI.endTransaction();
  SPI.end();
}

void setup() {
  Serial.begin(921600);
  delay(500);
  startNewSession();
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() == 0) {
      startNewSession();
      return;
    }

    
    switch (currentState) {
      case WAIT_FOR_MISO:
        pins[0] = input.toInt();
        Serial.print("Enter MOSI pin: ");
        currentState = WAIT_FOR_MOSI;
        break;
        
      case WAIT_FOR_MOSI:
        pins[1] = input.toInt();
        Serial.print("Enter CLK pin: ");
        currentState = WAIT_FOR_CLK;
        break;
        
      case WAIT_FOR_CLK:
        pins[2] = input.toInt();
        Serial.print("Enter CS pin: ");
        currentState = WAIT_FOR_CS;
        break;
        
      case WAIT_FOR_CS:
        pins[3] = input.toInt();
        Serial.print("All pins set. Send 'DUMP' to start: ");
        currentState = WAIT_FOR_COMMAND;
        break;
        
      case WAIT_FOR_COMMAND:
        input.toUpperCase();
        if (input == "DUMP") {
          Serial.println("STARTING");
          dumpExternalFlash(pins[0], pins[1], pins[2], pins[3]);
          startNewSession();
        } else {
          Serial.println("Invalid command. Restarting...");
          startNewSession();
        }
        break;
        
      case IDLE:
        break;
    }
  }
}
