import sys

def separate_qa_pairs(input_data):
    questions = []
    answers = []
    
    for pair in input_data:
        parts = pair.split(' A: ', 1)  
        question = parts[0].strip()
        answer = parts[1].strip() if len(parts) > 1 else "" 
        questions.append(question)
        answers.append(answer)
    
    return questions, answers

def save_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for line in data:
            file.write(line + '\n')

def main(input_file):
    with open(input_file, 'r') as f:
        input_data = [line.strip() for line in f if line.strip()]

    questions, answers = separate_qa_pairs(input_data)
    
    #questions to inputs.txt
    save_to_file(questions, '/Users/blakeweiss/Desktop/datalod/inputs.txt')
    
    #answers to answers.txt
    save_to_file(answers, '/Users/blakeweiss/Desktop/datalod/answers.txt')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input file as an argument.")
    else:
        main(sys.argv[1])
