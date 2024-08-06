
    #include <Arduino.h>
    #include <HTTPUpdate.h>
    #include <WiFi.h>
    #include <WiFiMulti.h>
    #include <EEPROM.h>

    #define LED1 27
    #define LED2 14
    #define LED3 33
    #define LED4 32
    // Biến khởi tạo
    WiFiMulti wifiMulti;
    String version = "2.2";
    hw_timer_t *My_timer = NULL;
    uint32_t updateCounter = 0;
    uint32_t counter = 0;
    const uint32_t connectTimeoutMs = 10000;
    String key = "e3f99ca6-cc4a-48a1-b3ce-aad15db116ff";


    int n = 6;
    int r = 4;
    int arrayHeader[]= { 1, 0, 0, 0, 1}; // Mã header
    int sizeHeader = sizeof(arrayHeader)/ sizeof(arrayHeader[0]);
    int binaryNumber1[] = {1, 0, 1, 0}; // Mã cần truyền 1 (10)
    int binaryNumber2[] = {1, 0, 0, 1}; // Mã cần truyền 2 (9)
    int binaryNumber3[] = {0, 1, 1, 0}; // Mã cần truyền 3 (6)
    int binaryNumber4[] = {0, 0, 1, 1}; // Mã cần truyền 4 (3)
    int sizeNumber = sizeof(binaryNumber1)/sizeof(binaryNumber1[0]);
    int size = n+sizeHeader;
    int* code1 = new int[size];
    int* code2 = new int[size];
    int* code3 = new int[size];
    int* code4 = new int[size];
    int T = 0;
    int timeLED = 80;
    int addressOfMyArray = 100;
    int eepromAddress = addressOfMyArray-1;

    // Hàm tính tổ hợp C(n, k)
    unsigned long long nchoosek(int n, int k) {
        if (k == 0 || k == n) {
            return 1;
        }
        if (k > n - k) {
            k = n - k;
        }
        unsigned long long result = 1;
        for (int i = 1; i <= k; ++i) {
            result *= n - i + 1;
            result /= i;
        }
    return result;
    }

    // Hàm gán giá trị của một mảng cho một mảng khác
    void assignArray(int source[], int destination[], int size) {
        for (int i = 0; i < size; ++i) {
            destination[i] = source[i];
        }
    }

    // Hàm thêm giá trị của một mảng vào cuối một mảng khác
    void appendArrays(int source[], int destination[], int sizeSource, int sizeDestination) {
        for (int i = 0; i < sizeSource; ++i) {
            destination[sizeDestination + i] = source[i];
        }
    }
    // Hàm mã hóa MPPM
    int* encode_MPPM(int sk, int n, int r) {
        // Khởi tạo khung rỗng
        int* encode_MPPM= new int[n];
        while (n > 0) {
            int y;
            if (0 < r && r < n) {
                y = nchoosek(n-1, r);
            } else {
                y = 0;
            }
            // Mã hóa sk bằng cách đặt xung vào các khe có giá trị vị trí phù hợp
            if (y <= sk) {
                sk = sk - y;
                encode_MPPM[n-1] = 1;
                r = r - 1;
            } else {
                encode_MPPM[n-1] = 0;
            }
            n = n - 1;
        }
        return encode_MPPM;
    }

    // Hàm chuyển mảng nhị phân sang thập phân
    int binaryToDecimal(int binaryArray[], int size) {
        int decimalValue = 0;

        // Duyệt qua từng bit của mảng nhị phân và tính giá trị thập phân
        for (int i = 0; i < size; ++i) {
            decimalValue = decimalValue * 2 + binaryArray[i];
        }

        return decimalValue;
    }
    void IRAM_ATTR onTimer(){
    
    if(T >= size){T = 0;}
    digitalWrite(LED1, code1[T]);
    digitalWrite(LED2, code2[T]);
    digitalWrite(LED3, code3[T]);
    digitalWrite(LED4, code4[T]);
    T++;
    }

    void update_FOTA();

    void getStoredValue() {
    // Đọc giá trị từ Preferences và cập nhật các mảng
    for (int i = 0; i < size; ++i) {
        code1[i] = EEPROM.read(i+addressOfMyArray);
        code2[i] = EEPROM.read(i + size+addressOfMyArray);
        code3[i] = EEPROM.read(i + 2*size+addressOfMyArray);
        code4[i] = EEPROM.read(i + 3*size+addressOfMyArray);
        }
    }
    // Hàm thực hiện phép tính
    void performCalculation() {
        int dataPackage[size]; // Gói tin dùng chung
        assignArray(arrayHeader, dataPackage, sizeHeader);
        // Truyền gói tin vào các LED 1
        int decimalNumber = binaryToDecimal(binaryNumber1,sizeNumber);
        int* encodedFrame = encode_MPPM(decimalNumber, n, r);

        appendArrays(encodedFrame, dataPackage, n, sizeHeader );
        delete [] encodedFrame;
        assignArray(dataPackage, code1, size);

        // Truyền gói tin vào các LED 2
        decimalNumber = binaryToDecimal(binaryNumber2,sizeNumber);
        encodedFrame = encode_MPPM(decimalNumber, n, r);

        appendArrays(encodedFrame, dataPackage, n, sizeHeader );
        delete [] encodedFrame;
        assignArray(dataPackage, code2, size);

        // Truyền gói tin vào các LED 3
        decimalNumber = binaryToDecimal(binaryNumber3,sizeNumber);
        encodedFrame = encode_MPPM(decimalNumber, n, r);

        appendArrays(encodedFrame, dataPackage, n, sizeHeader );
        delete [] encodedFrame;
        assignArray(dataPackage, code3, size);
        
        // Truyền gói tin vào các LED 4
        decimalNumber = binaryToDecimal(binaryNumber4,sizeNumber);
        encodedFrame = encode_MPPM(decimalNumber, n, r);

        appendArrays(encodedFrame, dataPackage, n, sizeHeader );
        delete [] encodedFrame;
        assignArray(dataPackage, code4, size);

        // Lưu trữ giá trị vào EEPROM
        for(int i=0; i<size; i++) {
            EEPROM.write(i+addressOfMyArray, code1[i]);
            EEPROM.write(i + size+addressOfMyArray, code2[i]);
            EEPROM.write(i + 2*size+addressOfMyArray, code3[i]);
            EEPROM.write(i + 3*size+addressOfMyArray, code4[i]);
        }

    }
    void setup() {    
        Serial.begin(9600);  // Khởi tạo kết nối với cổng Serial
        WiFi.mode(WIFI_STA);
        // Thêm danh sách wifi 
        wifiMulti.addAP("IoTEAM_Lab_VLC", "A11111z22222");
        // Kết nối với Wi-Fi sử dụng wifiMulti (kết nối với SSID có tín hiệu mạnh nhất)
        Serial.println("Connecting Wifi...");
        if(wifiMulti.run() == WL_CONNECTED) {
            Serial.println("");
        }

        // Đọc giá trị trạng thái từ EEPROM
        int bootCount = EEPROM.read(eepromAddress);

        // Kiểm tra xem đã mới nạp lại chương trình hay không
        if (bootCount != 1) {
            // Thực hiện các công việc cần thiết khi chương trình mới nạp lại
            performCalculation(); 
            // Lưu trạng thái mới vào EEPROM
            EEPROM.write(eepromAddress, 1);
            EEPROM.commit();
        }
        else {
            // Gọi hàm để lấy giá trị lưu trữ
            getStoredValue();
        } 
        // Cài đặt ngõ đầu ra tín hiệu LED
        pinMode(LED1, OUTPUT);
        pinMode(LED2, OUTPUT);
        pinMode(LED3, OUTPUT);
        pinMode(LED4, OUTPUT);
        My_timer = timerBegin(0, 80, true);
        timerAttachInterrupt(My_timer, &onTimer, true);
        timerAlarmWrite(My_timer, timeLED, true); // 500 microseconds= 0.5ms, t=1/f f=2000
        timerAlarmEnable(My_timer); //Just Enable
    }

    void loop()
    {
        //Nếu mất kết nối với điểm phát sóng mạnh nhất, nó sẽ kết nối với mạng tiếp theo trong danh sách
        if (wifiMulti.run(connectTimeoutMs) == WL_CONNECTED) {
        }
        delay(500);
        if (WiFi.status() == WL_CONNECTED)
        {
            updateCounter++;
            if (updateCounter > 120)
            {
            updateCounter = 0;
            update_FOTA();
            }
        }
    }

    String getChipId()
    {
        String ChipIdHex = String((uint32_t)(ESP.getEfuseMac() >> 32), HEX);
        ChipIdHex += String((uint32_t)ESP.getEfuseMac(), HEX);
        return ChipIdHex;
    }
    
    void update_FOTA()
    {
        String url = "http://otadrive.com/deviceapi/update?";
        url += "k=" + key;
        url += "&v=" + version;
        url += "&s=" + getChipId(); // định danh thiết bị trên Cloud
        WiFiClient client;
        httpUpdate.update(client, url, version);
    }
