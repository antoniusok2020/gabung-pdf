import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

# Konfigurasi halaman web
st.set_page_config(page_title="Penggabung PDF Selang-Seling v3", page_icon="📄")

st.title("📄 Web Penggabung PDF Selang-Seling (Fixed RAM)")
st.write("Versi optimasi untuk file berukuran besar hingga 500 MB.")

# Input unggahan terpisah
file_a = st.file_uploader("Unggah File Pertama (PDF 1)", type="pdf", key="pdf1")
file_b = st.file_uploader("Unggah File Kedua (PDF 2)", type="pdf", key="pdf2")

if file_a and file_b:
    st.success("Kedua file siap diproses!")
    
    if st.button("Gabungkan PDF Selang-Seling Sekarang"):
        with st.spinner("Sedang memproses halaman file besar... Mohon tunggu..."):
            try:
                # Membaca langsung dari objek file Streamlit
                reader_a = PdfReader(file_a)
                reader_b = PdfReader(file_b)
                
                merger = PdfWriter()
                
                len_a = len(reader_a.pages)
                len_b = len(reader_b.pages)
                max_pages = max(len_a, len_b)
                
                # Proses penggabungan selang-seling
                for i in range(max_pages):
                    if i < len_a:
                        merger.add_page(reader_a.pages[i])
                    if i < len_b:
                        merger.add_page(reader_b.pages[i])
                
                # SOLUSI: Menggunakan BytesIO untuk menampung aliran data hasil penggabungan
                bytes_buffer = io.BytesIO()
                merger.write(bytes_buffer)
                merger.close()
                
                # Mengembalikan posisi pembacaan buffer ke awal agar bisa diunduh
                bytes_buffer.seek(0)
                
                st.success("🎉 Penggabungan selesai! Siap diunduh.")
                
                # Tombol unduh dengan memanggil data yang sudah dialirkan ke buffer
                st.download_button(
                    label="📥 Unduh Hasil Gabungan",
                    data=bytes_buffer.getvalue(),
                    file_name="gabungan_selang_seling_besar.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses file: {e}")
