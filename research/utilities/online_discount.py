first_order_remainder = 269 % 10

if first_order_remainder == 0:
    first_order_coupon = "yes"
else:
    first_order_coupon = "no"

print(first_order_coupon)
second_order_remainder = 270 % 10

if second_order_remainder == 0:
    second_order_coupon = "yes"
else:
    second_order_coupon = "no"
print(second_order_coupon)
