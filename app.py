import streamlit as st
from pypdf import PdfReader, PdfWriter

# Konfigurasi halaman web
st.set_page_config(page_title="Penggabung PDF Selang-Seling v2", page_icon="📄")

st.title("📄 Web Penggabung PDF Selang-Seling (Versi Hemat RAM)")
st.write("Versi optimasi untuk file berukuran besar hingga 500 MB.")

# Input unggahan terpisah
file_a = st.file_uploader("Unggah File Pertama (PDF 1)", type="pdf", key="pdf1")
file_b = st.file_uploader("Unggah File Kedua (PDF 2)", type="pdf", key="pdf2")

if file_a and file_b:
    st.success("Kedua file siap diproses!")
    
    if st.button("Gabungkan PDF Selang-Seling Sekarang"):
        # Indikator loading agar pengguna tahu web sedang bekerja
        with st.spinner("Sedang memproses halaman file besar... Mohon tunggu..."):
            try:
                # OPTIMASI: Membaca langsung dari objek file Streamlit (tanpa .read() atau io.BytesIO)
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
                
                st.success("🎉 Penggabungan selesai! Siap diunduh.")
                
                # OPTIMASI: Menulis hasil langsung ke fungsi unduh untuk menghemat RAM
                st.download_button(
                    label="📥 Unduh Hasil Gabungan",
                    data=merger.stream, # Menggunakan stream internal pypdf, bukan buffer RAM tambahan
                    file_name="gabungan_selang_seling_besar.pdf",
                    mime="application/pdf"
                )
                
                # Bersihkan merger dari memori setelah selesai
                merger.close()
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses file: {e}")
