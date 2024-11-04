from sudoku import Sudoku
import pygame, random, time, os
from button import Button

# WINDOW VARIABLES & INITIALIZATION
WIDTH = 850
HEIGHT = 550
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
COLOR_CLICKED = (187, 222, 251)
COLOR_RELATIVE = (226, 235, 243)
COLOR_SAME_VALUE = (195, 215, 234)
COLOR_WRONG = (247, 207, 214)
COLOR_FONT_DEFAULT = (52, 72, 97)
COLOR_FONT_1 = (50, 90, 175)
COLOR_FONT_WRONG = (229, 92, 108)
COLOR_THICK = COLOR_FONT_DEFAULT
COLOR_THIN = (191, 198, 212)
COLOR_NOTE = (110, 124, 140)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
win.fill(WHITE)
font_board_size = 25
font_note_size = 12
myfont = pygame.font.SysFont('segoeuisemibold', font_board_size)
notefont =  pygame.font.SysFont('segoeuisemibold', font_note_size)
font_dif =  pygame.font.SysFont('segoeuisemibold', 18)
buffer = (50 - font_board_size) // 2

count_hint = 100
posBoard = [-1, -1]
is_paused = False
noteMode = False

#GET BOARD VALUE

puzzle = Sudoku(3).difficulty(0.40)
defaultBoard = [[x != None for x in row] for row in puzzle.board]
#Tạo một bảng sudoku 3x3, 50% số ô trống
solution = puzzle.solve()
#Đáp án của bảng sudoku 
noteBoard = [[[[None for _ in range(9)] for _ in range(9)] for _ in range(9)] for _ in range(9)]
isNote =   [[False for _ in range(9)] for _ in range(9)]
#Một mảng là note của các ô

#Biến đếm thời gian
font_time =  pygame.font.SysFont('segoeuisemibold', 17)
start_time = time.time()
paused_time = 0
played_time = 0
text_time = font_time.render("Thời gian: 999:999:999", True, (0, 0, 0))
text_time_rect = text_time.get_rect(topleft=(560, 50))

#Tạo button

#numpad

btn_numpad = []
button_width, button_height = 90, 90
button_padding = 5

for i in range(3):
    for j in range(3):
        button_text = str(i * 3 + j + 1)  # Generate text from 1 to 9
        button_x = 530 + j * (button_width + button_padding)
        button_y = 221 + i * (button_height + button_padding)
        button = Button(button_x, button_y, button_width, button_height,
                        (234, 238, 244), (220, 227, 237), (210, 218, 231), (50, 90, 175), button_text, font_size=30, border_rad=5)
        btn_numpad.append(button)

btn_erase = Button(530, 120, button_width, button_height,
                  (234, 238, 244), (220, 227, 237), (210, 218, 231), (50, 90, 175), text="xóa", font_size=20, border_rad=50)
btn_note = Button(530 + button_width + button_padding, 120, button_width, button_height,
                  (234, 238, 244), (220, 227, 237), (210, 218, 231), (50, 90, 175), text="nháp (OFF)", font_size=13, border_rad=50)
btn_hint = Button(530 + 2 * (button_width + button_padding), 120, button_width, button_height,
                  (234, 238, 244), (220, 227, 237), (210, 218, 231), (50, 90, 175), text="gợi ý ({})".format(count_hint), font_size=13, border_rad=50)

btn_pause =  Button(530, 50, 25, 25,
                  (234, 238, 244), (220, 227, 237), (210, 218, 231), (50, 90, 175), image_path="button-stop.png", font_size=10, border_rad=50)



text_dif = ["Dễ", "Trung bình", "Khó", "Chuyên gia"]
dic_dif = {"Dễ":0.3, "Trung bình":0.45, "Khó":0.6, "Chuyên gia":0.7}
cur_dif = "Trung bình"
btn_dif = []
btn_dif_y = 10
bth_dif_x = 130

for i in range(4):
  textt = text_dif[i]
  text_ren = font_dif.render(textt, True, (0, 0, 0))
  w = text_ren.get_width() + 10
  h = text_ren.get_height() + 5
  text_color = (110, 124, 140)
  if textt == cur_dif: text_color = (50, 90, 175)

  button = Button(bth_dif_x, btn_dif_y, w, h,
        (255, 255, 255), (241, 244, 248), (238, 234, 244), text_color, text=textt, font_size=18)
  bth_dif_x += w + 10
  btn_dif.append(button)

def NewGame(dif):
  global puzzle, defaultBoard, solution, noteBoard, isNote, count_hint, start_time, count_mistake, is_over
  puzzle = Sudoku(3, seed = random.randint(1, 1000)).difficulty(dif)
  defaultBoard = [[x != None for x in row] for row in puzzle.board]
  #Tạo một bảng sudoku 3x3, 50% số ô trống
  solution = puzzle.solve()
  #Đáp án của bảng sudoku 
  noteBoard = [[[[None for _ in range(9)] for _ in range(9)] for _ in range(9)] for _ in range(9)]
  isNote =   [[False for _ in range(9)] for _ in range(9)]
  count_hint = 3
  btn_hint.update_text("gợi ý ({})".format(count_hint))
  if noteMode: ChangeNoteMode()
  if is_paused: ChangePauseMode() 
  start_time = time.time()
  count_mistake = 0
  is_over = False
  DrawBoard()

count_mistake = 0
is_over = False

def GameOverNoti(is_win):
  global is_over
  font_noti = pygame.font.SysFont('segoeuisemibold', 25)
  text = font_noti.render("Chúc mừng bạn đã thắng!", True, (0, 0, 0))
  if not is_win:
    text = font_noti.render("Rất tiếc, bạn đã thua!", True, (0, 0, 0))
  if is_paused == False: ChangePauseMode()
  rect = pygame.Rect(75, 200, 400, 100)
  shadow_rect = rect.copy()
  shadow_rect.inflate_ip(4, 4)
  text_rect = text.get_rect(center=rect.center)
  pygame.draw.rect(win, (100, 100, 100), shadow_rect, border_radius=5)
  pygame.draw.rect(win, (255,255,255), rect, border_radius=5)
  win.blit(text, text_rect)
  is_over = True

def Check_win():
  return puzzle.board == solution.board

def InsideBoard(pos:list):
  return 0 <= pos[0] < 9 and 0 <= pos[1] < 9

def resetNote(pos:list):
  for i in range(3):
    for j in range(3):
      noteBoard[pos[0]][pos[1]][i][j] = None

def is_wrong(i:int, j:int):
  return puzzle.board[i][j] != solution.board[i][j]

def ChangeValue(value:int, isHint:bool = False):
  i, j = posBoard[0], posBoard[1]
  if not InsideBoard([i, j]):
    pass
  if defaultBoard[i][j] == False:
    if noteMode == False or isHint:
      if isNote[i][j]:
        resetNote(posBoard)
        isNote[i][j] = False
      if value == 0 or value == puzzle.board[i][j]:
        puzzle.board[i][j] = None
      else:
        puzzle.board[i][j] = value 
        if is_wrong(i, j):
          global count_mistake 
          count_mistake += 1
    elif noteMode == True:
      if isNote[i][j] == False:
        isNote[i][j] = True
      if puzzle.board[i][j] != None:
        puzzle.board[i][j] = None
      x = (value-1)//3
      y = (value-1)%3
      #print(x, y)
      if value == 0:
        resetNote(posBoard)
      else:
        if noteBoard[i][j][x][y] == None:
          noteBoard[i][j][x][y] = value
        elif noteBoard[i][j][x][y] == value:
          noteBoard[i][j][x][y] = None

      #print(noteBoard[i][j][x][y])
    DrawBoard()
    
def BlockVal(pos:list):
  return pos[0]//3*3+pos[1]//3

def CheckWrong(i:int, j:int):
  for k in range(9):
    if((puzzle.board[i][j] == puzzle.board[k][j] and k != i) or (puzzle.board[i][j] == puzzle.board[i][k] and k != j)): return True
  x1 = i//3*3
  y1 = j//3*3
  for x in range(3):
    for y in range(3):
      if puzzle.board[x+x1][y+y1] == puzzle.board[i][j] and (i != x+x1 or j != y+y1): return True
  return False

def HandleButtons(event):
  for button in btn_dif:
    button.handle_event(event)
  if is_over == False:
    for button in btn_numpad:
      button.handle_event(event)
    btn_erase.handle_event(event)
    btn_note.handle_event(event)
    btn_hint.handle_event(event)
    btn_pause.handle_event(event)

def UpdateDifButtons():
  for button in btn_dif:
    if button.text == cur_dif:
      button.update_text_color((50, 90, 175))
    else: 
      button.update_text_color((110, 124, 140))

def DrawButtons():
  for button in btn_dif:
    button.draw(win)
    if button.clicked():
      global cur_dif
      cur_dif = button.text
      UpdateDifButtons()
      global is_over
      is_over = False
      NewGame(dic_dif[cur_dif])

  for button in btn_numpad:
    button.draw(win)
    if button.clicked() and is_paused == False:
      ChangeValue(int(button.text))
  btn_erase.draw(win)
  btn_note.draw(win)
  btn_hint.draw(win)
  btn_pause.draw(win)
  if btn_erase.clicked() and is_paused == False:
    ChangeValue(0)
  if btn_note.clicked() and is_paused == False:
    ChangeNoteMode()
  if btn_hint.clicked() and InsideBoard(posBoard) and is_paused == False:
    global count_hint
    i, j = posBoard[0], posBoard[1]
    if defaultBoard[i][j] == False and count_hint > 0:
      isNote[i][j] = True
      count_hint -= 1
      ChangeValue(0, True)
      ChangeValue(solution.board[i][j], True)
      defaultBoard[i][j] = True
      btn_hint.update_text("gợi ý ({})".format(count_hint))
      DrawBoard()
  if btn_pause.clicked():
    ChangePauseMode()
    DrawBoard()

def DrawBoard(flag:bool=False):
  for i in range(9):
    for j in range(9):
      rectColor = WHITE
      if is_paused:
        pygame.draw.rect(win, rectColor, (50+i*50, 50+j*50, 50, 50))
      else:
        if(InsideBoard(posBoard)):
          x, y = posBoard[0], posBoard[1]
          if(i == posBoard[0] or j == posBoard[1] or BlockVal([i, j]) == BlockVal(posBoard)): 
            rectColor = COLOR_RELATIVE
          if(puzzle.board[i][j] != None and puzzle.board[i][j] == puzzle.board[x][y]): rectColor = COLOR_SAME_VALUE
          if(puzzle.board[i][j] != None and CheckWrong(i, j)):
            rectColor = COLOR_WRONG
          if(x == i and y == j): rectColor = COLOR_CLICKED
        pygame.draw.rect(win, rectColor, (50+i*50, 50+j*50, 50, 50))
        if puzzle.board[i][j] != None:
          colorFont = COLOR_FONT_DEFAULT
          if defaultBoard[i][j] == False: colorFont = COLOR_FONT_1
          if puzzle.board[i][j] != solution.board[i][j] and puzzle.board[i][j] != None: 
            colorFont = COLOR_FONT_WRONG
          if isNote[i][j] == False:
            value = myfont.render(str(puzzle.board[i][j]), True, colorFont)
            pos_x = 50+i*50+(50-value.get_width())//2
            pos_y = 50+j*50+(50-value.get_height())//2
            win.blit(value, (pos_x, pos_y))
        if isNote[i][j] == True: 
          value = notefont.render('0', True, colorFont)
          dif_x = (50-(value.get_width()*3+15))//2
          dif_y = (50-(value.get_height()*3-5))//2
          for mvy in range(3):
            for mvx in range(3):
              v = noteBoard[i][j][mvy][mvx]
              if v != None:
                value = notefont.render(str(v), True, COLOR_NOTE)
                pos_x = 50+i*50+mvx*15 + dif_x
                pos_y = 50+j*50+mvy*15 + dif_y
                win.blit(value, (pos_x, pos_y))

  DrawLines()

def DrawLines():
  for i in range(0, 10):
    if(i%3!=0):
      pygame.draw.line(win, COLOR_THIN, (50+50*i, 50), (50+50*i, 500), 1) 
      pygame.draw.line(win, COLOR_THIN, (50, 50+50*i), (500, 50+50*i), 1)

  for i in range(0, 10):
    if(i%3==0):
      pygame.draw.line(win, COLOR_THICK, (50+50*i, 50), (50+50*i, 500), 3) 
      pygame.draw.line(win, COLOR_THICK, (50, 50+50*i), (500, 50+50*i), 3)

def ShowTimeCounter():
  cur_time = time.time() - start_time
  if is_paused: 
    cur_time = paused_time
  global played_time
  played_time = cur_time
  formated_time = time.strftime("%H:%M:%S", time.gmtime(cur_time))
  pygame.draw.rect(win, (255, 255, 255), text_time_rect)
  text_time = font_time.render("Thời gian: {}".format(formated_time), True, (0, 0, 0))
  win.blit(text_time, text_time_rect)

def UpdateTimeBest():
  folder_path = os.path.dirname(__file__)
  file_path = os.path.join(folder_path, "timebest.txt")
  with open(file_path, 'r') as file:
    time_best = float(file.read())
  if played_time < time_best:
    with open(file_path, 'w') as file:
      file.write(str(played_time))
    ShowTimeBest()

def ShowTimeBest():
  folder_path = os.path.dirname(__file__)
  file_path = os.path.join(folder_path, "timebest.txt")
  time_best = 0.0
  with open(file_path, 'r') as file:
    time_best = float(file.read())
  formated_time = ""
  if time_best < 9999999999.0: formated_time = time.strftime("%H:%M:%S", time.gmtime(time_best))
  text_time = font_time.render("Tốt nhất:  {}".format(formated_time), True, (0, 0, 0))
  rect = text_time_rect.copy()
  rect.y += 20
  win.blit(text_time, rect)

def ShowMistakeCounter():
   text = font_time.render("Lỗi sai: {}/3".format(count_mistake), True, (0, 0, 0))
   text_rect = text.get_rect(topleft=(560, 20))
   text_rect.width += 5
   pygame.draw.rect(win, (255, 255, 255), text_rect)
   win.blit(text, text_rect)

def InitializationUI():
  difficulty_text = font_dif.render("Độ khó: ", True, (148, 163, 183))
  win.blit(difficulty_text, (50, 12))
  DrawBoard()

def ChangeNoteMode():
  global noteMode
  if noteMode == True:
    noteMode = False
    btn_note.update_text("nháp (OFF)")
  else:
    noteMode = True
    btn_note.update_text("nháp (ON)")
    
def ChangePauseMode():
  global is_paused, paused_time, start_time
  if is_over == False:
    if is_paused == False:
      is_paused = True
      btn_pause.update_img("button-play.png")
      paused_time = time.time() - start_time
    else:
      is_paused = False
      btn_pause.update_img("button-stop.png")
      start_time = time.time() - paused_time

def main():
  InitializationUI()
  global posBoard, start_time
  DrawButtons()
  ShowTimeBest()

  while True:
    if count_mistake == 3:
      GameOverNoti(False)
    if Check_win():
      UpdateTimeBest()
      GameOverNoti(True)

    for event in pygame.event.get():
      HandleButtons(event)
      if event.type == pygame.QUIT:
        pygame.quit()
        return
      if not is_over:
        if is_paused == False:
          if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #click chuot trai vao board
            x, y = (event.pos[0]-50)//50, (event.pos[1]-50)//50
            if InsideBoard([x, y]): 
              posBoard=[x, y]
              DrawBoard()
          elif event.type == pygame.KEYDOWN:
            if InsideBoard(posBoard):
              val = event.key - 48
              if(1 <= val <= 9):
                ChangeValue(val)
              elif event.key == pygame.K_BACKSPACE or val == 0:
                ChangeValue(0)
            if event.key == pygame.K_n:
              ChangeNoteMode()
        elif is_paused == True:
          DrawBoard()
    ShowTimeCounter()
    ShowMistakeCounter()
    DrawButtons()
    pygame.display.flip()

if __name__ == "__main__":
  main()