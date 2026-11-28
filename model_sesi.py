from kalkulator import (
    hitung_kalori,
    hitung_kecepatan_dan_pace,
    evaluasi_target,
    rekap_riwayat,
)
from penyimpan_csv import PenyimpanRiwayatCSV


class SesiLatihan:
    """Merepresentasikan satu data sesi latihan fisik beserta hasil perhitungannya."""

    def __init__(
        self,
        jenis,
        durasi_menit,
        jarak_km,
        berat_kg,
        target_kalori=None,
        kalori=None,
        kecepatan_kmh=None,
        pace_min_per_km=None,
        keterangan_pace=None,
        status_target=None,
    ):
        self.jenis = str(jenis)
        self.durasi_menit = float(durasi_menit)
        self.jarak_km = float(jarak_km)
        self.berat_kg = float(berat_kg)
        self.target_kalori = float(target_kalori) if target_kalori is not None else 0.0

        if kalori is None:
            self.kalori = hitung_kalori(self.jenis, self.durasi_menit, self.berat_kg, self.jarak_km)
        else:
            self.kalori = float(kalori)

        if kecepatan_kmh is None or pace_min_per_km is None or keterangan_pace is None:
            spd, pace, ket = hitung_kecepatan_dan_pace(self.jenis, self.jarak_km, self.durasi_menit)
            self.kecepatan_kmh = spd
            self.pace_min_per_km = pace
            self.keterangan_pace = ket
        else:
            self.kecepatan_kmh = float(kecepatan_kmh)
            self.pace_min_per_km = float(pace_min_per_km)
            self.keterangan_pace = str(keterangan_pace)

        if status_target is None:
            self.status_target = evaluasi_target(self.kalori, self.target_kalori)
        else:
            self.status_target = str(status_target)

    def ke_baris_tabel(self):
        """Mengembalikan tuple nilai untuk ditampilkan pada Treeview GUI."""
        durasi_tampil = int(self.durasi_menit) if self.durasi_menit.is_integer() else round(self.durasi_menit, 1)
        jarak_tampil = f"{self.jarak_km:.2f}" if self.jarak_km > 0 else "-"
        kalori_tampil = f"{self.kalori:.1f}"
        ringkasan_ket = f"{self.keterangan_pace} | {self.status_target}"
        return (self.jenis, durasi_tampil, jarak_tampil, kalori_tampil, ringkasan_ket)

    def ke_dict_csv(self):
        """Mengembalikan dictionary untuk disimpan ke file CSV."""
        return {
            "jenis": self.jenis,
            "durasi_menit": self.durasi_menit,
            "jarak_km": self.jarak_km,
            "berat_kg": self.berat_kg,
            "target_kalori": self.target_kalori,
            "kalori": self.kalori,
            "kecepatan_kmh": self.kecepatan_kmh,
            "pace_min_per_km": self.pace_min_per_km,
            "keterangan_pace": self.keterangan_pace,
            "status_target": self.status_target,
        }


class PelacakKebugaran:
    """Mengelola array/list objek SesiLatihan serta operasi penyimpanan CSV."""

    def __init__(self, nama_file="riwayat_stridetrack.csv"):
        self.nama_file = nama_file
        self.penyimpan = PenyimpanRiwayatCSV(nama_file)
        self.daftar_sesi = []

    def tambah_sesi(self, sesi):
        self.daftar_sesi.append(sesi)

    def hapus_sesi_di_indeks(self, indeks):
        if 0 <= indeks < len(self.daftar_sesi):
            return self.daftar_sesi.pop(indeks)
        return None

    def ambil_rekap(self):
        return rekap_riwayat(self.daftar_sesi)

    def simpan_ke_csv(self):
        self.penyimpan.simpan_sesi(self.daftar_sesi)

    def muat_dari_csv(self):
        self.daftar_sesi = self.penyimpan.muat_sesi(SesiLatihan)