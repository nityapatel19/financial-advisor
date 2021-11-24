

class Budget: # this class will be derived from goals class as mentioned in the chart
    salary = 360000 #temperory because it will not present here, it will be derived from Goals class
    inc_percent = 0.1 #temperory because it will not present here, it will be derived from Goals class
    need = 0.5 #by default need 30%
    want = 0.3 #by default want 30%
    investment = 0.2 #by default investment 20%
    year = 15 #by default year to be displayed is 15yrs
    monthlyNeed = [0]*(year+1)
    monthlyWant = [0]*(year+1)
    monthlyInvestment = [0]*(year+1)
    increment = [0]*(year+1)
    endingSalary = [0]*(year+1)

    @classmethod
    def __init__(cls, *args):

        if (len(args) != 0):
            cls.need = args[0] / 100
            cls.want = args[1] / 100
            cls.investment = args[2] / 100
            cls.year = args[3]
            cls.endingSalary = [0] * (cls.year + 1)
            cls.monthlyNeed = [0] * (cls.year + 1)
            cls.monthlyWant = [0] * (cls.year + 1)
            cls.monthlyInvestment = [0] * (cls.year + 1)
            cls.increment = [0] * (cls.year + 1)

    @classmethod
    def endingSals(cls):
        cls.endingSalary[1] = cls.salary
        for i in range(2, int(cls.year + 1)):
            cls.endingSalary[i] = round(cls.endingSalary[i - 1]*(1 + cls.inc_percent))

    @classmethod
    def increments(cls):
        for i in range(2, int(cls.year + 1)):
            cls.increment[i] = cls.endingSalary[i] - cls.endingSalary[i - 1]

    @classmethod
    def monthlyInvestments(cls):
        cls.monthlyInvestment[1] = (cls.salary * cls.investment) / 12
        for i in range(2, int(cls.year + 1)):
            cls.monthlyInvestment[i] = round(cls.monthlyInvestment[i - 1] + (cls.increment[i] * cls.need) / 12)

    @classmethod
    def monthlyWants(cls):
        cls.monthlyWant[1] = (cls.salary * cls.want) / 12
        for i in range(2, int(cls.year + 1)):
            cls.monthlyWant[i] = round(cls.monthlyWant[i - 1] + (cls.increment[i] * cls.want) / 12)

    @classmethod
    def monthlyNeeds(cls):
        cls.monthlyNeed[1] = (cls.salary * cls.need) / 12
        for i in range(2, int(cls.year + 1)):
            cls.monthlyNeed[i] = round(cls.monthlyNeed[i - 1] + (cls.increment[i] * cls.investment) / 12)



obj = Budget(50, 30, 20, 20)  # need,want,investment,data to be displayed uptill which year.


#remember below class method call order
obj.endingSals()
obj.increments()
obj.monthlyNeeds()
obj.monthlyWants()
obj.monthlyInvestments()

print("Monthly Needs")
for i in range (1,obj.year+1):
    print(obj.monthlyNeed[i],end=" ")
print()
print("\nMonthly Wants")
for i in range (1,obj.year+1):
    print(obj.monthlyWant[i],end=" ")
print()
print("\nMonthly Investments")
for i in range (1,obj.year+1):
    print(obj.monthlyInvestment[i],end=" ")