// HingeJoy Web Experience

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const soundWaveBars = document.querySelectorAll(".sound-wave-bars .bar");
  const reactionCards = document.querySelectorAll(".reaction-card");
  const soundPlayButtons = document.querySelectorAll(".btn-play-sound");
  const waitlistForm = document.getElementById("waitlist-form");
  const footerWaitlistForm = document.getElementById("footer-waitlist-form");
  const waitlistSuccess = document.getElementById("waitlist-success");

  // Web Audio Synthesizer Context
  let audioCtx = null;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
  }

  // Synthesize Sound Effects for Reaction Cards
  function playReactionSound(mode) {
    initAudio();
    if (!audioCtx) return;

    const now = audioCtx.currentTime;

    if (mode === "kiss") {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(587.33, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.15);
      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } else if (mode === "snap") {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(1200, now);
      osc.frequency.exponentialRampToValueAtTime(150, now + 0.05);
      gain.gain.setValueAtTime(0.6, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.06);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.06);
    } else if (mode === "slam") {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(40, now + 0.25);
      gain.gain.setValueAtTime(0.7, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.28);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.28);
    } else if (mode === "rage") {
      const bufferSize = audioCtx.sampleRate * 0.4;
      const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (audioCtx.sampleRate * 0.08));
      }
      const noise = audioCtx.createBufferSource();
      noise.buffer = buffer;
      const gain = audioCtx.createGain();
      gain.gain.setValueAtTime(0.9, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
      noise.connect(gain);
      gain.connect(audioCtx.destination);
      noise.start(now);
    }
  }

  function highlightActiveReactionCard(mode) {
    reactionCards.forEach(card => {
      if (card.getAttribute("data-mode") === mode) {
        card.classList.add("active");
      } else {
        card.classList.remove("active");
      }
    });
  }

  // Reaction Cards Sound Buttons & Click Handlers
  reactionCards.forEach(card => {
    card.addEventListener("click", () => {
      const mode = card.getAttribute("data-mode") || "snap";
      highlightActiveReactionCard(mode);
      playReactionSound(mode);
    });
  });

  soundPlayButtons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const card = btn.closest(".reaction-card");
      if (card) {
        const mode = card.getAttribute("data-mode") || "snap";
        highlightActiveReactionCard(mode);
        playReactionSound(mode);
      }
    });
  });

  // Waitlist Submissions
  function handleWaitlist(e, form) {
    e.preventDefault();
    const input = form.querySelector("input[type=\"email\"]");
    if (!input || !input.value) return;

    const emails = JSON.parse(localStorage.getItem("hingejoy_waitlist") || "[]");
    emails.push({ email: input.value, timestamp: new Date().toISOString() });
    localStorage.setItem("hingejoy_waitlist", JSON.stringify(emails));

    if (waitlistSuccess) {
      waitlistSuccess.classList.remove("hidden");
    }
    input.value = "";
    const btn = form.querySelector("button");
    if (btn) {
      btn.innerHTML = "<span>Spot Secured ✓</span>";
      btn.style.background = "#34c759";
    }
  }

  if (waitlistForm) {
    waitlistForm.addEventListener("submit", (e) => handleWaitlist(e, waitlistForm));
  }
  if (footerWaitlistForm) {
    footerWaitlistForm.addEventListener("submit", (e) => handleWaitlist(e, footerWaitlistForm));
  }
});
