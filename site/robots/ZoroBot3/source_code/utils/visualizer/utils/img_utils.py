############################################################################
# 1. CONVERTIR .BMP MONOCROMÁTICO -> ARRAY HEXADECIMAL CON DIBUJO ASCII
############################################################################


from PIL import Image
import os
import glob

def bmp_to_sprite_array(bmp_path):
    """Convierte .bmp monocromático → array hexadecimal CON DIBUJO"""
    img = Image.open(bmp_path).convert('1')
    width, height = img.size
    
    sprite_array = []
    for y in range(height):
        row = 0
        for x in range(width):
            pixel = img.getpixel((x, y))
            bit = 0 if pixel == 255 else 1
            row |= (bit << (width - 1 - x))
        sprite_array.append(row)
    
    return sprite_array


############################################################################
# 2. CONVERTIR SPRITES/*.BMP -> ARRAYS HEX CON PREVIEW EN COMENTARIO
############################################################################


def row_to_ascii(row, width):
    """Convierte número → dibujo ASCII con # y ."""
    ascii_row = ""
    for x in range(width):
        bit = (row >> (width - 1 - x)) & 1
        ascii_row += "#" if bit else "."
    return ascii_row

# ========================================
# BUCLE CON DIBUJO
# ========================================
bmp_files = glob.glob("sprites/*.bmp")

for bmp_path in bmp_files:
    name = os.path.splitext(os.path.basename(bmp_path))[0].upper().replace(" ", "_")
    sprite = bmp_to_sprite_array(bmp_path)
    width, _ = Image.open(bmp_path).convert('1').size
    
    # FORMATO EXACTO + DIBUJO
    print(f"{name} = [")
    for i, row in enumerate(sprite):
        hex_row = f"0x{row:03X}"
        ascii_drawing = row_to_ascii(row, width)
        print(f"    {hex_row},  # Fila {i}: \t{ascii_drawing}")
    print("]")
    print()


############################################################################
# 3. CONVERTIR .BMP COLOR -> MATRIZ DE COLORES RGB Y
############################################################################

from PIL import Image

def bmp_to_color_matrix(bmp_path, size=12):
    img = Image.open(bmp_path).convert("RGB")
    img = img.resize((size, size), Image.NEAREST)
    pixels = img.load()
    matrix = []
    for y in range(size):
        row = []
        for x in range(size):
            row.append(pixels[x, y])  # (R, G, B)
        matrix.append(row)
    return matrix

# Ejemplo de uso:
color_matrix = bmp_to_color_matrix("zoro head.bmp", size=12)

print(color_matrix)


############################################################################
# 4. MOSTRAR MATRIZ DE COLORES RGB COMO IMAGEN
############################################################################

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from IPython.display import display

def color_matrix_to_image(color_matrix):
    """Convierte matrix → imagen y la muestra (SIN GUARDAR)"""
    img_array = np.array(color_matrix, dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # MOSTRAR x3 grande
    plt.figure(figsize=(15,15))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
    # También display normal
    display(img)
    
    return img

# Uso
color_matrix = [[(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (120, 159, 92), (255, 255, 255), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (120, 159, 92), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (119, 160, 90), (139, 186, 106), (157, 212, 121), (157, 212, 121), (139, 186, 106), (157, 212, 121), (139, 186, 106), (139, 186, 106), (157, 212, 121), (120, 159, 92), (255, 255, 255)], [(255, 255, 255), (97, 134, 79), (119, 160, 90), (157, 212, 121), (139, 186, 106), (119, 160, 90), (139, 186, 106), (139, 186, 106), (139, 186, 106), (139, 186, 106), (120, 159, 92), (255, 255, 255)], [(255, 255, 255), (97, 134, 79), (97, 134, 79), (139, 186, 106), (119, 160, 90), (139, 186, 106), (119, 160, 90), (139, 186, 106), (119, 160, 90), (235, 217, 195), (97, 134, 79), (255, 255, 255)], [(255, 255, 255), (97, 134, 79), (97, 134, 79), (119, 160, 90), (235, 217, 195), (235, 217, 195), (235, 217, 195), (139, 186, 106), (235, 217, 195), (235, 217, 195), (97, 134, 79), (255, 255, 255)], [(255, 255, 255), (97, 134, 79), (235, 217, 195), (119, 160, 90), (33, 33, 33), (33, 33, 33), (235, 217, 195), (235, 217, 195), (33, 33, 33), (33, 33, 33), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255), (235, 217, 195), (215, 191, 161), (240, 241, 223), (78, 74, 81), (215, 191, 161), (215, 191, 161), (240, 241, 223), (78, 74, 81), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255), (255, 255, 255), (195, 169, 132), (215, 191, 161), (235, 217, 195), (235, 217, 195), (235, 217, 195), (235, 217, 195), (215, 191, 161), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (174, 143, 106), (195, 169, 132), (195, 169, 132), (195, 169, 132), (195, 169, 132), (255, 255, 255), (255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]]
img = color_matrix_to_image(color_matrix)
