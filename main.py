import fitz
import re
import random
import os

QUESTION_REGEX = re.compile(r"^\d+\. ")
ANSWER_REGEX = re.compile(r"^\([a-z]\) ")


class Question:
    def __init__(self, week: int, question: str, correct_answer: str):
        self.week = week
        self.question = question
        self.correct_answer = correct_answer

    def __str__(self) -> str:
        return "Week: {}\nQuestion: {}\nCorrect Answer: {}".format(self.week, self.question, self.correct_answer)

    def __repr__(self) -> str:
        return self.__str__()


questions_bank = []
answers = {}


def parse_question(week: int, question: list):
    question_number = question[0]["text"].split(".")[0]
    question_str = "\n".join([span["text"] for span in question])
    answer = answers[question_number]
    # print(question_str)
    questions_bank.append(Question(week, question_str, answer))
    # print(question_number)
    # print(answer)
    # for line in question:
    # if QUESTION_REGEX.match(line):
    # print(line)


boarders = list(map(int, input("Enter the range of weeks (boarders are included): ").split()))
for i in range(boarders[0], boarders[1] + 1):
    question_filepath = "./lessons/week{:02}/Week{:02}_Sample_Questions.pdf".format(
        i, i)
    key_filepath = "./lessons/week{:02}/Week{:02}_Sample_Key.pdf".format(i, i)

    question_doc = fitz.open(question_filepath)
    key_doc = fitz.open(key_filepath)

    q_met = False
    for page in key_doc:
        text = page.get_text("dict")
        blocks = text["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if "Question" in span["text"]:
                            q_met = True
                            continue
                        if "Answer Key" in span["text"]:
                            q_met = False
                        if q_met:
                            if span["text"][0].isdigit():
                                answers[span["text"]] = '0'
                                prev = span["text"]
                            else:
                                answers[prev] = span["text"][1]
    key_doc.close()

    current_question = []
    # skip the first page
    for page in question_doc:
        text = page.get_text("dict")
        blocks = text["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # print(span["text"])
                        if QUESTION_REGEX.match(span["text"]):
                            # if first_iteration
                            if len(current_question) == 0:
                                current_question.append(span)
                            else:
                                parse_question(i, current_question)
                                current_question = [span]
                        else:
                            if "Version A" in span["text"] or "Page" in span["text"]:
                                continue
                            if len(current_question) > 0:
                                current_question.append(span)
                        # # if is normal font
                        # if span["font"] is "CMR12":
                        #     # if is question
                        #     pass
                        # # if is monospaced font
                        # if span["font"] is "CMTT12":
                        #     pass

    question_doc.close()

print("---------------------------------LETS-GO-!-----------------------------------")
number_of_questions = 0
correct = 0
questions_bank_copy = questions_bank[:]
hard_questions = []
while True:
    if len(questions_bank_copy) == 0:
        print("You have answered all the questions! Congratulations!")
        print("Final accuracy:", round(correct / number_of_questions * 100, 2),
              '(' + str(correct) + '/' + str(number_of_questions) + ')')
        print("You had difficulties with these questions:")
        for question in hard_questions:
            print(question[0].question)
            print('                                                                                         ')
            print('Your answer:', question[1], 'Correct answer:', question[0].correct_answer)
            print('-----------------------------------------------------------------------------------------')
            print('                                                                                         ')

        break
    number_of_questions += 1
    index = random.randint(0, len(questions_bank_copy) - 1)
    question = questions_bank_copy[index]
    print(question.question)
    answer = input("Answer?")
    answer = answer.lower()
    if answer == question.correct_answer:
        correct += 1
        questions_bank_copy.pop(index)
        print("Correct!")
    else:
        hard_questions.append([questions_bank_copy[index], answer])
        print("Wrong! The correct answer is: {}".format(question.correct_answer))
        questions_bank_copy.pop(index)


    command = input("Print 's' for stats; 'r' to reset questions&stats; 'd' for difficult questions;"
                    "\n or any other button to continue...").lower()
    while (command == 's' or command == 'r' or command == 'd'):
        if command == 's':
            print('-----------------------------------------------------------------------------------------')
            print("Accuracy:", round(correct / number_of_questions * 100, 2),
                  '(' + str(correct) + '/' + str(number_of_questions) + ')')
            print('-----------------------------------------------------------------------------------------')

        if command == 'r':
            questions_bank_copy = questions_bank[:]
            print('-----------------------------------------------------------------------------------------')
            print("Question bank was reset")
            print('-----------------------------------------------------------------------------------------')

        if command == 'd':
            print("You had difficulties with these questions:")
            for question in hard_questions:
                print(question[0].question)
                print('                                                                                         ')
                print('Your answer:', question[1], 'Correct answer:', question[0].correct_answer)
                print('-----------------------------------------------------------------------------------------')
                print('                                                                                         ')

        command = input("Print 's' for stats; 'r' to reset questions&stats; 'd' for difficult questions;"
                        "\n or any other button to continue...").lower()

    print('                                                                                         ')
    print('#########################################################################################')
    print('                                                                                         ')
