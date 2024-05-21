import sys

def split_conversations(input_file_path, user_output_path, bot_output_path):
    #Open the input file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        user_dialogues = []
        bot_dialogues = []

        for line in input_file:
            clean_line = line.strip()
            #line starts with 'User:' or 'Bot:' and process accordingly
            if clean_line.startswith('User:'):
                user_dialogues.append(clean_line[len('User:'):].strip())
            elif clean_line.startswith('Bot:'):
                bot_dialogues.append(clean_line[len('Bot:'):].strip())

    #user dialogues to the user output file
    with open(user_output_path, 'w', encoding='utf-8') as user_file:
        for dialogue in user_dialogues:
            user_file.write(dialogue + '\n')

    #bot dialogues to the bot output file
    with open(bot_output_path, 'w', encoding='utf-8') as bot_file:
        for dialogue in bot_dialogues:
            bot_file.write(dialogue + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
    else:
        input_file_path = sys.argv[1]
        user_output_path = '/Users/blakeweiss/Desktop/newdatacleaning/datathatiscleaned/user_output.txt'
        bot_output_path = '/Users/blakeweiss/Desktop/newdatacleaning/datathatiscleaned/bot_output.txt'
        split_conversations(input_file_path, user_output_path, bot_output_path)
