from curses.textpad import Textbox
from typing import TypedDict, Dict
import enum
from User import *
import curses
from curses import wrapper

# Class Rates
annualRates = 10
jobChange = 30
inflation = 6
investmentReturn = 12


# # class User
# userName = user.name
# DOB = user.dob
# PAN = user.pan
# mobileNumber = user.mobile
# currentInhandSalary = user.in_hand_salary
# email = user.email

# class User

class goaml_damta:
    def __init__(self, amoumnt_amt_premsent: float, years_from_now: int):
        self.amoumnt_amt_premsent = amoumnt_amt_premsent
        self.years_from_now = years_from_now
        self.value_at_that_time = (1 + (inflation / 100)) * amoumnt_amt_premsent


class GoamlTypes(enum.Enum):
    short_goals = 0
    medium_goals = 1
    long_goals = 2


class goaml(TypedDict):
    name: str
    goal_type: GoamlTypes
    goaml: goaml_damta


class Goals(User, Rate):
    abcd = 32

    def __init__(self, **kwargs):
        # self.shortGoals: List[goaml] #0-3 years
        # self.mediumGoals: List[goaml] # 3- 10 years
        # self.longGoals: List[goaml]
        super().__init__(kwargs['name'], kwargs['email'], kwargs['dob'], kwargs['mobile'], kwargs['pan'], kwargs['ihs'])
        self.goals: Dict[str, goaml] = dict()

    def add_goal(self, name, present_amount, years):
        if years <= 3:
            self.goals[name] = goaml(name=name, goal_type=GoamlTypes.short_goals,
                                     goaml=goaml_damta(present_amount, years))

        elif 3 < years <= 10:
            self.goals[name] = goaml(name=name, goal_type=GoamlTypes.medium_goals,
                                     goaml=goaml_damta(present_amount, years))

        else:
            self.goals[name] = goaml(name=name, goal_type=GoamlTypes.long_goals,
                                     goaml=goaml_damta(present_amount, years))

    def get_goals(self, *names):
        return [self.goals.get(name) for name in names]


class Budget(Goals):  # this class will be derived from goals class as mentioned in the chart

    # salary = 360000
    inc_percent = 0.1  # temperory because it will not present here, it will be derived from Goals class
    __need = 0.5  # by default need 50%
    __want = 0.3  # by default want 30%
    __investment = 0.2  # by default investment 20%
    year = 45  # by default year to be displayed is 15yrs
    monthlyNeed = [0] * (year + 1)
    monthlyWant = [0] * (year + 1)
    monthlyInvestment = [0] * (year + 1)
    __increment = [0] * (year + 1)
    __endingSalary = [0] * (year + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if len(kwargs) != 0:
            # self.need = kwargs['need'] / 100
            # self.want = kwargs['want'] / 100
            # self.investment = kwargs['investment'] / 100
            # self.year = kwargs['year']
            self.__endingSalary = [0] * (self.year + 1)
            self.monthlyNeed = [0] * (self.year + 1)
            self.monthlyWant = [0] * (self.year + 1)
            self.monthlyInvestment = [0] * (self.year + 1)
            self.__increment = [0] * (self.year + 1)

    def endingSals(self):
        self.__endingSalary[1] = self.in_hand_salary
        for i in range(2, int(self.year + 1)):
            self.__endingSalary[i] = round(self.__endingSalary[i - 1] * (1 + self.inc_percent))

    def increments(self):
        for i in range(2, int(self.year + 1)):
            self.__increment[i] = self.__endingSalary[i] - self.__endingSalary[i - 1]

    def monthlyInvestments(self):
        self.monthlyInvestment[1] = (self.in_hand_salary * self.__investment) / 12
        for i in range(2, int(self.year + 1)):
            self.monthlyInvestment[i] = round(self.monthlyInvestment[i - 1] + (self.__increment[i] * self.__need) / 12)

    def monthlyWants(self):
        self.monthlyWant[1] = (self.in_hand_salary * self.__want) / 12
        for i in range(2, int(self.year + 1)):
            self.monthlyWant[i] = round(self.monthlyWant[i - 1] + (self.__increment[i] * self.__want) / 12)

    def monthlyNeeds(self):
        self.monthlyNeed[1] = (self.in_hand_salary * self.__need) / 12
        for i in range(2, int(self.year + 1)):
            self.monthlyNeed[i] = round(self.monthlyNeed[i - 1] + (self.__increment[i] * self.__investment) / 12)


class Cashflow(Budget):
    can_achieve = []
    wants_amount = []
    invest_ratio = 50
    wants_saved = []
    investment_amount = [0]
    annual_goals = [0] * 50

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        self.can_achieve = []
        self.wants_amount = list(map(lambda x: 12 * x, [0] + self.monthlyWant))
        self.invest_ratio = 50
        self.wants_saved = list(
            map(lambda x: x * (self.invest_ratio / 100) * (1 + investmentReturn / 100), self.wants_amount))

        self.investment_amount = [0]
        [self.investment_amount.append(
            round((self.investment_amount[-1] + self.monthlyInvestment[i] * 12) * (1 + investmentReturn / 100))) for i
            in range(1, len(self.monthlyInvestment) - 1)]

        self.annual_goals = [0] * 50

    def update_goals(self):
        for year in range(1, 46):
            for goal_name in self.goals.keys():
                if self.goals[goal_name]['goaml'].years_from_now == year:
                    self.annual_goals[year - 1] += self.goals[goal_name]['goaml'].value_at_that_time

        temp = list(map(lambda x: 12 * x, self.monthlyWant))
        for year in range(1, 46):
            if self.annual_goals[year - 1] <= self.wants_saved[year - 1]:
                self.can_achieve.append([True, year])
                self.wants_saved[year] += (self.wants_saved[year - 1] - self.annual_goals[year - 1])
            else:
                extra = self.wants_saved[year - 1] - self.annual_goals[year - 1]
                self.wants_saved[year] -= extra
                for i in range(year, 46):
                    if self.annual_goals[i - 1] <= self.wants_saved[year - 1]:
                        self.can_achieve.append([False, i])
                        break


if __name__ == '__main__':

    stdscr = curses.initscr()


    def home_page(stdscr, error):
        stdscr.clear()

        if not error:
            stdscr.addstr(0, 15, "Home Page", curses.A_STANDOUT | curses.A_UNDERLINE)
        else:
            stdscr.addstr(0, 15, f"{error}", curses.A_STANDOUT | curses.A_UNDERLINE)

        stdscr.addstr(2, 0, "Login (L)")
        stdscr.addstr(2, 15, "Register (R)")

        stdscr.refresh()

        while ch := stdscr.getch():
            if ch == ord('l'):
                return "L"
            elif ch == ord('r'):
                return "R"


    def login_page(stdscr, error):
        stdscr.clear()
        if not error:
            stdscr.addstr(0, 15, "Login Page", curses.A_STANDOUT | curses.A_UNDERLINE)
        else:
            stdscr.addstr(0, 15, f"{error}", curses.A_STANDOUT | curses.A_UNDERLINE)
        stdscr.addstr(2, 0, "Enter E-Mail: ")
        stdscr.addstr(4, 0, "Enter Password: ")

        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 2, 14)
        box = Textbox(edit_win)
        box.edit()
        login_email = box.gather()[:-1]
        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 4, 16)
        box = Textbox(edit_win)
        box.edit()
        login_password = box.gather()[:-1]
        stdscr.refresh()

        try:
            user = get_user(login_email, login_password)
        except UserNotFound:
            return None, "User not registered"
        except WrongPassword:
            return None, "Credentials do not match"
        except UserAlreadyExists:
            return None, "User Already Exists"
        except InvalidPAN:
            return None, "PAN Number should be 10 digits"
        except InvalidMobile:
            return None, "Mobile Number should be 10 digits"

        stdscr.refresh()
        return user, None


    def registration_page(stdscr, error=None):
        stdscr.clear()
        if not error:
            stdscr.addstr(0, 15, "Registration Page", curses.A_STANDOUT | curses.A_UNDERLINE)
        else:
            stdscr.addstr(0, 15, f"{error}", curses.A_STANDOUT | curses.A_UNDERLINE)
        stdscr.addstr(2, 0, "Enter Name: ")
        stdscr.addstr(4, 0, "Enter E-Mail: ")
        stdscr.addstr(6, 0, "Date of Birth (DD/MM/YYYY): ")
        stdscr.addstr(8, 0, "PAN: ")
        stdscr.addstr(10, 0, "Mobile Number: ")
        stdscr.addstr(12, 0, "In Hand Salary: ")
        stdscr.addstr(14, 0, "Create Password: ")

        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 2, 12)
        box = Textbox(edit_win)
        box.edit()
        regd_name = box.gather()[:-1]
        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 4, 14)
        box = Textbox(edit_win)
        box.edit()
        regd_email = box.gather()[:-1]
        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 6, 28)
        box = Textbox(edit_win)
        box.edit()
        regd_dob = box.gather()[:-1]
        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 8, 5)
        box = Textbox(edit_win)
        box.edit()
        regd_pan = box.gather()[:-1]
        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 10, 15)
        box = Textbox(edit_win)
        box.edit()
        regd_mobile = box.gather()[:-1]
        stdscr.refresh()

        edit_win = curses.newwin(1, 30, 12, 16)
        box = Textbox(edit_win)
        box.edit()
        regd_salary = box.gather()[:-1]

        edit_win = curses.newwin(1, 30, 14, 17)
        box = Textbox(edit_win)
        box.edit()
        regd_password = box.gather()[:-1]

        try:
            regd_user = Cashflow(name=regd_name, ihs=int(regd_salary), mobile=regd_mobile, dob=regd_dob,
                                 email=regd_email,
                                 pan=regd_pan, need=50, want=30, investment=20, year=45)
            add_user(regd_user, regd_password)
            user = get_user(regd_email, regd_password)
        except UserNotFound:
            return None, "User not registered"
        except WrongPassword:
            return None, "Credentials do not match"
        except UserAlreadyExists:
            return None, "User Already Exists"
        except InvalidPAN:
            return None, "PAN Number should be 10 digits"
        except InvalidMobile:
            return None, "Mobile Number should be 10 digits"

        stdscr.refresh()
        return user, None


    def dashboard(stdscr, user):

        user.endingSals()
        user.increments()
        user.monthlyNeeds()
        user.monthlyWants()
        user.monthlyInvestments()

        user.setup()

        # print(user.need, user.want, user.investment)
        #
        # print(user.endingSalary)
        # print("Monthly Needs")
        # for i in range(1, user.year + 1):
        #     print(user.monthlyNeed[i], end=" ")
        # print()
        # print("\nMonthly Wants")
        # for i in range(1, user.year + 1):
        #     print(user.monthlyWant[i], end=" ")
        # print()
        # print("\nMonthly Investments")
        # for i in range(1, user.year + 1):
        #     print(user.monthlyInvestment[i], end=" ")
        #
        # return

        stdscr.clear()
        stdscr.addstr(0, 15, f"Hello {user.name}", curses.A_STANDOUT | curses.A_UNDERLINE)
        stdscr.addstr(2, 0, "Press A to add goals.")

        while stdscr.getch() == ord('a'):
            stdscr.clear()
            stdscr.addstr(0, 15, f"Hello {user.name}", curses.A_STANDOUT | curses.A_UNDERLINE)
            stdscr.addstr(2, 0, "Press A to add goals.")
            stdscr.refresh()
            stdscr.addstr(4, 0, "Enter goal: ")
            stdscr.addstr(6, 0, "Enter present amount: ")
            stdscr.addstr(8, 0, "Enter years: ")
            stdscr.refresh()

            edit_win = curses.newwin(1, 30, 4, 12)
            box = Textbox(edit_win)
            box.edit()
            goal_name = box.gather()[:-1]
            stdscr.refresh()

            edit_win = curses.newwin(1, 30, 6, 22)
            box = Textbox(edit_win)
            box.edit()
            goal_amount = box.gather()[:-1]
            stdscr.refresh()

            edit_win = curses.newwin(1, 30, 8, 13)
            box = Textbox(edit_win)
            box.edit()
            goal_years = box.gather()[:-1]
            stdscr.refresh()
            user.add_goal(goal_name, int(goal_amount), int(goal_years))
            stdscr.addstr(10, 0, "Press A to add more goals.")
            stdscr.refresh()

        user.update_goals()

        print("Can Achieve?")
        print(user.can_achieve)
        print()
        print("Want amount:")
        print(user.wants_amount)
        print()
        print("Investment amount:")
        print(user.investment_amount)


    user, error = None, None

    while not user:
        print(error)
        l_or_r = wrapper(home_page, error)
        if l_or_r == "L":
            user, error = wrapper(login_page, error)
        else:
            user, error = wrapper(registration_page, error)

    wrapper(dashboard, user)

# stdscr.addstr(14, 0, "Press Q to exit.")
#         while True:
#             if stdscr.getch() == ord('q'):
#                 break
