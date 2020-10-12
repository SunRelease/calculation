# -*- coding: utf-8 -*-
# author :HXM

import random, logging, time
from sys import argv
from fractions import Fraction

# 输出日志设置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] - %(levelname)s: %(message)s')

class Check_repeated():
    '''
    检查式子是否重复
    '''

    def __init__(self):

        self.old_number = {}  # 已经存在的数字字典
        self.old_symbol = {}  # 已经存在的符号字典

    def check(self, number_list, symbol_list):
        '''
        检查式子是否重复
        :param number_list:
        :param symbol_list:
        :return:
        '''
        number_list.sort()
        symbol_list.sort()

        if self.old_number:
            '''
            对列表上的值进行比较是否相同
            '''
            for key, value in self.old_number.items():
                if value == number_list and self.old_symbol[key] == symbol_list:
                    return False
            self.old_number[key + 1] = number_list
            self.old_symbol[key + 1] = symbol_list
        else:
            self.old_number[0] = number_list
            self.old_symbol[0] = symbol_list
        return True


class Handle():
    '''
    运算和转换类
    '''
    def __init__(self):
        pass

    def tran_to_str(self, scores):
        '''
        分数转换为字符串,转换为符合要求额字符串
        :param scores:
        :return:
        '''
        try:
            molecular = scores.numerator  # 获取分子
            denominator = scores.denominator  # 获取分母
            if denominator == 0:
                return False
            int_number = int(molecular / denominator)  # 求整数
            remainder_number = molecular % denominator  # 取余数

            if remainder_number == 0 or denominator >= molecular:
                return str(Fraction(molecular, denominator))
            else:
                return str(int_number) + '\'' + str(Fraction(remainder_number, denominator))
        except Exception as e:
            logging.error(e)

    def tran_to_scores(self, string):
        '''
        字符串转换为分数
        :param string:
        :return:
        '''
        # try:
        if '\'' in string:
            full_scores = string.split('\'')
            int_number = int(full_scores[0])  # 获取假分数
            molecular = int((full_scores[1].split('/'))[0])  # 真分数的分子
            denominator = int((full_scores[1].split('/'))[1])  # 真分数的分母
            return Fraction((int_number * denominator + molecular), denominator)
        elif '/' in string:
            molecular = int((string.split('/'))[0])
            denominator = int((string.split('/'))[1])
            return Fraction((molecular, denominator))
        else:
            return Fraction(int(string), 1)

        # except Exception as e:
        #
        #     logging.error(e)

    def account(self, scores_one, scores_two, symbol):
        '''
        四则运算
        :param scores_one:
        :param scores_two:
        :param symbol:
        :return:
        '''
        # try:
        if (symbol == '+'):  # 加法
            return scores_one + scores_two
        elif (symbol == '-'):  # 减法
            if scores_one < scores_two:  # 判断是否为负数
                return False
            else:
                return scores_one - scores_two
        elif (symbol == '*'):  # 乘法
            return scores_one * scores_two
        else:  # 除法
            if scores_two == 0:
                return False
            else:
                return scores_one / scores_two
        # except Exception as e:
        #     logging.error(e)


class Make_Exercise():

    def __init__(self, max_number=10, max_account=10):
        self.account = max_account  # 生成题目数
        self.number_limit = max_number  # 最大自然数限制

    def make_question(self):
        '''
        制作题库
        :return:
        '''
        try:
            localtime = time.asctime(time.localtime(time.time()))  # 初始化生成题目当地时间
            with open('Exercises.txt', 'w',encoding='utf-8')as exercise_file:
                # exercise_file.write(f'questions_number:{self.account}' + f'\t localtime:{localtime}' + "\n")
                exercise_file.close()
            with open('Answers.txt', 'w',encoding='utf-8')as answer_file:
                answer_file.close()

            make_question_sequence = 0  # 从第一个数开始分析
            repeat = Check_repeated()  # 初始化监测重复类
            make_question_queue = Make_Library(repeat=repeat, max_number=self.number_limit)

            while make_question_sequence < self.account:
                choose_make = 2 + random.randint(0, 1)  # 随机生成获取两个到三个数
                if choose_make == 2:
                    make_question_queue.make_two_symbol(make_question_sequence + 1)
                elif choose_make == 3:
                    make_question_queue.make_third_symbol(make_question_sequence + 1)
                make_question_sequence = make_question_sequence + 1
        except Exception as e:
            logging.error(e)

    def confirmExe(self, exeFile, userFile):
        corrctQue = []  # 记录用户的错题和对题
        wrongQue = []
        try:
            with open(exeFile) as exeFile:  # 读取题目文件
                with open(userFile) as userFile:  # 读取用户文件
                    sequenceLine = 1  # 记录核对的第几道题
                    lineExe = exeFile.__next__()
                    # print(lineExe)
                    fracAcc = Handle()
                    for lineExe in exeFile:  # 遍历题目
                        lineExe = lineExe.strip()
                        div = lineExe.split(" ")
                        print(div)
                        # 两个数的题目
                        if len(div) == 5:
                            print(div[3])
                            frac1 = fracAcc.tran_to_scores(div[1])
                            frac2 = fracAcc.tran_to_scores(div[3])
                            rightAnswer = fracAcc.account(frac1, frac2, div[2])
                            rightAnswer = fracAcc.tran_to_str(rightAnswer)
                        # 三个数
                        elif len(div) == 7:
                            # 如果式子中有括号
                            if '(' in lineExe:
                                for locate in range(7):
                                    # 如果式子中有括号
                                    # print(div[locate])
                                    print(locate)
                                    if '(' in div[locate]:
                                        # 如果括号在左边
                                        if locate == 1:
                                            print(div[1].replace("(", ""))
                                            leftFrac = fracAcc.tran_to_scores(div[1].replace("(", ""))
                                            rightFrac = fracAcc.tran_to_scores(div[3].replace(")", ""))
                                            thirdFrac = fracAcc.tran_to_scores(div[5])

                                            firstSum = fracAcc.account(leftFrac, rightFrac, div[2])
                                            rightAnswer = fracAcc.tran_to_str(
                                                fracAcc.account(firstSum, thirdFrac, div[4]))
                                        else:
                                            leftFrac = fracAcc.tran_to_scores(div[3].replace("(", ""))
                                            rightFrac = fracAcc.tran_to_scores(div[5].replace(")", ""))
                                            thirdFrac = fracAcc.tran_to_scores(div[1])
                                            firstSum = fracAcc.account(leftFrac, rightFrac, div[4])
                                            rightAnswer = fracAcc.tran_to_str(
                                                fracAcc.account(thirdFrac, firstSum, div[2]))
                            # 如果式子没括号
                            else:
                                leftFrac = fracAcc.tran_to_scores(div[1])
                                rightFrac = fracAcc.tran_to_scores(div[3])
                                thirdFrac = fracAcc.tran_to_scores(div[5])
                                if (div[2] == '+' or div[2] == '-') and (div[4] == '*' or div[4] == "÷"):
                                    firstSum = fracAcc.account(rightFrac, thirdFrac, div[4])
                                    rightAnswer = fracAcc.tran_to_str(fracAcc.account(leftFrac, firstSum, div[2]))
                                else:
                                    firstSum = fracAcc.account(leftFrac, rightFrac, div[2])
                                    rightAnswer = fracAcc.tran_to_str(fracAcc.account(firstSum, thirdFrac, div[4]))
                        else:
                            print("题目出错了！")
                        try:
                            userAnswer = userFile.__next__().split(' ', 2)
                            # 如果用户答案还存在的话
                            if userAnswer[0] != '\n':
                                if (userAnswer[1].strip() == rightAnswer.strip()):
                                    corrctQue.append(sequenceLine)
                                else:
                                    wrongQue.append(sequenceLine)
                            # 用户答案已空
                            else:
                                wrongQue.append(sequenceLine)
                            sequenceLine = sequenceLine + 1
                        except StopIteration:
                            wrongQue.append(sequenceLine)
                            sequenceLine = sequenceLine + 1

                    print()
                    print("批卷完毕！答题情况如下：")
                    print("Corrct: " + str(len(corrctQue)))
                    print(str(corrctQue))
                    print("Wrong: " + str(len(wrongQue)))
                    print(str(wrongQue))

                    # 答题情况写入Grade.txt
                    with open("Grade.txt", 'w',encoding='utf-8') as grade_file:
                        grade_file.write("Corrct: " + str(len(corrctQue)))
                        grade_file.write(str(corrctQue) + '\n')
                        grade_file.write("Wrong: " + str(len(wrongQue)))
                        grade_file.write(str(wrongQue) + '\n')
        except FileNotFoundError:
            print("找不到文件！请重新输入！")


class Make_Library():
    '''
    初始化题库类
    '''
    def __init__(self, repeat, max_number):
        '''
        初始化生成
        '''
        self.repeat = repeat
        self.max_number = max_number

    def make_two_symbol(self, sequence):
        '''

        :param sequence:
        :return:
        '''
        try:
            while True:
                handle = Handle()
                symbol = self.random_symbol()
                number_list = []
                symbol_list = []
                first_num = self.random_scores()
                second_num = self.random_scores()

                questions = ''
                real_answer = ''
                number_list.append(str(first_num) + ',' + str(second_num))
                symbol_list.append(symbol)

                if (self.repeat.check(number_list, symbol_list) == True):
                    real_answer = handle.account(first_num, second_num, symbol)
                    if real_answer != False:

                        real_answer = str(real_answer)
                        questions = str(sequence) + '. ' + handle.tran_to_str(first_num) + ' ' + symbol + ' ' + handle.tran_to_str(
                            second_num) + " ="
                    else:
                        continue
                else:
                    continue
                with open("Exercises.txt", 'a', encoding='utf-8')as exercise_file:
                    exercise_file.write(questions + "\n")
                    exercise_file.close()
                with open("Answers.txt", 'a', encoding='utf-8')as answer_file:
                    answer_file.write(str(sequence) + '. ' + real_answer + "\n")
                    answer_file.close()

                break
        except Exception as e:
            logging.error(e)

    def make_third_symbol(self, sequence):
        '''
        生成三个数值运算符
        :param sequence:
        :return:
        '''
        # try:
        while True:
            frac_Handle = Handle()
            # 生成相应的数字和符号
            sign1 = self.random_symbol()
            sign2 = self.random_symbol()
            numberList = []
            signList = []
            firstNum = self.random_scores()
            secondNum = self.random_scores()
            thirdNum = self.random_scores()

            question = ''
            rightAnswer = ''
            numberList.append(str(firstNum) + ',' + str(secondNum) + ',' + str(thirdNum))
            signList.append(sign1 + ',' + sign2)
            if self.repeat.check(numberList, signList) == True:  # 检测是否重复
                brackets = random.randint(0, 2)  # 随机生成括号的位置
                # 不生成括号
                if (brackets == 0):
                    question = str(sequence) + ". " + frac_Handle.tran_to_str(
                        firstNum) + " " + sign1 + " " + frac_Handle.tran_to_str(
                        secondNum) + " " + sign2 + " " + frac_Handle.tran_to_str(thirdNum) + " ="
                    # 如果前面是加号和减号而后面不是
                    if (sign1 == '+' or sign1 == '-') and (sign2 == '*' or sign2 == '÷'):
                        firstSum = frac_Handle.account(secondNum, thirdNum, sign2)
                        if firstSum != False:
                            rightAnswer = frac_Handle.account(firstNum, firstSum, sign1)
                            if rightAnswer != False:
                                rightAnswer = frac_Handle.tran_to_str(rightAnswer)
                            else:
                                continue
                        else:
                            continue
                    # 其他情况
                    else:
                        firstSum = frac_Handle.account(firstNum, secondNum, sign1)
                        if firstSum != False:
                            rightAnswer = frac_Handle.account(firstSum, thirdNum, sign2)
                            if rightAnswer != False:
                                rightAnswer = frac_Handle.tran_to_str(rightAnswer)
                            else:
                                continue
                        else:
                            continue
                # 左边加一个括号：
                elif (brackets == 1):  # 左边加括号
                    question = str(sequence) + ". (" + frac_Handle.tran_to_str(
                        firstNum) + " " + sign1 + " " + frac_Handle.tran_to_str(
                        secondNum) + ") " + sign2 + " " + frac_Handle.tran_to_str(thirdNum) + " ="
                    firstSum = frac_Handle.account(firstNum, secondNum, sign1)
                    if firstSum != False:
                        rightAnswer = frac_Handle.account(firstSum, thirdNum, sign2)
                        if rightAnswer != False:
                            rightAnswer = frac_Handle.tran_to_str(rightAnswer)
                        else:
                            continue
                    else:
                        continue
                # 右边加括号
                else:
                    question = str(sequence) + ". " + frac_Handle.tran_to_str(
                        firstNum) + " " + sign1 + " (" + frac_Handle.tran_to_str(
                        secondNum) + " " + sign2 + " " + frac_Handle.tran_to_str(thirdNum) + ") ="

                    firstSum = frac_Handle.account(secondNum, thirdNum, sign2)
                    if firstSum != False:
                        rightAnswer = frac_Handle.account(firstNum, firstSum, sign1)
                        if rightAnswer != False:
                            rightAnswer = frac_Handle.tran_to_str(rightAnswer)
                        else:
                            continue
                    else:
                        continue

                with open("Exercises.txt", 'a',encoding='utf-8') as exercise_file:
                    exercise_file.write(question + "\n")
                    exercise_file.close()
                with open("Answers.txt", 'a',encoding='utf-8') as Answer_file:
                    Answer_file.write(str(sequence) + ". " + rightAnswer + "\n")
                    Answer_file.close()
                break
            # 运算式子重复
            else:
                continue
        # except Exception as e:
        #     logging.error(e)

    def random_symbol(self):
        '''
        随机生成四则运算符号
        :return:
        '''
        random_symbol = random.randint(1, 4)
        if random_symbol == 1:
            symbol = '+'
        elif random_symbol == 2:
            symbol = '-'
        elif random_symbol == 3:
            symbol = '*'
        else:
            symbol = '÷'
        return symbol

    def random_scores(self):
        '''
        随机生成分数
        :return:
        '''
        try:
            while (True):
                molecular = random.randint(0, self.max_number)
                denominator = random.randint(1, self.max_number)
                num = Fraction(molecular, denominator)
                if num:
                    break
            return num
        except Exception as e:
            logging.error(e)

    def random_digital(self):
        '''
        随机生成自然数
        :return:
        '''
        try:
            while (True):
                num = random.randint(0, self.max_number)
                if num:
                    break
            return num
        except Exception as  e:
            logging.error(e)


class Run():
    '''
    运行主函数
    '''

    def running(self, argv):
        inputLength = len(argv)
        # try:
        if (inputLength == 5) and ('-r' in argv) and ('-n' in argv):  # 判断并获取命令行参数，比如最大范围和题目道数
            for point in range(inputLength):
                if argv[point] == '-r':
                    max_number = int(argv[point + 1])
                elif argv[point] == '-n':
                    max_account = int(argv[point + 1])
                else:
                    continue
            make_Exercises = Make_Exercise(max_account=max_account, max_number=max_number)
            make_Exercises.make_question()
            logging.info("计算题答案和题目生成完毕！")

        elif (inputLength == 5) and (argv[1] == '-e') and (argv[3] == '-a'):  # 核对获取用户文件和输出比分
            print(argv[4])
            make_Exercises = Make_Exercise()
            check_file = argv[2]
            answer_file = argv[4]
            make_Exercises.confirmExe(check_file, answer_file)
            logging.info("核对完毕,成绩已经存入文本中！")
        # except Exception as e:
        #     logging.error("参数设置不正确，请确认参数输入无误！")


if __name__ == '__main__':
    run = Run()
    # argv = ['.\\Myapp.py', '-n', '10', '-r', '10']
    run.running(argv)
