use rsautogui::{keyboard, keyboard::Vk};
use std::{thread, time::Duration};
use rprompt::prompt_reply;
use std::io;
mod conduit;

fn main() {
    conduit::print_test();
    let word = prompt_reply("What word do you want to use?").unwrap();
    // let rows = prompt_reply("how many rows?").unwrap();
    let mut input_text = String::new();
    io::stdin()
        .read_line(&mut input_text)
        .expect("Failed to read from stdin");

    let trimmed = input_text.trim();
    match trimmed.parse::<u32>() {
        Ok(i) => {
            println!("Your integer input: {}", i);
            // let rows = i;
            thread::sleep(Duration::from_secs(10));
            for i in 1..=i {
                // println!("{}",word);
                keyboard::typewrite(&word);
                rsautogui::keyboard::key_tap(rsautogui::keyboard::Vk::Enter);
                rsautogui::keyboard::key_tap(rsautogui::keyboard::Vk::DownArrow);
                rsautogui::keyboard::key_down(rsautogui::keyboard::Vk::Shift);
                rsautogui::keyboard::key_down(rsautogui::keyboard::Vk::F2);
                rsautogui::keyboard::key_up(rsautogui::keyboard::Vk::Shift);
                rsautogui::keyboard::key_up(rsautogui::keyboard::Vk::F2);
            }
        }
        Err(..) => println!("This was not an integer: {}", trimmed),
    };
}