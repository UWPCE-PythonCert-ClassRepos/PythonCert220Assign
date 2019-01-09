class Divider(object):

    @staticmethod
    def calc(operand_1, operand_2):
        try:
            answer = operand_1/operand_2
            print(answer)
            return answer
        except ZeroDivisionError:
            print("denominator cannot be zero")
