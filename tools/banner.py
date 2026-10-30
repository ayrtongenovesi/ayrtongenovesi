"""Genera los banners pixel de los repos (SVG puro, sin fuentes externas).

Uso: python tools/banner.py <salida.svg> "<NUMERO>" "<TITULO>" "<BAJADA>" "<ESTADO>"
"""
import sys

FONT = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    "-": ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    ".": ["     ", "     ", "     ", "     ", "     ", "     ", "  #  "],
    ",": ["     ", "     ", "     ", "     ", "     ", "  #  ", " #   "],
    "·": ["     ", "     ", "     ", "  #  ", "     ", "     ", "     "],
    " ": ["     "] * 7,
}

AZUL, VERDE, AMARILLO, BLANCO = "#1d24ff", "#98ff2d", "#ffe600", "#ffffff"
W, H = 1200, 300


def texto(s, x, y, px, color):
    """Dibuja el texto con rectángulos de px de lado; devuelve (svg, ancho)."""
    rects, cx = [], x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for fila, linea in enumerate(glyph):
            for col, c in enumerate(linea):
                if c == "#":
                    rects.append(f'<rect x="{cx + col * px}" y="{y + fila * px}" width="{px}" height="{px}"/>')
        cx += 6 * px
    return f'<g fill="{color}">{"".join(rects)}</g>', cx - x - px


def banner(numero, titulo, bajada, estado):
    grilla = "".join(f'<line x1="{i}" y1="0" x2="{i}" y2="{H}"/>' for i in range(0, W, 40))
    grilla += "".join(f'<line x1="0" y1="{j}" x2="{W}" y2="{j}"/>' for j in range(0, H, 40))
    num, _ = texto(numero, 60, 52, 6, AMARILLO)
    tit, ancho = texto(titulo, 60, 120, 11, VERDE)
    if ancho > W - 120:  # si no entra, achica el píxel
        tit, _ = texto(titulo, 60, 128, 8, VERDE)
    for px in (4, 3):  # la bajada también se achica si no entra
        baj, ancho = texto(bajada, 60, 228, px, BLANCO)
        if ancho <= W - 120:
            break
    _, est_ancho = texto(estado, 0, 0, 4, AZUL)
    ex = W - 60 - est_ancho
    est_svg, _ = texto(estado, ex, 52, 4, AZUL)
    etiqueta = f'<rect x="{ex - 14}" y="38" width="{est_ancho + 28}" height="56" fill="{VERDE}"/>{est_svg}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{titulo} — {bajada}" shape-rendering="crispEdges">'
            f'<rect width="{W}" height="{H}" fill="{AZUL}"/>'
            f'<g stroke="{BLANCO}" stroke-opacity="0.12" stroke-width="1">{grilla}</g>'
            f'{num}{etiqueta}{tit}{baj}</svg>')


if __name__ == "__main__":
    salida, numero, titulo, bajada, estado = sys.argv[1:6]
    with open(salida, "w", encoding="utf-8") as f:
        f.write(banner(numero, titulo, bajada, estado))
