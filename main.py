import board, pieces, ai
import speech_recognition as sr






def speech():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as sourse:
        try:
            print('Говорите...')
            audio = r.listen(sourse, phrase_time_limit=5, timeout=7)
            qwery = (r.recognize_google(audio, language='ru-RU')).title()
        except:
            return 'Ошибка ввода. Повторите попытку'
        else:
            print(qwery)
            word = trans(qwery)
            print(word)
            if len(word)==4: 
                return word
            else:
                'Ошибка ввода'



def trans(word):
    try:
        slovar = {'А':'A', 'A':'A', 'B':'B', 'C':'C', 'С':'C', 'Д':'D', 'D':'D', 'Е':'E', 'E':'E', 'G':'G', 'Ф':'F','F':'F', 'Г':'G', 'Х':'H','H':'H', '1':'1', '2':'2', '3':'3', '4':'4', ' ':' ', '5':'5', '6':'6', '7':'7', '8':'8', 'ОДИН':'1', 'ДВА':'2', 'ТРИ':'3', 'ЧЕТЫРЕ':'4', 'ПЯТЬ':'5', 'ШЕСТЬ':'6', 'СЕМЬ':'7', 'ВОСЕМЬ':'8'}
        mess = word.upper().replace(' ', '')
        new_mess = ''
        if mess[0] in 'АО' or mess[0] in 'AO':
            if 'АОДИН' in mess:
                mess = mess.replace('AОДИН', 'A1')
            if 'АДВА' in mess:
                mess = mess.replace('АДВА', 'A2')
            if 'АТРИ' in mess:
                mess = mess.replace('АТРИ', 'A3')
            if 'АЧЕТЫРЕ' in mess:
                mess = mess.replace('АЧЕТЫРЕ', 'A4')
            if 'АПЯТЬ' in mess:
                mess = mess.replace('АПЯТЬ', 'A5')
            if 'ОПЯТЬ' in mess:
                mess = mess.replace('ОПЯТЬ', 'A5')
            if 'АШЕСТЬ' in mess:
                mess = mess.replace('АШЕСТЬ', 'A6')
            if 'АСЕМЬ' in mess:
                mess = mess.replace('АСЕМЬ', 'A7')
            if 'АВОСЕМЬ' in mess:
                mess = mess.replace('АВОСЕМЬ', 'A8')
        for i in range(len(mess)):
            new_mess += slovar.get(mess[i])
        return new_mess
    except:
        return 'Ошибка ввода'



# Returns a move object based on the users input. Does not check if the move is valid.
def get_user_move():
    print("Example Move: A2 A4")
    move_str = input("Your Move: ")
    if move_str == 'Сделать ход':
        move_str = speech()
    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2]) # The board is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4]) # The board is drawn "upside down", so flip the y coordinate.
        return ai.Move(xfrom, yfrom, xto, yto, False)
    except:
        print("Invalid format. Example: A2 A4")
        return get_user_move()

# Returns a valid move based on the users input.
def get_valid_user_move(board):
    while True:
        move = get_user_move()
        valid = False
        possible_moves = board.get_possible_moves(pieces.Piece.WHITE)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if (valid):
            break
        else:
            print("Invalid move.")
    return move

# Converts a letter (A-H) to the x position on the chess board.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7
    else:
        return 'Попробуйте ввести ещё раз'
    

#
# Entry point.
#
board = board.Board.new()
print(board.to_string())

while True:
    move = get_valid_user_move(board)
    if (move == 0):
        if (board.is_check(pieces.Piece.WHITE)):
            print("Checkmate. Black Wins.")
            break
        else:
            print("Stalemate.")
            break

    board.perform_move(move)

    print("User move: " + move.to_string())
    print(board.to_string())

    ai_move = ai.AI.get_ai_move(board, [])
    if (ai_move == 0):
        if (board.is_check(pieces.Piece.BLACK)):
            print("Checkmate. White wins.")
            break
        else:
            print("Stalemate.")
            break

    board.perform_move(ai_move)
    print("AI move: " + ai_move.to_string())
    print(board.to_string())
