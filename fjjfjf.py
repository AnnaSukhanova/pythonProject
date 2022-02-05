from yandex_testing_lesson import is_correct_mobile_phone_number_ru


def test_is_correct_mobile_phone_number_ru():
    test_cases = [
        ('', False),
        ('+7' + 'a' * 10, False),
        ('+89991112233', False),
        ('+79991112233', True),
        ('89991112233', True),
        ('8-800-111-11-11', True),
        ('+7-800-111-11-11', True),
        ('8 (999) 123-45-67', True),
        ('8 (999 123-45-67', False),
        ('8 )999( 123-45-67', False),
        ('8 (999) (123)-45-67', False)
    ]
    for input_s, correct_output_s in test_cases:
        answer = is_correct_mobile_phone_number_ru(input_s)
        if answer != correct_output_s:
            return False
    return True


print('YES' if test_is_correct_mobile_phone_number_ru() else 'NO')
