import pyautogui
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import os

from simulator_advanced import get_available_cells, simulate_moves

coordinates = [
    [(600, 375), (675, 375), (775, 375), (870, 375), (950, 375), (1033, 375)],
    [(600, 450), (675, 450), (775, 450), (870, 450), (950, 450), (1033, 450)],
    [(600, 540), (675, 540), (775, 540), (870, 540), (950, 540), (1033, 540)],
    [(600, 625), (675, 625), (775, 625), (870, 625), (950, 625), (1033, 625)],
    [(600, 700), (675, 700), (775, 700), (870, 700), (950, 700), (1033, 700)],
    [(600, 800), (675, 800), (775, 800), (870, 800), (950, 800), (1033, 800)]
]

# globals
last_move = (0, 0)
direction = -1


def run_the_hell_machine(ng):
    file_path = "image.png"
    output_path = "cropped_image.png"
    crop_image(file_path, output_path)

    output_path_for_squares = "output"
    # uncomment for splitting squares
    # split_image_into_squares(output_path, output_path_for_squares)

    parsed_board = compare(output_path)
    if contains_negative_one(parsed_board):
        return 'the_end'
    print(parsed_board)

    global last_move
    global direction

    if ng == '1':
        last_move = (0, 0)
        direction = -1

    possible_moves = get_available_cells(parsed_board, last_move, direction)

    all_moves = []
    for possible_move in possible_moves:
        board_copy = [row.copy() for row in parsed_board]
        simulated_moves = simulate_moves(board_copy, 30, possible_move)
        for move in simulated_moves:
            all_moves.append(move)

    longest_sequence = max(all_moves, key=len, default=[])
    print(longest_sequence)

    if len(longest_sequence) > 0:
        last_move = longest_sequence[0]
        direction = parsed_board[last_move[0]][last_move[1]]
        coord = coordinates[last_move[0]][last_move[1]]
        pyautogui.FAILSAFE = False
        pyautogui.click(coord[0], coord[1])
        return 'not_the_end'
    else:
        return 'the_end'


def contains_negative_one(board):
    return any(-1 in row for row in board)


def crop_image(file_path, output_path):
    with Image.open(file_path) as img:
        width, height = img.size

        left = 93
        top = 43
        right = width - 93
        bottom = height - 43

        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(output_path)


def split_image_into_squares(input_path, output_directory):
    with Image.open(input_path) as img:
        square_width = 84
        square_height = 84

        gap_width = 2
        gap_height = 2

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for j in range(6):
            for i in range(6):
                left = i * (square_width + gap_width)
                upper = j * (square_height + gap_height)
                right = left + square_width
                lower = upper + square_height

                square_img = img.crop((left, upper, right, lower))

                filename = f"square_{j + 1}_{i + 1}.png"
                square_img.save(os.path.join(output_directory, filename))


def compare(input_path):
    with Image.open(input_path) as img:
        square_width = 84
        square_height = 84

        gap_width = 2
        gap_height = 2

        results = []

        for j in range(6):
            row_results = []

            for i in range(6):
                left = i * (square_width + gap_width)
                upper = j * (square_height + gap_height)
                right = left + square_width
                lower = upper + square_height

                square_img = img.crop((left, upper, right, lower))
                res = get_best_match(square_img)
                row_results.append(res)

            results.append(row_results)

        return results


def get_best_match(new_cell):
    best_ssim = float('-inf')
    best_match = None

    # 0: empty
    # 1: left
    # 2: right
    # 3: top
    # 4: bottom
    # 5: horizontal (both left and right)
    # 6: vertical (both top and bottom)
    # 7: all directions
    folders = ['bot', 'empty', 'left', 'right', 'top', 'all', 'horizontal', 'vertical']
    base_path = "samples"

    image_paths = []
    for folder in folders:
        for image_name in os.listdir(os.path.join(base_path, folder)):
            if image_name.endswith('.png'):
                image_paths.append((folder, os.path.join(base_path, folder, image_name)))

    for folder, image_path in image_paths:
        cell = Image.open(image_path)
        score = ssim(np.array(cell.convert('L')), np.array(new_cell.convert('L')))

        if score > best_ssim:
            best_ssim = score
            best_match = folder

    if best_ssim > 0.7:
        return get_int_representation(best_match)
    else:
        return -1


def get_int_representation(folder_name):
    mapping = {
        'empty': 0,
        'left': 1,
        'right': 2,
        'top': 3,
        'bot': 4,
        'horizontal': 5,
        'vertical': 6,
        'all': 7
    }
    return mapping.get(folder_name, 0)

