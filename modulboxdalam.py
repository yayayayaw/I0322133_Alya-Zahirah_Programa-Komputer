import json

class UkuranError(Exception):
    pass

class ProvinsiTidakTersediaError(Exception):
    pass

def get_input():
    data = '''small = 200 × 130 × 120 cm (berat max. 1000kg)
    medium = 200 × 130 × 130 cm (berat max. 2000kg)
    large = 300 × 160 × 130 cm (berat max. 2000kg)'''
    rows = data.split('\n')
    print("| {:<7s} | {:^18s} | {:^17s} |".format("Ukuran", "Dimensi", "Berat Maks."))
    print("-" * 40)
    for row in rows:
        row_data = row.split('=')
        ukuran = row_data[0].strip()
        dimensi = row_data[1].split('(')[0].strip()
        berat = row_data[1].split('(')[1].split(')')[0].strip()
        print("| {:<7s} | {:^15s} | {:^12s} |".format(ukuran, dimensi, berat))
        print("-" * 40)

    input_ukuran = input("Ukuran Box : ")
    input_provinsi = input("Input Provinsi Asal : ")
    try:
        jarak = float(input("Jarak Pengiriman (km) : "))
    except ValueError:
        raise ValueError("Input jarak harus berupa angka")
    return input_ukuran, input_provinsi, jarak

def layanan_box_dalam_kota(layanan, input_ukuran, input_provinsi, jarak):
    with open("daftarharga.json", "r") as file1:
        data1 = json.load(file1)

        for item in data1[layanan]:
            if item["layanan"] == "Go Box" or item["layanan"] == "Grab Instant" or item["layanan"] == "Maxim Box":
                ukuran_data = item["ukuran"]
                if input_ukuran not in ukuran_data:
                    raise UkuranError("Input ukuran salah")
                provinsi_data = ukuran_data[input_ukuran]["provinsi"]
                if input_provinsi not in provinsi_data:
                    raise ProvinsiTidakTersediaError("Provinsi yang Anda input tidak terdapat di Pulau Jawa")
                harga_minimum = provinsi_data[input_provinsi]["harga_minimum"]
                harga_per_km = provinsi_data[input_provinsi]["harga_per_km"]
                if harga_minimum is not None and harga_per_km is not None:
                    total_harga = harga_minimum + (harga_per_km * jarak)
                    return total_harga

    raise Exception("Input Anda Tidak Sesuai, Silakan Cek Kembali")

def main():
    try:
        input_ukuran, input_provinsi, jarak = get_input()
        harga_MaximBox = layanan_box_dalam_kota("maxim", input_ukuran, input_provinsi, jarak)
        harga_GoBox = layanan_box_dalam_kota("gojek", input_ukuran, input_provinsi, jarak)
        harga_GrabInstant = layanan_box_dalam_kota("Grab", input_ukuran, input_provinsi, jarak)
        print("Harga Maxim Box: ", harga_MaximBox)
        print("Harga Go Box: ", harga_GoBox)
        print("Harga Grab Instant: ", harga_GrabInstant)

    except UkuranError as e:
        print("Terjadi kesalahan:", str(e))
    except ValueError as e:
        print("Terjadi kesalahan:", str(e))
    except ProvinsiTidakTersediaError as e:
        print("Terjadi kesalahan:", str(e))
    except Exception as e:
        print("Terjadi kesalahan:", str(e))

if __name__ == "__main__":
    main()
