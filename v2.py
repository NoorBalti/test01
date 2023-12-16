import cv2
import csv
import numpy as np
import textwrap
import time

def add_text_to_video(video_path, output_path, *texts, max_width=15,
                      font_size=1.3, text_font=cv2.FONT_HERSHEY_TRIPLEX,
                      text_color=(0, 255, 255), text_thickness=2,
                      background_color=(0, 0, 0), left_margin=200,
                      top_margin=40, line_space=180):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    word_indices = [0] * len(texts)
    current_words = [""] * len(texts)
    text_width = max_width

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_with_text = frame.copy()

        for i, text in enumerate(texts):
            if word_indices[i] < len(text):
                current_words[i] += text[word_indices[i]]
                word_indices[i] += 1

            wrapped_text = textwrap.wrap(current_words[i], width=text_width)

            if wrapped_text:
                text_position_x = (width - max([len(line) for line in wrapped_text]) * 10) // 2
                text_position_y = height // 7
                text_position_x -= left_margin
                text_position_y -= top_margin

                for line in wrapped_text:
                    word_width, word_height = cv2.getTextSize(line, text_font, font_size, text_thickness)[0]
                    background_height = word_height + 25
                    word_height += 10
                    text_image = np.zeros((background_height, word_width, 3), dtype=np.uint8)
                    text_image[:] = background_color
                    text_image = cv2.putText(text_image, line, (0, word_height), text_font, font_size, text_color, text_thickness, cv2.LINE_AA)
                    text_image_resized = cv2.resize(text_image, (word_width, background_height))
                    overlay_region = frame_with_text[text_position_y:text_position_y + background_height, text_position_x:text_position_x + word_width, :]

                    if text_image_resized.shape[0] <= overlay_region.shape[0] and text_image_resized.shape[1] <= overlay_region.shape[1]:
                        overlay_region[:text_image_resized.shape[0], :text_image_resized.shape[1], :] = text_image_resized
                    else:
                        text_position_y += line_space

        out.write(frame_with_text)

    cap.release()
    out.release()

def add_word_animation_to_video(video_path, output_path, *texts,
                                max_width=30, font_size=1.5, text_font=cv2.FONT_HERSHEY_TRIPLEX,
                                text_color=(0, 255, 255), text_thickness=2,
                                background_color=(0, 0, 0), left_margin=150, top_margin=40, line_space=80,
                                delay=0.1):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    word_indices = [0] * len(texts)
    current_words = [""] * len(texts)
    text_width = max_width

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_with_text = frame.copy()

        for i, text in enumerate(texts):
            if word_indices[i] < len(text):
                current_words[i] += text[word_indices[i]]
                word_indices[i] += 1

            wrapped_text = textwrap.wrap(current_words[i], width=text_width)

            if wrapped_text:
                text_position_x = (width - max([len(line) for line in wrapped_text]) * 10) // 2
                text_position_y = height - top_margin - line_space
                text_position_x -= left_margin

                for line in wrapped_text:
                    word_width, word_height = cv2.getTextSize(line, text_font, font_size, text_thickness)[0]
                    background_height = word_height + 25
                    word_height += 10
                    text_image = np.zeros((background_height, word_width, 3), dtype=np.uint8)
                    text_image[:] = background_color
                    text_image = cv2.putText(text_image, line, (0, word_height), text_font, font_size, text_color, text_thickness, cv2.LINE_AA)
                    text_image_resized = cv2.resize(text_image, (word_width, background_height))
                    overlay_region = frame_with_text[text_position_y:text_position_y + background_height, text_position_x:text_position_x + word_width, :]

                    if text_image_resized.shape[0] <= overlay_region.shape[0] and text_image_resized.shape[1] <= overlay_region.shape[1]:
                        overlay_region[:text_image_resized.shape[0], :text_image_resized.shape[1], :] = text_image_resized
                    else:
                        text_position_y += line_space

        out.write(frame_with_text)
        time.sleep(delay)

    cap.release()
    out.release()



def add_synchronized_text_to_video(video_path, output_path, text_01, text_02, text_03,
                                   max_width=15, font_size=1.3, text_font=cv2.FONT_HERSHEY_TRIPLEX,
                                   text_color=(0, 255, 255), text_thickness=2,
                                   background_color=(0, 0, 0), left_margin=200,
                                   top_margin=40, line_space=180):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    texts = [text_01, text_02, text_03]
    word_indices = [0] * len(texts)
    current_words = [""] * len(texts)
    text_width = max_width

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_with_text = frame.copy()

        for i, text in enumerate(texts):
            if word_indices[i] < len(text):
                current_words[i] += text[word_indices[i]]
                word_indices[i] += 1

            wrapped_text = textwrap.wrap(current_words[i], width=text_width)

            if wrapped_text:
                text_position_x = (width - max([len(line) for line in wrapped_text]) * 10) // 2
                text_position_y = height // 7
                text_position_x -= left_margin
                text_position_y -= top_margin

                for line in wrapped_text:
                    word_width, word_height = cv2.getTextSize(line, text_font, font_size, text_thickness)[0]
                    background_height = word_height + 25
                    word_height += 10
                    text_image = np.zeros((background_height, word_width, 3), dtype=np.uint8)
                    text_image[:] = background_color
                    text_image = cv2.putText(text_image, line, (0, word_height), text_font, font_size, text_color, text_thickness, cv2.LINE_AA)
                    text_image_resized = cv2.resize(text_image, (word_width, background_height))
                    overlay_region = frame_with_text[text_position_y:text_position_y + background_height, text_position_x:text_position_x + word_width, :]

                    if text_image_resized.shape[0] <= overlay_region.shape[0] and text_image_resized.shape[1] <= overlay_region.shape[1]:
                        overlay_region[:text_image_resized.shape[0], :text_image_resized.shape[1], :] = text_image_resized
                    else:
                        text_position_y += line_space

        out.write(frame_with_text)

    cap.release()
    out.release()



def main():
    # Paths to video and CSV file
    video_path = r"C:\Users\hp\Desktop\Projectss\1\vedios\test-01.mp4"
    csv_file_path = "facts.csv"

    # Read data from CSV file
    data = {}
    try:
        with open(csv_file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Read the header row
            for header in headers:
                data[header] = []  # Initialize empty lists for each column
            for row in csv_reader:
                for index, value in enumerate(row):
                    data[headers[index]].append(value)  # Store values in corresponding column list
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except Exception as e:
        print("An error occurred:", e)
        return

    # Extract text from data
    text_00 = [data["content1"][0], data["content2"][0], data["content3"][0]]
    text_01 = data["content1"][0]
    text_02 = data["content2"][0]
    text_03 = data["content3"][0]

    # Add text to video
    add_text_to_video(video_path, "output_text.mp4", *text_00)

    # Add synchronized text lines to video
    add_synchronized_text_to_video(video_path, "output_synchronized_text.mp4", text_01, text_02, text_03)

    # Add animated words to video
    add_word_animation_to_video(video_path, "output_word_animation.mp4", text_01, text_02, text_03)

if __name__ == "__main__":
    main()
