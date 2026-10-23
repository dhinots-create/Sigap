import datetime
import os
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st

# 1. KONFIGURASI HALAMAN SIGAP
st.set_page_config(
    page_title="SIGAP — Sistem Penugasan Terpadu Bawaslu",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS: Kartu Metrik Rapi Tanpa Gambar, Font Utuh, Angka Besar & Bold
st.markdown(
    """
    <style>
    /* Global Background */
    .stApp {
        background: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }
    
    /* Hero Login Typography */
    .sigap-hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        color: #7A0C17;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    .sigap-hero-subtitle {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 8px;
    }
    .sigap-tagline {
        font-size: 1rem;
        color: #64748B;
        font-weight: 500;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    
    /* Pillar Cards Hero Login */
    .pillar-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .pillar-title {
        font-weight: 800;
        font-size: 0.85rem;
        color: #7A0C17;
        margin-top: 6px;
    }
    .pillar-desc {
        font-size: 0.72rem;
        color: #64748B;
        margin-top: 2px;
    }
    
    /* Form Login Styling */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 36px;
        box-shadow: 0 10px 25px -5px rgba(122, 12, 23, 0.1);
    }
    
    /* Sidebar Merah Marun Bawaslu */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #7A0C17 0%, #4A050D 100%) !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    section[data-testid="stSidebar"] code {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: #A71D2A !important;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    section[data-testid="stSidebar"] div.stButton > button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: #A71D2A !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Top Banner Dashboard */
    .banner-container {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px 32px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        margin-bottom: 24px;
        border: 1px solid #E2E8F0;
    }
    .banner-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .banner-title span {
        color: #A71D2A;
    }
    .banner-subtitle {
        font-size: 1.1rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 12px;
    }
    .banner-tagline {
        font-size: 0.88rem;
        color: #64748B;
        font-weight: 500;
    }
    .motto-box {
        font-style: italic;
        font-weight: 600;
        color: #475569;
        font-size: 0.95rem;
        border-left: 3px solid #A71D2A;
        padding-left: 12px;
    }
    
    /* KARTU METRIK BESAR, TANPA GAMBAR, JUDUL UTUH, DAN ANGKA BESAR BOLD */
    div[data-testid="stColumn"] div.stButton > button,
    div[data-testid="column"] div.stButton > button {
        min-height: 120px !important;
        height: 120px !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.03) !important;
        padding: 16px 14px !important;
        transition: all 0.25s ease-in-out !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        justify-content: center !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    div[data-testid="stColumn"] div.stButton > button:hover,
    div[data-testid="column"] div.stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 20px rgba(167, 29, 42, 0.12) !important;
        border-color: #A71D2A !important;
        background: #FFFDFD !important;
    }

    div[data-testid="stColumn"] div.stButton > button p,
    div[data-testid="column"] div.stButton > button p {
        margin: 0 !important;
        line-height: 1.25 !important;
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        width: 100% !important;
    }

    /* Activity Panel */
    .activity-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #A71D2A 0%, #7A0C17 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(122, 12, 23, 0.3) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

UPLOAD_DIR = "Upload"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# 2. DATABASE INIT & MIGRASI AMAN (ALTER TABLE)
def init_db():
    conn = sqlite3.connect("penugasan_auditor.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            nama_lengkap TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penugasan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jenis_penugasan TEXT NOT NULL,
            no_surat_tugas TEXT UNIQUE NOT NULL,
            ketua_tim TEXT NOT NULL,
            anggota_tim TEXT NOT NULL,
            tgl_mulai DATE NOT NULL,
            tgl_selesai DATE NOT NULL,
            lama_penugasan INTEGER NOT NULL,
            pic_input TEXT NOT NULL,
            val_kt INTEGER DEFAULT 0,
            val_pt INTEGER DEFAULT 0,
            val_pm INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_laporan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            no_surat_tugas TEXT UNIQUE NOT NULL,
            no_laporan TEXT NOT NULL,
            file_pdf_path TEXT NOT NULL,
            tgl_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (no_surat_tugas) REFERENCES penugasan(no_surat_tugas)
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN is_first_login INTEGER DEFAULT 1"
        )
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute(
            "ALTER TABLE penugasan ADD COLUMN uraian_penugasan TEXT"
        )
    except sqlite3.OperationalError:
        pass

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, role, nama_lengkap, is_first_login) VALUES (?, ?, ?, ?, ?)",
            ("admin", "admin", "Admin / Superuser", "Administrator Sistem", 0),
        )

    conn.commit()
    conn.close()


init_db()


def get_db_connection():
    return sqlite3.connect("penugasan_auditor.db")


def hitung_hari_kerja(tgl_mulai, tgl_selesai):
    if tgl_mulai > tgl_selesai:
        return 0
    hari_kerja = np.busday_count(
        tgl_mulai, tgl_selesai + datetime.timedelta(days=1)
    )
    return int(hari_kerja)


# 3. MANAJEMEN SESSION
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None
if "force_change_password" not in st.session_state:
    st.session_state["force_change_password"] = False
if "dashboard_filter" not in st.session_state:
    st.session_state["dashboard_filter"] = "ALL"


# --- HALAMAN LOGIN DESAIN HERO SIGAP ---
if not st.session_state["logged_in"]:
    st.markdown(
        """
        <div style="text-align: right; font-size: 0.82rem; font-weight: 700; color: #64748B; margin-bottom: 15px;">
            Bersama Awasi Pemilu &nbsp;|&nbsp; Bersama Tegakkan Keadilan Pemilu
        </div>
    """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.3, 1], gap="large")

    with col_left:
        logo_path = None
        for img_name in ["logo_bawaslu.png", "images.png"]:
            if os.path.exists(img_name):
                logo_path = img_name
                break

        c_logo, c_title = st.columns([0.22, 1])
        with c_logo:
            if logo_path:
                st.image(logo_path, width=85)
            else:
                st.markdown("# ⚖️")
        with c_title:
            st.markdown(
                "<div class='sigap-hero-title'>SIGAP</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='sigap-hero-subtitle'>Sistem Penugasan Terpadu</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='sigap-tagline'>Tertib Penugasan, Optimal Kinerja,<br>Untuk Bawaslu yang Lebih Baik</div>",
            unsafe_allow_html=True,
        )

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.markdown(
                """
                <div class="pillar-box">
                    📋
                    <div class="pillar-title">Transparan</div>
                    <div class="pillar-desc">Informasi penugasan diakses dengan mudah.</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with p2:
            st.markdown(
                """
                <div class="pillar-box">
                    🎯
                    <div class="pillar-title">Terintegrasi</div>
                    <div class="pillar-desc">Proses penugasan dalam satu sistem.</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with p3:
            st.markdown(
                """
                <div class="pillar-box">
                    🛡️
                    <div class="pillar-title">Akuntabel</div>
                    <div class="pillar-desc">Mendukung tata kelola yang baik.</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with p4:
            st.markdown(
                """
                <div class="pillar-box">
                    👥
                    <div class="pillar-title">Berkinerja</div>
                    <div class="pillar-desc">Penugasan tepat sasaran & berdampak.</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

    with col_right:
        st.markdown(
            """
            <h3 style='margin-bottom: 2px; font-weight: 800; color: #0F172A;'>Selamat Datang di <span style='color:#7A0C17;'>SIGAP</span></h3>
            <p style='color: #64748B; font-size: 0.9rem; margin-bottom: 20px;'>Silakan masuk untuk mengakses portal penugasan terpadu Bawaslu.</p>
        """,
            unsafe_allow_html=True,
        )

        with st.form("login_form_sigap"):
            username = st.text_input("👤 Username", placeholder="Masukkan username")
            password = st.text_input(
                "🔒 Password", type="password", placeholder="Masukkan password"
            )
            submit = st.form_submit_button(
                "➔  Masuk ke Portal", type="primary", use_container_width=True
            )

            if submit:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username, role, nama_lengkap, password, is_first_login FROM users WHERE username=? AND password=?",
                    (username, password),
                )
                user = cursor.fetchone()
                conn.close()

                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = {
                        "username": user[0],
                        "role": user[1],
                        "nama": user[2],
                    }
                    if user[4] == 1 or password == "123456":
                        st.session_state["force_change_password"] = True
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")


# --- FORCE CHANGE PASSWORD ---
elif st.session_state["force_change_password"]:
    st.warning("⚠️ Anda masuk menggunakan password default. Harap perbarui password Anda.")
    with st.form("form_change_pass"):
        st.subheader("🔑 Perbarui Password Anda")
        new_pass = st.text_input("Password Baru", type="password")
        confirm_pass = st.text_input("Konfirmasi Password Baru", type="password")
        btn_update = st.form_submit_button("Simpan Password", type="primary")

        if btn_update:
            if new_pass and new_pass == confirm_pass:
                if new_pass == "123456":
                    st.error("Password baru tidak boleh sama dengan password default!")
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET password = ?, is_first_login = 0 WHERE username = ?",
                        (new_pass, st.session_state["user_info"]["username"]),
                    )
                    conn.commit()
                    conn.close()
                    st.session_state["force_change_password"] = False
                    st.success("Password diperbarui!")
                    st.rerun()


# --- HALAMAN UTAMA SETELAH LOGIN ---
else:
    user = st.session_state["user_info"]

    # SIDEBAR MERAH MARUN BAWASLU
    with st.sidebar:
        logo_path = None
        for img_name in ["logo_bawaslu.png", "images.png"]:
            if os.path.exists(img_name):
                logo_path = img_name
                break

        c_sb1, c_sb2 = st.columns([0.3, 1])
        with c_sb1:
            if logo_path:
                st.image(logo_path, width=45)
        with c_sb2:
            st.markdown(
                "<h2 style='margin:0; font-weight:900;'>SIGAP</h2>",
                unsafe_allow_html=True,
            )
            st.caption("Sistem Penugasan Terpadu")

        st.markdown("---")
        st.write(f"🏢 **Inspektorat Wilayah 1 Bawaslu**")
        st.write(f"👤 **{user['nama']}**")
        st.write(f"Akses Role: `{user['role']}`")
        st.markdown("---")

        menu_options = []
        if user["role"] == "Admin / Superuser":
            menu_options = [
                "Dashboard Utama",
                "Manajemen Pengguna (Admin)",
                "Input Penugasan Baru",
                "Upload Laporan Akhir",
            ]
        elif user["role"] == "Anggota Tim":
            menu_options = [
                "Dashboard Utama",
                "Input Penugasan Baru",
                "Upload Laporan Akhir",
            ]
        elif user["role"] == "Ketua Tim":
            menu_options = [
                "Dashboard Utama",
                "Validasi Draft Laporan (KT)",
            ]
        elif user["role"] == "Pengendali Teknis (Dalnis)":
            menu_options = [
                "Dashboard Utama",
                "Validasi Draft Laporan (Dalnis)",
            ]
        elif user["role"] == "Pengendali Mutu (Daltu)":
            menu_options = [
                "Dashboard Utama",
                "Validasi Draft Laporan (Daltu)",
            ]

        menu = st.radio("Navigasi Menu", menu_options)

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout Portal", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user_info"] = None
            st.session_state["force_change_password"] = False
            st.session_state["dashboard_filter"] = "ALL"
            st.rerun()

    # --- DASHBOARD UTAMA ---
    if "Dashboard Utama" in menu:
        b1, b2 = st.columns([2.5, 1])
        with b1:
            st.markdown(
                f"""
                <div class="banner-container">
                    <div class="banner-title">Selamat Datang di <span>SIGAP</span></div>
                    <div class="banner-subtitle">Sistem Penugasan Terpadu Bawaslu</div>
                    <div class="banner-tagline">Transparan &nbsp;•&nbsp; Akuntabel &nbsp;•&nbsp; Profesional</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with b2:
            st.markdown(
                f"""
                <div class="banner-container" style="text-align:right;">
                    <div style="font-size:0.85rem; font-weight:700; color:#64748B;">📅 {datetime.date.today().strftime('%A, %d %B %Y')}</div>
                    <br>
                    <div class="motto-box">"Bersama Mengawal Integritas Pengawasan Pemilu"</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        conn = get_db_connection()
        total_st = pd.read_sql_query("SELECT COUNT(*) FROM penugasan", conn).iloc[
            0, 0
        ]
        total_done = pd.read_sql_query(
            "SELECT COUNT(*) FROM monitoring_laporan", conn
        ).iloc[0, 0]
        total_ongoing = total_st - total_done
        val_pending = pd.read_sql_query(
            "SELECT COUNT(*) FROM penugasan WHERE val_kt=0 OR val_pt=0 OR val_pm=0",
            conn,
        ).iloc[0, 0]
        conn.close()

        col_main, col_side = st.columns([3, 1], gap="medium")

        with col_main:
            # KARTU METRIK BERUKURAN BESAR, KLIKABLE, TEKS LENGKAP UTUH & ANGKA BOLD
            k1, k2, k3, k4 = st.columns(4)

            # Card 1: Total Penugasan
            txt_k1 = f"**Total Penugasan**\n\n:red[# {total_st}] ST"
            if k1.button(txt_k1, key="card_total", use_container_width=True):
                st.session_state["dashboard_filter"] = "ALL"
                st.rerun()

            # Card 2: Penugasan On Going
            txt_k2 = f"**Penugasan On Going**\n\n:orange[# {total_ongoing}] ST"
            if k2.button(txt_k2, key="card_ongoing", use_container_width=True):
                st.session_state["dashboard_filter"] = "ONGOING"
                st.rerun()

            # Card 3: Laporan Selesai
            txt_k3 = f"**Laporan Selesai**\n\n:green[# {total_done}] ST"
            if k3.button(txt_k3, key="card_done", use_container_width=True):
                st.session_state["dashboard_filter"] = "DONE"
                st.rerun()

            # Card 4: Perlu Validasi Laporan
            txt_k4 = f"**Perlu Validasi Laporan**\n\n:red[# {val_pending}] ST"
            if k4.button(txt_k4, key="card_val", use_container_width=True):
                st.session_state["dashboard_filter"] = "PENDING_VAL"
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Status Filter Terpilih
            active_filter = st.session_state.get("dashboard_filter", "ALL")
            if active_filter == "ALL":
                st.caption("Filter Aktif: **Menampilkan Seluruh Penugasan**")
            elif active_filter == "ONGOING":
                st.caption("Filter Aktif: **Menampilkan Penugasan On Going**")
            elif active_filter == "DONE":
                st.caption("Filter Aktif: **Menampilkan Laporan Selesai**")
            elif active_filter == "PENDING_VAL":
                st.caption("Filter Aktif: **Menampilkan Penugasan Perlu Validasi Draft Laporan**")

            st.subheader("📋 Status & Monitoring Progres Penugasan")

            conn = get_db_connection()
            query = """
                SELECT 
                    p.id,
                    p.jenis_penugasan AS "Jenis Penugasan",
                    p.no_surat_tugas AS "No. Surat Tugas",
                    p.ketua_tim AS "Ketua Tim",
                    p.anggota_tim AS "Anggota Tim",
                    p.tgl_mulai AS "Mulai",
                    p.tgl_selesai AS "Deadline (Selesai)",
                    p.lama_penugasan AS "Durasi (Hari)",
                    p.uraian_penugasan AS "Detail Uraian Penugasan",
                    p.pic_input AS "PIC Input",
                    CASE WHEN p.val_kt = 1 THEN '☑️ Ya' ELSE '⬜ Belum' END AS "Val Draft KT",
                    CASE WHEN p.val_pt = 1 THEN '☑️ Ya' ELSE '⬜ Belum' END AS "Val Draft Dalnis",
                    CASE WHEN p.val_pm = 1 THEN '☑️ Ya' ELSE '⬜ Belum' END AS "Val Draft Daltu",
                    COALESCE(m.no_laporan, '-') AS "No. Laporan Akhir",
                    CASE 
                        WHEN m.no_laporan IS NOT NULL THEN '✅ Selesai'
                        ELSE '⏳ On Going'
                    END AS "Status Penugasan",
                    p.val_kt, p.val_pt, p.val_pm, m.no_laporan AS no_laporan_raw
                FROM penugasan p
                LEFT JOIN monitoring_laporan m ON p.no_surat_tugas = m.no_surat_tugas
                ORDER BY p.id DESC
            """
            df_status = pd.read_sql_query(query, conn)
            conn.close()

            if df_status.empty:
                st.info("Belum ada data penugasan tercatat.")
            else:
                if active_filter == "ONGOING":
                    df_status = df_status[df_status["no_laporan_raw"].isna()]
                elif active_filter == "DONE":
                    df_status = df_status[df_status["no_laporan_raw"].notna()]
                elif active_filter == "PENDING_VAL":
                    df_status = df_status[
                        (df_status["val_kt"] == 0)
                        | (df_status["val_pt"] == 0)
                        | (df_status["val_pm"] == 0)
                    ]

                today_str = datetime.date.today().strftime("%Y-%m-%d")

                def highlight_overdue(row):
                    is_overdue = (
                        pd.isna(row["no_laporan_raw"])
                        and str(row["Deadline (Selesai)"]) < today_str
                    )
                    if is_overdue:
                        return [
                            "background-color: #FEE2E2; color: #991B1B"
                        ] * len(row)
                    return [""] * len(row)

                styled_df = df_status.style.apply(highlight_overdue, axis=1)
                cols_to_hide = [
                    "id",
                    "Detail Uraian Penugasan",
                    "val_kt",
                    "val_pt",
                    "val_pm",
                    "no_laporan_raw",
                ]
                styled_df = styled_df.hide(subset=cols_to_hide, axis="columns")

                st.dataframe(styled_df, use_container_width=True)

                st.markdown("---")
                st.subheader("📑 Detail Uraian Penugasan")

                df_uraian = df_status[
                    [
                        "No. Surat Tugas",
                        "Jenis Penugasan",
                        "Ketua Tim",
                        "Anggota Tim",
                        "Detail Uraian Penugasan",
                    ]
                ].copy()
                df_uraian["Detail Uraian Penugasan"] = df_uraian[
                    "Detail Uraian Penugasan"
                ].fillna("Tidak ada uraian.")

                search_keyword = st.text_input(
                    "🔎 Cari Uraian Penugasan / No. ST / Nama Tim:",
                    placeholder="Ketik kata kunci pencarian...",
                )

                if search_keyword:
                    df_uraian = df_uraian[
                        df_uraian["No. Surat Tugas"].str.contains(
                            search_keyword, case=False
                        )
                        | df_uraian["Ketua Tim"].str.contains(
                            search_keyword, case=False
                        )
                        | df_uraian["Anggota Tim"].str.contains(
                            search_keyword, case=False
                        )
                        | df_uraian["Detail Uraian Penugasan"].str.contains(
                            search_keyword, case=False
                        )
                    ]

                st.dataframe(df_uraian, use_container_width=True, height=260)

        with col_side:
            st.markdown(
                """
                <div class="activity-card">
                    <h4 style="margin:0 0 12px 0; font-weight:800; color:#0F172A;">📊 Ringkasan Aktivitas</h4>
                    <p style="font-size:0.8rem; color:#64748B;">Catatan aktivitas penugasan terbaru di sistem.</p>
                    <hr style="margin:10px 0;">
                    <p style="font-size:0.82rem; font-weight:600; color:#1E293B;">✅ Laporan ST Terakhir</p>
                    <p style="font-size:0.75rem; color:#64748B;">Sistem terintegrasi aktif melakukan pemantauan draft validasi.</p>
                    <br>
                    <p style="font-size:0.82rem; font-weight:600; color:#1E293B;">📌 Penugasan Aktif</p>
                    <p style="font-size:0.75rem; color:#64748B;">Monitoring jadwal & deadline secara realtime.</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="activity-card" style="background: linear-gradient(135deg, #7A0C17 0%, #4A050D 100%); color:white;">
                    <h5 style="margin:0; font-weight:700; color:white;">"Tugas yang baik adalah langkah kecil untuk perubahan besar."</h5>
                </div>
            """,
                unsafe_allow_html=True,
            )

    # --- MANAJEMEN PENGGUNA (ADMIN) ---
    elif "Manajemen Pengguna" in menu:
        st.title("👤 Manajemen Pengguna & Database SSO")

        t1, t2 = st.tabs(["➕ Tambah User Baru", "🔑 Database User & Password"])

        with t1:
            with st.form("form_add_user"):
                new_user = st.text_input("Username Baru")
                new_nama = st.text_input("Nama Lengkap")
                new_role = st.selectbox(
                    "Otoritas / Role",
                    [
                        "Anggota Tim",
                        "Ketua Tim",
                        "Pengendali Teknis (Dalnis)",
                        "Pengendali Mutu (Daltu)",
                    ],
                )
                st.caption("Default password user baru: **123456**")

                btn_add = st.form_submit_button(
                    "Simpan User Baru", type="primary"
                )
                if btn_add:
                    if new_user and new_nama:
                        try:
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                """
                                INSERT INTO users (username, password, role, nama_lengkap, is_first_login)
                                VALUES (?, ?, ?, ?, ?)
                            """,
                                (
                                    new_user,
                                    "123456",
                                    new_role,
                                    new_nama,
                                    1,
                                ),
                            )
                            conn.commit()
                            conn.close()
                            st.success(
                                f"User **{new_user}** ({new_nama}) berhasil ditambahkan!"
                            )
                        except sqlite3.IntegrityError:
                            st.error("Username sudah terdaftar!")
                    else:
                        st.warning("Lengkapi data user!")

        with t2:
            st.write("Record Seluruh Password User Terdaftar:")
            conn = get_db_connection()
            df_users = pd.read_sql_query(
                "SELECT username, password, role, nama_lengkap, is_first_login FROM users",
                conn,
            )
            conn.close()
            st.dataframe(df_users, use_container_width=True)

    # --- INPUT PENUGASAN BARU ---
    elif "Input Penugasan Baru" in menu:
        st.title("📝 Input Data Penugasan Baru")

        conn = get_db_connection()
        list_kt = pd.read_sql_query(
            "SELECT nama_lengkap FROM users WHERE role = 'Ketua Tim'", conn
        )["nama_lengkap"].tolist()
        conn.close()

        with st.form("form_input_uraian"):
            c1, c2 = st.columns(2)
            with c1:
                jenis_penugasan = st.selectbox(
                    "Jenis Penugasan",
                    [
                        "Audit",
                        "Reviu",
                        "Evaluasi",
                        "Pemantauan",
                        "Pengawasan Lainnya",
                    ],
                )
                no_surat_tugas = st.text_input("Nomor Surat Tugas")

                if list_kt:
                    ketua_tim = st.selectbox(
                        "Ketua Tim (Terdaftar di Sistem)", list_kt
                    )
                else:
                    st.warning("Belum ada Ketua Tim yang terdaftar di sistem.")
                    ketua_tim = st.text_input("Ketua Tim (Manual Input)")

                anggota_tim = st.text_area("Anggota Tim")

            with c2:
                tgl_mulai = st.date_input("Tanggal Mulai", datetime.date.today())
                tgl_selesai = st.date_input(
                    "Tanggal Selesai (Deadline)", datetime.date.today()
                )

                hari_otomatis = hitung_hari_kerja(tgl_mulai, tgl_selesai)
                st.caption(f"Estimasi Hari Kerja: **{hari_otomatis} Hari**")

                lama_penugasan = st.number_input(
                    "Durasi Penugasan (Custom):",
                    min_value=1,
                    value=max(1, hari_otomatis),
                )
                st.text_input(
                    "Operator Input Data", value=user["nama"], disabled=True
                )

            uraian_penugasan = st.text_area(
                "Uraian Penugasan (Bisa Panjang / Tanpa Batas Kata)", height=150
            )

            btn_simpan = st.form_submit_button(
                "💾 Simpan Data Penugasan",
                type="primary",
                use_container_width=True,
            )

            if btn_simpan:
                if no_surat_tugas and ketua_tim:
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            """
                            INSERT INTO penugasan 
                            (jenis_penugasan, no_surat_tugas, ketua_tim, anggota_tim, tgl_mulai, tgl_selesai, lama_penugasan, uraian_penugasan, pic_input)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                            (
                                jenis_penugasan,
                                no_surat_tugas,
                                ketua_tim,
                                anggota_tim,
                                tgl_mulai,
                                tgl_selesai,
                                lama_penugasan,
                                uraian_penugasan,
                                user["nama"],
                            ),
                        )
                        conn.commit()
                        conn.close()
                        st.success("Penugasan berhasil disimpan!")
                    except sqlite3.IntegrityError:
                        st.error("Nomor Surat Tugas sudah terdaftar!")
                else:
                    st.warning("Lengkapi isian wajib!")

    # --- VALIDASI DRAFT LAPORAN KETUA TIM ---
    elif "Validasi Draft Laporan (KT)" in menu:
        st.title(f"🔍 Validasi Draft Laporan Akhir — Ketua Tim ({user['nama']})")

        conn = get_db_connection()
        df = pd.read_sql_query(
            "SELECT id, jenis_penugasan, no_surat_tugas, ketua_tim, anggota_tim, uraian_penugasan, pic_input FROM penugasan WHERE val_kt = 0 AND ketua_tim = ?",
            conn,
            params=(user["nama"],),
        )
        conn.close()

        if df.empty:
            st.success(
                f"✨ Tidak ada antrean validasi draft laporan untuk penugasan yang dipimpin **{user['nama']}**."
            )
        else:
            for idx, row in df.iterrows():
                with st.expander(
                    f"📌 ST No: {row['no_surat_tugas']} — Ketua Tim: {row['ketua_tim']}"
                ):
                    st.write(f"**Jenis Penugasan:** {row['jenis_penugasan']}")
                    st.write(f"**Anggota Tim:** {row['anggota_tim']}")
                    st.write(
                        f"**Uraian Penugasan:**\n{row['uraian_penugasan'] if row['uraian_penugasan'] else '-'}"
                    )

                    st.markdown("---")
                    chk = st.checkbox(
                        f"Saya meyakini kebenaran draft laporan untuk Surat Tugas No. {row['no_surat_tugas']}",
                        key=f"chk_kt_{row['id']}",
                    )
                    if chk:
                        if st.button(
                            "Proses Validasi Draft Laporan (KT)",
                            key=f"btn_kt_{row['id']}",
                            type="primary",
                        ):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE penugasan SET val_kt = 1 WHERE id = ?",
                                (row["id"],),
                            )
                            conn.commit()
                            conn.close()
                            st.success(
                                f"Draft Laporan Surat Tugas {row['no_surat_tugas']} divalidasi Ketua Tim!"
                            )
                            st.rerun()

    # --- VALIDASI DRAFT LAPORAN DALNIS ---
    elif "Validasi Draft Laporan (Dalnis)" in menu:
        st.title("🔍 Validasi Draft Laporan Akhir — Pengendali Teknis (Dalnis)")
        conn = get_db_connection()
        df = pd.read_sql_query(
            "SELECT id, jenis_penugasan, no_surat_tugas, ketua_tim, anggota_tim, uraian_penugasan, pic_input FROM penugasan WHERE val_kt = 1 AND val_pt = 0",
            conn,
        )
        conn.close()

        if df.empty:
            st.success(
                "✨ Tidak ada antrean validasi draft laporan tingkat Dalnis."
            )
        else:
            for idx, row in df.iterrows():
                with st.expander(
                    f"📌 ST No: {row['no_surat_tugas']} — Ketua Tim: {row['ketua_tim']}"
                ):
                    st.write(f"**Ketua Tim:** {row['ketua_tim']}")
                    st.write(
                        f"**Uraian Penugasan:**\n{row['uraian_penugasan'] if row['uraian_penugasan'] else '-'}"
                    )
                    chk = st.checkbox(
                        f"Saya meyakini kebenaran draft laporan untuk Surat Tugas No. {row['no_surat_tugas']}",
                        key=f"chk_pt_{row['id']}",
                    )
                    if chk:
                        if st.button(
                            "Proses Validasi Draft Laporan (Dalnis)",
                            key=f"btn_pt_{row['id']}",
                            type="primary",
                        ):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE penugasan SET val_pt = 1 WHERE id = ?",
                                (row["id"],),
                            )
                            conn.commit()
                            conn.close()
                            st.success("Draft Laporan divalidasi Dalnis!")
                            st.rerun()

    # --- VALIDASI DRAFT LAPORAN DALTU ---
    elif "Validasi Draft Laporan (Daltu)" in menu:
        st.title("🔍 Validasi Draft Laporan Akhir — Pengendali Mutu (Daltu)")
        conn = get_db_connection()
        df = pd.read_sql_query(
            "SELECT id, jenis_penugasan, no_surat_tugas, ketua_tim, anggota_tim, uraian_penugasan, pic_input FROM penugasan WHERE val_kt = 1 AND val_pt = 1 AND val_pm = 0",
            conn,
        )
        conn.close()

        if df.empty:
            st.success(
                "✨ Tidak ada antrean validasi draft laporan tingkat Daltu."
            )
        else:
            for idx, row in df.iterrows():
                with st.expander(
                    f"📌 ST No: {row['no_surat_tugas']} — Ketua Tim: {row['ketua_tim']}"
                ):
                    st.write(f"**Ketua Tim:** {row['ketua_tim']}")
                    st.write(
                        f"**Uraian Penugasan:**\n{row['uraian_penugasan'] if row['uraian_penugasan'] else '-'}"
                    )
                    chk = st.checkbox(
                        f"Saya meyakini kebenaran draft laporan untuk Surat Tugas No. {row['no_surat_tugas']}",
                        key=f"chk_pm_{row['id']}",
                    )
                    if chk:
                        if st.button(
                            "Proses Validasi Draft Laporan (Daltu)",
                            key=f"btn_pm_{row['id']}",
                            type="primary",
                        ):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE penugasan SET val_pm = 1 WHERE id = ?",
                                (row["id"],),
                            )
                            conn.commit()
                            conn.close()
                            st.success(
                                "Draft Laporan divalidasi Daltu (Final)!"
                            )
                            st.rerun()

    # --- UPLOAD LAPORAN AKHIR ---
    elif "Upload Laporan Akhir" in menu:
        st.title("📤 Upload Laporan Akhir Penugasan")
        conn = get_db_connection()
        df_valid = pd.read_sql_query(
            "SELECT no_surat_tugas FROM penugasan WHERE val_kt = 1 AND val_pt = 1 AND val_pm = 1",
            conn,
        )
        conn.close()

        if df_valid.empty:
            st.error(
                "⚠️ Belum ada Penugasan yang draft laporannya LULUS 3 tahap validasi (KT, Dalnis, Daltu)."
            )
        else:
            with st.form("form_upload_sigap"):
                selected_st = st.selectbox(
                    "Pilih Nomor Surat Tugas Ter-validasi",
                    df_valid["no_surat_tugas"].tolist(),
                )
                no_laporan = st.text_input("Nomor Laporan Akhir")
                uploaded_file = st.file_uploader(
                    "Upload Laporan PDF", type=["pdf"]
                )
                btn_upload = st.form_submit_button(
                    "Simpan Laporan", type="primary", use_container_width=True
                )

                if btn_upload:
                    if no_laporan and uploaded_file is not None:
                        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT OR REPLACE INTO monitoring_laporan (no_surat_tugas, no_laporan, file_pdf_path) VALUES (?, ?, ?)",
                            (selected_st, no_laporan, file_path),
                        )
                        conn.commit()
                        conn.close()
                        st.success("Laporan berhasil disimpan!")