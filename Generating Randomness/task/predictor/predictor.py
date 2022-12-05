import random


def obtain_user_string_training(valid_user_input, max_length_string=None):
    final_string = ""
    print("Please give AI some data to learn...")
    print("The current data length is 0, 100 symbols left")
    while True:
        print("Print a random string containing 0 or 1:")
        user_input = input()
        user_input = obtain_valid_string(user_input, valid_user_input)
        final_string += user_input
        len_final_string = len(final_string)
        if max_length_string > len_final_string:
            print(f"The current data length is {len_final_string}, {max_length_string - len_final_string} symbols left")
        else:
            return final_string


def obtain_valid_string(input_string, valid_inputs):
    return ''.join([letter for letter in input_string if letter in valid_inputs])


def obtain_user_string(valid_user_input):
    is_exit = False
    print("Print a random string containing 0 or 1:")
    user_input = input()
    is_exit = (user_input == "enough")
    user_input = obtain_valid_string(user_input, valid_user_input)
    return dict(is_exit=is_exit, input=user_input)


def generate_binary(number):
    partial_number = number % 2
    if number <= 1:
        return f"{partial_number}"
    else:
        return generate_binary(number // 2) + f"{partial_number}"


def generate_binary_filled(number, generator_combinations):
    return generate_binary(number).zfill(generator_combinations)


def evaluate_triads(random_string, valid_user_input, triad_length_combinations):
    valid_options = len(valid_user_input)
    numbers_triads = valid_options ** triad_length_combinations
    triads_result = dict()
    for number in range(numbers_triads):
        triad = generate_binary_filled(number, triad_length_combinations)
        triads_result.update({triad: {"0": 0, "1": 0}})

    word = random_string[:3]
    for number in random_string[3:]:
        triad = triads_result.get(word)
        triad[number] = triad[number] + 1
        word = word[1:] + number

    return triads_result


def predict_string(user_money, user_string, trained_triads, triad_length_combinations):
    if len(user_string) < triad_length_combinations:
        return user_money

    total_prediction = len(user_string[triad_length_combinations:])
    correct_prediction = 0
    max_number = (2 ** triad_length_combinations) - 1
    string_predicted = generate_binary_filled(random.randint(0, max_number), triad_length_combinations)

    key_triad = user_string[:triad_length_combinations]
    for number in user_string[triad_length_combinations:]:
        triad = trained_triads.get(key_triad)

        if triad["0"] > triad["1"]:
            next_number = 0
        elif triad["1"] > triad["0"]:
            next_number = 1
        else:
            next_number = random.randint(0, 1)

        if next_number == int(number):
            correct_prediction += 1

        key_triad = key_triad[1:] + number
        string_predicted += str(next_number)

    correct_percentage = (correct_prediction / total_prediction) * 100
    user_money += (total_prediction - correct_prediction)
    user_money -= correct_prediction

    print("prediction:")
    print(f"{string_predicted}")
    print()
    print(f"Computer guessed right {correct_prediction} out of {total_prediction} symbols "
          f"({correct_percentage:.2f} %)")
    print(f"Your balance is now ${user_money}")

    return user_money


def main():
    max_length_string = 100
    user_money = 1_000
    valid_user_input = ["0", "1"]
    triad_length_combinations = 3

    training_string = obtain_user_string_training(valid_user_input, max_length_string)
    print("Final data string:")
    print(training_string)
    print()
    trained_triads = evaluate_triads(training_string, valid_user_input, triad_length_combinations)
    print("You have $1000. Every time the system successfully predicts your next press, you lose $1.")
    print("Otherwise, you earn $1. Print \"enough\" to leave the game. Let's go!")
    while True:
        user_dict = obtain_user_string(valid_user_input)
        if user_dict["is_exit"] or user_money <= 0:
            print("Game over!")
            return
        else:
            user_input = user_dict["input"]
            user_money = predict_string(user_money, user_input, trained_triads, triad_length_combinations)
            training_string += user_input
            trained_triads = evaluate_triads(training_string, valid_user_input, triad_length_combinations)


if __name__ == "__main__":
    main()
