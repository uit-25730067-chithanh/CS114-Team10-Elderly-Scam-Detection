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

        if (key === 'hospital') {
          badgeClass = 'badge-threat';
          badgeText = 'Tống tiền cấp cứu';
        } else if (key === 'gift') {
          badgeClass = 'badge-warning';
          badgeText = 'Bẫy trúng thưởng';
        } else if (key === 'family') {
          badgeClass = 'badge-safe';
          badgeText = 'Gia đình an toàn';
        }

        const card = document.createElement('div');
        card.className = 'preset-card';
        card.innerHTML = `
          <div class="preset-top">
            <span class="preset-name">${item.title}</span>
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
