// HingeJoy Interactive Web Experience

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const hingeSlider = document.getElementById("hinge-slider");
  const angleDisplay = document.getElementById("angle-display");
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

  // Controls & Triggers
  const presetButtons = document.querySelectorAll(".btn-preset");
  const reactionCards = document.querySelectorAll(".reaction-card");
  const foldActionBtns = document.querySelectorAll(".btn-fold-action");
  const waitlistForm = document.getElementById("waitlist-form");
  const footerWaitlistForm = document.getElementById("footer-waitlist-form");
  const waitlistSuccess = document.getElementById("waitlist-success");

  // Tab Elements
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
  let lastAngle = 180;
  let lastTimestamp = performance.now();
  let calculatedVelocity = 0;

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

  // Update 3D Phone Angle & Telemetry
  function setHingeAngle(angle, simulatedVelocity = null) {
    const currentAngle = parseInt(angle, 10);
    const now = performance.now();
    const dt = (now - lastTimestamp) / 1000;

    if (simulatedVelocity !== null) {
      calculatedVelocity = simulatedVelocity;
    } else if (dt > 0.01) {
      const dAngle = Math.abs(currentAngle - lastAngle);
      calculatedVelocity = Math.round(dAngle / dt);
    }

    lastAngle = currentAngle;
    lastTimestamp = now;

    if (hingeSlider) hingeSlider.value = currentAngle;
    if (angleDisplay) angleDisplay.textContent = `${currentAngle}°`;
    if (gaugeAngle) gaugeAngle.textContent = `${currentAngle}°`;
    if (liveSpeedBadge) liveSpeedBadge.textContent = `${calculatedVelocity}°/s`;

    // 3D Transform: 180° = flat (0deg rotation), 0° = closed (-180deg rotation showing Cover Display)
    const rotateY = -(180 - currentAngle);
    if (phoneLeftPanel) {
      phoneLeftPanel.style.transform = `rotateY(${rotateY}deg)`;
    }

    // Sync angle preset buttons
    if (presetButtons) {
      presetButtons.forEach(b => {
        const bAngle = parseInt(b.getAttribute("data-angle"), 10);
        if (bAngle === currentAngle) {
          b.classList.add("active");
        } else {
          b.classList.remove("active");
        }
      });
    }

    if (currentAngle <= 15 && lastAngle > 15) {
      applyReaction(null, calculatedVelocity);
    }
  }

  // Apply Reaction: Updates BOTH Inner Screen & Outer Cover Screen
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

    // 2. Update Outer Cover Screen Display (Visible when 0° closed)
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

  // Fold Action Buttons Click Handlers (Gentle, Normal, Slam, Rage)
  foldActionBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      initAudio();
      const speed = parseInt(btn.getAttribute("data-speed"), 10) || 240;
      const mode = btn.getAttribute("data-mode") || "snap";

      // 1. Immediately apply reaction emoji, title, and sound
      applyReaction(mode, speed);

      // 2. Physically fold phone to 0° (Closed), showing the Outer Cover Screen directly!
      setHingeAngle(0, speed);
    });
  });

  // Slider Listener
  if (hingeSlider) {
    hingeSlider.addEventListener("input", (e) => {
      setHingeAngle(e.target.value);
    });
  }

  // Preset Buttons (180, 90, 45, 0)
  presetButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      presetButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const targetAngle = btn.getAttribute("data-angle");
      if (targetAngle !== null) {
        setHingeAngle(targetAngle, 180);
      }
    });
  });

  // Reaction Cards Click Listener
  reactionCards.forEach(card => {
    card.addEventListener("click", () => {
      const mode = card.getAttribute("data-mode");
      const speed = parseInt(card.getAttribute("data-speed"), 10) || 240;
      applyReaction(mode, speed);
      setHingeAngle(0, speed);
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
