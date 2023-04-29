# telegram api
import telebot
import math

# vars
token = ''
bot = telebot.TeleBot(token)
min_count_sum_difference_product_quotient = 2
max_count_sum_difference_product_quotient = 10
count_area_of_a_circle_and_square = 1
count_area_of_a_rectangle = 2
min_count_area_of_a_triangle = 2
max_count_area_of_a_triangle = 3
number_of_decimal_places_to_round = 10


# checks arguments for being less than or equal to zero
def less_than_or_equal_to_zero(args):
    for arg in args:
        if float(arg) <= 0:
            return True
    return False


# get command
def get_cmd(message):
    return ''.join(message.text.split()[:1])


# getting command arguments and checking if they are numbers
def extract_args(message, min_count, max_count):
    args = message.text.split()[1:]
    if min_count <= len(args) <= max_count:
        flag = True
        for arg in args:
            if not arg.lstrip('-').replace('.', '', 1).isdigit():
                flag = False
                bot.send_message(message.chat.id, f"\"{arg}\" is not a number")
                break
        if flag:
            return args
    else:
        bot.send_message(message.chat.id, f'*min args count -* _{min_count}_\n'
                                          f'*max args count -* _{max_count}_', parse_mode='Markdown')


# /s or /d or /p or /q
@bot.message_handler(commands=['s', 'd', 'p', 'q'])
def sum_difference_product_quotient_message(message):
    cmd = get_cmd(message)
    args = extract_args(message, min_count_sum_difference_product_quotient, max_count_sum_difference_product_quotient)
    if args is not None:
        if cmd == '/p':
            result = 1
        elif cmd == '/q' or cmd == '/d':
            result = float(args[0])
            args.pop(0)
        else:
            result = 0
        try:
            for arg in args:
                if cmd == '/s':
                    result += float(arg)
                elif cmd == '/d':
                    result -= float(arg)
                elif cmd == '/p':
                    result *= float(arg)
                elif cmd == '/q':
                    result /= float(arg)
            result = round(result, number_of_decimal_places_to_round)
        except ZeroDivisionError:
            result = 'division by zero'
        bot.send_message(message.chat.id, f'= {result}')


# /acr or /acd
@bot.message_handler(commands=['acr', 'acd'])
def area_of_a_circle_message(message):
    cmd = get_cmd(message)
    args = extract_args(message, count_area_of_a_circle_and_square, count_area_of_a_circle_and_square)
    if args is not None:
        if less_than_or_equal_to_zero(args):
            bot.send_message(message.chat.id, '*D or R cannot be less than or equal to zero*', parse_mode='Markdown')
        else:
            result = 0
            if cmd == '/acr':
                result = math.pi * float(args[0]) * float(args[0])
            elif cmd == '/acd':
                result = math.pi / 4.0 * float(args[0]) * float(args[0])
            bot.send_message(message.chat.id, f'= {round(result, number_of_decimal_places_to_round)}')


# /at
@bot.message_handler(commands=['at'])
def area_of_a_triangle_message(message):
    args = extract_args(message, min_count_area_of_a_triangle, max_count_area_of_a_triangle)
    if args is not None:
        if less_than_or_equal_to_zero(args):
            bot.send_message(message.chat.id, "*Triangle arguments cannot be less than or equal to zero*",
                             parse_mode='Markdown')
        else:
            if len(args) == 2:
                result = 0.5 * float(args[0]) * float(args[1])
            else:
                semi_perimeter = (float(args[0]) + float(args[1]) + float(args[2])) / 2.0
                result = math.sqrt(semi_perimeter *
                                   (semi_perimeter - float(args[0])) *
                                   (semi_perimeter - float(args[1])) *
                                   (semi_perimeter - float(args[2])))
            bot.send_message(message.chat.id, f'= {round(result, number_of_decimal_places_to_round)}')


@bot.message_handler(commands=['as', 'asd'])
def area_of_a_square_message(message):
    cmd = get_cmd(message)
    args = extract_args(message, count_area_of_a_circle_and_square, count_area_of_a_circle_and_square)
    if args is not None:
        if less_than_or_equal_to_zero(args):
            bot.send_message(message.chat.id, '*Square arguments cannot be less than or equal to zero*',
                             parse_mode='Markdown')
        else:
            if cmd == '/as':
                result = float(args[0]) * float(args[0])
            else:
                result = 0.5 * float(args[0]) * float(args[0])
            bot.send_message(message.chat.id, f'= {round(result, number_of_decimal_places_to_round)}')


@bot.message_handler(commands=['ar'])
def area_of_a_rectangle_message(message):
    args = extract_args(message, count_area_of_a_rectangle, count_area_of_a_rectangle)
    if args is not None:
        if less_than_or_equal_to_zero(args):
            bot.send_message(message.chat.id, "*Rectangle arguments cannot be less than or equal to zero*",
                             parse_mode='Markdown')
        else:
            result = float(args[0]) * float(args[1])
            bot.send_message(message.chat.id, f'= {round(result, number_of_decimal_places_to_round)}')


# /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '*Hi, i\'m a telegram bot*\n'
                                      '/help *- to view commands*', parse_mode='Markdown')


# /help or other text
@bot.message_handler(content_types=['text'])
def help_message(message):
    if message.text == '/help':
        bot.send_message(message.chat.id, f'*sum -* /s _arg1 arg2 argN_ '
                                          f'*- N =* _{max_count_sum_difference_product_quotient}_\n'
                                          f'*difference -* /d _arg1 arg2 argN_ '
                                          f'*- N =* _{max_count_sum_difference_product_quotient}_\n'
                                          f'*product -* /p _arg1 arg2 argN_ '
                                          f'*- N =* _{max_count_sum_difference_product_quotient}_\n'
                                          f'*quotient -* /q _arg1 arg2 argN_ '
                                          f'*- N =* _{max_count_sum_difference_product_quotient}_\n'
                                          f'*area of a circle through the radius -* /acr _argR_\n'
                                          f'*area of a circle through the diameter -* /acd _argD_\n'
                                          f'*area of a triangle -* /at _argA_ _argH_ *or* _argA_ _argB_ _argC_\n'
                                          f'*area of a square through the side -* /as _argS_\n'
                                          f'*area of a square through the diagonal -* /asd _argD_\n'
                                          f'*area of a rectangle -* /ar _argA_ _argB_',
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, '/help *- to view commands*', parse_mode='Markdown')


# check messages
bot.polling(none_stop=True, interval=0)
