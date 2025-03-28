use rsautogui::{keyboard};
use std::{thread, time::Duration};
use dotenv::dotenv;
use menu_rs::{Menu, MenuOption};
use std::error::Error;
use std::fs::File;
use std::io::Read;
use csv::ReaderBuilder;

fn tmp_fn(){
    println!("this does nothing");
}

pub fn main(){
    println!("Conduit");

    let menu = Menu::new(vec![
        MenuOption::new("Add Device", device_menu),
        MenuOption::new("DownLink", downlink),
        MenuOption::new("something else", tmp_fn),
        //change fsb
        //change channel plan
        
    ]);

    menu.show();
}

fn downlink(){
    //argumnets needed:
    // conduit ip
    // deveui
    // vobo type?
    // vobo FWV?
    //functions to implement:
    //-pull config
    //-toggle acks
    //-60s cycle time
    //-toggle cycle sub bands
    //todo
    // let mqttBrokerIP = std::env::var("MQTT_BROKER_IP");
    // let devEUI = std::env::var("DEV_EUI");
    // let voboType = std::env::var("VOBO_TYPE");
    // let fwv = std::env::var("FWV");
    //format input
    // println!("{:?}, {:?}, {:?}, {:?}",mqttBrokerIP, devEUI, voboType, fwv);
    // thread::sleep(Duration::from_secs(10));
}

fn device_menu(){
    // dont forget to creat a .env file and add your vobo credentials to it
    // dotenv().ok();
    
    // let dev_names_str = std::env::var("DEV_NAMES").expect("dev_name");//String::new();
    // if let Err(err) = read_csv("VoBoDevices.csv") {
    //     println!("Error reading CSV file: {}", err);
    //     println!("{}", Err);
    //     thread::sleep(Duration::from_secs(10));
    //     return;
    // }
    let file_path = "VoBoDevices.csv";
    let mut dev_names = Vec::new();
    match read_csv(file_path) {
        Ok(records) => {
            for record in records {
                if let Some(first_element) = record.get(0) {
                    let dev_name = first_element.to_string() + " " + record.get(1).expect("deveui");
                    dev_names.push(dev_name);
                }
            }
        }
        Err(e) => {
            eprintln!("Error reading CSV file: {}", e);
            return;
        }
    }

    
    // let dev_ei
    println!("test");
    // thread::sleep(Duration::from_secs(10));
    let mut menu_options = Vec::new();
    for (i, name) in dev_names.iter().enumerate(){
        println!("test");
        menu_options.push(MenuOption::new(name, move || { add_device(i.clone())}));
    }
    // menu_options.push(MenuOption::new("add device", add_device));
    //im not mutating devNum proprely with this code ToDo
    let menu = Menu::new(menu_options);

    menu.show();
}

fn add_device(devNum: usize){
    // move || {
    //     println!("device added");
    // }
    // let devNum = 1;
    println!("selected device {}", devNum);
    // dotenv().ok();
    // let dev_euis_str = std::env::var("DEV_EUIS").expect("dev_eui");//String::new();
    // let app_euis_str = std::env::var("APP_EUIS").expect("app_eui");//String::new();
    // let app_keys_str = std::env::var("APP_KEYS").expect("app_key");//String::new();
    let mut dev_euis = Vec::new();
    let mut app_euis = Vec::new();
    let mut app_keys = Vec::new();

    let file_path = "VoBoDevices.csv";

    match read_csv(file_path) {
        Ok(records) => {
            for record in records {
                if let Some(element) = record.get(1) {
                    dev_euis.push(element.to_string());
                }
                if let Some(element) = record.get(2) {
                    app_euis.push(element.to_string());
                }
                if let Some(element) = record.get(3) {
                    app_keys.push(element.to_string());
                }
            }
        }
        Err(e) => {
            eprintln!("Error reading CSV file: {}", e);
        }
    }

    // let dev_euis: Vec<&str> = dev_euis_str.split(',').collect();
    // let app_euis: Vec<&str> = app_euis_str.split(',').collect();
    // let app_keys: Vec<&str> = app_keys_str.split(',').collect();

    println!("waiting so you can navigate to textfeild");
    thread::sleep(Duration::from_secs(10));

    println!("adding device");
    keyboard::typewrite(&dev_euis[devNum]);
    rsautogui::keyboard::key_tap(rsautogui::keyboard::Vk::Tab);
    keyboard::typewrite(&app_euis[devNum]);
    rsautogui::keyboard::key_tap(rsautogui::keyboard::Vk::Tab);
    keyboard::typewrite(&app_keys[devNum]);
    rsautogui::keyboard::key_tap(rsautogui::keyboard::Vk::Tab);

    
}

fn read_csv(file_path: &str) -> Result<Vec<csv::StringRecord>, Box<dyn Error>> {
    let file = File::open(file_path)?;
    let mut rdr = ReaderBuilder::new().from_reader(file);
    let mut records = Vec::new();

    for result in rdr.records() {
        let record = result?;
        records.push(record);
    }
    Ok(records)
}