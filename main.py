#!/usr/bin/env python3
"""
Sign Language Letter Speller — Arduino UNO Q

Uses the video_object_detection brick for Edge Impulse inference to
recognise which letter of the sign-language alphabet is being shown
to the camera, and lets the user "capture" detected letters to spell
words, similar to how the original RPS demo captured a gesture.

Flask on port 5001 serves the custom web UI.
"""

import os
import time
import logging
import threading
from flask import Flask, render_template, jsonify

# ─── Silence Flask HTTP logs ─────────────────────────────────────────────
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# ─── Video Object Detection Brick ────────────────────────────────────────
_detector = None
try:
    from arduino.app_bricks.video_objectdetection import VideoObjectDetection
    _detector = VideoObjectDetection(confidence=0.6, debounce_sec=0.0)
    print("[BRICK] VideoObjectDetection initialized")
except ImportError:
    print("[WARN] VideoObjectDetection brick not available — detection disabled")

# ─── App Runner ──────────────────────────────────────────────────────────
_App = None
try:
    from arduino.app_utils import App as _App
except ImportError:
    try:
        from arduino.app import App as _App
    except ImportError:
        try:
            from arduino import App as _App
        except ImportError:
            pass

# ─── Configuration ───────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.6
PORT = int(os.environ.get('FLASK_PORT', '5001'))
RESULT_HOLD_SECS = 1.5

# Non-letter gesture classes your model may output, mapped to actions.
# Rename/remove these to match the actual class names of your model —
# everything else is treated as a plain letter of the alphabet.
SPECIAL_LABELS = {
    'space': 'SPACE',
    'del': 'DELETE',
    'clear': 'CLEAR',
}


# ─── Speller State ────────────────────────────────────────────────────────
class SpellerState:
    """Thread-safe state for live letter detection + word spelling."""

    def __init__(self):
        self._lock = threading.Lock()
        self.state = 'idle'          # idle | countdown | evaluating | result
        self.countdown = None
        self.detection = None        # currently seen label, live
        self.confidence = 0.0
        self.captured_letter = None  # result of the last capture
        self.spelled_text = ''
        self.round_number = 0
        self.history = []
        self._detection_locked = False

    def update_detection(self, label, confidence):
        with self._lock:
            if self._detection_locked:
                return
            prev = self.detection
            self.detection = label
            self.confidence = confidence
        if label != prev:
            print(f"[DETECT] {label} ({confidence:.0%})")

    def capture_letter(self):
        """Lock the current detection, run a short countdown, then commit it."""
        with self._lock:
            self._detection_locked = True
            detected = self.detection
            conf = self.confidence
            self.state = 'countdown'
            self.captured_letter = None

        print(f"[SPELL] Locked detection: {detected} ({conf:.0%})" if detected else
              "[SPELL] Locked detection: none")

        for tick in [3, 2, 1]:
            with self._lock:
                self.countdown = tick
            time.sleep(1)

        with self._lock:
            self.state = 'evaluating'
            self.countdown = None

        letter = None
        action = detected if detected in SPECIAL_LABELS else None
        if detected and not action:
            letter = detected.upper()

        with self._lock:
            self.round_number += 1

            if letter:
                self.spelled_text += letter
                self.captured_letter = letter
            elif action == 'space':
                self.spelled_text += ' '
                self.captured_letter = 'SPACE'
            elif action == 'del':
                self.spelled_text = self.spelled_text[:-1]
                self.captured_letter = 'DELETE'
            elif action == 'clear':
                self.spelled_text = ''
                self.captured_letter = 'CLEAR'
            else:
                self.captured_letter = None  # no valid detection

            record = {
                'round': self.round_number,
                'captured': self.captured_letter,
                'confidence': conf,
                'text': self.spelled_text,
            }
            self.history.insert(0, record)
            self.state = 'result'

        print(f"[SPELL] Capture {record['round']}: "
              f"{record['captured'] or '?'} -> \"{self.spelled_text}\"")

        time.sleep(RESULT_HOLD_SECS)

        with self._lock:
            self.state = 'idle'
            self._detection_locked = False

        return record

    def backspace(self):
        with self._lock:
            self.spelled_text = self.spelled_text[:-1]

    def add_space(self):
        with self._lock:
            self.spelled_text += ' '

    def reset(self):
        with self._lock:
            self.state = 'idle'
            self.countdown = None
            self.captured_letter = None
            self.spelled_text = ''
            self.round_number = 0
            self._detection_locked = False
            self.history.clear()
        print("[SPELL] Reset")

    def to_dict(self):
        with self._lock:
            return {
                'state': self.state,
                'countdown': self.countdown,
                'detection': self.detection,
                'confidence': self.confidence,
                'capturedLetter': self.captured_letter,
                'spelledText': self.spelled_text,
                'round': self.round_number,
                'history': list(self.history),
            }


speller = SpellerState()


# ─── Brick Detection Callback ────────────────────────────────────────────
def handle_detections(detections):
    """Called by the video_object_detection brick with detection results.

    The brick may pass either:
      - {label: {"confidence": float}} (dict values)
      - {label: float}                 (plain float values)

    Any class above the confidence threshold is accepted — letters and
    the SPECIAL_LABELS actions alike — since the label set now depends
    entirely on your Edge Impulse model's classes.
    """
    if not detections:
        return
    print(f"[BRICK-RAW] {detections}")
    valid = {}
    for k, v in detections.items():
        label = k.lower()
        if isinstance(v, dict):
            conf = v.get("confidence")
        elif isinstance(v, list):
            conf = v[0].get("confidence") if v and isinstance(v[0], dict) else None
        else:
            conf = v
        if conf is not None and conf >= CONFIDENCE_THRESHOLD:
            valid[label] = conf
    if valid:
        best = max(valid, key=valid.get)
        speller.update_detection(best, valid[best])


if _detector:
    _detector.on_detect_all(handle_detections)


# ─── Flask Application ───────────────────────────────────────────────────
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def api_state():
    return jsonify(speller.to_dict())


@app.route('/api/capture', methods=['POST'])
def api_capture():
    state = speller.to_dict()
    if state['state'] != 'idle':
        return jsonify({'status': 'busy', 'message': 'Capture in progress'}), 409
    threading.Thread(target=speller.capture_letter, daemon=True).start()
    return jsonify({'status': 'ok', 'message': 'Capture started'})


@app.route('/api/backspace', methods=['POST'])
def api_backspace():
    speller.backspace()
    return jsonify({'status': 'ok', 'spelledText': speller.to_dict()['spelledText']})


@app.route('/api/space', methods=['POST'])
def api_space():
    speller.add_space()
    return jsonify({'status': 'ok', 'spelledText': speller.to_dict()['spelledText']})


@app.route('/api/reset', methods=['POST'])
def api_reset():
    speller.reset()
    return jsonify({'status': 'ok'})


# ─── Entry Point ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('=' * 50)
    print('  Sign Language Letter Speller — Arduino UNO Q')
    print('=' * 50)
    print(f'[MODE] Brick: {"yes" if _detector else "no"}')
    print(f'[MODE] App runner: {"yes" if _App else "no"}')

    threading.Thread(
        target=lambda: app.run(
            host='0.0.0.0', port=PORT, threaded=True, use_reloader=False
        ),
        daemon=True
    ).start()
    print(f'[WEB] http://0.0.0.0:{PORT}')

    if _App:
        _App.run()
    else:
        print('[INFO] Running standalone (no App runner)')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('\n[EXIT] Shutting down')
