import csv
import os


class PenyimpanRiwayatCSV:
    """Mengurus penyimpanan dan pemuatan data riwayat ke/dari file CSV."""

    KOLOM_CSV = [
        "jenis",
        "durasi_menit",
        "jarak_km",
        "berat_kg",
        "target_kalori",
        "kalori",
        "kecepatan_kmh",
        "pace_min_per_km",
        "keterangan_pace",
        "status_target",
    ]

    def __init__(self, nama_file="riwayat_stridetrack.csv"):
        self.nama_file = nama_file

    def simpan_sesi(self, daftar_sesi):
        with open(self.nama_file, mode="w", newline="", encoding="utf-8") as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=self.KOLOM_CSV)
            writer.writeheader()
            for sesi in daftar_sesi:
                writer.writerow(sesi.ke_dict_csv())

    def muat_sesi(self, pembuat_objek_sesi):
        hasil_sesi = []
        if not os.path.exists(self.nama_file):
            return hasil_sesi

        with open(self.nama_file, mode="r", newline="", encoding="utf-8") as file_csv:
            reader = csv.DictReader(file_csv)
            for baris in reader:
                try:
                    sesi = pembuat_objek_sesi(
                        jenis=baris.get("jenis", "Lari"),
                        durasi_menit=float(baris.get("durasi_menit", 0)),
                        jarak_km=float(baris.get("jarak_km", 0)),
                        berat_kg=float(baris.get("berat_kg", 50)),
                        target_kalori=float(baris.get("target_kalori", 0)),
                        kalori=float(baris.get("kalori", 0)),
                        kecepatan_kmh=float(baris.get("kecepatan_kmh", 0)),
                        pace_min_per_km=float(baris.get("pace_min_per_km", 0)),
                        keterangan_pace=baris.get("keterangan_pace", ""),
                        status_target=baris.get("status_target", ""),
                    )
                    hasil_sesi.append(sesi)
                except (ValueError, KeyError):
                    continue
        return hasil_sesi