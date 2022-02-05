from PIL import Image, ImageDraw


def board(num, size):
    x = size * num
    y = size * num
    im = Image.new('RGB', (x, y), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(0, x, size):
        if i % (size * 2) == 0:
            for j in range(0, y, size):
                if j % (size * 2) == 0:
                    draw.rectangle([i, j, i + size - 1, j + size - 1], fill='black', width=0)
        else:
            for j in range(size, y, size):
                if j % (size * 2) != 0:
                    draw.rectangle([i, j, i + size - 1, j + size - 1], fill='black', width=0)
    im.save('res.png', 'PNG')
