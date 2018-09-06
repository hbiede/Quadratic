# coding: UTF-8

from __future__ import division
from fractions import Fraction, gcd
from math import ceil, log10
import ui

shows_result = False
a = 0.0
b = 0.0
c = 0.0


def calculate_quadform(label):
    """@type label: ui.Button.superview"""
    global a, b, c
    imaginary = False

    if a == 0:
        if b == 0:
            label.text = 'B cannot be 0'
        else:
            label.text = str(Fraction(str(-c / b)))
    else:
        if a != int(a) and b != int(b) and c != int(c):
            x = 1
            while True:
                if (x * a) == int(x * a) and (x * b) == int(x * b) and (x * c) == int(x * c):
                    a *= x
                    b *= x
                    c *= x
                    break
                x += 1

        determinant = (b ** 2 - 4 * a * c)
        if determinant < 0:
            imaginary = True
            determinant *= -1
        if determinant ** 0.5 == int(determinant ** 0.5):
            answer1 = str(Fraction(((-b + determinant ** 0.5) / (2 * a))))
            answer2 = str(Fraction(((-b - determinant ** 0.5) / (2 * a))))
            if answer1 == answer2:
                label.text = answer1 + ' DR'
            else:
                label.text = answer1 + ' and ' + answer2
            if imaginary:
                label.text += ' *i'
        else:
            determinant_whole = 1
            if determinant != 1:
                for x in range(determinant):
                    if (determinant % (x ** 2)) == 0:
                        determinant /= x ** 2
                        determinant_whole *= x
            if determinant_whole != 1 and a != 0.5 and b != 1:
                divisor = gcd(a, gcd(b, c))
                a /= divisor
                b /= divisor
                c /= divisor
            label.text = ''
            if b != 0:
                label.text += str(-b)
            if determinant != 0:
                label.text += '±'
                if determinant_whole != 1:
                    label.text += determinant_whole
                if determinant != 1:
                    label.text += '√' + determinant
            length = len(label.text)
            label.text += '\n'
            for x in range(length):
                label.text += '-'
            label.text += '\n'
            for x in range(int(ceil((length - 0.5 * (log10(2 * a))) * 0.5))):
                label.text += ' '
            label.text += str(2 * a)


def button_tapped(sender):
    """@type sender: ui.Button"""
    # Get the button's title for the following logic:
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label1']
    label2 = sender.superview['label2']
    label3 = sender.superview['label3']
    label4 = sender.superview['label4']
    label5 = sender.superview['label5']
    if t in '0123456789':
        if shows_result or label.text == '0':
            # Replace 0 or last result with number:
            label.text = t
        else:
            # Append number:
            label.text += t
    elif t == '.' and label.text[-1] != '.':
        # Append decimal point (if not already there)
        label.text += t
    elif t in '+-÷×':
        if label.text[-1] in '+-÷×':
            # Replace current operator
            label.text = label.text[:-1] + t
        else:
            # Append operator
            label.text += t
    elif t == 'AC':
        # Clear All
        label.text = '0'
        label2.text = ''
        label3.text = ''
        label4.text = ''
        label5.text = ''
    elif t == 'C':
        # Delete the last character:
        label.text = label.text[:-1]
        if len(label.text) == 0:
            label.text = '0'
    if t != 'Enter':
        shows_result = False


def enter_tapped(sender):
    """@type sender: ui.Button"""
    global shows_result
    global a, b, c
    temp = 0
    # Get the labels:
    label = sender.superview['label1']
    label2 = sender.superview['label2']
    label3 = sender.superview['label3']
    label4 = sender.superview['label4']
    label5 = sender.superview['label5']
    # Evaluate the result:
    try:
        expr = label.text.replace('÷', '/').replace('×', '*')
        temp = eval(expr)
    except (SyntaxError, ZeroDivisionError):
        label.text = 'ERROR'
    # Saving to vars
    if label2.text == '':
        a = float(temp)
        label2.text = 'A = ' + str(a)
        label5.text = 'B ='
        label.text = '0'
    elif label3.text == '':
        b = float(temp)
        label3.text = 'B = ' + str(b)
        label5.text = 'C ='
        label.text = '0'
    elif label4.text == '':
        c = float(temp)
        label4.text = 'C = ' + str(c)
        label5.text = 'X ='
        calculate_quadform(label)
    else:
        label2.text = ''
        label3.text = ''
        label4.text = ''
        label5.text = 'A = '
        label.text = '0'


v = ui.load_view('Calculator')
if min(ui.get_screen_size()) >= 768:
    # iPad
    v.frame = (0, 0, 360, 400)
    v.present('sheet')
else:
    # iPhone
    v.present(orientations = ['portrait'])