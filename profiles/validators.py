def cpf_validator(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    resto = total % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    if digito1 != int(cpf[9]):
        return False

    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    resto = total % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    if digito2 != int(cpf[10]):
        return False

    return True
