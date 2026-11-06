import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

# Konfigurasi halaman web
st.set_page_config(page_title="Penggabung PDF Selang-Seling", page_icon="📄")

st.title("📄 Web Penggabung PDF Selang-Seling")
st.write("Unggah file pertama (1.pdf) dan file kedua (2.pdf) untuk menggabungkan halamannya secara berselang-seling otomatis.")

# Input unggahan terpisah untuk menjaga urutan file A dan file B
file_a = st.file_uploader("Unggah File Pertama (PDF 1)", type="pdf", key="pdf1")
file_b = st.file_uploader("Unggah File Kedua (PDF 2)", type="pdf", key="pdf2")

if file_a and file_b:
    st.success("Kedua file berhasil diunggah!")
    
    if st.button("Gabungkan PDF Selang-Seling"):
        with st.spinner("Sedang memproses halaman..."):
            try:
                # Membaca kedua file PDF
                reader_a = PdfReader(io.BytesIO(file_a.read()))
                reader_b = PdfReader(io.BytesIO(file_b.read()))
                
                # Inisialisasi penulis PDF baru
                merger = PdfWriter()
                
                # Mendapatkan jumlah total halaman dari masing-masing file
                len_a = len(reader_a.pages)
                len_b = len(reader_b.pages)
                
                # Mengambil jumlah putaran maksimal berdasarkan file yang memiliki halaman paling banyak
                max_pages = max(len_a, len_b)
                
                # Proses penggabungan selang-seling halaman demi halaman
                for i in range(max_pages):
                    # Jika file A masih memiliki halaman di indeks ke-i, masukkan
                    if i < len_a:
                        merger.add_page(reader_a.pages[i])
                    
                    # Jika file B masih memiliki halaman di indeks ke-i, masukkan
                    if i < len_b:
                        merger.add_page(reader_b.pages[i])
                
                # Menyimpan hasil ke memori sementara (buffer)
                output_pdf = io.BytesIO()
                merger.write(output_pdf)
                merger.close()
                output_pdf.seek(0)
                
                st.success("🎉 Penggabungan selang-seling selesai!")
                
                # Tombol unduh untuk pengguna
                st.download_button(
                    label="📥 Unduh Hasil Gabungan",
                    data=output_pdf,
                    file_name="gabungan_selang_seling.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
elif file_a or file_b:
    st.info("Silakan unggah kedua file PDF terlebih dahulu untuk mulai menggabungkan.")
