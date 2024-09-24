values = [False, 0, 0.0, None, '', (), [], {}, range(0), (None), (None,), [None], {None}]

for val in values:
    if val:
        print(f'{val} is True.')
    else:
        print(f'{val} is False.')
        
    # (None) is not a tuple, it is just a value in parentheses.한국말