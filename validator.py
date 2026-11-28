from kalkulator import JENIS_OLAHRAGA


class ValidatorInputSesi:
    """Memvalidasi masukan pengguna dari form GUI sebelum dibuat objek SesiLatihan."""

    def __init__(self, daftar_jenis=None):
        self.daftar_jenis = daftar_jenis if daftar_jenis is not None else JENIS_OLAHRAGA

    def validasi(self, jenis, teks_durasi, teks_jarak, teks_berat, teks_target):
        jenis_bersih = str(jenis).strip()
        if jenis_bersih not in self.daftar_jenis:
            return None, ("error", "Input Tidak Valid", "Silakan pilih jenis olahraga yang tersedia.")

        durasi_str = str(teks_durasi).strip().replace(",", ".")
        jarak_str = str(teks_jarak).strip().replace(",", ".")
        berat_str = str(teks_berat).strip().replace(",", ".")
        target_str = str(teks_target).strip().replace(",", ".")

        if not durasi_str or not berat_str:
            return None, ("warning", "Input Kurang", "Durasi latihan (menit) dan berat badan (kg) wajib diisi.")

        try:
            durasi = float(durasi_str)
            berat = float(berat_str)
            jarak = float(jarak_str) if jarak_str else 0.0
            target = float(target_str) if target_str else 0.0
        except ValueError:
            return None, (
                "error",
                "Format Angka Salah",
                "Pastikan durasi, jarak, berat badan, dan target berupa angka valid.",
            )

        if durasi <= 0:
            return None, ("warning", "Nilai Tidak Valid", "Durasi latihan harus lebih dari 0 menit.")

        if berat <= 0:
            return None, ("warning", "Nilai Tidak Valid", "Berat badan harus lebih dari 0 kg.")

        if jarak < 0:
            return None, ("warning", "Nilai Tidak Valid", "Jarak tempuh tidak boleh bernilai negatif.")

        if target < 0:
            return None, ("warning", "Nilai Tidak Valid", "Target kalori tidak boleh bernilai negatif.")

        return (jenis_bersih, durasi, jarak, berat, target), None