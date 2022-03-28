from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


def generate_art(path):
    print("Generating Art")
    target_size_px = 256
    scale_factor = 2
    image_size_px = target_size_px * scale_factor
    # image_size_px = 128
    image_bg_color = (0, 0, 0)
    padding_px = 10 * scale_factor
    thickness = 1
    image = Image.new("RGB", (image_size_px, image_size_px),
                      image_bg_color)  # in memory

    # Generating points
    points = []
    num_lines = 10
    draw = ImageDraw.Draw(image)
    for _ in range(num_lines):
        random_point = (random.randint(0, image_size_px - padding_px),
                        random.randint(0, image_size_px - padding_px))
        points.append(random_point)

    # Center image.
    # Find the bounding box.
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    # Find offsets.
    x_offset = (min_x - padding_px) - (image_size_px - padding_px - max_x)
    y_offset = (min_y - padding_px) - (image_size_px - padding_px - max_y)

    # Move all points by offset.
    for i, point in enumerate(points):
        points[i] = (point[0] - x_offset // 2, point[1] - y_offset // 2)

    # Drawing lines
    n_points = len(points) - 1
    for i, point in enumerate(points):
        overlay_image = Image.new("RGB", (image_size_px, image_size_px),
                                  image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)
        p1 = point
        if (i == len(points) - 1):
            p2 = points[0]
        else:
            p2 = points[i + 1]
        line_xy = (p1, p2)
        start_color = random_color()
        end_color = random_color()
        factor = i/n_points
        line_color = interpolate(start_color, end_color, factor)
        print("E", line_color)

        thickness += scale_factor
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size_px, target_size_px),
                         resample=Image.ANTIALIAS)
    image.save(path)


def random_color():

 # I want a bright, vivid color, so max V and S and only randomize HUE.
    h = random.random()
    s = 1
    v = 1

    float_rbg = colorsys.hsv_to_rgb(h, s, v)

    # Return as integer RGB.
    return (
        int(float_rbg[0] * 255),
        int(float_rbg[1] * 255),
        int(float_rbg[2] * 255),
    )
    # float_rbg = (random.randint(0, 255), random.randint(
    #     0, 255), random.randint(0, 255))
    # return float_rbg


def interpolate(start_color, end_color, factor: float):
    # Find the color that is exactly factor (0.0 - 1.0) between the two colors.
    return (int(factor * end_color[0] + (1 - factor) * start_color[0]), int(factor * end_color[1] + (1 - factor) * start_color[1]), int(factor * end_color[1] + (1 - factor) * start_color[1]))


if __name__ == "__main__":
    for i in range(10):
        generate_art(f"test_image_{i}.png")
