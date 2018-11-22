import turtle
import random
stage=[0]
import random
import os

game_folder = os.path.dirname(__file__)
wrd_files= ['animal','bollywood','hollywood','sports','fruits']

def wordlist():
    filepath = wrd_files[random.randint(0,len(wrd_files))]
    wrd_file = os.path.join(game_folder, filepath+".txt")
    input_file=open(wrd_file,'r')
    wordlst=input_file.readlines()
    input_file.close()
    return (wordlst[random.randint(0,len(wordlst))],filepath)

def createturtle():
    turtle.setup(400,600)
    window=turtle.Screen()
    window.title("Hangman")
    turtle.pensize(5)
    turtle.hideturtle()
def go_to(x, y, p):
	turtle.hideturtle()
	turtle.penup()
	turtle.goto(x,y)
	turtle.setheading(p)
	turtle.pendown()

def hang():
	if stage[0]==0:
		go_to(-110,0,0)
		turtle.speed(0)
		turtle.forward(120)
		turtle.right(90)
		turtle.forward(30)
		turtle.right(90)
		turtle.forward(120)
		turtle.right(90)
		turtle.forward(30)
		turtle.right(90)
		cb = turtle.right
		for i in range(0,5):
			turtle.forward(120)
			cb(90)
			turtle.forward(5)
			cb(90)
			if cb is turtle.right:
				cb = turtle.left
			else:
				cb = turtle.right
		turtle.forward(120)
		go_to(-100,0, 90)
		turtle.forward(200)
		turtle.right(90)
		turtle.forward(100)
		turtle.right(90)
		turtle.forward(25)
	elif stage[0]==1:
		go_to(0, 150, 0)
		turtle.circle(12.5)
	elif stage[0]==2:
		go_to(0,150, -90)
		turtle.forward(50)
	elif stage[0]==3:
		go_to(0,140, -45)
		turtle.forward(25)
	elif stage[0]==4:
		go_to(0,140, -135)
		turtle.forward(25)
	elif stage[0]==5:
		go_to(0,100, -45)
		turtle.forward(25)
	elif stage[0]==6:
		go_to(0,100, -135)
		turtle.forward(25)
	stage[0]+=1
	return 0

def main():
    res = wordlist()
    word=res[0].strip('\n').lower()
    genre = res[1].lower()
    charlist=list(word)
    defaultstr=""
    count=0
    length=len(word)
    print("Welcome to hangman!!")
    for i in range(0,length):
        defaultstr+="_ "
    print("Here is your word:")
    print(defaultstr)
    createturtle()
    terminate=False
    donewrd = []
    while not terminate:
            if '_' not in defaultstr:
                print("Congratulations!! You guessed it right. The correct word was",word)
                print("Close the hangman window to end the game.")
                turtle.bgcolor("green")
                turtle.exitonclick()
                break
            print("Word Genre:",genre)
            char=input("Enter a letter:")
            if len(char) != 1 or ord(char.upper())<65 or ord(char.upper())>90:
                print("Invalid input. Please try again")
                continue
            if char in donewrd:
                print("You have already guessed this letter. Please try another")
                continue
            donewrd.append(char)
            if char in charlist:
                for i in range(len(word)):
                    if(char in word[i]):
                        defaultstr=(defaultstr[0:i*2])+char+(defaultstr[i*2+1:])
                print(defaultstr)
                del charlist[charlist.index(char)]
            else:
                hang()
                print("The letter you entered is not in the word")
                print(defaultstr)
                if stage[0]==7:
                    turtle.bgcolor("red")
                    print("You lose!!")
                    print("The correct word was:",word)
                    print("Close the hangman window to end the game.")
                    terminate=True
                    turtle.exitonclick()
if __name__ == '__main__':
	main()

'''
	print(word)
	spaces(word)
	out=''
	for i in range(len(word)):
		out+='_'
	while out != word and stage[0]<=4:
		print(out)
		out=play(word, out)
	if stage[0] > 4:
		print('DEAD!')
		turtle.bgcolor('red')
		turtle.exitonclick()
	else:
		print('CONGRATS!!!! The word was ' + word + '!')
		turtle.exitonclick()
'''
