def square_bracket_validation(working_domain):
    count = 0
    # color = Color.Color()
    for i, c in enumerate(working_domain):
        if c == '[':
            count += 1
        elif c == ']':
            count -= 1
        if count < 0 or count == 0 and i < (len(working_domain) - 1):
            #   color.coloring_char(working_domain, i, 'RED')
            print(working_domain[0:i], end='')
            print('**' + working_domain[i] + '**', end='')
            print(working_domain[(i + 1):len(working_domain)])
            raise Exception("Wrong working domain, too many: ']', (indicated with ** **)")
    if count > 0:
        # color.append_color_char(working_domain, ']' * count, 'RED')
        print(working_domain + '**' + ']' * count + '**')
        raise Exception("Wrong working domain, " + str(count) + " ']' are missing, (indicated with ** **)")
