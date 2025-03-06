#include <iostream>
#include <vector>
#include <filesystem>
#include <regex>
#include <utility>
#include <thread>
#include <windows.h>
#include <string>
#include <iomanip>

namespace fs = std::filesystem;

std::string getDesiredVersion(){
  std::vector<std::string> paths;
  std::string voboUtilsPath = "C:\\Users\\JonathanEisenbrandt\\Desktop\\VoBoUtils\\firmware";
  int pathNum = 0;
  for (const auto & entry : fs::directory_iterator(voboUtilsPath))
//    std::cout << entry.path() << std::endl;
    //store the list of paths in a vector
    paths.push_back(entry.path().string());
  std::cout << "Enter a number to select the directory of the firmware you'd like to flash your vobo with\n";
  int count = 0;
  for (auto it = begin(paths); it != end(paths); ++it) {
    std::string fwFile = *it;
    size_t pos = fwFile.find_last_of('\\');
    std::string result = "";
    if (pos != std::string::npos) {
      result = fwFile.substr(pos + 1);
      // std::cout << result << std::endl;
    } else {
      std::cout << "No '/' character found in the string." << std::endl;
    }
    std::cout << '(' << count << ")" << std::setfill('_') << std::setw(40) << result << std::endl;
    count ++;
  }
  std::cin >> pathNum;
  //todo: check that input is valid, assuming it is valid for now
  std::cout << "selected path: " << paths[pathNum] << std::endl;
  return paths[pathNum];
}

std::vector<std::string> getBin(std::string path, char analytics) {
  std::vector<std::string> res_files;
  bool flag_installer = false;
  bool flag_bin = false;
  std::string installerFile = "";
  std::string binFile = "";
  //regex
  for (const auto & entry : fs::directory_iterator(path)) {
    //std::cout << entry.path() << std::endl;
    std::string file = entry.path().string();
    std::cout << "file: " << file << std::endl;
    if(file.find("installer.bin") != std::string::npos){
      std::cout << "found installer\n" << file << std::endl;
      flag_installer = true;
      installerFile = file;
    }
    std::cout << path.back() <<std::endl;
    
    if(analytics == 'y'){
      std::cout << "WARN analytics not supported at the moment" <<std::endl;
      std::regex bin_regex(R"(analytics\d+\.bin)");
      // if(c)
    } else {
      std::regex bin_regex(R"(\d+\.bin)");
      if(std::regex_search(file, bin_regex)) {
        std::cout << "found bin\n" << file << std::endl;
        flag_bin = true;
        binFile = file;
      }
    }
  }
  //std::cout << flag_installer << " " << flag_bin << std::endl;
  std:: cout << "Installer file path: " << installerFile << "\nBin path: " << binFile << std::endl;
  return {installerFile, binFile};
}

int flashVoBo(std::vector<std::string> paths){
  //auto target = paths[2] + "\\tep.bin";
  try{
    /*auto target = "C:\\Users\\JonathanEisenbrandt\\Documents\\";
      std::cout << "Coping " << paths[0] << "\nTo " << target << std::endl;
      fs::copy_file(paths[0], target, fs::copy_options::overwrite_existing);*/
    //needs to handel error cases
    // Extract the source and target paths
    std::string source_path = paths[0];
    std::string target_directory = paths[2];

    // Create the target directory if it doesn't exist
    fs::create_directories(target_directory);

    // Get the filename from the source path
    std::string filename = fs::path(source_path).filename().string();

    // Construct the full target path
    std::string target_path = target_directory + "/" + filename;

    // Copy the file
    fs::copy_file(source_path, target_path, fs::copy_options::overwrite_existing);

    std::cout << "File " << filename << " successfully copied to " << target_directory << std::endl;
  } catch (const std::exception& e) {
    std::cout << "Error: " << e.what() << std::endl;
    return 1;
  }
  std::cout << "sleeping between flashes\n";
  std::this_thread::sleep_for(std::chrono::seconds(5));
  int tc_idx = paths[0].find("TC");
  int xp_idx = paths[0].find("XP");
  if (tc_idx != -1) {
    std::cout << tc_idx << std::endl;
    std::cout << "Sleeping extra for TC tables" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(25));
  }
  if (xp_idx != -1) {
    std::cout << xp_idx << std::endl;
    std::cout << "Sleeping extra for XP for some reason" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(20));
  }
  std::cout << "resuming\n";
  try{
    /*auto target = "C:\\Users\\JonathanEisenbrandt\\Documents\\";
      std::cout << "Coping " << paths[0] << "\nTo " << target << std::endl;
      fs::copy_file(paths[0], target, fs::copy_options::overwrite_existing);*/
    //needs to handel error cases
    // Extract the source and target paths
    std::string source_path = paths[1];
    std::string target_directory = paths[2];
    // std::cout << "Source: " << source_path << " Target: " << target_directory << std::endl;

    // Create the target directory if it doesn't exist
    fs::create_directories(target_directory);//not sure that this should exist

    // Get the filename from the source path
    std::string filename = fs::path(source_path).filename().string();

    // Construct the full target path
    std::string target_path = target_directory + "/" + filename;

    // Copy the file
    fs::copy_file(source_path, target_path, fs::copy_options::overwrite_existing);

    std::cout << "File " << filename << " successfully copied to " << target_directory << std::endl;
  } catch (const std::exception& e) {
    std::cout << "Error: " << e.what() << std::endl;
    return 2;
  }
  return 0;

}

std::string findDriveByVolumeName(const std::string& volumeName) {
    char volumeNameBuffer[MAX_PATH];
    char fileSystemNameBuffer[MAX_PATH];
    DWORD serialNumber = 0, maxComponentLen = 0, fileSystemFlags = 0;
    char drive[] = "A:\\";

    for (char letter = 'A'; letter <= 'Z'; ++letter) {
        drive[0] = letter;
        if (GetVolumeInformationA(drive, volumeNameBuffer, sizeof(volumeNameBuffer), &serialNumber, &maxComponentLen, &fileSystemFlags, fileSystemNameBuffer, sizeof(fileSystemNameBuffer))) {
            if (volumeName == volumeNameBuffer) {
                return std::string(drive);
            }
        }
    }
    return "";
}

int checkConnection(std::string path) {
  if(path == ""){
    return 1;
  }
  fs::path filePath = fs::path(path) / "FAIL.TXT";
  if (fs::exists(filePath)) {
    return 2;
  }
  return 0;
}

int main () {
  std::cout << "Start Auto VoBo Flasher" << std::endl;
  std::string devboardPath = findDriveByVolumeName("MULTITECH");
  int con = checkConnection(devboardPath);
  if(con != 0){
    std::cout << "dev board connection error: " << con << std::endl;
    return 1;//this error val should probably be defined somewhere
  }
  //prompt user for version they would like to use of those available
  std::string firmwarePath = getDesiredVersion();
  //std::cout << "FWPath: " << firmwarePath << std::endl;
  //ask user if they would like to use analytics plugin or default
  char analytics = false;
  std::cout << "Would you like to use the analytics plugin(y/n)";
  //kinda lazy and should be a boolean input that's validated but fine for now
  std::cin >> analytics;
  //check if both installer and desired binary exist in the version selected else restart at step 1 excluding the failed path
  std::vector<std::string> paths = getBin(firmwarePath, analytics);
  //flash vobo with installer then flash with desired binary
  paths.push_back(devboardPath);//devboard isn't always the same
  std::cout << "devboard path: " << devboardPath << std::endl;
  // std::cout << "paths 1 " << paths[1] << std::endl;
  int err = flashVoBo(paths);
  //print completed message
  return err;
}
