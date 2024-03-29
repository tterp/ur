
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time
import datetime
from time import sleep
from rpi_hardware_pwm import HardwarePWM

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 24
LCD_D5 = 25
LCD_D6 = 23
LCD_D7 = 12
TAST   = 4
LYS    = 16



# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False



LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#define pwm
pwm = HardwarePWM(pwm_channel=0, hz=1600)
pwm.start(0)


def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LYS, GPIO.OUT)
  GPIO.setup(TAST, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.output(LYS, False)
  a = False

  # Initialise display
  lcd_init()


  while True:


    ur = datetime.datetime.now()
    if ur.strftime("%a") == "Mon":
      dag(0x80,0x4D,0x61,0x6E,0x64,0x61,0x01,0xFE) # start adresse = 0x80, og derefter karakter ,0x4D,0x61,0x6E,0x64,0x61,0x01,0xFE
    if ur.strftime("%a") == "Tue":
      dag(0x80,0x54,0x69,0x72,0x73,0x64,0x61,0x01) # start adresse = 0x80, og derefter karakter ,0x54,0x69,0x72,0x73,0x64,0x61,0x01
    if ur.strftime("%a") == "Wed":
      dag(0x80,0x4F,0x6E,0x73,0x64,0x61,0x01,0xFE) # start adresse = 0x80, og derefter karakter ,0x4F,0x6E,0x73,0x64,0x61,0x01,0xFE
    if ur.strftime("%a") == "Thu":
      dag(0x80,0x54,0x6F,0x72,0x73,0x64,0x61,0x01) # start adresse = 0x80, og derefter karakter ,0x54,0x6F,0x72,0x73,0x64,0x61,0x01
    if ur.strftime("%a") == "Fri":
      dag(0x80,0x46,0x72,0x65,0x64,0x61,0x01,0xFE) # start adresse = 0x80, og derefter karakter ,0x46,0x72,0x65,0x64,0x61,0x01,0xFE
    if ur.strftime("%a") == "Sat":
      dag(0x80,0x4C,0x00,0x72,0x64,0x61,0x01,0xFE) # start adresse = 0x80, og derefter karakter ,0x4C,0x00,0x72,0x64,0x61,0x01,0xFE
    if ur.strftime("%a") == "Sun":
      dag(0x80,0x53,0x00,0x6E,0x64,0x61,0x01,0xFE) # start adresse = 0x80, og derefter karakter ,0x53,0x00,0x6E,0x64,0x61,0x01,0xFE
    f = open("tid.txt",'r')
    d = f.read(8)
    t = ur.strftime("%H:%M:%S")

    #lcd_string(d, 0x87)
    lcd_string(ur.strftime("  %d %b %Y"),0x87)
    lcd_string(ur.strftime("Klokken er %H:%M:%S") ,LCD_LINE_2)

    if t == d:
        a = True

    if a == True:
        lyd()
        GPIO.output(LYS, True)

    if GPIO.input(TAST) == GPIO.LOW:
        GPIO.output(LYS, True)
        a = False
        pwm.change_duty_cycle(0)

    if ((GPIO.input(TAST) == GPIO.HIGH) and (a == False)):
        GPIO.output(LYS, False)


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

  lcd_byte(0x40,LCD_CMD)  # saetter adr for gcram
  lcd_byte(0x00,LCD_CHR)  # vaerdi for foerste linie  karakter oe paa dansk
  lcd_byte(0x00,LCD_CHR)  # vaerdi for anden linie
  lcd_byte(0x0E,LCD_CHR)  # vaerdi for tredie linie
  lcd_byte(0x11,LCD_CHR)  # vaerdi for fjerde linie
  lcd_byte(0x15,LCD_CHR)  # vaerdi for femte linie
  lcd_byte(0x11,LCD_CHR)  # vaerdi for sjete linie
  lcd_byte(0x0E,LCD_CHR)  # vaerdi for syvende linie
  lcd_byte(0x00,LCD_CHR)  # vaerdi for ottende linie

  lcd_byte(0x48,LCD_CMD)
  lcd_byte(0x00,LCD_CHR)
  lcd_byte(0x00,LCD_CHR)
  lcd_byte(0x0F,LCD_CHR)
  lcd_byte(0x11,LCD_CHR)
  lcd_byte(0x11,LCD_CHR)
  lcd_byte(0x0F,LCD_CHR)
  lcd_byte(0x01,LCD_CHR)
  lcd_byte(0x0E,LCD_CHR)


def dag(a,b,c,d,e,f,g,h):
  lcd_byte(a, LCD_CMD)
  lcd_byte(b, LCD_CHR)
  lcd_byte(c, LCD_CHR)
  lcd_byte(d, LCD_CHR)
  lcd_byte(e, LCD_CHR)
  lcd_byte(f, LCD_CHR)
  lcd_byte(g, LCD_CHR)
  lcd_byte(h, LCD_CHR)

def lyd():
  pwm.change_duty_cycle(50)
  pwm.change_frequency(1200)
  sleep(0.1)
  pwm.change_frequency(1233)
  sleep(0.1)
  pwm.change_frequency(1266)
  sleep(0.1)
  pwm.change_frequency(1300)
  sleep(0.1)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
