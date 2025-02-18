def lzw_decompress(codes):
    """
    Giải nén danh sách mã (codes) theo thuật toán LZW.
    """
    # Khởi tạo từ điển với các ký tự đơn (0-255)
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256

    # Lấy chuỗi đầu tiên
    w = dictionary[codes[0]]
    result = [w]

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Bad compressed code: %s" % code)
        result.append(entry)
        # Thêm chuỗi mới vào từ điển
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    return ''.join(result)


def decompress_data_file(input_filename, output_filename):
    """
    Giải nén file nhị phân đã nén thành file JSON ban đầu,
    đồng thời khôi phục lại key theo mapping đã định nghĩa.
    """
    # Đọc file nhị phân
    with open(input_filename, 'rb') as f:
        data = f.read()

    # Byte đầu tiên chứa số bit dùng cho mỗi mã
    bits = data[0]

    # Phần còn lại là dữ liệu nén
    compressed_bytes = data[1:]
    bit_string = ""
    for byte in compressed_bytes:
        bit_string += format(byte, '08b')

    # Tách chuỗi bit thành các mã với độ dài cố định 'bits'
    codes = []
    for i in range(0, len(bit_string), bits):
        chunk = bit_string[i:i+bits]
        if len(chunk) < bits:
            break  # bỏ qua phần dư không đủ bits
        codes.append(int(chunk, 2))

    # Giải nén các mã theo thuật toán LZW
    decompressed_text = lzw_decompress(codes)

    # Bản đồ ánh xạ đã dùng trong quá trình nén:
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

    # Tạo bản đồ đảo ngược: key ngắn -> key gốc
    reverse_key_map = {v: k for k, v in key_map.items()}

    def revert_keys(json_text, reverse_key_map):
        """
        Thay thế key ngắn bằng key gốc ở cả cấp ngoài và bên trong chuỗi escaped.
        """
        for short_key, original_key in reverse_key_map.items():
            # Thay thế ở cấp ngoài
            json_text = json_text.replace('"' + short_key + '":', '"' + original_key + '":')
            # Thay thế trong các chuỗi JSON lồng nhau (escaped)
            json_text = json_text.replace('\\"' + short_key + '\":', '\\"' + original_key + '":')
        return json_text

    # Khôi phục lại key gốc
    reverted_text = revert_keys(decompressed_text, reverse_key_map)

    # Ghi kết quả ra file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(reverted_text)

    print("Giải nén thành công, file:", output_filename)


# Ví dụ sử dụng:
decompress_data_file("data_compressed.bin", "data_decompressed.json")
