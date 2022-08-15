from validators import email_val

def test(a):
    if a == 2:
        send = email_val()
        temp = send.new_auth_number()
        print(temp)
    return 

print(test(2))