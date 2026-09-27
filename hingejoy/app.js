// HingeJoy Interactive Web Experience (2-State Open/Closed Simulator)

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const gaugeAngle = document.getElementById("gauge-angle");
  const liveSpeedBadge = document.getElementById("live-speed-badge");
  const phoneLeftPanel = document.querySelector(".panel-left");
  
  // Inner Screen Elements
  const reactionEmoji = document.getElementById("reaction-emoji");
  const reactionTitle = document.getElementById("reaction-title");
  const currentModeLabel = document.getElementById("current-mode-label");
  const soundWaveBars = document.querySelectorAll(".sound-wave-bars .bar");

  // Outer Cover Screen Elements
  const coverEmoji = document.getElementById("cover-emoji");
  const coverTitle = document.getElementById("cover-title");
  const coverSpeedChip = document.getElementById("cover-speed-chip");

  // 2-State Switch Buttons
  const btnStateOpen = document.getElementById("btn-state-open");
  const btnStateClosed = document.getElementById("btn-state-closed");

  // Reaction Buttons & Cards
  const reactionCards = document.querySelectorAll(".reaction-card");
  const foldActionBtns = document.querySelectorAll(".btn-fold-action");
  const waitlistForm = document.getElementById("waitlist-form");
  const footerWaitlistForm = document.getElementById("footer-waitlist-form");
  const waitlistSuccess = document.getElementById("waitlist-success");

  // Tab Elements (Simulator vs Video)
  const tabSim = document.getElementById("tab-sim");
  const tabVideo = document.getElementById("tab-video");
  const contentSim = document.getElementById("content-sim");
  const contentVideo = document.getElementById("content-video");

  if (tabSim && tabVideo && contentSim && contentVideo) {
    tabSim.addEventListener("click", () => {
      tabSim.classList.add("active");
      tabVideo.classList.remove("active");
      contentSim.classList.remove("hidden");
      contentVideo.classList.add("hidden");
    });

    tabVideo.addEventListener("click", () => {
      tabVideo.classList.add("active");
      tabSim.classList.remove("active");
      contentVideo.classList.remove("hidden");
      contentSim.classList.add("hidden");
    });
  }

  // Telemetry Metrics
  const metricFolds = document.getElementById("metric-folds");
  const metricPeak = document.getElementById("metric-peak");

  let foldCount = 12;
  let peakSpeed = 480;
  let currentState = "open"; // "open" (180deg) or "closed" (0deg)

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

  // Synthesize Sound Effects
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

    animateWaveform();
  }

  function animateWaveform() {
    soundWaveBars.forEach((bar) => {
      const randomHeight = Math.floor(Math.random() * 14) + 4;
      bar.style.height = `${randomHeight}px`;
      setTimeout(() => {
        bar.style.height = "4px";
      }, 250);
    });
  }

  // 2-State Transition Controller (Open: 180° | Closed: 0°)
  function setDeviceState(state) {
    currentState = state;

    if (state === "open") {
      if (btnStateOpen) btnStateOpen.classList.add("active");
      if (btnStateClosed) btnStateClosed.classList.remove("active");
      if (phoneLeftPanel) phoneLeftPanel.style.transform = "rotateY(0deg)";
      if (gaugeAngle) gaugeAngle.textContent = "180°";
    } else {
      if (btnStateClosed) btnStateClosed.classList.add("active");
      if (btnStateOpen) btnStateOpen.classList.remove("active");
      if (phoneLeftPanel) phoneLeftPanel.style.transform = "rotateY(-180deg)";
      if (gaugeAngle) gaugeAngle.textContent = "0°";
    }
  }

  // Apply Reaction: Updates Reaction Data, Sounds, and Displays
  function applyReaction(explicitMode, speed) {
    let mode = explicitMode;
    let emoji = "📱";
    let title = "Classic Snap";

    if (!mode) {
      if (speed < 120) mode = "kiss";
      else if (speed <= 300) mode = "snap";
      else if (speed <= 600) mode = "slam";
      else mode = "rage";
    }

    if (mode === "kiss") {
      emoji = "💋";
      title = "Lover's Kiss";
    } else if (mode === "snap") {
      emoji = "📱";
      title = "Classic Snap";
    } else if (mode === "slam") {
      emoji = "🐷";
      title = "Boss Slam";
    } else if (mode === "rage") {
      emoji = "💥";
      title = "Rage Mode";
    }

    foldCount++;
    if (metricFolds) metricFolds.textContent = foldCount;

    if (speed > peakSpeed) {
      peakSpeed = speed;
      if (metricPeak) metricPeak.textContent = `${peakSpeed}°/s`;
    }

    if (liveSpeedBadge) liveSpeedBadge.textContent = `${speed}°/s`;

    // 1. Update Inner Screen Display
    if (reactionEmoji) reactionEmoji.textContent = emoji;
    if (reactionTitle) reactionTitle.textContent = title;
    if (currentModeLabel) currentModeLabel.textContent = title;

    // 2. Update Outer Cover Screen Display (Facing user when 0° closed)
    if (coverEmoji) {
      coverEmoji.textContent = emoji;
      coverEmoji.style.transform = "scale(1.3)";
      setTimeout(() => {
        coverEmoji.style.transform = "scale(1)";
      }, 200);
    }
    if (coverTitle) coverTitle.textContent = title;
    if (coverSpeedChip) coverSpeedChip.textContent = `${speed}°/s Shut Speed`;

    playReactionSound(mode);
    highlightActiveReactionCard(mode);

    // Sync button active states
    if (foldActionBtns) {
      foldActionBtns.forEach(b => {
        if (b.getAttribute("data-mode") === mode) {
          b.classList.add("active");
        } else {
          b.classList.remove("active");
        }
      });
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

  // 2-State Switch Button Handlers
  if (btnStateOpen) {
    btnStateOpen.addEventListener("click", () => {
      setDeviceState("open");
    });
  }

  if (btnStateClosed) {
    btnStateClosed.addEventListener("click", () => {
      setDeviceState("closed");
    });
  }

  // Fold Action Buttons: Tap to Snap Shut & Play
  foldActionBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      initAudio();
      const speed = parseInt(btn.getAttribute("data-speed"), 10) || 240;
      const mode = btn.getAttribute("data-mode") || "snap";

      // 1. Apply reaction data & sound
      applyReaction(mode, speed);

      // 2. Snap to CLOSED (0°) state showing Cover Display
      setDeviceState("closed");
    });
  });

  // Reaction Cards Click Listener
  reactionCards.forEach(card => {
    card.addEventListener("click", () => {
      const mode = card.getAttribute("data-mode");
      const speed = parseInt(card.getAttribute("data-speed"), 10) || 240;
      applyReaction(mode, speed);
      setDeviceState("closed");
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
