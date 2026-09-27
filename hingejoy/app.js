// HingeJoy Interactive Web Experience

document.addEventListener("DOMContentLoaded", () => {

  // Fold Action Buttons (Gentle, Normal, Slam, Rage)
  const foldActionBtns = document.querySelectorAll(".btn-fold-action");
  foldActionBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      initAudio();
      foldActionBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      const speed = parseInt(btn.getAttribute("data-speed"), 10) || 240;
      const mode = btn.getAttribute("data-mode") || "snap";

      // Animate fold: start from 180, snap to 0 with target velocity, then reopen to 180
      setHingeAngle(180);
      setTimeout(() => {
        setHingeAngle(0, speed);
        highlightActiveReactionCard(mode);
        setTimeout(() => {
          setHingeAngle(180, 80);
        }, 800);
      }, 100);
    });
  });


  // Simulator vs Video Tab Switching
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

  // DOM Elements
  const hingeSlider = document.getElementById("hinge-slider");
  const angleDisplay = document.getElementById("angle-display");
  const gaugeAngle = document.getElementById("gauge-angle");
  const liveSpeedBadge = document.getElementById("live-speed-badge");
  const phoneLeftPanel = document.querySelector(".panel-left");
  const reactionEmoji = document.getElementById("reaction-emoji");
  const reactionTitle = document.getElementById("reaction-title");
  const currentModeLabel = document.getElementById("current-mode-label");
  const soundWaveBars = document.querySelectorAll(".sound-wave-bars .bar");
  const presetButtons = document.querySelectorAll(".btn-preset");
  const btnSnapTest = document.getElementById("btn-snap-test");
  const reactionCards = document.querySelectorAll(".reaction-card");
  const soundPlayButtons = document.querySelectorAll(".btn-play-sound");
  const waitlistForm = document.getElementById("waitlist-form");
  const footerWaitlistForm = document.getElementById("footer-waitlist-form");
  const waitlistSuccess = document.getElementById("waitlist-success");

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
      // Gentle Kiss Chime / Sine swell
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(587.33, now); // D5
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.15); // A5
      gain.gain.setValueAtTime(0.3, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } else if (mode === "snap") {
      // Crisp mechanical click
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
      // Heavy Boss Slam impact
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
      // Explosive Sonic Boom
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
    soundWaveBars.forEach((bar, index) => {
      const randomHeight = Math.floor(Math.random() * 12) + 4;
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
    const dt = (now - lastTimestamp) / 1000; // seconds

    if (simulatedVelocity !== null) {
      calculatedVelocity = simulatedVelocity;
    } else if (dt > 0.01) {
      const dAngle = Math.abs(currentAngle - lastAngle);
      calculatedVelocity = Math.round(dAngle / dt);
    }

    lastAngle = currentAngle;
    lastTimestamp = now;

    // Update displays
    if (hingeSlider) hingeSlider.value = currentAngle;
    if (angleDisplay) angleDisplay.textContent = `${currentAngle}°`;
    if (gaugeAngle) gaugeAngle.textContent = `${currentAngle}°`;
    if (liveSpeedBadge) liveSpeedBadge.textContent = `${calculatedVelocity}°/s`;

    // 3D Transform: 180° = flat (0deg rotation), 0° = closed (-180deg rotation)
    const rotateY = -(180 - currentAngle);
    if (phoneLeftPanel) {
      phoneLeftPanel.style.transform = `rotateY(${rotateY}deg)`;
    }

    // Trigger Fold Detection if fully closed (< 15°)
    if (currentAngle <= 15 && lastAngle > 15) {
      triggerFoldEvent(calculatedVelocity);
    }
  }

  function triggerFoldEvent(velocity) {
    foldCount++;
    if (metricFolds) metricFolds.textContent = foldCount;

    if (velocity > peakSpeed) {
      peakSpeed = velocity;
      if (metricPeak) metricPeak.textContent = `${peakSpeed}°/s`;
    }

    // Classify Reaction Mode
    let mode = "snap";
    let emoji = "📱";
    let title = "Classic Snap";

    if (velocity < 120) {
      mode = "kiss";
      emoji = "💋";
      title = "Lover's Kiss";
    } else if (velocity <= 300) {
      mode = "snap";
      emoji = "📱";
      title = "Classic Snap";
    } else if (velocity <= 600) {
      mode = "slam";
      emoji = "🐷";
      title = "Boss Slam";
    } else {
      mode = "rage";
      emoji = "💥";
      title = "Rage Mode";
    }

    if (reactionEmoji) {
      reactionEmoji.textContent = emoji;
      reactionEmoji.style.transform = "scale(1.3)";
      setTimeout(() => {
        reactionEmoji.style.transform = "scale(1)";
      }, 200);
    }
    if (reactionTitle) reactionTitle.textContent = title;
    if (currentModeLabel) currentModeLabel.textContent = title;

    playReactionSound(mode);
    highlightActiveReactionCard(mode);
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

  // Slider Listener
  if (hingeSlider) {
    hingeSlider.addEventListener("input", (e) => {
      setHingeAngle(e.target.value);
    });
  }

  // Preset Buttons
  presetButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      presetButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const targetAngle = btn.getAttribute("data-angle");
      if (targetAngle !== null) {
        setHingeAngle(targetAngle, 200);
      }
    });
  });

  // Test Fast Fold Button
  if (btnSnapTest) {
    btnSnapTest.addEventListener("click", () => {
      initAudio();
      setHingeAngle(180);
      setTimeout(() => {
        setHingeAngle(0, 520);
        setTimeout(() => {
          setHingeAngle(180, 100);
        }, 600);
      }, 150);
    });
  }

  // Reaction Cards Sound Buttons
  reactionCards.forEach(card => {
    card.addEventListener("click", () => {
      const mode = card.getAttribute("data-mode");
      const speed = parseInt(card.getAttribute("data-speed"), 10) || 200;
      highlightActiveReactionCard(mode);
      triggerFoldEvent(speed);
    });
  });

  // Supabase config
  const SUPABASE_URL = "https://nxodbwoiwnplbzjdepib.supabase.co";
  const SUPABASE_KEY = "sb_publishable_oBqdUjVQYGL_U5SR6OELag_aM76Uw6F";

  // Waitlist Submissions
  async function handleWaitlist(e, form) {
    e.preventDefault();
    const input = form.querySelector('input[type="email"]');
    if (!input || !input.value) return;

    const email = input.value.trim();
    const source = form.id === "footer-waitlist-form" ? "footer" : "hero";
    const btn = form.querySelector("button");

    if (btn) {
      btn.disabled = true;
      btn.innerHTML = "<span>Saving...</span>";
    }

    try {
      const res = await fetch(`${SUPABASE_URL}/rest/v1/waitlist`, {
        method: "POST",
        headers: {
          "apikey": SUPABASE_KEY,
          "Authorization": `Bearer ${SUPABASE_KEY}`,
          "Content-Type": "application/json",
          "Prefer": "return=minimal"
        },
        body: JSON.stringify({ email, source })
      });

      if (res.ok || res.status === 201) {
        if (waitlistSuccess) waitlistSuccess.classList.remove("hidden");
        input.value = "";
        if (btn) {
          btn.innerHTML = "<span>Spot Secured ✓</span>";
          btn.style.background = "#34c759";
        }
      } else if (res.status === 409) {
        // Duplicate email
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = "<span>Already registered ✓</span>";
          btn.style.background = "#636366";
        }
      } else {
        throw new Error(`HTTP ${res.status}`);
      }
    } catch (err) {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = "<span>Try again</span>";
      }
    }
  }

  if (waitlistForm) {
    waitlistForm.addEventListener("submit", (e) => handleWaitlist(e, waitlistForm));
  }
  if (footerWaitlistForm) {
    footerWaitlistForm.addEventListener("submit", (e) => handleWaitlist(e, footerWaitlistForm));
  }

});
