import json

class ProvinsiTidakTersediaError(Exception):
    pass

class AsalTidakTersedia(Exception):
    pass

class TujuanTidakTersedia(Exception):
    pass

class ukuranerror(Exception):
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
    input_provinsi = input("Input provinsi Asal : ")
    input_asal = input("Kota Asal : ")
    input_tujuan = input("Kota Tujuan  : ")
    return input_ukuran, input_provinsi, input_asal, input_tujuan


def layananboxluarkota(layanan, input_ukuran, input_provinsi, input_asal, input_tujuan):
    with open("daftarharga.json", "r") as file1:
        data1 = json.load(file1)

    with open("jarakkotaluarprov.json", "r") as file2:
        data2 = json.load(file2)

    provinsi_data = data2.get(input_provinsi)

    if provinsi_data is None:
        raise ProvinsiTidakTersediaError("Provinsi yang anda input tidak terdapat di Pulau Jawa")
    
    if input_asal not in provinsi_data:
        raise AsalTidakTersedia("Asal tidak tersedia dalam provinsi ini")

    if input_tujuan not in provinsi_data[input_asal]:
        raise TujuanTidakTersedia("Tujuan tidak tersedia")


    for asal in provinsi_data:
        for tujuan in provinsi_data[asal]:
            jarak = provinsi_data[asal][tujuan]
        
            for item in data1[layanan]:
                if item.get("layanan") == "Maxim Box" or item.get("layanan") == "Go Box" or item.get("layanan") == "Grab Instant":
                    ukuran_data = item.get("ukuran", {}).get(input_ukuran)
                    if ukuran_data is None:
                        raise ukuranerror("Ukuran tidak sesuai")
                    if ukuran_data is not None and input_asal == asal and input_tujuan == tujuan:
                        harga_minimum = ukuran_data.get("provinsi", {}).get(input_provinsi, {}).get("harga_minimum")
                        harga_per_km = ukuran_data.get("provinsi", {}).get(input_provinsi, {}).get("harga_per_km")
                        if harga_minimum is not None and harga_per_km is not None:
                            if jarak <= 3:
                                total_harga = harga_minimum
                            else:
                                total_harga = harga_minimum + (harga_per_km * jarak)
                            return total_harga
                        
    raise Exception("Input Anda Tidak Sesuai, Silakan Cek Kembali")

def main():
    try : 
        input_ukuran, input_provinsi, input_asal, input_tujuan = get_input()
        harga_MaximBox = layananboxluarkota("maxim", input_ukuran, input_provinsi, input_asal, input_tujuan)
        harga_GoBox = layananboxluarkota("gojek", input_ukuran, input_provinsi, input_asal, input_tujuan)
        harga_GrabInstant = layananboxluarkota("Grab", input_ukuran, input_provinsi, input_asal, input_tujuan)
        print("Harga Maxim Box : ", harga_MaximBox)
        print("Harga Go Box : ",harga_GoBox)
        print("Harga Grab Instant : ",harga_GrabInstant)

    except ukuranerror as e:
        print("Terjadi kesalahan : ", str(e))
    except ProvinsiTidakTersediaError as e:
        print("Terjadi kesalahan : ", str(e))
    except AsalTidakTersedia as e:
        print("Terjadi kesalahan : ", str(e))
    except TujuanTidakTersedia as e:
        print("Terjadi kesalahan : ", str(e))
    except Exception as e:
        print("Terjadi kesalahan : ", str(e))

if __name__ == "__main__":
    main()
    