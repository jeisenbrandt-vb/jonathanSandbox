use rsautogui::{keyboard, keyboard::Vk};
use std::{thread, time::Duration};

fn main() {
    let ten_millis = Duration::from_millis(1000);
    thread::sleep(ten_millis);
    keyboard::typewrite("Lorem ipsum!"); // Simulates typing the string provided.

    // Print `A` using virtual key `Vk`
    keyboard::key_down(Vk::Shift); // Presses specified key down.
    keyboard::key_tap(Vk::A); // Performs specified key_down and key_up.
    keyboard::key_up(Vk::Shift); // Releases specified key up.

    // Print `A` with one line
    keyboard::key_tap('A');
}