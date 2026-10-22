def salary(exp, edu, job, base_salary = 20000000):
    salary = base_salary
    salary = salary + .1 * exp * salary
    edu_grade = {
        'phd':.4,
        'ms':.3,
        'bc':.2
    }.get(edu, 0)
    salary = salary + edu_grade * salary
    '''
    match edu:
        case 'phd':
            edu_grade = .4
        case 'ms':
            edu_grade = .3
        case 'bc':
            edu_grade = .2
        case _:
            edu_grade = 0
    '''
    if job == 1:
        salary += .2 * salary
    return salary

def tax(salary):
    tax = 0
    if salary >= 40000000:
        tax +=  (salary - 40000000)* .1
    return tax

def insu(salary):
    return salary * .07

def net_salary(salary):
    return salary - tax(salary) - insu(salary)

if __name__ == '__main__':    
    p1_salary = salary(20,'ms',1)
    p1_net_salary = net_salary(p1_salary)
    print(f'p1 salary = {p1_salary} , net salary = {p1_net_salary}')

    p2_salary = salary(2,'ms',1,25000000)
    p2_net_salary = net_salary(p2_salary)
    print(f'p2 salary = {p2_salary} , net salary = {p2_net_salary}')

