"""
City Hall Sign Kiosk — Streamlit app (YOLO-compatible, final merged)

This file is the full, merged Streamlit app prepared to run with your YOLO-style checkpoint `best.pt`.

Key features:
- Loads a YOLO checkpoint using `ultralytics.YOLO` (best.pt) and sets class names to A–Z if necessary.
- Live OpenCV camera feed for continuous ASL recognition (no photo capture required).
- Real-time letter predictions appended to a word buffer (auto-append on confidence).
- Intent mapping from spelled words to city hall actions.
- Mock API action form with receipt and QR generation.

HOW TO RUN
1. Put `best.pt` in the same folder as this script.
2. Install dependencies:
   pip install streamlit torch torchvision pillow opencv-python qrcode ultralytics
3. Run:
   streamlit run city_hall_kiosk_streamlit.py

NOTES
- If your YOLO model's class names are not letters A–Z, the script will override names with a standard A–Z mapping.
- The script uses `model.predict(...)` to run inference on frames; for better production behavior consider `streamlit-webrtc`.

"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import os
import time
import uuid
import json
import difflib

# ML imports
import torch

# ultralytics YOLO
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except Exception:
    YOLO = None
    ULTRALYTICS_AVAILABLE = False

# Optional features
try:
    import qrcode
except Exception:
    qrcode = None

# OpenCV for live camera
try:
    import cv2
    OPENCV_AVAILABLE = True
except Exception:
    cv2 = None
    OPENCV_AVAILABLE = False

MODEL_PATH = "best.pt"
MODEL_INPUT_SIZE = 640  # typical YOLO inference size; can be adjusted
CLASS_NAMES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Simple service keyword list (expand as needed)
SERVICE_KEYWORDS = [
    "renew",
    "appointment",
    "apply",
    "report",
    "complaint",
    "permit",
    "license",
    "certificate",
    "tax",
    "id",
    "birth",
    "marriage",
]

INTENT_MAP = {
    "renew": "Renew ID",
    "appointment": "Book Appointment",
    "apply": "Apply for ID/Permit",
    "report": "Report Issue",
    "complaint": "File Complaint",
    "permit": "Apply for Permit",
    "license": "Apply for License",
    "certificate": "Request Certificate",
    "tax": "Tax Inquiry/Payment",
}

st.set_page_config(page_title="City Hall Sign Kiosk", layout="wide")

@st.cache_resource
def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        st.warning(f"Model file not found at {path}. Please place your 'best.pt' file in the app folder and restart.")
        return None
    if not ULTRALYTICS_AVAILABLE:
        st.error("Ultralytics is not installed. Install it with `pip install ultralytics` and restart.")
        return None
    try:
        model = YOLO(path)
        # ensure model on correct device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            model.to(device)
        except Exception:
            # some ultralytics versions handle device internally
            pass
        # Ensure class names are letters A-Z (if model was trained that way)
        try:
            names = model.names
            if not names or len(names) < 26:
                # override with A-Z mapping
                model.names = {i: chr(65 + i) for i in range(26)}
        except Exception:
            model.names = {i: chr(65 + i) for i in range(26)}
        st.success("YOLO model loaded successfully")
        return (model, device)
    except Exception as e:
        st.error(f"Failed to load YOLO model: {e}")
        return None


def predict_letter(model_tuple, frame_rgb, conf_thresh=0.5):
    """Run YOLO predict on a single RGB frame (numpy array) and return a letter + confidence."""
    if model_tuple is None:
        return None, 0.0
    model, device = model_tuple
    try:
        # ultralytics accepts numpy arrays as sources
        results = model.predict(source=frame_rgb, imgsz=MODEL_INPUT_SIZE, conf=conf_thresh, verbose=False)
        if len(results) == 0:
            return None, 0.0
        res = results[0]
        # res.boxes is a Boxes object; get confidences and classes
        try:
            boxes = res.boxes
            if boxes is None or len(boxes) == 0:
                return None, 0.0
            # take highest-confidence detection
            # boxes.conf and boxes.cls are Tensor-like
            confs = boxes.conf.cpu().numpy()
            cls_idxs = boxes.cls.cpu().numpy().astype(int)
            best_idx = int(np.argmax(confs))
            cls = int(cls_idxs[best_idx])
            conf = float(confs[best_idx])
            label = model.names.get(cls, str(cls))
            return label.upper(), conf
        except Exception:
            # fallback: try res.boxes.data
            try:
                data = res.boxes.data.cpu().numpy()
                if data.size == 0:
                    return None, 0.0
                # data columns: x1,y1,x2,y2,confidence,class
                best_idx = int(np.argmax(data[:,4]))
                cls = int(data[best_idx,5])
                conf = float(data[best_idx,4])
                label = model.names.get(cls, str(cls))
                return label.upper(), conf
            except Exception:
                return None, 0.0
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None, 0.0


def preprocess_pil(pil_img, size=MODEL_INPUT_SIZE):
    # Convert PIL to RGB numpy for YOLO (ultralytics handles resizing internally)
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    arr = np.array(pil_img)
    return arr


@st.cache_data
def make_service_wordlist():
    common = SERVICE_KEYWORDS + [
        "hello", "yes", "no", "help", "where", "when", "how", "who", "pay", "status",
        "document", "documents", "id", "renewal", "renew", "apply", "appointment"
    ]
    return list(set(common))


def extract_intent_from_text(text: str):
    if not text:
        return None, []
    text_l = text.lower()
    found = []
    for kw in INTENT_MAP.keys():
        if kw in text_l:
            found.append(INTENT_MAP[kw])
    words = text_l.split()
    for w in words:
        close = difflib.get_close_matches(w, SERVICE_KEYWORDS, n=1, cutoff=0.8)
        if close:
            found.append(INTENT_MAP.get(close[0], close[0]))
    unique = []
    for f in found:
        if f not in unique:
            unique.append(f)
    return (unique[0] if unique else None, unique)


def generate_qr(data: dict):
    if qrcode is None:
        return None
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio


def make_receipt_image(details: dict):
    w, h = 600, 400
    img = Image.new("RGB", (w, h), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", size=16)
    except Exception:
        font = ImageFont.load_default()
    y = 20
    draw.text((20, y), "City Hall Kiosk Receipt", font=font)
    y += 30
    for k, v in details.items():
        draw.text((20, y), f"{k}: {v}", font=font)
        y += 24
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio

# --- UI ---
st.title("City Hall Sign Agent — Kiosk Demo (YOLO live)")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Live camera input / ASL recognition")
    st.write("Use the live camera feed for continuous ASL recognition. Predictions update in real time.")

    model_tuple = load_model()
    if model_tuple is None:
        st.info("Model not loaded. Place 'best.pt' next to this script and ensure ultralytics is installed.")

    if not OPENCV_AVAILABLE:
        st.error("OpenCV is required for live feed. Install opencv-python and restart.")

    # Live feed controls
    start_live = st.button("Start live feed")
    stop_live = st.button("Stop live feed")

    if 'word_buffer' not in st.session_state:
        st.session_state.word_buffer = ""
    if 'live_running' not in st.session_state:
        st.session_state.live_running = False

    if start_live:
        st.session_state.live_running = True
    if stop_live:
        st.session_state.live_running = False

    stframe = st.empty()
    info_box = st.empty()

    if st.session_state.live_running and OPENCV_AVAILABLE and model_tuple is not None:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Failed to open camera. Check device index or permissions.")
            st.session_state.live_running = False
        else:
            try:
                while st.session_state.live_running:
                    ret, frame = cap.read()
                    if not ret:
                        info_box.warning("No frame captured. Retrying...")
                        time.sleep(0.1)
                        continue

                    # frame is BGR; convert to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Predict letter
                    letter, conf = predict_letter(model_tuple, frame_rgb, conf_thresh=0.4)
                    display_text = ""
                    if letter is not None:
                        display_text = f"Predicted: {letter} ({conf:.2f})"
                        if conf is not None and conf > 0.75:
                            st.session_state.word_buffer += letter

                    # Draw overlay
                    cv2.putText(frame, display_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
                    stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                    info_box.markdown(f"**Spelled text:** `{st.session_state.word_buffer}`")

                    time.sleep(0.05)

            except Exception as e:
                st.error(f"Live feed error: {e}")
            finally:
                cap.release()

    elif not st.session_state.live_running:
        st.info("Live feed stopped. Press 'Start live feed' to begin.")

    # Word builder controls (manual)
    st.subheader("Word builder")
    col_a, col_b, col_c = st.columns([1,1,2])
    with col_a:
        if st.button("Add last predicted letter"):
            pass
    with col_b:
        if st.button("Clear word"):
            st.session_state.word_buffer = ""
    with col_c:
        st.write("")

    st.markdown("**Current spelled text:**")
    st.code(st.session_state.word_buffer or "(empty)")

    st.write("Or type/edit the spelled text manually:")
    st.session_state.word_buffer = st.text_input("Edit spelled text", value=st.session_state.word_buffer)

    # intent suggestion
    suggested_intent, all_intents = extract_intent_from_text(st.session_state.word_buffer)
    st.subheader("Detected intent (suggestions)")
    if all_intents:
        for it in all_intents:
            st.info(it)
    else:
        st.write("No clear intent detected. Try keywords like 'renew', 'appointment', 'apply', 'report', etc.")

    chosen_options = all_intents if all_intents else ["None", "Book Appointment", "Renew ID", "File Complaint"]
    chosen_intent = st.selectbox("Choose intent to perform", options=chosen_options)

    with st.form("action_form"):
        st.write("Provide user details (mock)")
        user_name = st.text_input("Name")
        user_contact = st.text_input("Contact (email/phone)")
        preferred_date = st.date_input("Preferred date")
        preferred_time = st.time_input("Preferred time")
        submitted = st.form_submit_button("Confirm and perform action")
        if submitted:
            action_id = str(uuid.uuid4())[:8]
            details = {
                "id": action_id,
                "name": user_name,
                "contact": user_contact,
                "intent_chosen": chosen_intent,
                "spelled_text": st.session_state.word_buffer,
                "datetime_requested": f"{preferred_date} {preferred_time}"
            }
            st.success("Action submitted — mock API received your request.")
            st.json(details)
            qr = generate_qr(details) if qrcode is not None else None
            receipt = make_receipt_image(details)
            st.download_button("Download receipt (PNG)", data=receipt, file_name=f"receipt_{action_id}.png")
            if qr:
                st.image(qr, caption="QR (scan for details)")
                st.download_button("Download QR (PNG)", data=qr, file_name=f"qr_{action_id}.png")

with col2:
    st.header("Kiosk Controls & Info")
    st.write("Large UI controls you can map to kiosk physical buttons.")
    if st.button("Reset session"):
        st.session_state.word_buffer = ""
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("Admin: Mock API Log")
    if 'mock_log' not in st.session_state:
        st.session_state.mock_log = []
    if st.button("Simulate previous requests"):
        for i in range(3):
            st.session_state.mock_log.append({
                "id": str(uuid.uuid4())[:6],
                "intent": "Book Appointment",
                "name": f"User {i+1}",
                "time": time.asctime()
            })
    if st.session_state.mock_log:
        for e in reversed(st.session_state.mock_log[-10:]):
            st.write(e)
    else:
        st.write("No requests yet.")

    st.markdown("---")
    st.subheader("Operator Notes")
    st.write("- Put the user-facing tablet in full-screen kiosk mode.\n- Camera must point at user's hands at comfortable distance.\n- Tune MODEL_INPUT_SIZE and confidence threshold if needed.\n- For production consider streamlit-webrtc for non-blocking live audio/video.")

st.markdown("---")
st.caption("Demo app: City Hall Sign Agent — For hackathon/demo purposes only. Customize intent mapping & service words for your municipality.")
