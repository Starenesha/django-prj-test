

def consuptions(a):
    copy = a[:]

    a_ = a[:]
    date = []
    value = []


    for dict in a_:
        temp = dict['_d_a_t_e_']
        date.append(temp)
        a_ = dict

    for dict in copy:
        temp=dict['_v_a_l_u_e_']
        value.append(temp)
        copy = dict

    value_ = list(map(float,value))

    diff = [value_[n-1] - value_[n] for n in range(1, len(value_))]
    date_ = date[1:]

    result_lst = list(zip(date, date_, diff))

    return result_lst
