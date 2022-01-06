"""
This file contains the goals of the user.
"""
# Class Rates
annualRates = 0.1
jobChange = 0.3
inflation = 6
ivestmentReturn = 0.12

# class User
userName = ""
# DOB=
PAN = 0
mobileNumber = 8649668881
currentInhandSalary = 240000
email = "huehuehue@gmail.com"

from typing import TypedDict, List, Dict
import enum


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


class Goals:
    def __init__(self):
        # self.shortGoals: List[goaml] #0-3 years
        # self.mediumGoals: List[goaml] # 3- 10 years
        # self.longGoals: List[goaml]
        self.goals: Dict[str, goaml] = dict()

    def add_goal(self, name, present_amount, years):
        if years <= 3:
            self.goals[name] = goaml(name=name, goal_type=GoamlTypes.short_goals, goaml=goaml_damta(present_amount, years))

        elif 3 < years <= 10:
            self.goals[name] = goaml(name=name, goal_type=GoamlTypes.medium_goals, goaml=goaml_damta(present_amount, years))

        else:
            self.goals[name] = goaml(name=name, goal_type=GoamlTypes.long_goals,goaml=goaml_damta(present_amount, years))

    def get_goals(self, *names):
        return [self.goals.get(name) for name in names]


Selmon_Bhoi = Goals()
Selmon_Bhoi.add_goal('car', 500000, 4)
Selmon_Bhoi.add_goal('mobile', 50000, 2)
Selmon_Bhoi.add_goal('Dubai_with_Jacq', 277000, 2)


print(Selmon_Bhoi.goals['car']['goaml'].value_at_that_time)
print(Selmon_Bhoi.goals['mobile']['goaml'].years_from_now)

# for goal in Om_Nalinde.get_goals("mobile", "car"):
#     print(f"{goal.get('value_at_that_time')}\n"
#           f"{goal.get('years_from_now')}\n"
#           f"{goal.get('amoumnt_amt_premsent')}")


monthlyWant = [
    9000,
    9900,
    10890,
    11979,
    15573,
    17130,
    18843,
    20727,
    22800,
    25080,
    32604,
    35864,
    39451,
    43396,
    47735,
    52509,
    57760,
    63536,
    69890,
    76878,
    99942,
    109936,
    120930,
    133023,
    146325,
    160958,
    209245,
    230169,
    253186,
    278505,
    306356,
    336991,
    438088,
    481897,
    530087,
    583096,
    641405,
    705546,
    917210,
    1008930,
    1109824,
    1220806,
    1342886,
    1477175,
    1624893,
    0
]
monthlyInvestment = [
    6000,
    7500,
    9150,
    10965,
    16955,
    19550,
    22405,
    25545,
    29000,
    32800,
    45340,
    50774,
    56751,
    63327,
    70559,
    78515,
    87267,
    96893,
    107483,
    119131,
    157570,
    174227,
    192550,
    212705,
    234875,
    259263,
    339742,
    374616,
    412977,
    455175,
    501593,
    552652,
    721147,
    794162,
    874478,
    962826,
    1060009,
    1166910,
    1519683,
    1672551,
    1840706,
    2025676,
    2229144,
    2452958,
    2699154
]
investment_returns = 12


class Cashflow(Goals):
    def __init__(self):
        super().__init__()
        self.can_achieve = []
        self.wants_amount = list(map(lambda x: 12 * x, monthlyWant))
        self.invest_ratio = 50
        self.wants_saved = list(
            map(lambda x: x * (self.invest_ratio / 100) * (1 + investment_returns / 100), self.wants_amount))
        self.investment_amounts = [
            80640,
            191117,
            300917,
            432497,
            635951,
            870550,
            1139410,
            1445955,
            1793955,
            2187554,
            2731634,
            3340922,
            4021938,
            4781856,
            5628566,
            942181,
            1989380,
            3152099,
            4441890,
            5871459,
            7762300,
            9853025,
            12163623,
            14716080,
            17534583,
            3111153,
            7188052,
            11683441,
            16639169,
            22101270,
            28120380,
            34752202,
            43405971,
            52935916,
            63429655,
            74983569,
            87703674,
            101706590,
            119942780,
            140013389,
            162101859,
            186409976,
            213159705,
            242595207,
            274985059
        ]
        self.annual_goals = [0] * 50

    def update_goals(self):
        for year in range(1, 46):
            for goal_name in self.goals.keys():
                if self.goals[goal_name]['goaml'].years_from_now == year:
                    self.annual_goals[year - 1] += self.goals[goal_name]['goaml'].value_at_that_time

        temp = list(map(lambda x: 12 * x, monthlyWant))
        for year in range(1, 46):
            if self.annual_goals[year - 1] <= self.wants_saved[year - 1]:
                self.can_achieve.append([True, year])
                self.wants_saved[year] += (self.wants_saved[year-1] - self.annual_goals[year-1])
            else:
                extra = self.wants_saved[year - 1] - self.annual_goals[year - 1]
                self.wants_saved[year] -= extra
                for i in range(year, 46):
                    if self.annual_goals[i - 1] <= self.wants_saved[year - 1]:
                        self.can_achieve.append([False, i])
                        break


Selmon_Bhoi = Cashflow()
Selmon_Bhoi.add_goal('car', 500000, 4)
Selmon_Bhoi.add_goal('mobile', 50000, 2)
Selmon_Bhoi.add_goal('dubai', 277123, 5)
# print(Selmon_Bhoi.goals['car']['goaml'].value_at_that_time)
# print(Selmon_Bhoi.goals['car']['goaml'].years_from_now)
# print(Selmon_Bhoi.goals['mobile']['goaml'].value_at_that_time)
# print(Selmon_Bhoi.goals['mobile']['goaml'].years_from_now)
Selmon_Bhoi.update_goals()
print(Selmon_Bhoi.can_achieve)
print(Selmon_Bhoi.goals['mobile']['goaml'].value_at_that_time)
print(Selmon_Bhoi.goals['car']['goaml'].value_at_that_time)
print(Selmon_Bhoi.goals['dubai']['goaml'].value_at_that_time)
# print(Selmon_Bhoi.wants_saved)