# ==============================================================================
# MODUL 1, 2, 3, 4 & 5: DATA ACUAN, FUNGSI PERHITUNGAN, DAN CLASS KALKULATOR
# ==============================================================================

JENIS_OLAHRAGA = [
    "Lari",
    "Jalan Kaki",
    "Bersepeda",
    "Renang",
    "Latihan Kekuatan",
]

MET_OLAHRAGA = {
    "Lari": 8.3,
    "Jalan Kaki": 3.5,
    "Bersepeda": 6.8,
    "Renang": 6.0,
    "Latihan Kekuatan": 4.5,
}


def hitung_kalori(jenis, durasi_menit, berat_kg, jarak_km=0.0):
    """Menghitung estimasi kalori terbakar (kkal) berbasis MET, berat badan, dan durasi."""
    met_dasar = MET_OLAHRAGA.get(jenis, 4.0)
    durasi_jam = durasi_menit / 60.0

    if jenis == "Lari" and jarak_km > 0:
        kecepatan = jarak_km / durasi_jam
        if kecepatan >= 10.0:
            met_efektif = 9.8
        elif kecepatan >= 8.0:
            met_efektif = 8.3
        else:
            met_efektif = 7.0
    elif jenis == "Jalan Kaki" and jarak_km > 0:
        kecepatan = jarak_km / durasi_jam
        if kecepatan >= 5.0:
            met_efektif = 4.3
        else:
            met_efektif = 3.5
    elif jenis == "Bersepeda" and jarak_km > 0:
        kecepatan = jarak_km / durasi_jam
        if kecepatan >= 19.0:
            met_efektif = 8.0
        elif kecepatan >= 16.0:
            met_efektif = 6.8
        else:
            met_efektif = 5.5
    elif jenis == "Renang":
        met_efektif = met_dasar
    elif jenis == "Latihan Kekuatan":
        met_efektif = met_dasar
    else:
        met_efektif = met_dasar

    kalori = met_efektif * berat_kg * durasi_jam
    return round(kalori, 1)


def hitung_kecepatan_dan_pace(jenis, jarak_km, durasi_menit):
    """Menghitung kecepatan rata-rata (km/jam) dan pace (menit/km) jika jarak > 0."""
    if jenis == "Latihan Kekuatan":
        return 0.0, 0.0, "Berbasis durasi (tanpa jarak)"

    if jarak_km > 0 and durasi_menit > 0:
        kecepatan_kmh = round(jarak_km / (durasi_menit / 60.0), 2)
        pace_min_per_km = round(durasi_menit / jarak_km, 2)
        keterangan = f"{kecepatan_kmh:.2f} km/jam | {pace_min_per_km:.2f} mnt/km"
        return kecepatan_kmh, pace_min_per_km, keterangan

    return 0.0, 0.0, "Jarak tidak dicatat"


def evaluasi_target(kalori, target_kalori):
    """Mengevaluasi pencapaian target kalori sesi."""
    if target_kalori is None or target_kalori <= 0:
        return "Target tidak diatur"

    selisih = round(kalori - target_kalori, 1)
    if kalori >= target_kalori:
        return f"Target tercapai (+{selisih:.1f} kkal)"
    else:
        kurang = abs(selisih)
        return f"Kurang {kurang:.1f} kkal dari target"


def rekap_riwayat(daftar_sesi):
    """Perulangan (for) untuk merekap total sesi, durasi, jarak, dan kalori."""
    total_sesi = len(daftar_sesi)
    total_durasi = 0.0
    total_jarak = 0.0
    total_kalori = 0.0

    for sesi in daftar_sesi:
        total_durasi += sesi.durasi_menit
        total_jarak += sesi.jarak_km
        total_kalori += sesi.kalori

    return {
        "total_sesi": total_sesi,
        "total_durasi": round(total_durasi, 1),
        "total_jarak": round(total_jarak, 2),
        "total_kalori": round(total_kalori, 1),
    }


class KalkulatorKebugaran:
    """Membungkus fungsi perhitungan kalori, kecepatan/pace, dan evaluasi target."""

    def __init__(self, daftar_jenis=None, data_met=None):
        self.daftar_jenis = daftar_jenis if daftar_jenis is not None else JENIS_OLAHRAGA
        self.data_met = data_met if data_met is not None else MET_OLAHRAGA

    def hitung_kalori_sesi(self, jenis, durasi_menit, berat_kg, jarak_km=0.0):
        return hitung_kalori(jenis, durasi_menit, berat_kg, jarak_km)

    def hitung_metrik_gerak(self, jenis, jarak_km, durasi_menit):
        return hitung_kecepatan_dan_pace(jenis, jarak_km, durasi_menit)

    def cek_target_kalori(self, kalori, target_kalori):
        return evaluasi_target(kalori, target_kalori)