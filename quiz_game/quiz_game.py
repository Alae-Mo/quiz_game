import sys
import random
import requests
import html

#-------------------------------------------------------------------------------------------------------------------------------------
def main():
    print("Quiz Game")
    n_qsts= int(input(f"Choose a number of questions: "))
    wrongs = []
    while True:
        ready = input("Are you ready (y/n)? ").strip().lower()
        if ready == 'y':
            score = API_questions(wrongs, n_qsts)
            break
        elif ready == "n":
            sys.exit("See you next time when you are ready!")
        else:
            print("(Error) You need to input y or n.")
            
        
    
    print(f"\nYour score is: {score}/{n_qsts}")
    print(grading(score, n_qsts) + "\n")
    print_corrections(wrongs)
    

#-------------------------------------------------------------------------------------------------------------------------------------

def API_questions(wrongs, n_qsts):
    url = f"https://opentdb.com/api.php?amount={n_qsts}&difficulty=easy"
    response = requests.get(url)
    data = response.json()
    

    score = 0
    for i, q_data in enumerate(data["results"], start=1):
        print("\nCategory:", q_data["category"])
        print("Type:", q_data["type"])

        q_question = html.unescape(q_data["question"])
        print(f"Q: {q_question}" )

        if q_data["type"] == 'multiple':
            correct_answer = html.unescape(q_data["correct_answer"])
            choices = [correct_answer] + [html.unescape(c) for c in q_data["incorrect_answers"]]
            random.shuffle(choices)

            for idx, choice in enumerate(choices, start=1):
                print(f"{idx}. {choice}")
            
            while True:
                try:
                    answer_idx = int(input("Choose a number: "))
                    user_answer = choices[answer_idx - 1]
                    break
                except (ValueError, IndexError):
                    print("Wrong input!")
                    continue
        
        elif q_data["type"] == 'boolean':
            correct_answer = html.unescape(q_data["correct_answer"])
            print("1.True\n 2.False")
            while True:
                try:
                    answer_idx = int(input("Your choice: "))
                    user_answer = "True" if answer_idx == 1 else "False"
                    break
                except (ValueError, IndexError):
                    print("Wrong input!")
                    continue



        if user_answer.lower() == correct_answer.lower():
            score += 1
        else:
            wrongs.append((i, q_question, user_answer, correct_answer))
    
    return score


#-------------------------------------------------------------------------------------------------------------------------------------

def grading(score, n_qsts): #returns str
    if score == n_qsts:
        return "Excellent!"
    elif (n_qsts / 2) < score < n_qsts:
        return "Good job!"
    elif score > 0:
        return "Keep trying!"
    else:
        return "Better luck next time!"

#-------------------------------------------------------------------------------------------------------------------------------------

def print_corrections(wrongs):
    if not wrongs:
        print("You got all the answers right!")
        return
    
    print("Correction:")
    #for each wrong answer do this (shows you where you're wrong)
    for q, question, user_answer, correct_answer in wrongs:
        print(f"Question {q} was answered wrongly: ")
        print(f"Q: {question}")
        print(f"Your answer: {user_answer}")
        print(f"Right answer: {correct_answer} \n")


#-------------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    main()

