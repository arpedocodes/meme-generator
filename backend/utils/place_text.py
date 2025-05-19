import cv2
import numpy as np
from typing import Tuple, List

def wrap_text(text: str, font, font_scale, thickness, max_width) -> List[str]:
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        (line_width, _), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def put_text_in_rectangle(
    image: np.ndarray,
    text: str,
    top_left: Tuple[int, int],
    bottom_right: Tuple[int, int],
    font=cv2.FONT_HERSHEY_SIMPLEX,
    text_color=(255, 255, 255),
    stroke_color=(0, 0, 0),
    thickness=2,
    stroke_thickness=4,
    padding=0.9,
):
    x1, y1 = top_left
    x2, y2 = bottom_right
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    rect_w = x2 - x1
    rect_h = y2 - y1

    font_scale = 1.0
    line_spacing = 5  # spacing between lines

    while True:
        lines = wrap_text(text, font, font_scale, thickness, rect_w * padding)
        line_heights = [cv2.getTextSize(line, font, font_scale, thickness)[0][1] for line in lines]
        total_text_height = sum(line_heights) + (len(lines) - 1) * line_spacing

        if total_text_height > rect_h * padding:
            font_scale *= 0.95
        else:
            break

    # Compute vertical start point
    current_y = y1 + (rect_h - total_text_height) // 2 + line_heights[0]

    for line in lines:
        (line_w, line_h), baseline = cv2.getTextSize(line, font, font_scale, thickness)
        text_x = x1 + (rect_w - line_w) // 2
        text_y = current_y

        # Stroke
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    cv2.putText(image, line, (text_x + dx, text_y + dy), font, font_scale, stroke_color, stroke_thickness, cv2.LINE_AA)

        # Main text
        cv2.putText(image, line, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)
        current_y += line_h + line_spacing

    return font_scale


if __name__ == "__main__":
    # Example usage
    image = cv2.imread(r"C:\AI EVO (Journey)\Ai Agents\meme-generator\backend\server\data\375f3bb7-1e56-4eef-9ab9-994a6e294aa9_annotated.png")
    put_text_in_rectangle(
        image,
        '''Me explaining why I' need to nap after doing absolutely nothing all day''',
        (132, 111),
        (313, 221),
        text_color=(255, 0, 0),
        stroke_color=(0, 255, 0),
        thickness=2,
        stroke_thickness=4,
    )
    cv2.imshow("Image with Text", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()