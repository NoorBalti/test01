import cv2
import csv
import numpy as np
import textwrap
import time

def add_word_animation_to_video(video_path, output_path, text_01, text_02, text_03, 
                                max_width=30, font_size=1.5, text_font=cv2.FONT_HERSHEY_TRIPLEX, 
                                text_color=(0, 255, 255), text_thickness=2, 
                                background_color=(0, 0, 0), left_margin=150, top_margin=40, line_space=80,
                                delay=0.1):  # Delay in seconds between writing each word
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    current_word_01 = ""
    current_word_02 = ""
    current_word_03 = ""

    word_index_01 = 0
    word_index_02 = 0
    word_index_03 = 0

    text_width = max_width

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_with_text = frame.copy()

        # Add animation for text_01 at the top
        if word_index_01 < len(text_01):
            current_word_01 += text_01[word_index_01]
            word_index_01 += 1

        wrapped_text_01 = textwrap.wrap(current_word_01, width=text_width)
        text_position_x_01 = (width - max([len(line) for line in wrapped_text_01]) * 10) // 2
        text_position_y_01 = top_margin
        text_position_x_01 -= left_margin

        for line in wrapped_text_01:
            word_width, word_height = cv2.getTextSize(line, text_font, font_size, text_thickness)[0]
            background_height = word_height + 25
            word_height += 10
            text_image = np.zeros((background_height, word_width, 3), dtype=np.uint8)
            text_image[:] = background_color
            text_image = cv2.putText(text_image, line, (0, word_height), text_font, font_size, text_color, text_thickness, cv2.LINE_AA)
            text_image_resized = cv2.resize(text_image, (word_width, background_height))
            overlay_region = frame_with_text[text_position_y_01:text_position_y_01 + background_height, text_position_x_01:text_position_x_01 + word_width, :]
            
            if text_image_resized.shape[0] <= overlay_region.shape[0] and text_image_resized.shape[1] <= overlay_region.shape[1]:
                overlay_region[:text_image_resized.shape[0], :text_image_resized.shape[1], :] = text_image_resized
            else:
                text_position_y_01 += line_space

        # Add animation for text_02 above mid of screen
        if word_index_02 < len(text_02):
            current_word_02 += text_02[word_index_02]
            word_index_02 += 1

        wrapped_text_02 = textwrap.wrap(current_word_02, width=text_width)
        text_position_x_02 = (width - max([len(line) for line in wrapped_text_02]) * 10) // 2
        text_position_y_02 = height // 3
        text_position_x_02 -= left_margin

        for line in wrapped_text_02:
            word_width, word_height = cv2.getTextSize(line, text_font, font_size, text_thickness)[0]
            background_height = word_height + 25
            word_height += 10
            text_image = np.zeros((background_height, word_width, 3), dtype=np.uint8)
            text_image[:] = background_color
            text_image = cv2.putText(text_image, line, (0, word_height), text_font, font_size, text_color, text_thickness, cv2.LINE_AA)
            text_image_resized = cv2.resize(text_image, (word_width, background_height))
            overlay_region = frame_with_text[text_position_y_02:text_position_y_02 + background_height, text_position_x_02:text_position_x_02 + word_width, :]
            
            if text_image_resized.shape[0] <= overlay_region.shape[0] and text_image_resized.shape[1] <= overlay_region.shape[1]:
                overlay_region[:text_image_resized.shape[0], :text_image_resized.shape[1], :] = text_image_resized
            else:
                text_position_y_02 += line_space

        # Add animation for text_03 before bottom of screen
        if word_index_03 < len(text_03):
            current_word_03 += text_03[word_index_03]
            word_index_03 += 1

        wrapped_text_03 = textwrap.wrap(current_word_03, width=text_width)

        # Check if wrapped_text_03 is not empty before calculating maximum width
        if wrapped_text_03:
            text_position_x_03 = (width - max([len(line) for line in wrapped_text_03]) * 10) // 2
            text_position_y_03 = height - top_margin - line_space  # Move text slightly above bottom
            text_position_x_03 -= left_margin

            for line in wrapped_text_03:
                word_width, word_height = cv2.getTextSize(line, text_font, font_size, text_thickness)[0]
                background_height = word_height + 25
                word_height += 10
                text_image = np.zeros((background_height, word_width, 3), dtype=np.uint8)
                text_image[:] = background_color
                text_image = cv2.putText(text_image, line, (0, word_height), text_font, font_size, text_color, text_thickness, cv2.LINE_AA)
                text_image_resized = cv2.resize(text_image, (word_width, background_height))
                overlay_region = frame_with_text[text_position_y_03:text_position_y_03 + background_height, text_position_x_03:text_position_x_03 + word_width, :]
                
                if text_image_resized.shape[0] <= overlay_region.shape[0] and text_image_resized.shape[1] <= overlay_region.shape[1]:
                    overlay_region[:text_image_resized.shape[0], :text_image_resized.shape[1], :] = text_image_resized
                else:
                    text_position_y_03 += line_space

        out.write(frame_with_text)
        time.sleep(delay)  # Introduce delay between writing each word

    cap.release()
    out.release()

# Example usage:
video_path = r"C:\Users\hp\Desktop\Projectss\1\vedios\test-01.mp4"
output_path = "output_video.mp4"

data = {}
try:
    with open("facts.csv", 'r', newline='') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Read the header row
        for header in headers:
            data[header] = []  # Initialize empty lists for each column
        for row in csv_reader:
            for index, value in enumerate(row):
                data[headers[index]].append(value)  # Store values in corresponding column list
except FileNotFoundError:
    print("Error: File not found.")
    exit()
except Exception as e:
    print("An error occurred:", e)
    exit()

text_01 = data["content1"][0]
text_02 = data["content2"][0]
text_03 = data["content3"][0]

add_word_animation_to_video(video_path, output_path, text_01, text_02, text_03)
