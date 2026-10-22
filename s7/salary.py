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

print(salary(20,'ms',1))

