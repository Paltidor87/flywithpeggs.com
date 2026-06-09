#!/usr/bin/env python3
import sys

path = '/Users/peggs/Projects/flywithpeggs.com/app.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate // EFT
start_idx = content.find('// EFT\nconst EFT_PTS=')
if start_idx == -1:
    # Try with \r\n
    start_idx = content.find('// EFT\r\nconst EFT_PTS=')
    if start_idx == -1:
        print("Error: Could not find start marker '// EFT'")
        sys.exit(1)

# Locate the end of analyzeSong function
end_marker = "async function analyzeSong(){const song=document.getElementById('freq-song')?.value?.trim();if(!song){toast('Describe a song first');return;}const btn=document.getElementById('freq-song-btn');const text=document.getElementById('freq-song-result');btn.disabled=true;btn.textContent='Analyzing...';text.textContent='Reading the frequency field...';try{const r=await fetch('https://api.anthropic.com/v1/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:'claude-sonnet-4-20250514',max_tokens:400,system:'You are an expert in music frequencies, Solfeggio tones, and how sound affects the human energy field. Analyze songs based on musical key, tempo, frequency range, and emotional resonance.',messages:[{role:'user',content:`Analyze this song: \"${song}\". What frequency field is it operating in? Healing, activation, sedation, programming, elevation, or disruption? Give specific musical and energetic reasons.`}]})});const d=await r.json();text.textContent=d.content?.[0]?.text||'Cannot analyze.';btn.textContent='↻ Analyze Again';btn.disabled=false;}catch(e){text.textContent='Connection disrupted.';btn.disabled=false;btn.textContent='☽ Analyze This Song';}}"

end_idx = content.find(end_marker)
if end_idx == -1:
    # Try with single quotes or normalized quotes
    print("Error: Could not find end marker (analyzeSong function)")
    sys.exit(1)

# Add length of end marker to get total length to replace
end_idx += len(end_marker)

NEW_JS = """// EFT
const EFT_ZONES = [
  {
    id: 'crown',
    name: 'Crown',
    meridian: 'Governing Vessel',
    emotion: 'Divine connection, integration, blockages to higher self',
    zodiac: 'Aries',
    house: '1st',
    instruction: 'Tap the crown of the head with all fingers.',
    color: '#c8a84b',
    coords: [{x: 0, y: 1.17, z: 0}]
  },
  {
    id: 'brow',
    name: 'Brow',
    meridian: 'Bladder',
    emotion: 'Restlessness, anxiety, trauma, mental fog',
    zodiac: 'Aquarius',
    house: '11th',
    instruction: 'Tap the beginning of the eyebrow just above the nose.',
    color: '#4080c0',
    coords: [{x: 0, y: 0.96, z: 0.18}]
  },
  {
    id: 'throat',
    name: 'Throat',
    meridian: 'Large Intestine',
    emotion: 'Expression, speaking truth, holding back, resentment',
    zodiac: 'Taurus',
    house: '2nd',
    instruction: 'Tap the throat area / collarbone junction.',
    color: '#3abfb0',
    coords: [{x: 0, y: 0.58, z: 0.15}]
  },
  {
    id: 'heart',
    name: 'Heart/Chest',
    meridian: 'Kidney',
    emotion: 'Fear, terror, insecurity, grief, lack of love',
    zodiac: 'Capricorn',
    house: '10th',
    instruction: 'Tap the center of the chest (Heart chakra / collarbone area).',
    color: '#b04040',
    coords: [{x: 0, y: 0.32, z: 0.16}]
  },
  {
    id: 'solar',
    name: 'Solar Plexus',
    meridian: 'Spleen',
    emotion: 'Self-worth, worry, vulnerability, low self-esteem, anxiety',
    zodiac: 'Leo',
    house: '5th',
    instruction: 'Tap the upper abdomen, just below the ribs.',
    color: '#e09030',
    coords: [{x: 0, y: 0.05, z: 0.16}]
  },
  {
    id: 'abdomen',
    name: 'Abdomen',
    meridian: 'Stomach',
    emotion: 'Worry, nourishment, future anxiety, digestion of life',
    zodiac: 'Cancer',
    house: '4th',
    instruction: 'Tap the lower abdomen, below the navel.',
    color: '#6090b8',
    coords: [{x: 0, y: -0.22, z: 0.16}]
  },
  {
    id: 'left_hand',
    name: 'Left Hand',
    meridian: 'Heart Protector',
    emotion: 'Boundaries, defense, vulnerability, safety, protection',
    zodiac: 'Scorpio',
    house: '8th',
    instruction: 'Tap the side of your left hand (Karate Chop point) or wrist.',
    color: '#9d6fd1',
    coords: [{x: -0.85, y: -0.22, z: 0}]
  },
  {
    id: 'right_hand',
    name: 'Right Hand',
    meridian: 'Heart Protector',
    emotion: 'Boundaries, defense, vulnerability, safety, protection',
    zodiac: 'Scorpio',
    house: '8th',
    instruction: 'Tap the side of your right hand (Karate Chop point) or wrist.',
    color: '#9d6fd1',
    coords: [{x: 0.85, y: -0.22, z: 0}]
  },
  {
    id: 'hips',
    name: 'Hips',
    meridian: 'Gallbladder',
    emotion: 'Indecision, anger, frustration, stored trauma',
    zodiac: 'Libra',
    house: '7th',
    instruction: 'Tap the hip points on either side of the pelvis.',
    color: '#c090b8',
    coords: [{x: 0, y: -0.46, z: 0.15}]
  },
  {
    id: 'knees',
    name: 'Knees',
    meridian: 'Bladder',
    emotion: 'Fear of change, rigidity, resistance, submission',
    zodiac: 'Sagittarius',
    house: '9th',
    instruction: 'Tap the knees gently on the sides or front.',
    color: '#c87030',
    coords: [
      {x: -0.22, y: -0.9, z: 0.13},
      {x: 0.22, y: -0.9, z: 0.13}
    ]
  },
  {
    id: 'feet',
    name: 'Feet',
    meridian: 'Kidney Root',
    emotion: 'Insecurity, grounding, safety foundation, survival',
    zodiac: 'Pisces',
    house: '12th',
    instruction: 'Tap your feet on the ground or rub the soles.',
    color: '#7070c0',
    coords: [
      {x: -0.22, y: -1.35, z: 0.18},
      {x: 0.22, y: -1.35, z: 0.18}
    ]
  }
];

let eftStep=-1, eftActive=false, eftDone=new Set(), eftSUD=-1, eftIssue='', eftReminder='', eftInit=false;
let eftScene, eftCamera, eftRenderer, eftControls, eftMannequin, eftHotspots = [], eftSelectedZone = null, eftAnimationFrameId = null, eftIsRotating = true;

function initEftPanel(){
  if(eftInit) return;
  eftInit = true;
  
  // Set up SUD track
  const track = document.getElementById('eft-sud-track');
  if(track && !track.children.length){
    for(let i=0; i<=10; i++){
      const b = document.createElement('button');
      b.className = 'card-btn';
      b.style.cssText = 'flex:1;padding:5px 2px;font-size:.65rem;min-width:0;';
      b.textContent = i;
      const ii = i;
      b.onclick = () => {
        eftSUD = ii;
        document.querySelectorAll('#eft-sud-track button').forEach(x => {
          x.style.background = '';
          x.style.color = '';
          x.style.borderColor = '';
        });
        b.style.background = 'rgba(42,175,170,.3)';
        b.style.color = 'var(--teal)';
        b.style.borderColor = 'var(--teal)';
        document.getElementById('eft-sud-display').textContent = ii + ' / 10';
        eftGeneratePhrase();
      };
      track.appendChild(b);
    }
  }

  // Quick nav points list at bottom
  const quickNav = document.getElementById('eft-quick-nav-points');
  if (quickNav && !quickNav.children.length) {
    quickNav.innerHTML = EFT_ZONES.map(z => 
      `<button class="card-btn" data-id="${z.id}" onclick="eftSelectZone('${z.id}')" style="font-size:0.68rem; padding:4px 9px; margin:2px; transition:all 0.3s; border-color: rgba(255,255,255,0.08);">${z.name}</button>`
    ).join('');
  }

  // Meridian map tab static list rendering
  const mg = document.getElementById('eft-meridian-grid');
  if(mg && !mg.children.length){
    mg.innerHTML = EFT_ZONES.map(pt => `
      <div style="background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:16px;transition:border-color .3s;cursor:pointer;" onmouseover="this.style.borderColor='${pt.color}'" onmouseout="this.style.borderColor=''" onclick="switchEftTab('session'); eftSelectZone('${pt.id}');">
        <div style="font-family:'Cinzel',serif;font-size:.7rem;letter-spacing:.09em;color:${pt.color};margin-bottom:6px;">${pt.name}</div>
        <div style="font-size:.78rem;color:var(--text-dim);margin-bottom:4px;">${pt.meridian} Meridian</div>
        <div style="font-size:.85rem;color:var(--text);line-height:1.6;margin-bottom:8px;">${pt.emotion}</div>
        <div style="display:flex;gap:5px;flex-wrap:wrap;">
          <span style="font-family:'Cinzel',serif;font-size:.58rem;padding:2px 7px;border-radius:2px;border:1px solid var(--gold-dim);color:var(--gold-dim);">${pt.zodiac}</span>
          <span style="font-family:'Cinzel',serif;font-size:.58rem;padding:2px 7px;border-radius:2px;border:1px solid var(--border-bright);color:var(--silver);">House ${pt.house}</span>
        </div>
      </div>
    `).join('');
  }

  // Matrix and Qigong setups remain the same
  const ms = document.getElementById('eft-matrix-steps');
  if(ms && !ms.children.length){
    const steps = [
      {t:'Identify the Issue',b:'Ask: What is not working right now? Find an early memory relating to this theme. Trust what surfaces.',p:'"What is my earliest memory of feeling this way?"'},
      {t:'Enter the Memory — Find the ECHO',b:'Close your eyes. Step into the memory as a compassionate adult observer. Find your younger self — the ECHO. You are not reliving it. You are entering the field to help.',p:'"I can see my younger self. I am going to help them."'},
      {t:'Tap on the ECHO',b:'Ask permission to tap on the ECHO. Tap your own physical points while imagining tapping on the ECHO simultaneously.',p:'"Even though you felt this, you are safe now. I am here."'},
      {t:'Bring in Resources',b:'Ask the ECHO what they need. Bring in any resource — a person, a feeling, a color. The ECHO chooses.',p:'"What do you need right now to feel safe?"'},
      {t:'Transform the Scene',b:'Allow the memory to shift into something positive and true that the ECHO can genuinely believe and feel.',p:'"How would you like this memory to look?"'},
      {t:'Send Into the Field',b:'Take the new image and send it through your mind, into your heart, and out into the unified matrix. Breathe it in. Feel it as real.',p:'"I send this new picture into my cells and my future."'},
      {t:'Test the Memory',b:'Open your eyes. Attempt to access the original memory. Most people find only the new version is available.',p:'"When I try to remember the original, what do I see?"'}
    ];
    ms.innerHTML = steps.map((s,i) => `<div style="background:var(--panel);border:1px solid var(--border);border-left:3px solid var(--teal);border-radius:2px;padding:16px 20px;margin-bottom:11px;"><div style="font-family:'Cinzel',serif;font-size:.7rem;letter-spacing:.1em;color:var(--silver);margin-bottom:7px;">Step ${i+1} — ${s.t}</div><div style="font-size:.88rem;color:var(--text-dim);line-height:1.65;margin-bottom:8px;">${s.b}</div><div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.95rem;color:var(--gold);padding:7px 11px;background:var(--surface);border-radius:2px;">${s.p}</div></div>`).join('');
  }

  const qg = document.getElementById('eft-qigong-grid');
  if(qg && !qg.children.length){
    const ps = [
      {i:'🌬️',t:'Quiescent Sitting',d:'Sit comfortably. Regulate breath. Allow the mind to settle. Qi follows attention — where the mind goes, energy flows. Same entry state as the Silva centering exercise.',tag:'BEGINNER · 10–20 MIN'},
      {i:'🌊',t:'Standing Like a Stake',d:'Feet shoulder-width, knees slightly bent, arms rounded as if holding a large ball. Hold the posture. The Qi accumulates.',tag:'BEGINNER · 10–30 MIN'},
      {i:'🌿',t:'Eight Pieces of Brocade',d:'Eight gentle movements that regulate Qi through all twelve meridians. The most widely practiced Qigong form.',tag:'INTERMEDIATE · 20 MIN'},
      {i:'🔥',t:'Health Cultivation Massage',d:'Self-massage of the meridian points in sequence — the same points used in EFT tapping. Morning practice.',tag:'BEGINNER · 15 MIN'},
      {i:'🌙',t:'Relaxed Recumbent',d:'Lying down, regulate breath. Used for recovery, insomnia, and chronic conditions. The body heals when the mind is still.',tag:'ALL LEVELS · BEFORE SLEEP'},
      {i:'✨',t:'Five Animals Frolic',d:'Bear, deer, monkey, bird, and tiger movements corresponding to the five organ systems. Han dynasty physician Hua Tuo.',tag:'ADVANCED · 30 MIN'}
    ];
    qg.innerHTML = ps.map(p => `<div style="background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:16px;cursor:pointer;transition:all .3s;" onmouseover="this.style.borderColor='var(--teal)'" onmouseout="this.style.borderColor=''"><div style="font-size:1.2rem;margin-bottom:7px;">${p.i}</div><div style="font-family:'Cinzel',serif;font-size:.7rem;letter-spacing:.09em;color:var(--teal);margin-bottom:5px;">${p.t}</div><div style="font-size:.85rem;color:var(--text-dim);line-height:1.6;margin-bottom:8px;">${p.d}</div><span style="font-family:'Cinzel',serif;font-size:.58rem;letter-spacing:.08em;padding:2px 8px;border-radius:2px;border:1px solid rgba(42,175,170,.3);color:var(--teal);">${p.tag}</span></div>`).join('');
  }

  // Initialize Three.js Mannequin
  initThreeJsMannequin();
}

function initThreeJsMannequin() {
  const container = document.getElementById('eft-3d-viewport');
  if (!container) return;

  const width = container.clientWidth || 300;
  const height = container.clientHeight || 500;

  // Scene
  eftScene = new THREE.Scene();

  // Camera
  eftCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  eftCamera.position.set(0, 0, 3.2);

  // Renderer
  eftRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  eftRenderer.setSize(width, height);
  eftRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(eftRenderer.domElement);

  // Controls
  eftControls = new THREE.OrbitControls(eftCamera, eftRenderer.domElement);
  eftControls.enableDamping = true;
  eftControls.dampingFactor = 0.05;
  eftControls.minDistance = 1.5;
  eftControls.maxDistance = 6.0;
  eftControls.target.set(0, -0.15, 0);

  // Lights
  const ambientLight = new THREE.AmbientLight(0x221a48, 1.8);
  eftScene.add(ambientLight);

  const dirLight1 = new THREE.DirectionalLight(0xffeedd, 1.2);
  dirLight1.position.set(5, 5, 5);
  eftScene.add(dirLight1);

  const dirLight2 = new THREE.DirectionalLight(0x7b4fa6, 0.8);
  dirLight2.position.set(-5, 3, -5);
  eftScene.add(dirLight2);

  const pointLight = new THREE.PointLight(0x3abfb0, 1.5, 4.0);
  pointLight.position.set(0, 0.5, 1.5);
  eftScene.add(pointLight);

  // Mannequin Group
  eftMannequin = new THREE.Group();

  // Translucent Hologram styling materials
  const bodyMat = new THREE.MeshStandardMaterial({
    color: 0x17123a,
    roughness: 0.2,
    metalness: 0.2,
    transparent: true,
    opacity: 0.8,
    emissive: 0x090518,
    side: THREE.DoubleSide
  });

  const wireMat = new THREE.MeshBasicMaterial({
    color: 0x8a5cb5,
    wireframe: true,
    transparent: true,
    opacity: 0.15
  });

  // Helper function to add dual mesh segments
  function addSegment(geom, yPos, xPos = 0, zPos = 0, rotZ = 0, rotY = 0) {
    const mesh = new THREE.Mesh(geom, bodyMat);
    const wire = new THREE.Mesh(geom, wireMat);
    
    const segment = new THREE.Group();
    segment.add(mesh);
    segment.add(wire);
    segment.position.set(xPos, yPos, zPos);
    if (rotZ) segment.rotation.z = rotZ;
    if (rotY) segment.rotation.y = rotY;
    
    eftMannequin.add(segment);
  }

  // Torso
  addSegment(new THREE.CylinderGeometry(0.25, 0.2, 0.6, 16), 0.1);
  
  // Pelvis
  addSegment(new THREE.CylinderGeometry(0.2, 0.22, 0.28, 16), -0.34);
  
  // Neck
  addSegment(new THREE.CylinderGeometry(0.065, 0.08, 0.16, 16), 0.48);
  
  // Head
  addSegment(new THREE.SphereGeometry(0.16, 32, 32), 0.72);

  // Left Arm
  addSegment(new THREE.CylinderGeometry(0.045, 0.04, 0.44, 16), 0.14, -0.35, 0, -Math.PI / 10);
  addSegment(new THREE.CylinderGeometry(0.04, 0.035, 0.4, 16), -0.22, -0.44, 0, -Math.PI / 25);
  addSegment(new THREE.SphereGeometry(0.038, 16, 16), -0.46, -0.48, 0);

  // Right Arm
  addSegment(new THREE.CylinderGeometry(0.045, 0.04, 0.44, 16), 0.14, 0.35, 0, Math.PI / 10);
  addSegment(new THREE.CylinderGeometry(0.04, 0.035, 0.4, 16), -0.22, 0.44, 0, Math.PI / 25);
  addSegment(new THREE.SphereGeometry(0.038, 16, 16), -0.46, 0.48, 0);

  // Left Leg
  addSegment(new THREE.CylinderGeometry(0.095, 0.075, 0.52, 16), -0.66, -0.13, 0);
  addSegment(new THREE.CylinderGeometry(0.075, 0.05, 0.52, 16), -1.18, -0.13, 0);
  addSegment(new THREE.BoxGeometry(0.07, 0.05, 0.16), -1.45, -0.13, 0.04);

  // Right Leg
  addSegment(new THREE.CylinderGeometry(0.095, 0.075, 0.52, 16), -0.66, 0.13, 0);
  addSegment(new THREE.CylinderGeometry(0.075, 0.05, 0.52, 16), -1.18, 0.13, 0);
  addSegment(new THREE.BoxGeometry(0.07, 0.05, 0.16), -1.45, 0.13, 0.04);

  eftScene.add(eftMannequin);

  // Instantiating Hotspots
  eftHotspots = [];
  EFT_ZONES.forEach(zone => {
    zone.coords.forEach(coord => {
      const geom = new THREE.SphereGeometry(0.045, 16, 16);
      const mat = new THREE.MeshBasicMaterial({
        color: new THREE.Color(zone.color),
        transparent: true,
        opacity: 0.85
      });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(coord.x, coord.y, coord.z);
      mesh.userData = { zoneId: zone.id };
      
      eftMannequin.add(mesh);
      eftHotspots.push(mesh);
    });
  });

  // Setup Raycaster events
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  function onMouseMove(event) {
    const rect = eftRenderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, eftCamera);
    const intersects = raycaster.intersectObjects(eftHotspots);
    if (intersects.length > 0) {
      eftRenderer.domElement.style.cursor = 'pointer';
    } else {
      eftRenderer.domElement.style.cursor = 'default';
    }
  }

  function onMouseClick(event) {
    const rect = eftRenderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, eftCamera);
    const intersects = raycaster.intersectObjects(eftHotspots);
    if (intersects.length > 0) {
      const zoneId = intersects[0].object.userData.zoneId;
      eftSelectZone(zoneId);
    }
  }

  eftRenderer.domElement.addEventListener('mousemove', onMouseMove);
  eftRenderer.domElement.addEventListener('click', onMouseClick);

  // Animation render loop
  function animate(time) {
    eftAnimationFrameId = requestAnimationFrame(animate);
    
    if (eftIsRotating && eftControls.state === -1) {
      eftMannequin.rotation.y += 0.005;
    }

    // Pulse Hotspots
    const pulseFactor = 1.0 + Math.sin(time * 0.004) * 0.16;
    eftHotspots.forEach(mesh => {
      const zId = mesh.userData.zoneId;
      if (zId === eftSelectedZone) {
        mesh.scale.set(pulseFactor * 1.4, pulseFactor * 1.4, pulseFactor * 1.4);
        mesh.material.color.setHex(0xffd700);
        mesh.material.opacity = 0.95;
      } else {
        mesh.scale.set(pulseFactor, pulseFactor, pulseFactor);
        const zData = EFT_ZONES.find(z => z.id === zId);
        mesh.material.color.setStyle(zData.color);
        mesh.material.opacity = 0.7 + Math.sin(time * 0.004) * 0.12;
      }
    });

    eftControls.update();
    eftRenderer.render(eftScene, eftCamera);
  }

  animate(0);

  window.addEventListener('resize', onWindowResize);
  function onWindowResize() {
    if (!container || !eftRenderer || !eftCamera) return;
    const w = container.clientWidth;
    const h = container.clientHeight;
    eftCamera.aspect = w / h;
    eftCamera.updateProjectionMatrix();
    eftRenderer.setSize(w, h);
  }
}

function eftSelectZone(zoneId) {
  eftSelectedZone = zoneId;
  const zone = EFT_ZONES.find(z => z.id === zoneId);
  if (!zone) return;

  document.querySelectorAll('#eft-quick-nav-points button').forEach(btn => {
    const isMatched = btn.dataset.id === zoneId;
    btn.classList.toggle('active', isMatched);
    if (isMatched) {
      btn.style.background = 'rgba(42,175,170,.25)';
      btn.style.borderColor = 'var(--teal)';
      btn.style.color = 'var(--teal)';
      btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    } else {
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
    }
  });

  document.getElementById('eft-details-empty').style.display = 'none';
  document.getElementById('eft-details-content').style.display = 'flex';

  document.getElementById('eft-detail-name').textContent = zone.name;
  document.getElementById('eft-detail-meridian').textContent = zone.meridian + ' Meridian';
  document.getElementById('eft-detail-zodiac').textContent = zone.zodiac;
  document.getElementById('eft-detail-house').textContent = zone.house + ' House';
  document.getElementById('eft-detail-emotion').textContent = zone.emotion;
  document.getElementById('eft-detail-instruction').textContent = zone.instruction;

  const issue = document.getElementById('eft-issue')?.value?.trim();
  const oracleText = document.getElementById('eft-oracle-text');
  if (issue) {
    oracleText.innerHTML = `Ready to analyze somatic holdings. Ask the Oracle for insights on why <strong>"${issue}"</strong> is stored in the ${zone.name} zone.`;
  } else {
    oracleText.textContent = `Identify somatic blockage patterns: Ask the Oracle what emotional theme lives in the ${zone.name} zone (${zone.emotion}).`;
  }

  const oracleBtn = document.getElementById('eft-oracle-btn');
  oracleBtn.disabled = false;
  oracleBtn.textContent = '☽ Ask Oracle About This Zone';

  eftGeneratePhrase();

  if (eftActive) {
    const idx = EFT_ZONES.findIndex(z => z.id === zoneId);
    if (idx !== -1 && idx !== eftStep) {
      eftStep = idx;
      eftActivateStep(idx);
    }
  }
}

function eftSetView(view) {
  if (!eftCamera || !eftControls || !eftMannequin) return;
  eftIsRotating = false;
  const btn = document.getElementById('eft-rotate-btn');
  if (btn) {
    btn.textContent = 'AUTO-ROTATE: OFF';
    btn.style.color = 'var(--text-dim)';
    btn.style.borderColor = 'var(--border)';
  }

  if (view === 'front') {
    eftCamera.position.set(0, 0, 3.2);
    eftControls.target.set(0, -0.15, 0);
    eftMannequin.rotation.set(0, 0, 0);
  } else if (view === 'back') {
    eftCamera.position.set(0, 0, -3.2);
    eftControls.target.set(0, -0.15, 0);
    eftMannequin.rotation.set(0, Math.PI, 0);
  } else if (view === 'reset') {
    eftCamera.position.set(0, 0, 3.2);
    eftControls.target.set(0, -0.15, 0);
    eftMannequin.rotation.set(0, 0, 0);
    eftControls.reset();
  }
  eftControls.update();
}

function eftToggleRotate() {
  eftIsRotating = !eftIsRotating;
  const btn = document.getElementById('eft-rotate-btn');
  if (btn) {
    if (eftIsRotating) {
      btn.textContent = 'AUTO-ROTATE: ON';
      btn.style.color = 'var(--teal)';
      btn.style.borderColor = 'var(--teal)';
    } else {
      btn.textContent = 'AUTO-ROTATE: OFF';
      btn.style.color = 'var(--text-dim)';
      btn.style.borderColor = 'var(--border)';
    }
  }
}

function switchEftTab(t){
  ['session','meridians','matrix','qigong'].forEach(x=>{
    const el=document.getElementById('eft-panel-'+x);
    if(el)el.style.display=x===t?'block':'none';
    const b=document.getElementById('eft-tab-'+x);
    if(b){
      b.style.background='';
      b.style.borderColor='';
      b.style.color='';
    }
  });
  const ab=document.getElementById('eft-tab-'+t);
  if(ab){
    ab.style.background='rgba(42,175,170,.1)';
    ab.style.borderColor='var(--teal)';
    ab.style.color='var(--teal)';
  }
}

function eftGeneratePhrase(){
  const issue=document.getElementById('eft-issue')?.value?.trim();
  if(!issue) return;
  eftIssue=issue;
  eftReminder='this '+issue.split(' ').slice(0,5).join(' ').toLowerCase();
  
  const selectedZoneData = EFT_ZONES.find(z => z.id === eftSelectedZone);
  const zoneContext = selectedZoneData ? ` held in my ${selectedZoneData.name} (${selectedZoneData.meridian})` : '';
  
  const phrases=[
    'Even though ' + issue + zoneContext + ', I deeply and completely accept myself.',
    'Even though I feel ' + issue + zoneContext + ', I choose to release this and be safe.',
    'Even though ' + issue + zoneContext + ', I honor how my body is talking to me.'
  ];
  
  const el=document.getElementById('eft-setup-phrase');
  if(el) el.textContent=phrases[Math.floor(Math.random()*phrases.length)];
}

function eftStartSession(){
  const issue=document.getElementById('eft-issue')?.value?.trim();
  if(!issue){
    toast('Enter your issue first');
    return;
  }
  eftIssue=issue;
  eftActive=true;
  eftDone.clear();
  eftStep=0;
  
  document.getElementById('eft-prev').disabled=false;
  document.getElementById('eft-prev').style.opacity='1';
  document.getElementById('eft-next').disabled=false;
  document.getElementById('eft-reset').style.display='inline-block';
  document.getElementById('eft-start-session-btn').textContent = '◎ Active Session';
  
  eftActivateStep(0);
}

function eftActivateStep(i){
  eftStep=i;
  const zone = EFT_ZONES[i];
  if (!zone) return;
  
  eftSelectedZone = zone.id;

  document.getElementById('eft-details-empty').style.display = 'none';
  document.getElementById('eft-details-content').style.display = 'flex';
  document.getElementById('eft-detail-name').textContent = zone.name;
  document.getElementById('eft-detail-meridian').textContent = zone.meridian + ' Meridian';
  document.getElementById('eft-detail-zodiac').textContent = zone.zodiac;
  document.getElementById('eft-detail-house').textContent = zone.house + ' House';
  document.getElementById('eft-detail-emotion').textContent = zone.emotion;
  document.getElementById('eft-detail-instruction').textContent = zone.instruction;

  document.querySelectorAll('#eft-quick-nav-points button').forEach(btn => {
    const isMatched = btn.dataset.id === zone.id;
    btn.classList.toggle('active', isMatched);
    if (isMatched) {
      btn.style.background = 'rgba(42,175,170,.25)';
      btn.style.borderColor = 'var(--teal)';
      btn.style.color = 'var(--teal)';
      btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    } else {
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
    }
  });

  if (eftMannequin && eftControls && eftCamera) {
    eftIsRotating = false;
    const rotateBtn = document.getElementById('eft-rotate-btn');
    if (rotateBtn) {
      rotateBtn.textContent = 'AUTO-ROTATE: OFF';
      rotateBtn.style.color = 'var(--text-dim)';
      rotateBtn.style.borderColor = 'var(--border)';
    }

    let rotY = 0;
    if (zone.id === 'feet' || zone.id === 'knees') {
      rotY = 0;
    } else if (zone.id === 'left_hand') {
      rotY = Math.PI / 4;
    } else if (zone.id === 'right_hand') {
      rotY = -Math.PI / 4;
    }
    
    eftMannequin.rotation.y = rotY;
    
    let targetY = 0;
    if (zone.coords.length > 0) {
      targetY = zone.coords[0].y;
    }
    eftControls.target.set(0, targetY - 0.1, 0);
    eftControls.update();
  }

  eftGeneratePhrase();

  const pct=Math.round((eftDone.size/EFT_ZONES.length)*100);
  const prog=document.getElementById('eft-progress');
  if(prog) prog.style.width=pct+'%';
  const cnt=document.getElementById('eft-step-count');
  if(cnt) cnt.textContent=eftDone.size+' / '+EFT_ZONES.length;
}

function eftNext(){
  if(!eftActive) return;
  eftDone.add(eftStep);
  if(eftStep<EFT_ZONES.length-1){
    eftActivateStep(eftStep+1);
  }else{
    const prog=document.getElementById('eft-progress');
    if(prog) prog.style.width='100%';
    const cnt=document.getElementById('eft-step-count');
    if(cnt) cnt.textContent=EFT_ZONES.length+' / '+EFT_ZONES.length+' — COMPLETE';
    toast('Round complete. Check your SUD and begin another round if needed.');
  }
}

function eftPrev(){
  if(!eftActive||eftStep<=0) return;
  eftActivateStep(eftStep-1);
}

function eftReset(){
  eftActive=false;
  eftStep=-1;
  eftDone.clear();
  eftSelectedZone = null;
  
  document.getElementById('eft-details-empty').style.display = 'block';
  document.getElementById('eft-details-content').style.display = 'none';

  document.querySelectorAll('#eft-quick-nav-points button').forEach(btn => {
    btn.classList.remove('active');
    btn.style.background = '';
    btn.style.borderColor = '';
    btn.style.color = '';
  });

  const prog=document.getElementById('eft-progress');
  if(prog) prog.style.width='0%';
  const cnt=document.getElementById('eft-step-count');
  if(cnt) cnt.textContent='0 / '+EFT_ZONES.length;
  
  const prev=document.getElementById('eft-prev');
  if(prev){
    prev.disabled=true;
    prev.style.opacity='.4';
  }
  const nxt=document.getElementById('eft-next');
  if(nxt) nxt.disabled=true;
  
  const rst=document.getElementById('eft-reset');
  if(rst) rst.style.display='none';

  document.getElementById('eft-start-session-btn').textContent = '◎ Begin Session';

  eftSetView('reset');
  eftIsRotating = true;
  const rotateBtn = document.getElementById('eft-rotate-btn');
  if (rotateBtn) {
    rotateBtn.textContent = 'AUTO-ROTATE: ON';
    rotateBtn.style.color = 'var(--teal)';
    rotateBtn.style.borderColor = 'var(--teal)';
  }
}

async function eftAskOracle(){
  const zone = EFT_ZONES.find(z => z.id === eftSelectedZone);
  if(!zone){
    toast('Select a somatic zone first');
    return;
  }
  const issue = document.getElementById('eft-issue')?.value?.trim() || 'General emotional holding pattern';
  const btn = document.getElementById('eft-oracle-btn');
  const text = document.getElementById('eft-oracle-text');
  
  btn.disabled = true;
  btn.textContent = 'Consulting...';
  text.textContent = 'Opening connection to somatic intelligence...';
  
  try{
    const r = await fetch('/api/oracle', {
      method: 'POST',
      headers: ah(),
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 500,
        system: 'You are a master somatic psychologist, astrologer, and EFT practitioner. You help translate body sensations and tension into emotional holdings. Explain why tension lives in specific areas, how it relates to planetary energies, and how to tap it out.',
        messages: [{
          role: 'user',
          content: `Analyze somatic holding pattern. Issue stated: "${issue}". Location: ${zone.name} zone (${zone.meridian} meridian, emotional domain: ${zone.emotion}, astrological correspondence: ${zone.zodiac} in the ${zone.house} house). Provide deep esoteric somatic guidance.`
        }]
      })
    });
    
    let d = {};
    try { d = await r.json(); } catch (_) {}
    if (r.ok && d.content?.[0]?.text) {
      text.innerHTML = d.content[0].text.replace(/\\n/g, '<br>');
      btn.textContent = '↻ Ask Again';
    } else {
      text.textContent = 'The somatic channel is unclear. Try again.';
      btn.textContent = '☽ Ask Oracle About This Zone';
    }
  } catch(e) {
    text.textContent = 'Connection to somatic oracle disrupted. Breathe and try again.';
    btn.textContent = '☽ Ask Oracle About This Zone';
  }
  btn.disabled = false;
}

async function gemAskOracle(){
  if(!gWord){
    toast('Calculate a word first');
    return;
  }
  const btn = document.getElementById('gem-oracle-btn');
  const text = document.getElementById('gem-oracle-text');
  btn.disabled = true;
  btn.textContent = 'Consulting...';
  text.textContent = 'Reading the numerical field...';
  
  const vals = Object.entries(GC).map(([n,c]) => {
    const r = c.fn(gWord);
    const {final,isMaster} = gReduce(r);
    return `${n}: ${r} → ${final}${isMaster ? ' (MASTER)' : ''}`;
  }).join(', ');
  
  try {
    const r = await fetch('/api/oracle', {
      method: 'POST',
      headers: ah(),
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 500,
        system: 'You are a master Gematria scholar. Give specific deep esoteric interpretation. Connect to Kabbalah, planetary correspondence, and practical meaning.',
        messages: [{
          role: 'user',
          content: `Word: "${gWord}". Values: ${vals}. Give deep esoteric interpretation of this word's numerical field.`
        }]
      })
    });
    
    let d = {};
    try { d = await r.json(); } catch (_) {}
    if (r.ok && d.content?.[0]?.text) {
      text.innerHTML = d.content[0].text.replace(/\\n/g, '<br>');
      btn.textContent = '↻ Ask Again';
    } else {
      text.textContent = 'Numerical Oracle channel disrupted. Try again.';
      btn.textContent = '☽ Ask the Oracle';
    }
  } catch(e) {
    text.textContent = 'Connection disrupted.';
    btn.textContent = '☽ Ask the Oracle';
  }
  btn.disabled = false;
}

async function analyzeSong(){
  const song = document.getElementById('freq-song')?.value?.trim();
  if(!song){
    toast('Describe a song first');
    return;
  }
  const btn = document.getElementById('freq-song-btn');
  const text = document.getElementById('freq-song-result');
  btn.disabled = true;
  btn.textContent = 'Analyzing...';
  text.textContent = 'Reading the frequency field...';
  
  try {
    const r = await fetch('/api/oracle', {
      method: 'POST',
      headers: ah(),
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 400,
        system: 'You are an expert in music frequencies, Solfeggio tones, and how sound affects the human energy field. Analyze songs based on musical key, tempo, frequency range, and emotional resonance.',
        messages: [{
          role: 'user',
          content: `Analyze this song: "${song}". What frequency field is it operating in? Healing, activation, sedation, programming, elevation, or disruption? Give specific musical and energetic reasons.`
        }]
      })
    });
    
    let d = {};
    try { d = await r.json(); } catch (_) {}
    if (r.ok && d.content?.[0]?.text) {
      text.innerHTML = d.content[0].text.replace(/\\n/g, '<br>');
      btn.textContent = '↻ Analyze Again';
    } else {
      text.textContent = 'Song Analysis channel disrupted. Try again.';
      btn.textContent = '☽ Analyze This Song';
    }
  } catch(e) {
    text.textContent = 'Connection disrupted.';
    btn.disabled = false;
    btn.textContent = '☽ Analyze This Song';
  }
  btn.disabled = false;
}"""

# Replace in content
replaced_content = content[:start_idx] + NEW_JS + content[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(replaced_content)

print("SUCCESS: Javascript code updated programmatically!")
