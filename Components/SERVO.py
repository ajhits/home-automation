
def move_servo_smoothly(angle,servo):
    # Convert angle (0 to 180) to the appropriate duty cycle
    duty_cycle = (angle / 18.0) + 2.5
    servo.ChangeDutyCycle(duty_cycle)
    
def move_two_servos_smoothly(angle_1,angle_2,servo_1,servo_2):
    
    # Move servo 1
    duty_cycle1 = angle_1 / 18.0 + 2.5
    servo_1.ChangeDutyCycle(duty_cycle1)

    # Move servo 2
    duty_cycle2 = angle_2 / 18.0 + 2.5
    servo_2.ChangeDutyCycle(duty_cycle2)
