import streamlit as st
from pypdf import PdfWriter
import io

# Konfigurasi halaman web
st.set_page_config(page_title="Penggabung PDF Otomatis", page_icon="📄")

st.title("📄 Web Penggabung PDF")
st.write("Unggah file PDF Anda (misal: `1.pdf` dan `2.pdf`) untuk digabungkan secara otomatis menggunakan Python.")

# Fitur unggah file (mendukung banyak file sekaligus)
uploaded_files = st.file_uploader(
    "Pilih file-file PDF yang ingin digabungkan", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file berhasil diunggah.")
    
    # Tombol untuk memproses penggabungan
    if st.button("Gabungkan PDF Sekarang"):
        with st.spinner("Sedang menggabungkan..."):
            try:
                # Inisialisasi penggabung PDF
                merger = PdfWriter()
                
                # Membaca setiap file dari memori web
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    merger.append(io.BytesIO(bytes_data))
                
                # Menyimpan hasil gabungan ke memori sementara (buffer)
                output_pdf = io.BytesIO()
                merger.write(output_pdf)
                merger.close()
                output_pdf.seek(0)
                
                st.success("🎉 Penggabungan selesai!")
                
                # Menyediakan tombol unduh untuk pengguna web
                st.download_button(
                    label="📥 Unduh Hasil Gabungan",
                    data=output_pdf,
                    file_name="gabungan_otomatis.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
