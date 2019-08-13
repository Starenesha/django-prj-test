def consumption(records):
    '''Function which  create  list of tuples with consumption and date - for chart'''

#    records_ =records[:]
    value_list = [] # list with value
    date_list = [] # list with date
    
    for x in records:
        date_list.append(x.date.isoformat())
        value_list.append(x.value)
        records = x
        
#     for x in records:
#         tmp = x.value
#         value_list.append(tmp)
#         records = x

#     for x in records_:
#         tmp = x.date.isoformat()
#         date_list.append(tmp)
#         records_ = x

    diff = [value_list[n - 1] - value_list[n] for n in range(1, len(value_list))] #Performing of calculation consumptions
    result_lst = list(zip(date_list, date_list[1:], diff))  # create list of tuples with consumption and date
    return result_lst
