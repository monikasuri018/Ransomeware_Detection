import streamlit as st
import pandas as pd
import joblib
import tempfile
import os

from crypto_module import encrypt_file, decrypt_file


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Ransomware Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Based Ransomware Detection & Prevention")

st.write(
    "Random Forest detects ransomware-like behavior, "
    "while AES-256-GCM protects important files."
)


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load("ransomware_model.pkl")
feature_names = joblib.load("feature_names.pkl")


# ==========================================
# TABS
# ==========================================

detect_tab, recover_tab = st.tabs([
    "🧠 Detect & Protect",
    "🔓 Recover Backup"
])


# ==========================================================
# DETECT & PROTECT
# ==========================================================

with detect_tab:

    st.header("🧠 Ransomware Detection & Protection")

    # ------------------------------------------
    # 1. Behavioral Dataset
    # ------------------------------------------

    st.subheader("1️⃣ Upload Behavioral Dataset")

    csv_file = st.file_uploader(
        "Upload ransomware behavioral data",
        type=["csv"],
        key="behavior_csv"
    )

    # ------------------------------------------
    # 2. Important File
    # ------------------------------------------

    st.subheader("2️⃣ Select Important File to Protect")

    important_file = st.file_uploader(
        "Upload an important file for protected backup",
        type=None,
        key="important_file"
    )

    if important_file:
        st.success(
            f"📄 Selected file: {important_file.name}"
        )

    # ------------------------------------------
    # 3. Password
    # ------------------------------------------

    st.subheader("3️⃣ Set Backup Password")

    password = st.text_input(
        "Password for AES-256-GCM backup",
        type="password"
    )

    # ------------------------------------------
    # Analyze
    # ------------------------------------------

    if st.button(
        "🔍 Analyze & Protect",
        type="primary",
        use_container_width=True
    ):

        if csv_file is None:
            st.warning("⚠️ Please upload the behavioral CSV.")
            st.stop()

        if important_file is None:
            st.warning("⚠️ Please upload an important file.")
            st.stop()

        if not password:
            st.warning("⚠️ Please enter a backup password.")
            st.stop()

        # --------------------------------------
        # Read CSV
        # --------------------------------------

        df = pd.read_csv(csv_file)

        st.info(
            f"📊 Dataset loaded: {len(df):,} behavioral samples"
        )

        # --------------------------------------
        # Check required features
        # --------------------------------------

        missing_features = [
            feature
            for feature in feature_names
            if feature not in df.columns
        ]

        if missing_features:

            st.error(
                "❌ Required behavioral features are missing."
            )

            st.stop()

        X = df[feature_names]

        # --------------------------------------
        # Random Forest Prediction
        # --------------------------------------

        predictions = model.predict(X)

        ransomware_count = int(
            (predictions == 1).sum()
        )

        benign_count = int(
            (predictions == 0).sum()
        )

        # ==================================================
        # THREAT DETECTED
        # ==================================================

        if ransomware_count > 0:

            # FIRST → ALERT
            st.error(
                f"🚨 RANSOMWARE THREAT DETECTED!\n\n"
                f"{ransomware_count:,} suspicious behavioral "
                f"samples detected."
            )

            st.warning(
                "⚠️ Ransomware-like behavior detected. "
                "Creating a protected recovery backup..."
            )

            # SECOND → ENCRYPTED BACKUP

            original_bytes = important_file.getvalue()

            # Temporary original file
            input_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(
                    important_file.name
                )[1]
            )

            input_temp.write(original_bytes)
            input_temp.close()

            # Temporary encrypted file
            encrypted_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".enc"
            )

            encrypted_temp.close()

            # AES-256-GCM encryption
            encrypt_file(
                input_temp.name,
                encrypted_temp.name,
                password
            )

            # Read encrypted backup
            with open(
                encrypted_temp.name,
                "rb"
            ) as file:

                encrypted_bytes = file.read()

            st.success(
                "🔐 AES-256-GCM encrypted backup "
                "created successfully!"
            )

            st.info(
                "🛡️ Your original file has not been modified. "
                "The encrypted copy can be used for recovery."
            )

            # Download backup

            st.download_button(
                label="⬇️ Download Protected Backup",
                data=encrypted_bytes,
                file_name=important_file.name + ".enc",
                mime="application/octet-stream",
                use_container_width=True
            )

            # Clean temporary files

            try:
                os.remove(input_temp.name)
                os.remove(encrypted_temp.name)
            except:
                pass

        # ==================================================
        # NO THREAT
        # ==================================================

        else:

            st.success(
                "✅ No ransomware behavior detected."
            )

            st.info(
                "🟢 Your file remains untouched. "
                "No encrypted backup was created."
            )

        # ------------------------------------------
        # Detection summary
        # ------------------------------------------

        st.divider()

        st.subheader("📊 Detection Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Benign Samples",
                f"{benign_count:,}"
            )

        with col2:
            st.metric(
                "Ransomware Samples",
                f"{ransomware_count:,}"
            )


# ==========================================================
# RECOVER BACKUP
# ==========================================================

with recover_tab:

    st.header("🔓 Recover Protected File")

    st.write(
        "Upload your encrypted backup and enter "
        "the password used during protection."
    )

    encrypted_file = st.file_uploader(
        "Upload encrypted backup",
        type=["enc"],
        key="encrypted_file"
    )

    recovery_password = st.text_input(
        "Recovery password",
        type="password",
        key="recovery_password"
    )

    if st.button(
        "🔓 Decrypt & Recover",
        use_container_width=True
    ):

        if encrypted_file is None:

            st.warning(
                "⚠️ Please upload an encrypted backup."
            )

        elif not recovery_password:

            st.warning(
                "⚠️ Please enter the recovery password."
            )

        else:

            # Save encrypted file temporarily

            encrypted_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".enc"
            )

            encrypted_temp.write(
                encrypted_file.getvalue()
            )

            encrypted_temp.close()

            # Recovered file

            recovered_temp = tempfile.NamedTemporaryFile(
                delete=False
            )

            recovered_temp.close()

            # Decrypt

            success = decrypt_file(
                encrypted_temp.name,
                recovered_temp.name,
                recovery_password
            )

            if success:

                st.success(
                    "✅ File successfully recovered!"
                )

                with open(
                    recovered_temp.name,
                    "rb"
                ) as file:

                    recovered_bytes = file.read()

                recovered_name = encrypted_file.name[:-4]

                st.download_button(
                    label="⬇️ Download Recovered File",
                    data=recovered_bytes,
                    file_name=recovered_name,
                    use_container_width=True
                )

            else:

                st.error(
                    "❌ Decryption failed. "
                    "Please check your password."
                )

            try:
                os.remove(encrypted_temp.name)
                os.remove(recovered_temp.name)
            except:
                pass