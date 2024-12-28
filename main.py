import re
import os
import time
import pydirectinput
import pyautogui
import pytesseract
from pynput.mouse import Controller, Button

def start_auto_algorithm(screenshot_coordinates, duration_in_seconds):
    last_extracted_numbers = []
    last_best_factor = None
    for i in range(duration_in_seconds):
        screenshot = capture_screen(screenshot_coordinates[0], screenshot_coordinates[1], screenshot_coordinates[2], screenshot_coordinates[3], i)
        number_string = perform_ocr(screenshot)
        extracted_numbers = extract_numbers(number_string)

        if extracted_numbers != last_extracted_numbers:
            best_factor = determine_best_factor(extracted_numbers)
            print(f"{best_factor}: {extracted_numbers[best_factor]}")
            if best_factor != last_best_factor:
                click_x_coordinate = screenshot_coordinates[0] - 156
                click_y_coordinates = (
                screenshot_coordinates[1] + 10, screenshot_coordinates[1] + 65, screenshot_coordinates[1] + 121,
                screenshot_coordinates[1] + 179)
                click_best_factor(click_x_coordinate, click_y_coordinates, best_factor)
            else:
                print("ignoring factor, as it did not change")

        else:
            print("ignoring numbers, as they did not change")

        last_extracted_numbers = extracted_numbers

        last_best_factor = best_factor
        time.sleep(1)

def capture_screen(x, y, width, height, i: int = 0):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(f'screenshot{i}.png')
    return screenshot

def perform_ocr(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update to your Tesseract path

    try:
        # Perform OCR
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
        return None

def extract_numbers(input_string):
    number_pattern = r'\b\d*\.\d+(?=x)'
    numbers = re.findall(number_pattern, input_string)
    return numbers

def determine_best_factor(numbers):
    numbers = [float(num) for num in numbers]
    return numbers.index(max(numbers))


def click_best_factor(x, y_coordinates: tuple, index):
    y = y_coordinates[index]
    pydirectinput.click(x, y)

    mouse = Controller()
    start_x, start_y = mouse.position  # Get the current mouse position

    intermediate_x = x -100
    steps = 100
    for i in range(steps + 1):
        current_x = start_x + (intermediate_x - start_x) * (i / steps)
        current_y = start_y
        mouse.position = (current_x, current_y)
        time.sleep(0.1 / steps)

    # Step 2: Smoothly move to the target position (x, y)
    for i in range(steps + 1):
        current_x = intermediate_x + (x - intermediate_x) * (i / steps)
        current_y = start_y + (y - start_y) * (i / steps)
        mouse.position = (current_x, current_y)
        time.sleep(0.1 / steps)

    # Step 3: Click at the target position
    mouse.click(Button.left, 2)

if __name__ == '__main__':
    screen_coordinates = (324, 807, 74, 188)
    # screen_coordinates = (324, 811, 74, 189)
    start_auto_algorithm(screen_coordinates, 1)