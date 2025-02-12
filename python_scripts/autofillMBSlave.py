import pyautogui as pg
import time

def main():
    word = input("what would you like to put in every row?");
    rows = input("how many rows?")
    try:
        rows = int(rows)
    except ValueError:
        print("row not entered as int")
    time.sleep(5);
    fillColumn(word=word, rows=rows)

def fillColumn(word, rows):
    for i in range(rows):
        pg.typewrite(word)
        print("row:", i, "val:", word)

if __name__ == '__main__':
    main();
    print("Done");