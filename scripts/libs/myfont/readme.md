## run

    otf2bdf -o converted_16_s3.bdf -p 16 -c 3 CircularStd-Book.otf

## explanation

    STARTCHAR 0046
    ENCODING 70       # ord("F")
    SWIDTH 565 0      # source width
    DWIDTH 10 0       # destination width
    BBX 8 14 2 0      # w h space_left space_bottom
    BITMAP
    FF # print bin(int("FF", 16))[2:]
    FF
    C0
    C0
    C0
    C0
    FF
    FF
    C0
    C0
    C0
    C0
    C0
    C0
    ENDCHAR

    # inverse
    # hex(int("11111111",2))[2:]

## Correction

    before:
      1011110011110000
      1110111110111000
      1100011100011000
      1000001000011000
      1000001000011000
      1000001000011000
      1000001000011000
      1000001000011000
      1000001000011000
      1000001000011000

    after:
      1111011111101110
      1110001111000110
      1100000110000110
      1100000110000110
      1100000110000110
      1100000110000110
      1100000110000110
      1100000110000110
      1100000110000110
