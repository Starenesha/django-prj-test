#records = CSVUpload.objects.filter(name_place=slug_)  # [{},{}]

def consumption(records):
    records_ =records[:]

    tmp_value = []  # list all values
    for x in records:
        tmp = x.value
        tmp_value.append(tmp)
        records = x

    tmp_date = []  # list of all date

    #records_ = CSVUpload.objects.filter(name_place=slug_)  # [{},{}]
    for x in records_:
        tmp = x.date.isoformat()
        tmp_date.append(tmp)
        records_ = x

    tmp_date_ = tmp_date[1:]

    lst_consumption = []
    diff = [tmp_value[n - 1] - tmp_value[n] for n in range(1, len(tmp_value))]
    result_lst = list(zip(tmp_date, tmp_date_, diff))
    return result_lst