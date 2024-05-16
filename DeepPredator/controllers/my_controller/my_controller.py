from controller import Robot, Motor, GPS
import math

# تنظیمات اولیه
TIME_STEP = 64
MAX_SPEED = 6.28

# تابع محاسبه فاصله
def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# ایجاد ربات
robot = Robot()

# موتورها را دریافت کنید
left_motor = robot.getDevice('left_motor')
right_motor = robot.getDevice('right_motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# دریافت GPS
gps = robot.getDevice('gps')
gps.enable(TIME_STEP)

# مختصات طعمه
prey_position = [0.5, 0.5]

# حلقه اصلی کنترلر
while robot.step(TIME_STEP) != -1:
    # دریافت موقعیت فعلی ربات
    position = gps.getValues()
    x, y = position[0], position[2]

    # محاسبه فاصله تا طعمه
    distance = get_distance(x, y, prey_position[0], prey_position[1])

    # محاسبه زاویه به سمت طعمه
    angle = math.atan2(prey_position[1] - y, prey_position[0] - x)

    # تنظیم سرعت موتورها برای حرکت به سمت طعمه
    left_speed = MAX_SPEED * (1 - distance)
    right_speed = MAX_SPEED * (1 - distance)
    
    # در صورتی که ربات به طعمه نزدیک شد، توقف کنید
    if distance < 0.1:
        left_speed = 0
        right_speed = 0

    # تنظیم سرعت موتورها
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
