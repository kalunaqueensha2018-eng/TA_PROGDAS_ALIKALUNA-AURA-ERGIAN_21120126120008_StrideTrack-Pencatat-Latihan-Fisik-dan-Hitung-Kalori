import tkinter as tk
from tkinter import ttk, messagebox

from kalkulator import JENIS_OLAHRAGA, MET_OLAHRAGA, KalkulatorKebugaran
from model_sesi import SesiLatihan, PelacakKebugaran
from validator import ValidatorInputSesi


class StrideTrackApp:
    """Antarmuka grafis utama aplikasi StrideTrack bertema pastel lembut."""

    def __init__(self, root):
        self.root = root
        self.root.title("StrideTrack - Pencatatan Latihan Fisik & Perhitungan Kalori")
        self.root.geometry("1080x670")
        self.root.minsize(950, 590)

        self.warna = {
            "bg_utama": "#F6F8FC",
            "bg_kartu": "#FFFFFF",
            "border_halus": "#DCE5F2",
            "header_bg": "#DCEBFA",
            "header_badge": "#D8EFE3",
            "kuning_pastel": "#FFF5D6",
            "hijau_pastel": "#DDF2E6",
            "biru_tombol": "#7EA6E0",
            "biru_hover": "#6B95D6",
            "pink_hapus": "#F6C8CC",
            "abu_tombol": "#E8EEF7",
            "baris_ganjil": "#FFFFFF",
            "baris_genap": "#F2F7FD",
            "teks_utama": "#27364B",
            "teks_sub": "#5C6F87",
        }

        self.font_keluarga = "Segoe UI"
        self.validator = ValidatorInputSesi(JENIS_OLAHRAGA)
        self.kalkulator = KalkulatorKebugaran(JENIS_OLAHRAGA, MET_OLAHRAGA)
        self.pelacak = PelacakKebugaran("riwayat_stridetrack.csv")
        self.pelacak.muat_dari_csv()

        self._atur_gaya_ttk()
        self._bangun_ui()
        self._muat_awal_data()

    def _atur_gaya_ttk(self):
        self.root.configure(bg=self.warna["bg_utama"])
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "Pastel.TCombobox",
            fieldbackground=self.warna["bg_kartu"],
            background=self.warna["header_bg"],
            foreground=self.warna["teks_utama"],
            bordercolor=self.warna["border_halus"],
            lightcolor=self.warna["header_bg"],
            darkcolor=self.warna["header_bg"],
            arrowcolor=self.warna["teks_utama"],
            padding=5,
        )
        style.map(
            "Pastel.TCombobox",
            fieldbackground=[("readonly", self.warna["bg_kartu"])],
            selectbackground=[("readonly", self.warna["header_bg"])],
            selectforeground=[("readonly", self.warna["teks_utama"])],
        )

        style.configure(
            "Pastel.Treeview",
            background=self.warna["baris_ganjil"],
            foreground=self.warna["teks_utama"],
            fieldbackground=self.warna["baris_ganjil"],
            bordercolor=self.warna["border_halus"],
            rowheight=28,
            font=(self.font_keluarga, 9),
        )
        style.configure(
            "Pastel.Treeview.Heading",
            background=self.warna["header_bg"],
            foreground=self.warna["teks_utama"],
            bordercolor=self.warna["border_halus"],
            relief="flat",
            padding=(6, 7),
            font=(self.font_keluarga, 9, "bold"),
        )
        style.map(
            "Pastel.Treeview.Heading",
            background=[("active", "#C8DFF7")],
        )
        style.map(
            "Pastel.Treeview",
            background=[("selected", "#CBE0FA")],
            foreground=[("selected", self.warna["teks_utama"])],
        )

        style.configure(
            "Pastel.Vertical.TScrollbar",
            background=self.warna["header_bg"],
            troughcolor=self.warna["bg_utama"],
            bordercolor=self.warna["border_halus"],
            arrowcolor=self.warna["teks_sub"],
        )

    def _buat_entry_pastel(self, parent, nilai_awal=""):
        entry = tk.Entry(
            parent,
            font=(self.font_keluarga, 10),
            bg=self.warna["bg_kartu"],
            fg=self.warna["teks_utama"],
            insertbackground=self.warna["teks_utama"],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=self.warna["border_halus"],
            highlightcolor=self.warna["biru_tombol"],
        )
        if nilai_awal != "":
            entry.insert(0, str(nilai_awal))
        return entry

    def _bangun_ui(self):
        frame_header = tk.Frame(
            self.root,
            bg=self.warna["header_bg"],
            padx=20,
            pady=14,
            highlightbackground=self.warna["border_halus"],
            highlightthickness=1,
        )
        frame_header.pack(fill=tk.X, padx=16, pady=(14, 6))

        tk.Label(
            frame_header,
            text="StrideTrack",
            font=(self.font_keluarga, 19, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["header_bg"],
        ).pack(side=tk.LEFT)

        tk.Label(
            frame_header,
            text="  Konsistensi > Kesempurnaan  ·  Pelacak Latihan Fisik & Kalori Mandiri  ",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["header_badge"],
            padx=8,
            pady=4,
        ).pack(side=tk.LEFT, padx=(14, 0), pady=(2, 0))

        frame_konten = tk.Frame(self.root, bg=self.warna["bg_utama"], padx=16, pady=8)
        frame_konten.pack(fill=tk.BOTH, expand=True)

        panel_kiri = tk.LabelFrame(
            frame_konten,
            text="  Input Sesi & Kalkulator  ",
            font=(self.font_keluarga, 10, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
            padx=14,
            pady=12,
            width=385,
            relief="solid",
            bd=1,
            highlightbackground=self.warna["border_halus"],
        )
        panel_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        panel_kiri.pack_propagate(False)

        panel_kanan = tk.Frame(frame_konten, bg=self.warna["bg_utama"])
        panel_kanan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_kiri,
            text="Jenis Olahraga",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
        ).pack(anchor=tk.W)

        self.combo_jenis = ttk.Combobox(
            panel_kiri,
            values=JENIS_OLAHRAGA,
            state="readonly",
            style="Pastel.TCombobox",
            font=(self.font_keluarga, 10),
        )
        self.combo_jenis.set("Lari")
        self.combo_jenis.pack(fill=tk.X, pady=(3, 9))
        self.combo_jenis.bind("<<ComboboxSelected>>", self._on_jenis_berubah)

        tk.Label(
            panel_kiri,
            text="Durasi Latihan (menit) *",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
        ).pack(anchor=tk.W)
        self.entry_durasi = self._buat_entry_pastel(panel_kiri)
        self.entry_durasi.pack(fill=tk.X, pady=(3, 9), ipady=4)

        self.label_jarak = tk.Label(
            panel_kiri,
            text="Jarak Tempuh (km)",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
        )
        self.label_jarak.pack(anchor=tk.W)
        self.entry_jarak = self._buat_entry_pastel(panel_kiri, "0")
        self.entry_jarak.pack(fill=tk.X, pady=(3, 9), ipady=4)

        tk.Label(
            panel_kiri,
            text="Berat Badan (kg) *",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
        ).pack(anchor=tk.W)
        self.entry_berat = self._buat_entry_pastel(panel_kiri, "51")
        self.entry_berat.pack(fill=tk.X, pady=(3, 9), ipady=4)

        tk.Label(
            panel_kiri,
            text="Target Kalori Sesi (kkal, opsional)",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
        ).pack(anchor=tk.W)
        self.entry_target = self._buat_entry_pastel(panel_kiri)
        self.entry_target.pack(fill=tk.X, pady=(3, 12), ipady=4)

        frame_tombol_1 = tk.Frame(panel_kiri, bg=self.warna["bg_kartu"])
        frame_tombol_1.pack(fill=tk.X, pady=(0, 7))

        self.btn_hitung_simpan = tk.Button(
            frame_tombol_1,
            text="Hitung & Simpan Sesi",
            font=(self.font_keluarga, 10, "bold"),
            bg=self.warna["biru_tombol"],
            activebackground=self.warna["biru_hover"],
            fg=self.warna["teks_utama"],
            activeforeground=self.warna["teks_utama"],
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self.hitung_dan_simpan,
        )
        self.btn_hitung_simpan.pack(fill=tk.X)

        frame_tombol_2 = tk.Frame(panel_kiri, bg=self.warna["bg_kartu"])
        frame_tombol_2.pack(fill=tk.X)

        tk.Button(
            frame_tombol_2,
            text="Bersihkan Form",
            font=(self.font_keluarga, 9, "bold"),
            bg=self.warna["abu_tombol"],
            activebackground="#D7E2F2",
            fg=self.warna["teks_utama"],
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.bersihkan_form,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        tk.Button(
            frame_tombol_2,
            text="Simpan ke File",
            font=(self.font_keluarga, 9, "bold"),
            bg=self.warna["hijau_pastel"],
            activebackground="#C7E8D6",
            fg=self.warna["teks_utama"],
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.simpan_manual_csv,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        frame_hasil = tk.LabelFrame(
            panel_kiri,
            text="  Hasil Perhitungan Terakhir  ",
            font=(self.font_keluarga, 9, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["kuning_pastel"],
            padx=12,
            pady=10,
            relief="solid",
            bd=1,
            highlightbackground="#EADCA6",
        )
        frame_hasil.pack(fill=tk.BOTH, expand=True, pady=(14, 0))

        self.label_hasil_kalori = tk.Label(
            frame_hasil,
            text="Kalori Terbakar: - kkal",
            font=(self.font_keluarga, 11, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["kuning_pastel"],
            anchor=tk.W,
        )
        self.label_hasil_kalori.pack(fill=tk.X, pady=(0, 5))

        self.label_hasil_metrik = tk.Label(
            frame_hasil,
            text="Kecepatan / Pace: -",
            font=(self.font_keluarga, 9),
            fg=self.warna["teks_utama"],
            bg=self.warna["kuning_pastel"],
            anchor=tk.W,
            justify=tk.LEFT,
        )
        self.label_hasil_metrik.pack(fill=tk.X, pady=(0, 5))

        self.label_hasil_target = tk.Label(
            frame_hasil,
            text="Status Target: -",
            font=(self.font_keluarga, 9, "italic"),
            fg=self.warna["teks_sub"],
            bg=self.warna["kuning_pastel"],
            anchor=tk.W,
            justify=tk.LEFT,
        )
        self.label_hasil_target.pack(fill=tk.X)

        frame_riwayat = tk.LabelFrame(
            panel_kanan,
            text="  Riwayat Sesi Latihan  ",
            font=(self.font_keluarga, 10, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["bg_kartu"],
            padx=12,
            pady=10,
            relief="solid",
            bd=1,
            highlightbackground=self.warna["border_halus"],
        )
        frame_riwayat.pack(fill=tk.BOTH, expand=True)

        kolom_tabel = ("olahraga", "durasi", "jarak", "kalori", "keterangan")
        self.tabel = ttk.Treeview(
            frame_riwayat,
            columns=kolom_tabel,
            show="headings",
            height=14,
            style="Pastel.Treeview",
        )

        self.tabel.heading("olahraga", text="Olahraga")
        self.tabel.heading("durasi", text="Durasi (mnt)")
        self.tabel.heading("jarak", text="Jarak (km)")
        self.tabel.heading("kalori", text="Kalori (kkal)")
        self.tabel.heading("keterangan", text="Pace / Kecepatan & Target")

        self.tabel.column("olahraga", width=120, anchor=tk.W)
        self.tabel.column("durasi", width=90, anchor=tk.CENTER)
        self.tabel.column("jarak", width=90, anchor=tk.CENTER)
        self.tabel.column("kalori", width=100, anchor=tk.CENTER)
        self.tabel.column("keterangan", width=250, anchor=tk.W)

        self.tabel.tag_configure("ganjil", background=self.warna["baris_ganjil"])
        self.tabel.tag_configure("genap", background=self.warna["baris_genap"])

        scrollbar_y = ttk.Scrollbar(
            frame_riwayat,
            orient=tk.VERTICAL,
            command=self.tabel.yview,
            style="Pastel.Vertical.TScrollbar",
        )
        self.tabel.configure(yscrollcommand=scrollbar_y.set)

        self.tabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        frame_bawah_kanan = tk.Frame(panel_kanan, bg=self.warna["bg_utama"], pady=10)
        frame_bawah_kanan.pack(fill=tk.X)

        tk.Button(
            frame_bawah_kanan,
            text="Hapus Sesi Terpilih",
            font=(self.font_keluarga, 9, "bold"),
            bg=self.warna["pink_hapus"],
            activebackground="#EEB2B7",
            fg=self.warna["teks_utama"],
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=7,
            command=self.hapus_sesi_terpilih,
        ).pack(side=tk.LEFT)

        frame_rekap_box = tk.Frame(
            frame_bawah_kanan,
            bg=self.warna["hijau_pastel"],
            padx=14,
            pady=7,
            highlightbackground="#B7DEC8",
            highlightthickness=1,
        )
        frame_rekap_box.pack(side=tk.RIGHT)

        self.label_rekap = tk.Label(
            frame_rekap_box,
            text="Total: 0 Sesi  |  0.0 mnt  |  0.00 km  |  0.0 kkal",
            font=(self.font_keluarga, 10, "bold"),
            fg=self.warna["teks_utama"],
            bg=self.warna["hijau_pastel"],
        )
        self.label_rekap.pack()

    def _on_jenis_berubah(self, _event=None):
        jenis = self.combo_jenis.get()
        if jenis == "Latihan Kekuatan":
            self.label_jarak.config(text="Jarak Tempuh (km) - opsional / 0 untuk workout")
            self.entry_jarak.delete(0, tk.END)
            self.entry_jarak.insert(0, "0")
        else:
            self.label_jarak.config(text="Jarak Tempuh (km)")

    def _validasi_dan_ambil_input(self):
        hasil, pesan_error = self.validator.validasi(
            self.combo_jenis.get(),
            self.entry_durasi.get(),
            self.entry_jarak.get(),
            self.entry_berat.get(),
            self.entry_target.get(),
        )
        if pesan_error is not None:
            level, judul, isi = pesan_error
            if level == "error":
                messagebox.showerror(judul, isi)
            elif level == "warning":
                messagebox.showwarning(judul, isi)
            else:
                messagebox.showinfo(judul, isi)
            return None

        return hasil

    def hitung_dan_simpan(self):
        hasil_input = self._validasi_dan_ambil_input()
        if hasil_input is None:
            return

        jenis, durasi, jarak, berat, target = hasil_input
        sesi_baru = SesiLatihan(
            jenis=jenis,
            durasi_menit=durasi,
            jarak_km=jarak,
            berat_kg=berat,
            target_kalori=target,
        )

        self.pelacak.tambah_sesi(sesi_baru)
        self.pelacak.simpan_ke_csv()

        self._tampilkan_hasil_terakhir(sesi_baru)
        self._segarkan_tabel_dan_rekap()
        self.bersihkan_form(pertahankan_berat=True)

    def hapus_sesi_terpilih(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showinfo("Pilih Baris", "Klik salah satu baris sesi di tabel riwayat untuk menghapusnya.")
            return

        indeks_baris = self.tabel.index(terpilih[0])
        konfirmasi = messagebox.askyesno("Konfirmasi Hapus", "Hapus sesi latihan yang dipilih dari riwayat?")
        if not konfirmasi:
            return

        self.pelacak.hapus_sesi_di_indeks(indeks_baris)
        self.pelacak.simpan_ke_csv()
        self._segarkan_tabel_dan_rekap()

    def simpan_manual_csv(self):
        self.pelacak.simpan_ke_csv()
        messagebox.showinfo("Tersimpan", f"Data riwayat berhasil disimpan ke '{self.pelacak.nama_file}'.")

    def bersihkan_form(self, pertahankan_berat=False):
        self.entry_durasi.delete(0, tk.END)
        self.entry_jarak.delete(0, tk.END)
        self.entry_jarak.insert(0, "0")
        self.entry_target.delete(0, tk.END)
        if not pertahankan_berat:
            self.entry_berat.delete(0, tk.END)

    def _tampilkan_hasil_terakhir(self, sesi):
        self.label_hasil_kalori.config(text=f"Kalori Terbakar: {sesi.kalori:.1f} kkal ({sesi.jenis})")
        self.label_hasil_metrik.config(text=f"Metrik: {sesi.keterangan_pace}")
        self.label_hasil_target.config(text=f"Target: {sesi.status_target}")

    def _segarkan_tabel_dan_rekap(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        for idx, sesi in enumerate(self.pelacak.daftar_sesi):
            tag_baris = "genap" if idx % 2 == 1 else "ganjil"
            self.tabel.insert("", tk.END, values=sesi.ke_baris_tabel(), tags=(tag_baris,))

        rekap = self.pelacak.ambil_rekap()
        self.label_rekap.config(
            text=(
                f"Total: {rekap['total_sesi']} Sesi  |  "
                f"{rekap['total_durasi']:.1f} mnt  |  "
                f"{rekap['total_jarak']:.2f} km  |  "
                f"{rekap['total_kalori']:.1f} kkal"
            )
        )

    def _muat_awal_data(self):
        self._segarkan_tabel_dan_rekap()
        if self.pelacak.daftar_sesi:
            self._tampilkan_hasil_terakhir(self.pelacak.daftar_sesi[-1])


if __name__ == "__main__":
    root = tk.Tk()
    app = StrideTrackApp(root)
    root.mainloop()