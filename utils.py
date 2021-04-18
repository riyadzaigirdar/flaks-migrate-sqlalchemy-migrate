

def to_json_list(list_obj):
    arr = []
    for i in list_obj:
        # arr.append({
        #     "id": i.id,
        #     "username": i.email
        # })
        arr.append(i.to_json())
    return arr
