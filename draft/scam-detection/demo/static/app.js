/**
 * Civic Guard — Public Safety Console Engine
 * Realtime XGBoost ML Scoring • Interactive Highlighting • State Transitions
 */

document.addEventListener('DOMContentLoaded', () => {
  // Input Controls
  const smsInput = document.getElementById('smsInput');
  const btnPaste = document.getElementById('btnPaste');
  const btnClear = document.getElementById('btnClear');
  const btnAnalyze = document.getElementById('btnAnalyze');
  const presetsGrid = document.getElementById('presetsGrid');
  const btnElderlyToggle = document.getElementById('btnElderlyToggle');

  // Console States
  const stateStandby = document.getElementById('stateStandby');
  const stateScanning = document.getElementById('stateScanning');
  const stateResult = document.getElementById('stateResult');

  // Result Metrics & Content
  const scoreProgress = document.getElementById('scoreProgress');
  const scoreVal = document.getElementById('scoreVal');
  const verdictBadge = document.getElementById('verdictBadge');
  const verdictTitle = document.getElementById('verdictTitle');
  const verdictDesc = document.getElementById('verdictDesc');
  
  const trapsContainer = document.getElementById('trapsContainer');
  const trapsGrid = document.getElementById('trapsGrid');
  const highlightedContent = document.getElementById('highlightedContent');
  const emergencyPanel = document.getElementById('emergencyPanel');

  let activePresetCard = null;

  // 1. Elderly Mode Preference
  if (localStorage.getItem('civic_elderly_mode') === 'true') {
    document.body.classList.add('elderly-mode');
    btnElderlyToggle.classList.add('active');
  }

  btnElderlyToggle.addEventListener('click', () => {
    const isElderly = document.body.classList.toggle('elderly-mode');
    btnElderlyToggle.classList.toggle('active', isElderly);
    localStorage.setItem('civic_elderly_mode', isElderly);
  });

  // 2. Fetch and render real scenario presets
  fetch('/api/samples')
    .then(res => res.json())
    .then(samples => {
      presetsGrid.innerHTML = '';
      const keys = Object.keys(samples);

      keys.forEach(key => {
        const item = samples[key];
        let badgeClass = 'badge-threat';
        let badgeText = 'Đe dọa bắt giữ';
        let iconClass = 'icon-box-police';
        let iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#BE123C" stroke-width="2.2"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/></svg>`;

        if (key === 'hospital') {
          badgeClass = 'badge-threat';
          badgeText = 'Tống tiền cấp cứu';
          iconClass = 'icon-box-hospital';
          iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#E11D48" stroke-width="2.2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>`;
        } else if (key === 'gift') {
          badgeClass = 'badge-warning';
          badgeText = 'Bẫy trúng thưởng';
          iconClass = 'icon-box-gift';
          iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>`;
        } else if (key === 'family') {
          badgeClass = 'badge-safe';
          badgeText = 'Gia đình an toàn';
          iconClass = 'icon-box-family';
          iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`;
        }

        const card = document.createElement('div');
        card.className = 'preset-card';
        card.innerHTML = `
          <div class="preset-top">
            <div class="preset-title-group">
              <div class="preset-icon-box ${iconClass}">${iconSvg}</div>
              <span class="preset-name">${item.title}</span>
            </div>
            <span class="preset-badge ${badgeClass}">${badgeText}</span>
          </div>
          <p class="preset-snippet">${item.content}</p>
        `;

        card.addEventListener('click', () => {
          if (activePresetCard) activePresetCard.classList.remove('active');
          card.classList.add('active');
          activePresetCard = card;

          smsInput.value = item.content;
          updateToolbar();
          runDetection(item.content);
        });

        presetsGrid.appendChild(card);
      });
    })
    .catch(err => console.error('Lỗi nạp kịch bản mẫu:', err));

  // 3. Toolbar actions
  function updateToolbar() {
    if (smsInput.value.trim().length > 0) {
      btnClear.style.display = 'inline-flex';
    } else {
      btnClear.style.display = 'none';
    }
  }

  smsInput.addEventListener('input', () => {
    if (activePresetCard) {
      activePresetCard.classList.remove('active');
      activePresetCard = null;
    }
    updateToolbar();
  });

  btnClear.addEventListener('click', () => {
    smsInput.value = '';
    updateToolbar();
    if (activePresetCard) {
      activePresetCard.classList.remove('active');
      activePresetCard = null;
    }
    // Return to standby state
    switchState('standby');
    smsInput.focus();
  });

  btnPaste.addEventListener('click', async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        smsInput.value = text;
        updateToolbar();
        runDetection(text);
      }
    } catch (e) {
      smsInput.focus();
      document.execCommand('paste');
      updateToolbar();
    }
  });

  btnAnalyze.addEventListener('click', () => {
    const text = smsInput.value.trim();
    if (!text) {
      smsInput.focus();
      return;
    }
    runDetection(text);
  });

  // 4. State Switcher
  function switchState(stateName) {
    stateStandby.style.display = 'none';
    stateScanning.style.display = 'none';
    stateResult.style.display = 'none';

    if (stateName === 'standby') {
      stateStandby.style.display = 'flex';
    } else if (stateName === 'scanning') {
      stateScanning.style.display = 'flex';
    } else if (stateName === 'result') {
      stateResult.style.display = 'block';
    }
  }

  // 5. Execute ML Detection API
  async function runDetection(text) {
    switchState('scanning');
    btnAnalyze.disabled = true;

    // Smooth scroll down to scanning box on mobile
    if (window.innerWidth <= 1024) {
      setTimeout(() => {
        stateScanning.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    }

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      if (!response.ok) throw new Error('Yêu cầu giám định thất bại');
      const data = await response.json();

      // Realistic scanning feedback timing (500ms)
      setTimeout(() => {
        btnAnalyze.disabled = false;
        displayVerdict(data);
        switchState('result');

        // Smooth scroll down to verdict card on mobile
        if (window.innerWidth <= 1024) {
          setTimeout(() => {
            stateResult.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }, 80);
        }
      }, 500);

    } catch (err) {
      console.error(err);
      btnAnalyze.disabled = false;
      switchState('standby');
      alert('Không thể kết nối máy chủ phân tích. Vui lòng thử lại.');
    }
  }

  // 6. Display Verdict & Visuals
  function displayVerdict(data) {
    const pct = Math.round(data.risk_score * 100);
    const isThreat = data.is_scam;

    // SVG Dial circumference: 2 * PI * 50 = 314.159
    const circumference = 314.159;
    const offset = circumference - (pct / 100) * circumference;
    scoreProgress.style.strokeDashoffset = offset;

    // Dial color & Verdict Text
    if (isThreat) {
      scoreProgress.style.stroke = '#E11D48';
      scoreVal.style.color = '#BE123C';

      verdictBadge.className = 'verdict-badge badge-danger-level';
      verdictBadge.textContent = 'MỨC NGUY CƠ CAO (LỪA ĐẢO)';
      verdictTitle.textContent = 'Cảnh Báo: Kịch Bản Lừa Đảo';
      verdictTitle.style.color = '#BE123C';
      verdictDesc.textContent = 'Phát hiện nhiều thủ đoạn đe dọa khởi tố, ép nộp tiền khẩn cấp hoặc tống tiền viện phí.';
      
      emergencyPanel.style.display = 'block';
    } else {
      scoreProgress.style.stroke = '#059669';
      scoreVal.style.color = '#065F46';

      verdictBadge.className = 'verdict-badge badge-safe-level';
      verdictBadge.textContent = 'AN TÂM - TIN CẬY';
      verdictTitle.textContent = 'Tin Nhắn Bình Thường';
      verdictTitle.style.color = '#065F46';
      verdictDesc.textContent = 'Nội dung giao tiếp sinh hoạt lành mạnh, không phát hiện dấu hiệu mạo danh hay ép buộc chuyển tiền.';
      
      emergencyPanel.style.display = 'none';
    }

    // Number Counter Animation
    animateNumber(scoreVal, 0, pct, 600);

    // Render Psychological Indicators
    if (data.detected_indicators && data.detected_indicators.length > 0) {
      trapsContainer.style.display = 'block';
      trapsGrid.innerHTML = data.detected_indicators.map(ind => `
        <div class="trap-pill">
          <div class="trap-name">${escapeHtml(ind.label)}</div>
          <div class="trap-evidence">Cụm từ nhận diện: ${escapeHtml(ind.keywords.join(', '))}</div>
        </div>
      `).join('');
    } else {
      trapsContainer.style.display = 'none';
    }

    // Render Highlighted Content
    highlightedContent.innerHTML = formatHighlightedText(data.text, data.matched_keywords);
  }

  // Smooth Counter
  function animateNumber(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(easeOut * (end - start) + start);
      element.textContent = current + '%';
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        element.textContent = end + '%';
      }
    };
    window.requestAnimationFrame(step);
  }

  // Highlight keywords
  function formatHighlightedText(text, keywords) {
    if (!keywords || keywords.length === 0) {
      return `<p>${escapeHtml(text)}</p>`;
    }

    // Sort keywords by length descending
    const sorted = [...keywords].sort((a, b) => b.length - a.length);
    const regex = new RegExp('(' + sorted.map(escapeRegex).join('|') + ')', 'gi');

    const escaped = escapeHtml(text);
    const replaced = escaped.replace(regex, (match) => {
      return `<mark class="mark-scam">${match}</mark>`;
    });

    return `<p>${replaced}</p>`;
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
});
