import random
from tkinter import *

TEXTS = [
    'For writers, a random sentence can help them get their creative juices flowing. Since the topic of the sentence is completely unknown, it forces the writer to be creative when the sentence appears. There are a number of different ways a writer can use the random sentence for creativity. The most common way to use the sentence is to begin a story. Another option is to include it somewhere in the story. A much more difficult challenge is to use it to end a story. In any of these cases, it forces the writer to think creatively since they have no idea what sentence will appear from the tool.',
    'The goal of Python Code is to provide Python tutorials, recipes, problem fixes and articles to beginner and intermediate Python programmers, as well as sharing knowledge to the world. Python Code aims for making everyone in the world be able to learn how to code for free. Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.',
    'As always, we start with the imports. Because we make the UI with tkinter, we need to import it. We also import the font module from tkinter to change the fonts on our elements later. We continue by getting the partial function from functools, it is a genius function that excepts another function as a first argument and some args and kwargs and it will return a reference to this function with those arguments. This is especially useful when we want to insert one of our functions to a command argument of a button or a key binding.'
]


class Timer:
    def __init__(self):
        # WINDOW -------------------
        self.window = Tk()
        self.window.title('Typing Speed Test')
        self.window.option_add("*Label.Font", "consolas 30")
        self.window.option_add("*Button.Font", "consolas 20")
        self.window.config(padx=20, pady=20)
        # VARIABLES -------------------
        self.passed_seconds = 0
        self.mistakes = 0
        self.correct = 0
        self.point_split = 0
        self.passedSeconds = 0
        # TEXTBOX  -------------------
        self.text = random.choice(TEXTS).lower()
        self.textbox = Text(height=10)
        self.textbox.insert(END, self.text)
        self.textbox.grid(column=0, columnspan=3, row=0, sticky=EW)
        # TEXT -------------------
        self.right_text = Label(self.window, text=self.text[self.point_split:], width=20, anchor="w")
        self.right_text.grid(column=2, row=2)
        self.left_text = Label(self.window, text=self.text[0:self.point_split], fg='grey', width=20, anchor="e")
        self.left_text.grid(column=0, row=2)
        self.current_letter = Label(self.window, text=self.text[self.point_split], fg='grey')
        self.current_letter.grid(column=1, row=3)
        # TIME & ACCURACY -------------------
        self.speed_label = Label(self.window, text=f'{self.passed_seconds} seconds', fg='grey')
        self.speed_label.grid(column=0, columnspan=2, row=4, sticky=W)
        self.accuracy_label = Label(self.window, text=f'Accuracy: %{self.calculate_accuracy()}', fg='grey')
        self.accuracy_label.grid(column=0, columnspan=3, row=4, sticky=E)

        self.is_on = None
        self.window.bind('<Key>', self.on_key_press)

        self.window.mainloop()

    def calculate_accuracy(self):
        if self.correct < 1:
            return 100
        else:
            total_letters = self.correct + self.mistakes
            accuracy = 100 - (total_letters - self.correct) / self.correct * 100
            return 0 if self.mistakes > self.correct else int(accuracy)

    def on_key_press(self, event=None):
        # Start counter if first click -------------------
        if self.is_on == None:
            self.is_on = True
            self.timer()
            self.window.after(60000, self.end_test)
        # Check input letter and move indexes if letter is correct-------------------
        try:
            if event.char.lower() == self.right_text.cget("text")[0].lower():
                self.correct += 1
                self.current_letter.config(fg='grey')
                self.right_text.config(text=self.right_text.cget('text')[1:])
                self.left_text.config(text=self.left_text.cget('text') + event.char.lower())
                self.current_letter.config(text=self.right_text.cget('text')[0])
                self.accuracy_label.config(text=f'Accuracy: %{self.calculate_accuracy()}')

                self.textbox.tag_add("start", '1.0', f'1.{len(self.left_text.cget("text"))}')
                self.textbox.tag_config("start", background="black", foreground="yellow")
            else:
                self.mistakes += 1
                self.current_letter.config(fg='red')
                self.accuracy_label.config(text=f'Accuracy: %{self.calculate_accuracy()}')

                self.textbox.tag_add("start",f'1.{len(self.left_text.cget("text"))-1}')
                self.textbox.tag_config("start", background="black", foreground="red")
        except TclError:
            pass

    def timer(self):
        if self.is_on:
            self.passed_seconds += 1
            self.speed_label.config(text=f'{self.passed_seconds} seconds')
            self.window.after(1000, self.timer)

    def end_test(self):
        self.is_on = False
        words_amount = len(self.left_text.cget('text').split(' '))

        self.left_text.destroy()
        self.right_text.destroy()
        self.current_letter.destroy()

        self.speed_label.config(fg='green')
        self.accuracy_label.config(fg='green')

        restart_button = Button(self.window, text='Restart', fg='grey', command=self.restart)
        restart_button.grid(column=1, row=3)
        result_label = Label(self.window, text=f'Words per Minute: {words_amount}', fg='grey', width=20, pady=5)
        result_label.grid(column=0, columnspan=3, row=2)

    def restart(self):
        self.window.destroy()
        Timer()


Timer()
