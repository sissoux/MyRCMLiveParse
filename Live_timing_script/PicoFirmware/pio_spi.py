import rp2
from machine import Pin

# Pinout definition
pin_cs = 13
pin_sck = 10
pin_mosi = 11
pin_miso = 12

@rp2.asm_pio()
def spi_slave():
    wrap_target()
    wait(0, gpio, pin_cs)   # Wait for CS = 0
    label("daisy_chain")
    wait(0, gpio, pin_sck)  # SCK Falling Edge
    mov(osr, isr)           # IRS -> OSR
    out(pins, 1)            # OSR -> MISO
    wait(1, gpio, pin_sck)  # SCK Rising Edge
    in_(pins, 1)            # MOSI -> ISR
    jmp(pin, "end")         # Jump if CS = 1
    jmp("daisy_chain")
    label("end")
    push()                  # IRS -> RX FIFO
    irq(0)                  # IRQ SET 0
    wrap()


sm = rp2.StateMachine(0, spi_slave, out_base=Pin(pin_miso), in_base=Pin(pin_mosi), jmp_pin=Pin(pin_cs))
sm.irq(lambda p: print(f"SPI RX: {sm.get():08X}"))
sm.active(1)
