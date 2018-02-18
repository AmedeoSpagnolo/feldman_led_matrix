## run

    otf2bdf -o converted_16.bdf -p 16 CircularStd-Book.otf

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
