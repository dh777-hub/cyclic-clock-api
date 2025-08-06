from flask import Flask, jsonify
import datetime
from decimal import *
from fractions import Fraction

getcontext().prec = 100
app = Flask(__name__)

def base_conversion(year):
    res = Fraction(year)
    num_digits = 1
    digits = []
    while res > 12:
        res /= 12
        num_digits += 1
    for i in range(num_digits):
        digits.append(int(res))
        res = (res-int(res))*12
    while 0 in digits[1:]:
        for i in range(num_digits-1):
            if digits[i+1] == 0:
                digits[i] -= 1
                digits[i+1] = 12
    if digits[0] == 0:
        digits.pop(0)
    return digits

@app.route("/clock")
def get_clock_data():
    seconds_since_big_bang = Decimal('466576408532613321.5304043206646')
    reference_time = datetime.datetime(2020, 12, 31, 23, 59, 59)
    input_time = datetime.datetime.now()
    print("SERVER TIME:", input_time)
    second_multiplier = Decimal(285738202.060366731702559) / Decimal(299792458)

    difference_in_seconds = (input_time - reference_time).total_seconds()
    total_seconds = Decimal(difference_in_seconds) + seconds_since_big_bang
    new_total_seconds = total_seconds * second_multiplier

    new_total_min = new_total_seconds / 72
    new_seconds = round((new_total_min - int(new_total_min)) * 72)

    new_total_hours = Decimal(int(new_total_min)) / 54
    new_minutes = round((new_total_hours - int(new_total_hours)) * 54)

    new_total_days = Decimal(int(new_total_hours)) / 24
    new_hours = round((new_total_days - int(new_total_days)) * 24)

    new_total_months = Decimal(int(new_total_days)) / 36
    new_days = round((new_total_months - int(new_total_months)) * 36) + 1

    new_total_years = Decimal(int(new_total_months)) / 12
    new_months = round((new_total_years - int(new_total_years)) * 12) + 1
    new_years = int(new_total_years)

    return jsonify({
        "years": base_conversion(new_years),
        "months": base_conversion(new_months),
        "days": base_conversion(new_days),
        "hours": base_conversion(new_hours),
        "minutes": base_conversion(new_minutes),
        "seconds": base_conversion(new_seconds)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
