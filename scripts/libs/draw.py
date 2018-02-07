# stampa sempre feld anche se è vuoto

        self.prev_word   = ""

    def print_word(self, word, canvas, prefix):

        def ll(string):
            return sum([font.CharacterWidth(ord(c)) for c in string])

        c   = 0
        font    = self.font

        margin_bottom   = 2
        margin_top      = self.matrix.height - 8
        word_length     = margin_bottom + ll("FELD" + word)
        prev_word_len   = margin_bottom + ll("FELD" + self.prev_word)
        sign            = 1 if (prev_word_len < word_length) else -1

        self.matrix.brightness = 50
        font.LoadFont("assets/fonts/4x6.bdf")

        while (c < ANIM_TIME):
            canvas.Clear()

            # line
            l = {
                "x0": margin_bottom + ll("FELD"),
                "y0": margin_top + 1,
                "x1": word_length + (int((float(abs(prev_word_len - word_length)) / ANIM_TIME) * (ANIM_TIME - c))) * sign,
                "y1": margin_top + 1,
                "color": graphics.Color(255,255,255)
            }
            graphics.DrawLine(canvas, l["x0"], l["y0"], l["x1"], l["y1"], l["color"])

            # dot
            d = {
                "x": l["x1"],
                "y": margin_top - 1,
                "col": {"r": 255, "g": 255, "b": 255}
            }
            canvas.SetPixel(d["x"], d["y"], d["col"]["r"], d["col"]["g"], d["col"]["b"])

            # feld
            f = {
                "x0": margin_bottom,
                "y0": margin_top,
                "color": graphics.Color(255,255,255)
            }
            graphics.DrawText(canvas, font, f["x0"], f["y0"], f["color"], "FELD")

            # man
            m = {
                "x0": margin_bottom + ll("FELD"),
                "y0": margin_top - int((float(5) / ANIM_TIME) * (ANIM_TIME - c)),
                "color": graphics.Color(255,255,255)
            }
            graphics.DrawText(canvas, font, m["x0"], m["y0"], m["color"], word)

            c += 1
            time.sleep(0.01)

            canvas = self.matrix.SwapOnVSync(canvas)

        self.prev_word = word


        # else:
        #     font = graphics.Font()
        #     font.LoadFont("assets/fonts/4x6.bdf")
        #     print dir(self.matrix)
        #     while True:
        #         m = {
        #             "text":     "boris",
        #             "x0":       2,
        #             "y0":       self.matrix.height,
        #             "canvas":   self.matrix.CreateFrameCanvas(),
        #             "color":    graphics.Color(255,255,255)}
        #         graphics.DrawText(m["canvas"], font, m["x0"], m["y0"], m["color"], m["text"])
        #         m["canvas"] = self.matrix.SwapOnVSync(m["canvas"])
