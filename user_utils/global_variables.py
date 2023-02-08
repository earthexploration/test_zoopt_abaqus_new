from user_utils.get_value import get_value

def global_variables(input, input_length):
    output = get_value("./parameters.csv", input, input_length)
    return output
