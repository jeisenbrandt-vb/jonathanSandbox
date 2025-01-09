mod conduit;
mod modbus;
mod serial;
use menu_rs::{Menu, MenuOption};

fn action_2(val: u32) {
    println!("action 2 with number {}", val)
}
fn action_3(msg: &str, val: f32) {
    println!("action 3 with string {} and float {}", msg, val)
}
fn action_4() {
    println!("action 4")
}

fn conduit_menu() {
    conduit::main();
}

fn modbus_menu() {
    modbus::main();
}

fn serial_menu() {
    serial::main()
}

fn main() {
    loop {
        let Menu = Menu::new(vec![
            MenuOption::new("Conduit", conduit_menu),
            MenuOption::new("Modbus", modbus_menu),
            MenuOption::new("Serial", serial_menu),
            MenuOption::new("Option 4", action_4),
            MenuOption::new("Option 5", move || action_2(83)),
        ]);

        Menu.show();
    }
}