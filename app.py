# ==========================================================
# FRUITVISION AI
# Deteksi Kematangan & Kualitas Buah Menggunakan Gemini AI
# Bagian 1 : UI, Kamera, Upload, Preview
# ==========================================================

import streamlit as st
from google import genai
from PIL import Image
from google.genai import types

# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================

st.set_page_config(
    page_title="FruitVision AI",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# GEMINI CLIENT
# ==========================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "hasil" not in st.session_state:
    st.session_state.hasil = None

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.main > div{
    padding-top:20px;
}

h1{
    text-align:center;
}

.card{
    border-radius:15px;
    padding:20px;
    border:1px solid #dcdcdc;
    background:#ffffff;
    box-shadow:0px 3px 10px rgba(0,0,0,.08);
}

.result-card{
    border-radius:15px;
    padding:18px;
    background:#f8f9fa;
    border-left:6px solid #28a745;
    margin-bottom:15px;
}

.big-button button{
    height:60px;
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.title("🍎 FruitVision AI")

st.markdown(
"""
### Deteksi Kematangan & Kualitas Buah

Sistem ini menggunakan **Google Gemini AI** untuk membantu menganalisis kondisi buah berdasarkan gambar.

AI akan memberikan informasi mengenai:

- 🍎 Nama buah
- 🟢 Tingkat kematangan
- ❤️ Status kelayakan konsumsi
- 🐛 Indikasi hama
- 🍂 Indikasi pembusukan
- 📄 Deskripsi kondisi buah
- 💡 Saran
"""
)

st.divider()

# ==========================================================
# INPUT GAMBAR
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📷 Ambil Foto")

    camera_image = st.camera_input(
        "Gunakan kamera perangkat"
    )

with col2:

    st.subheader("📁 Upload Gambar")

    uploaded_image = st.file_uploader(
        "Pilih gambar buah",
        type=["jpg", "jpeg", "png"]
    )

# ==========================================================
# MEMILIH GAMBAR
# PRIORITAS:
# 1. Kamera
# 2. Upload
# ==========================================================

image = None

if camera_image is not None:

    image = Image.open(camera_image)

elif uploaded_image is not None:

    image = Image.open(uploaded_image)

# ==========================================================
# PREVIEW
# ==========================================================

if image is not None:

    st.divider()

    st.subheader("🖼️ Preview Gambar")

    st.image(
        image,
        use_container_width=True
    )

    st.markdown("<div class='big-button'>", unsafe_allow_html=True)

    analisis = st.button(
        "🔍 Analisis Buah",
        use_container_width=True,
        type="primary"
    )

    st.markdown("</div>", unsafe_allow_html=True)

else:

    analisis = False

    st.info(
        "Silakan ambil foto menggunakan kamera atau upload gambar buah terlebih dahulu."
    )
    # ==========================================================
# BAGIAN 2
# ANALISIS GEMINI AI
# ==========================================================

import io
import json

if analisis:

    with st.spinner("🧠 AI sedang menganalisis buah..."):

        try:

            # ---------------------------------------------
            # Konversi gambar ke bytes
            # ---------------------------------------------

            if image.mode != "RGB":
                image = image.convert("RGB")

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()

            # ---------------------------------------------
            # Prompt AI
            # ---------------------------------------------

            prompt = """
Kamu adalah seorang ahli hortikultura dan inspeksi kualitas buah.

Analisis gambar buah yang diberikan.

Jawab HANYA dalam format JSON VALID.

Jangan gunakan markdown.
Jangan gunakan ```json.

Format yang harus dikembalikan:

{
    "buah":"",
    "status":"",
    "tingkat_kematangan":"",
    "tingkat_keyakinan":0,
    "indikasi_hama":"",
    "indikasi_busuk":"",
    "warna":"",
    "tekstur":"",
    "deskripsi":"",
    "saran":""
}

Keterangan:

status:
- Layak Dikonsumsi
- Perlu Diperiksa
- Tidak Layak Dikonsumsi

tingkat_kematangan:
- Mentah
- Setengah Matang
- Matang
- Terlalu Matang
- Busuk

indikasi_hama:
- Ada
- Tidak Ada

indikasi_busuk:
- Ada
- Tidak Ada

tingkat_keyakinan:
Nilai antara 0 sampai 100.

deskripsi:
Jelaskan kondisi buah berdasarkan gambar.

saran:
Berikan rekomendasi singkat kepada pengguna.
"""

            # ---------------------------------------------
            # Request ke Gemini
            # ---------------------------------------------

            response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        prompt,
        types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg"
        )
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)
            hasil_text = response.text.strip()

            # ---------------------------------------------
            # Bersihkan markdown jika AI masih membandel
            # ---------------------------------------------

            hasil_text = hasil_text.replace("```json", "")
            hasil_text = hasil_text.replace("```", "")
            hasil_text = hasil_text.strip()

            # ---------------------------------------------
            # Parsing JSON
            # ---------------------------------------------

            hasil = json.loads(hasil_text)

            # Simpan ke Session State
            st.session_state.hasil = hasil

            st.success("✅ Analisis berhasil dilakukan.")

        except json.JSONDecodeError:

            st.error(
                "❌ AI mengembalikan format yang tidak sesuai (JSON tidak valid)."
            )

        except Exception as e:

            st.error(f"❌ Terjadi kesalahan:\n\n{e}")
            # ==========================================================
# BAGIAN 3
# TAMPILAN HASIL ANALISIS
# ==========================================================

if st.session_state.hasil is not None:

    hasil = st.session_state.hasil

    st.divider()

    st.header("📊 Hasil Analisis")

    # ==========================================
    # STATUS
    # ==========================================

    status = hasil.get("status", "-")

    if status == "Layak Dikonsumsi":
        st.success(f"✅ {status}")

    elif status == "Perlu Diperiksa":
        st.warning(f"⚠️ {status}")

    else:
        st.error(f"❌ {status}")

    # ==========================================
    # INFORMASI UTAMA
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="🍎 Nama Buah",
            value=hasil.get("buah", "-")
        )

        st.metric(
            label="🟢 Tingkat Kematangan",
            value=hasil.get("tingkat_kematangan", "-")
        )

        st.metric(
            label="🐛 Indikasi Hama",
            value=hasil.get("indikasi_hama", "-")
        )

    with col2:

        st.metric(
            label="🍂 Indikasi Busuk",
            value=hasil.get("indikasi_busuk", "-")
        )

        confidence = hasil.get("tingkat_keyakinan", 0)

        try:
            confidence = int(confidence)
        except:
            confidence = 0

        st.metric(
            label="🎯 Tingkat Keyakinan AI",
            value=f"{confidence}%"
        )

        st.progress(confidence)

    st.divider()

    # ==========================================
    # DETAIL ANALISIS
    # ==========================================

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("🎨 Warna")

        st.info(
            hasil.get("warna", "-")
        )

    with col4:

        st.subheader("🍊 Tekstur")

        st.info(
            hasil.get("tekstur", "-")
        )

    st.subheader("📄 Deskripsi")

    st.write(
        hasil.get("deskripsi", "-")
    )

    st.subheader("💡 Saran")

    st.success(
        hasil.get("saran", "-")
    )

    st.divider()

    # ==========================================
    # ANALISIS ULANG
    # ==========================================

    if st.button(
        "🔄 Analisis Gambar Baru",
        use_container_width=True
    ):

        st.session_state.hasil = None

        st.rerun()
        # ==========================================================
# BAGIAN 4
# FINISHING
# ==========================================================

# Footer
st.divider()

st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:14px;">
        🍎 <b>FruitVision AI</b><br>
        Sistem Deteksi Kematangan & Kualitas Buah menggunakan
        <b>Google Gemini AI</b><br><br>
        Dibuat menggunakan ❤️ Streamlit + Gemini API
    </div>
    """,
    unsafe_allow_html=True
)
