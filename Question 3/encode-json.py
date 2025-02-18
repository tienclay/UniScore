# Bước 1: Minify JSON (loại bỏ khoảng trắng không cần thiết)
def minify_json(text):
    in_string = False
    escape = False
    result = []
    for c in text:
        if c == '"' and not escape:
            in_string = not in_string
            result.append(c)
        elif in_string:
            if c == '\\' and not escape:
                escape = True
            else:
                escape = False
            result.append(c)
        else:
            if c in " \n\t\r":
                continue
            else:
                result.append(c)
    return "".join(result)

# Bước 2: Thay thế key dài bằng key ngắn
def replace_keys(json_text, key_map):
    # Thay thế các key ở cấp ngoài dạng: "key":
    for key, short_key in key_map.items():
        json_text = json_text.replace('"' + key + '":', '"' + short_key + '":')
    return json_text

def replace_nested_keys(json_text, key_map):
    # Thay thế các key nằm trong chuỗi (escaped) của các object lồng nhau,
    # ví dụ: \"status_id\": thay vì "status_id":
    for key, short_key in key_map.items():
        json_text = json_text.replace('\\"' + key + '\":', '\\"' + short_key + '\":')
    return json_text

# Bước 3: Nén bằng thuật toán LZW (tự cài)
def lzw_compress(uncompressed):
    # Khởi tạo từ điển với các ký tự đơn
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

def lzw_compress_to_bytes(uncompressed):
    codes = lzw_compress(uncompressed)
    # Tính số bit cần dùng để biểu diễn code lớn nhất
    max_code = max(codes) if codes else 0
    bits = 1
    while (1 << bits) <= max_code:
        bits += 1
    # Chuyển các mã sang chuỗi bit cố định độ dài 'bits'
    bit_string = ""
    for code in codes:
        bit_string += format(code, '0{}b'.format(bits))
    # Nếu số bit không chia hết cho 8, thêm 0 vào cuối
    if len(bit_string) % 8 != 0:
        bit_string += '0' * (8 - (len(bit_string) % 8))
    output = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]
        output.append(int(byte, 2))
    return output, bits

# Hàm chính: Đọc file, nén và lưu kết quả
def compress_data_file(input_filename, output_filename):
    # Đọc file ban đầu
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = f.read()
    # Minify JSON
    minified = minify_json(data)
    
    # Bản đồ ánh xạ các key: thay đổi theo cấu trúc file của bạn
    key_map = {
        "id": "a",
        "season_id": "b",
        "stage_id": "c",
        "group_num": "d",
        "round_num": "e",
        "start_time": "f",
        "start_timestamp": "g",
        "sport_event_status": "h",
        "status_id": "i",
        "updated_at": "j",
        "record_updated_at": "k",
        "home_team_id": "l",
        "away_team_id": "m",
        "competition_id": "n",
        "lineup": "o",
        "venue_id": "p",
        "referee_id": "q",
        "related_id": "r",
        "agg_score": "s"
    }
    # Thay thế key ở cấp ngoài và các key lồng nhau (escaped)
    replaced = replace_keys(minified, key_map)
    replaced = replace_nested_keys(replaced, key_map)
    
    # Nén chuỗi kết quả bằng thuật toán LZW
    compressed_bytes, bits = lzw_compress_to_bytes(replaced)
    
    # Để hỗ trợ giải nén, ta lưu số bit dùng để mã hóa trong 1 byte header
    header = bytearray([bits])
    final_data = header + compressed_bytes
    
    with open(output_filename, 'wb') as f:
        f.write(final_data)
    print("Nén xong. File kết quả:", output_filename)

# Ví dụ sử dụng:
compress_data_file("data.json", "data_compressed.bin")
