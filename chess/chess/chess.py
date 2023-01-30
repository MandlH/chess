from asyncio.windows_events import NULL
from cmath import nan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Firefox()
driver.get("https://www.chess.com/play/computer")
div_elements = []

driver_2 = webdriver.Firefox()
driver_2.get("https://www.chess.com/play/computer")
div_elements_2 = []

user_input = input("Enter w or b: ");
player = user_input

#viewBox="0 0 100 100"
tile_x = nan
tile_y = nan
#player = 'w' # w for white and b for black 

def get_alphabet_letter(n):
    if n < 1 or n > 26:
        return None
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet[n-1]

def get_first_number_from_string(string):
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    return None

def get_number_from_letter(letter):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    letter = letter.lower()
    if letter in alphabet:
        return alphabet.index(letter) + 1
    return None

def find_tile(row, col):
    x = 100 + col * tile_x
    y = 100 + row * tile_y
    return (x, y)

tile_x = 12.5
tile_y = 12.5

#chess grid
chess_grid = {}
chess_tile_coordinates = {}
for row in range(8):
    for col in range(8):
        if row == 0:
            continue
        if col == 0:
            continue

        value = nan
        #white start
        if row == 1 & col == 1:
            value = f'piece wr square-{col}{row}'
        if row == 1 & col == 2:
            value = f'piece wn square-{col}{row}'
        if row == 1 & col == 3:
            value = f'piece wb square-{col}{row}'
        if row == 1 & col == 4:
            value = f'piece wq square-{col}{row}'
        if row == 1 & col == 5:
            value = f'piece wk square-{col}{row}'
        if row == 1 & col == 6:
            value = f'piece wb square-{col}{row}'
        if row == 1 & col == 7:
            value = f'piece wn square-{col}{row}'
        if row == 1 & col == 8:
            value = f'piece wr square-{col}{row}'
        if row == 2:
            value = f'piece wp square-{col}{row}'
        #black start
        if row == 8 & col == 1:
            value = f'piece wr square-{col}{row}'
        if row == 8 & col == 2:
            value = f'piece wn square-{col}{row}'
        if row == 8 & col == 3:
            value = f'piece wb square-{col}{row}'
        if row == 8 & col == 4:
            value = f'piece wq square-{col}{row}'
        if row == 8 & col == 5:
            value = f'piece wk square-{col}{row}'
        if row == 8 & col == 6:
            value = f'piece wb square-{col}{row}'
        if row == 8 & col == 7:
            value = f'piece wn square-{col}{row}'
        if row == 8 & col == 8:
            value = f'piece wr square-{col}{row}'
        if row == 7:
            value = f'piece wp square-{col}{row}'

        col = get_alphabet_letter(col)

        key = (row, col)
        chess_grid[key] = value

        if value != nan:
            chess_tile_coordinates[key] = find_tile(row, get_number_from_letter(col))




last_ai_move = nan
last_ai_figure = nan
last_ai_col = nan
last_ai_row = nan

while True:
    html = driver.page_source
    html2 = driver_2.page_source

    soup = BeautifulSoup(html, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')

    new_div_elements = soup.find_all('div', {'data-ply': True})

    if len(new_div_elements) > len(div_elements):
        div_elements = new_div_elements

        max_ply = max([int(div.get('data-ply')) for div in div_elements if div.get('data-ply')])

        if player == "w":
            if max_ply % 2 == 0:
                continue

        max_ply_element = [div for div in div_elements if div.get('data-ply') == str(max_ply)][0]

        element_text = max_ply_element.text
        last_ai_move = element_text.replace(" ", "").replace("x", "")
        last_ai_figure = last_ai_move[0]
        if len(last_ai_move) == 2:
            last_ai_figure = 'p'
            last_ai_col = get_number_from_letter(last_ai_move[0])
            last_ai_row = int(last_ai_move[1])

        if len(last_ai_move) == 3:
            last_ai_figure == last_ai_move[0]
            last_ai_col = get_number_from_letter(last_ai_move[1])
            last_ai_row = int(last_ai_move[2])


        print("A new element was added:", element_text)

        #find element PROBLEM HOW DO I KNOW WHICH WHAT I WANT TO MOVE???
        key = (last_ai_col, last_ai_row)
        for item in chess_grid:
            value = chess_grid[item]
            if value == nan:
                continue

            chess_board = driver.find_element(By.ID, "board-vs-personalities")
            driver.switch_to.frame(chess_board)

            e = driver.find_element(By.CSS_SELECTOR, f'.{value}')
            #svg_element = driver_2.find_element(By.CSS_SELECTOR, 'coordinates')

            actions = ActionChains(driver)
            coordinate = find_tile(last_ai_row, last_ai_col)
            actions.move_to_element_with_offset(svg_element, coordinate[0], coordinate[1])
            actions.perform()
            actions.click()
            actions.perform()

            new_figure_position_text = f'piece {player}{last_ai_figure} square-{last_ai_col}{last_ai_row}'

        
        key = last_ai_figure;
        chess_grid[key] = new_figure_position_text;

        
         
        print(chess_grid[key])

    time.sleep(1)

driver.quit()