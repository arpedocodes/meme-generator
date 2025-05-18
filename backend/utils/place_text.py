import cv2

def put_text_in_rectangle(
    image,
    text,
    top_left,
    bottom_right,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    text_color=(255, 255, 255),
    stroke_color=(0, 0, 0),
    thickness=2,
    stroke_thickness=4,
    padding=0.9,
):
    x1, y1 = top_left
    x2, y2 = bottom_right

    # Normalize coordinates
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    rect_w = x2 - x1
    rect_h = y2 - y1

    # Find best font scale to fit width and height
    font_scale = 1.0
    while True:
        (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        if text_w > rect_w * padding or (text_h + baseline) > rect_h * padding:
            font_scale *= 0.95  # Reduce font size slightly
        else:
            break

    # Center the text in the rectangle
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = x1 + (rect_w - text_w) // 2
    text_y = y1 + (rect_h + text_h) // 2 - baseline

    # Stroke text
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                cv2.putText(image, text, (text_x + dx, text_y + dy), font, font_scale, stroke_color, stroke_thickness, cv2.LINE_AA)

    # Main text
    cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)

    return font_scale

if __name__ == "__main__":
    # Example usage
    image = cv2.imread("example.jpg")
    put_text_in_rectangle(
        image,
        "Hello, World!",
        (50, 50),
        (300, 150),
        text_color=(255, 0, 0),
        stroke_color=(0, 255, 0),
        thickness=2,
        stroke_thickness=4,
    )
    cv2.imshow("Image with Text", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()