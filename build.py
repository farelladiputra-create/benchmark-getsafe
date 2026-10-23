#!/usr/bin/env python3
"""Getsafe benchmark prototype.

One self-contained HTML file. Real app screenshots embedded as base64 on the
left, short plain-language notes on the right, tap-through navigation.

Lineage: same layout idea as the earlier PhonePe / Kakao / Paytm prototype
(phone left, notes right, back / next arrows). Copy is deliberately short, one
idea per bullet, so nothing needs scrolling.
"""

import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "layar-asli")
OUT = os.path.join(HERE, "index.html")

# Each screen: what is on it, why it is like that, what we can copy.
SCREENS = [
    {
        "id": "onboarding",
        "group": "1 · Masuk",
        "img": "01b-onboarding-slide2.jpg",
        "imglabel": "Slide pembuka: 'PREVENT RISKS. SAVE MONEY'",
        "title": "Tiga slide, satu janji: poin",
        "what": [
            "Slide 1: semua asuransi di satu tempat.",
            "Slide 2: cegah risiko, dapat 5.000 poin.",
            "Slide 3: minta bantuan lewat telepon.",
        ],
        "why": [
            "Sejak awal yang dijual poin, bukan polis.",
            "Bantuan manusia sudah ditawarkan sebelum akun jadi.",
        ],
        "forus": [
            "Buka app dengan satu janji yang bisa ditagih.",
            "Tawarkan bantuan sejak layar pertama.",
        ],
    },
    {
        "id": "login",
        "group": "1 · Masuk",
        "img": "03-login-code.jpg",
        "imglabel": "Layar kode 4 angka",
        "title": "Masuk pakai kode, tanpa password",
        "what": [
            "Isi email, lalu dapat kode 4 angka.",
            "Ada tombol 'I didn't get an email'.",
        ],
        "why": [
            "Tanpa password, jadi lebih sedikit orang yang gagal masuk.",
            "Kode 4 angka cepat disalin dari email.",
        ],
        "forus": [
            "Ganti password dengan kode sekali pakai.",
            "Selalu sediakan jalan keluar kalau email tidak datang.",
        ],
    },
    {
        "id": "coverage",
        "group": "2 · Isi app",
        "img": "05-coverage-home.jpg",
        "imglabel": "Tab Home (Coverage)",
        "title": "Home: cek dulu, baru tawarkan",
        "what": [
            "Kartu 'Protection Check' bilang 'Unprotected'.",
            "Empat saran: Liability, Income Protection, Pension, Contents.",
            "Dua label: 'Must-have' dan 'Nice-to-have'.",
        ],
        "why": [
            "Home tidak menampilkan 12 produk, hanya 4 yang paling mendesak.",
            "Urutannya ikut risiko hidup, bukan ikut harga.",
        ],
        "forus": [
            "Mulai dari 'cek risiko kamu', bukan dari daftar produk.",
            "Beri label wajib dan boleh ditunda.",
        ],
    },
    {
        "id": "products",
        "group": "2 · Isi app",
        "img": "06-products-top.jpg",
        "imglabel": "Tab Products, bagian atas",
        "title": "Products: filter ikut situasi hidup",
        "what": [
            "Filter: All, New to Germany, Starting a New Job.",
            "12 produk, harga 'from' di tiap kartu.",
            "Poin ditulis di bawah harga.",
        ],
        "why": [
            "Dua filter menjawab dua keadaan paling umum: baru pindah, baru kerja.",
            "Harga dan poin tampil bersamaan, jadi orang bisa banding.",
        ],
        "forus": [
            "Filter pakai situasi, bukan cuma jenis produk.",
            "Tulis poin sebagai angka di kartu.",
        ],
    },
    {
        "id": "product-detail",
        "group": "2 · Isi app",
        "img": "17-product-detail.jpg",
        "imglabel": "Halaman detail Liability",
        "title": "Detail: tiga kartu, satu tombol",
        "what": [
            "Tiga kartu: Worldwide, EUR 50M, Flexible.",
            "Janji 'Earn 60.000 Safepoints after purchase'.",
            "Kotak tanya dan tombol GetsafeAI ungu.",
        ],
        "why": [
            "Poin hanya cair setelah beli.",
            "Tombol 'Get quote' selalu menempel di bawah.",
        ],
        "forus": [
            "Ringkas benefit jadi tiga kartu.",
            "Beri tempat bertanya di halaman yang sedang dibaca.",
        ],
    },
    {
        "id": "quote-excess",
        "group": "2 · Isi app",
        "img": "19-get-quote-excess.jpg",
        "imglabel": "Layar pertama Get quote: pilih excess",
        "title": "Quote: tanya yang paling mengubah harga",
        "what": [
            "Pertanyaan pertama: pilih excess EUR 150 atau EUR 300.",
            "Ada contoh angka: klaim EUR 80, 150, 400.",
            "Tombol 'Correct, continue'.",
        ],
        "why": [
            "Excess adalah alat harga paling kuat, jadi ditanya dulu.",
            "Penjelasan pakai contoh, bukan definisi.",
        ],
        "forus": [
            "Tanya hal yang paling mengubah harga lebih dulu.",
            "Jelaskan istilah pakai angka.",
        ],
    },
    {
        "id": "quote-question",
        "group": "2 · Isi app",
        "img": "19c-quote-step2.jpg",
        "imglabel": "Pertanyaan riwayat polis",
        "title": "Satu pertanyaan, satu layar",
        "what": [
            "'Punya asuransi liability di Jerman 5 tahun terakhir?'",
            "Jawaban cuma Yes atau No.",
            "Catatan: kalau ikut polis orang tua atau pasangan, pilih No.",
        ],
        "why": [
            "Satu pertanyaan per layar, jadi tidak ada form panjang.",
            "Catatan kecil menutup kesalahan paling umum.",
        ],
        "forus": [
            "Satu pertanyaan per layar.",
            "Taruh catatan di bawah pertanyaan, bukan di halaman bantuan.",
        ],
    },
    {
        "id": "quote-postcode",
        "group": "2 · Isi app",
        "img": "19e-quote-postcode.jpg",
        "imglabel": "Layar kode pos",
        "title": "Kode pos: sudah diisi, tidak bisa diubah",
        "what": [
            "Kode pos 10178 sudah terisi dari profil.",
            "Info: 'This is the postcode you have entered before'.",
            "Untuk ubah, harus lewat Profile lalu Edit profile.",
        ],
        "why": [
            "Data profil dipakai ulang, jadi orang tidak mengetik dua kali.",
            "Tapi kalau salah, orang harus keluar dari alur beli.",
        ],
        "forus": [
            "Isi ulang data yang sudah ada.",
            "Beri tombol edit langsung di layar itu.",
        ],
    },
    {
        "id": "quote-price",
        "group": "2 · Isi app",
        "img": "20-quote-price.jpg",
        "imglabel": "Layar harga",
        "title": "Harga: satu angka besar, dua pilihan",
        "what": [
            "Angka besar: EUR 2,81 per bulan.",
            "Tanggal mulai bisa diubah.",
            "Banner 'Earn 60.000 Safepoints after purchase'.",
        ],
        "why": [
            "Harga bulanan ditulis besar, jadi mudah dibanding.",
            "Dua paket: Comfort EUR 2,14 dan Premium EUR 2,81.",
            "Tombol 'Next' menulis harga lagi.",
        ],
        "forus": [
            "Tampilkan harga bulanan sebagai angka utama.",
            "Tulis harga di tombol, biar tidak ada kejutan.",
        ],
    },
    {
        "id": "compare-plans",
        "group": "2 · Isi app",
        "img": "21-compare-plans.jpg",
        "imglabel": "Tabel banding paket",
        "title": "Bandingkan: tabel, bukan cerita",
        "what": [
            "Dua kolom: Comfort dan Premium.",
            "Batas tanggungan EUR 20 juta vs EUR 50 juta.",
            "Baris lain: cover global, bisa batal kapan saja, klaim lewat app.",
        ],
        "why": [
            "Beda utama langsung terlihat di baris pertama.",
            "Semua baris pakai centang, jadi cepat dibaca.",
        ],
        "forus": [
            "Pakai tabel untuk paket yang mirip.",
            "Tandai beda paling penting di baris atas.",
        ],
    },
    {
        "id": "claims",
        "group": "2 · Isi app",
        "img": "09-claims-centre.jpg",
        "imglabel": "Tab Claims",
        "title": "Klaim: dipandu, bukan formulir",
        "what": [
            "'Something happened? We're here for you'.",
            "Chatbot memandu klaim langkah demi langkah.",
            "Tombol 'File claim' menempel di bawah.",
        ],
        "why": [
            "Klaim itu momen panik, jadi diberi urutan langkah.",
            "Iklan Safepoints juga muncul di halaman ini.",
        ],
        "forus": [
            "Pakai langkah-langkah untuk klaim.",
            "Letakkan tawaran tambahan di halaman klaim.",
        ],
    },
    {
        "id": "safepoints",
        "group": "2 · Isi app",
        "img": "10-safepoints.jpg",
        "imglabel": "Tab Safepoints",
        "title": "Safepoints: poin dari tugas",
        "what": [
            "Saldo 0 poin dan EUR 0 credit.",
            "Dua tab: Actions dan Benefits.",
            "Tugas: lengkapi profil 2.000, kuis gigi 600, kuis care 200.",
        ],
        "why": [
            "Poin didapat dari mengerjakan hal, bukan hanya dari bayar.",
            "Poin terbesar untuk melengkapi profil.",
        ],
        "forus": [
            "Beri poin untuk tugas, bukan cuma diskon.",
            "Beri poin besar untuk data yang kamu butuhkan.",
        ],
    },
    {
        "id": "safepoints-vouchers",
        "group": "2 · Isi app",
        "img": "22c-safepoints-benefits3.jpg",
        "imglabel": "Tab Benefits, daftar voucher",
        "title": "Voucher: 2.000 poin jadi EUR 1",
        "what": [
            "Lieferando EUR 10 = 20.000 poin.",
            "Amazon EUR 15 = 30.000 poin.",
            "Netflix dan Uber EUR 25 = 50.000 poin.",
            "Ada tiga link bantuan dan syarat di bawah.",
        ],
        "why": [
            "Kursnya tetap 2.000 poin per euro, jadi mudah dihitung.",
            "Voucher dipilih dari merek yang sering dipakai orang.",
        ],
        "forus": [
            "Pakai satu kurs yang mudah dihitung.",
            "Pilih merek yang benar-benar dipakai sehari-hari.",
        ],
    },
    {
        "id": "voucher-detail",
        "group": "2 · Isi app",
        "img": "23-safepoints-how.jpg",
        "imglabel": "Detail voucher Netflix",
        "title": "Detail voucher: jelas sebelum tukar",
        "what": [
            "Judul 'EUR 25 Netflix voucher'.",
            "Bar progres 0 dari 50.000 poin.",
            "Dua baris: 'You redeem 50.000' dan 'You get EUR 25'.",
        ],
        "why": [
            "Orang lihat tepat berapa poin keluar dan apa yang masuk.",
            "Tombol tukar mati selama poin belum cukup.",
        ],
        "forus": [
            "Tulis poin keluar dan hadiah masuk berdampingan.",
            "Matikan tombol selama belum cukup, jangan sembunyikan.",
        ],
    },
    {
        "id": "safepoints-faq",
        "group": "2 · Isi app",
        "img": "24-safepoints-faq.jpg",
        "imglabel": "FAQ Safepoints",
        "title": "FAQ: aturan poin ditulis terbuka",
        "what": [
            "Delapan pertanyaan, dari 'apa itu' sampai 'bisa dipakai untuk asuransi apa'.",
            "Jawaban pertama: poin dikumpulkan dari tindakan, lalu jadi credit.",
            "Jawaban kedua: 2.000 poin sama dengan EUR 1.",
        ],
        "why": [
            "Orang tahu aturannya sebelum mengejar poin.",
            "Credit hanya bisa dipakai untuk delapan produk, tidak semua.",
        ],
        "forus": [
            "Tulis kurs poin di FAQ, jangan disembunyikan.",
            "Sebutkan produk mana saja yang menerima credit.",
        ],
    },
    {
        "id": "concierge",
        "group": "2 · Isi app",
        "img": "12-concierge.jpg",
        "imglabel": "Tab Service (Concierge)",
        "title": "Support: ada nama, ada status",
        "what": [
            "'Hi hermes', pakai nama depan.",
            "'Gabrielle is online', ajak menulis langsung.",
            "Empat tombol FAQ.",
        ],
        "why": [
            "Empat FAQ itu pertanyaan yang paling sering masuk.",
            "Nama dan status online bikin terasa manusia.",
        ],
        "forus": [
            "Tampilkan nama dan status online.",
            "Ubah pertanyaan yang sering jadi tombol.",
        ],
    },
    {
        "id": "profile",
        "group": "3 · Referral",
        "img": "13-profile.jpg",
        "imglabel": "Halaman Profile",
        "title": "Profile: referral di posisi kedua",
        "what": [
            "Di bawah nama: 'Refer your friends and get EUR 30'.",
            "'They'll get a EUR 15 credit, too!'.",
            "Tombol 'Invite friends'.",
        ],
        "why": [
            "Banner tidak disembunyikan di Settings.",
            "Hadiah berupa credit, bukan uang, jadi balik ke premi.",
        ],
        "forus": [
            "Taruh referral di atas halaman Profile.",
            "Sebut nominal kedua pihak.",
        ],
    },
    {
        "id": "referral-invite",
        "group": "3 · Referral",
        "img": "14-referral-invite.jpg",
        "imglabel": "Halaman Invite a friend",
        "title": "Undang: syaratnya bisa dihitung",
        "what": [
            "Judul 'GET EUR 30 FOR FREE'.",
            "Kamu dapat EUR 30, teman dapat EUR 15.",
            "Syaratnya: setelah teman beli polis pertama.",
            "Saldo EUR 0,00 dan 0 undangan diterima.",
        ],
        "why": [
            "Hadiah baru cair setelah polis pertama dibayar.",
            "Saldo dan jumlah undangan bikin progres kelihatan.",
        ],
        "forus": [
            "Tulis syarat dalam satu kalimat.",
            "Tampilkan saldo dan progres.",
        ],
    },
    {
        "id": "referral-share",
        "group": "3 · Referral",
        "img": "15-referral-share-sheet.jpg",
        "imglabel": "Share sheet Android",
        "title": "Pesan share: link ada, hadiah tidak disebut",
        "what": [
            "Pesan: 'Join me and over 500,000 users...'.",
            "Link dan kode FEXD-KRL3 ikut terkirim.",
            "Share sheet Android biasa.",
        ],
        "why": [
            "Link berbrand, jadi bisa dilacak.",
            "Tapi EUR 15 dan syarat beli tidak ada di pesan.",
        ],
        "forus": [
            "Tulis nominal di pesan yang dikirim.",
            "Sebut syarat singkat di pesan.",
        ],
    },
    {
        "id": "referral-landing",
        "group": "3 · Referral",
        "img": "16-referral-landing-web.jpg",
        "imglabel": "Halaman web untuk teman",
        "title": "Teman buka web, bukan app",
        "what": [
            "'You received EUR 15 Getsafe credit'.",
            "Syarat: beli polis pertama.",
            "Bukti sosial: 500.000 pelanggan, rating 4,5.",
            "Tiga langkah: pilih, dapat harga, bayar.",
        ],
        "why": [
            "Tanpa install, hambatan masuk kecil.",
            "Nominal hadiah ada di paling atas.",
        ],
        "forus": [
            "Bikin halaman undangan di web.",
            "Taruh nominal di atas layar.",
            "Tambah bukti sosial.",
        ],
    },
]

# --------------------------------------------------------------- build ----
def b64(fname):
    with open(os.path.join(SHOTS, fname), "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


def main():
    imgs = {}
    for s in SCREENS:
        if s["img"] not in imgs:
            imgs[s["img"]] = b64(s["img"])

    payload = [{
        "id": s["id"], "group": s["group"], "img": s["img"],
        "imglabel": s["imglabel"], "title": s["title"],
        "what": s["what"], "why": s["why"], "forus": s["forus"],
    } for s in SCREENS]

    data_json = json.dumps({"screens": payload, "imgs": imgs}, ensure_ascii=False)

    with open(os.path.join(HERE, "template.html"), "r", encoding="utf-8") as fh:
        html = fh.read()

    html = html.replace("__DATA__", data_json)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
