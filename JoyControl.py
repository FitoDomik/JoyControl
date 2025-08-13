import pygame
import pyautogui
import time
import threading
class GamepadController:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.sensitivity = 500  
        self.running = True
        self.deadzone = 0.15  
        if pygame.joystick.get_count() == 0:
            return
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.button_states = {}
        self.dpad_states = {"up": False, "down": False, "left": False, "right": False}
    def apply_deadzone(self, value):
        if abs(value) < self.deadzone:
            return 0
        return value
    def handle_mouse_movement(self, x_axis, y_axis):
        x_axis = self.apply_deadzone(x_axis)
        y_axis = self.apply_deadzone(y_axis)
        if x_axis != 0 or y_axis != 0:
            current_x, current_y = pyautogui.position()
            new_x = current_x + (x_axis * self.sensitivity)
            new_y = current_y + (y_axis * self.sensitivity)
            screen_width, screen_height = pyautogui.size()
            new_x = max(0, min(new_x, screen_width - 1))
            new_y = max(0, min(new_y, screen_height - 1))
            pyautogui.moveTo(new_x, new_y)
    def handle_button_press(self, button, pressed):
        if button not in self.button_states:
            self.button_states[button] = False
        if pressed and not self.button_states[button]:
            if button == 0:  
                pyautogui.click(button='left')
            elif button == 1:  
                pyautogui.click(button='right')
            elif button == 7:  
                self.running = False
        self.button_states[button] = pressed
    def handle_dpad(self):
        if self.joystick.get_numhats() > 0:
            hat = self.joystick.get_hat(0)
            hat_x, hat_y = hat
            if hat_x == -1 and not self.dpad_states["left"]:  
                pyautogui.press('left')
                self.dpad_states["left"] = True
            elif hat_x == 1 and not self.dpad_states["right"]:  
                pyautogui.press('right')
                self.dpad_states["right"] = True
            else:
                self.dpad_states["left"] = False
                self.dpad_states["right"] = False
            if hat_y == 1 and not self.dpad_states["up"]:  
                pyautogui.press('up')
                self.dpad_states["up"] = True
            elif hat_y == -1 and not self.dpad_states["down"]:  
                pyautogui.press('down')
                self.dpad_states["down"] = True
            else:
                self.dpad_states["up"] = False
                self.dpad_states["down"] = False
    def run(self):
        if not hasattr(self, 'joystick'):
            return
        clock = pygame.time.Clock()
        try:
            while self.running:
                pygame.event.pump()
                left_x = self.joystick.get_axis(0)  
                left_y = self.joystick.get_axis(1)  
                self.handle_mouse_movement(left_x, left_y)
                for i in range(self.joystick.get_numbuttons()):
                    button_pressed = self.joystick.get_button(i)
                    if button_pressed or i in self.button_states:
                        self.handle_button_press(i, button_pressed)
                self.handle_dpad()
                clock.tick(60)
        except KeyboardInterrupt:
            pass
        finally:
            pygame.quit()
def main():
    try:
        controller = GamepadController()
        controller.run()
    except Exception as e:
        pass
if __name__ == "__main__":
    main()