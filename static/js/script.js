/* =========================================================
   DATA LAYER (mock / demo data — clearly labelled)
   Everything here is placeholder data for the SIH prototype.
   Replace via services/*.js once backend APIs are available.
   ========================================================= */
const NER_STATES = ["Assam","Arunachal Pradesh","Meghalaya","Manipur","Mizoram","Nagaland","Tripura","Sikkim"];

const DATA = {
  kpis: [
    {label:"Routes monitored", val:"186", icon:"route", delta:"+4 this week", tone:"up"},
    {label:"Active vehicles", val:"342", icon:"truck", delta:"+18 today", tone:"up"},
    {label:"Deliveries in transit", val:"97", icon:"box", delta:"12 delayed", tone:"warn"},
    {label:"Critical alerts", val:"5", icon:"alert", delta:"2 new", tone:"down"},
    {label:"High-risk corridors", val:"11", icon:"warn", delta:"stable", tone:"warn"},
    {label:"Accessible districts", val:"71 / 78", icon:"check", delta:"91% open", tone:"up"},
  ],
  places: ["Guwahati","Shillong","Itanagar","Gangtok","Kohima","Imphal","Aizawl","Agartala","Tezpur","Nagaon","Dimapur","Silchar","Tawang","Along","Ziro"],
  highways: ["NH-27","NH-10","NH-6","NH-2","NH-37","NH-40","NH-702"],
  routeAlternates: [
    {name:"Route A — Recommended", risk:"green", distance:"312 km", time:"7h 40m", delay:"Minimal"},
    {name:"Route B — Moderate risk", risk:"amber", distance:"296 km", time:"7h 05m", delay:"~45 min possible"},
    {name:"Route C — High risk", risk:"red", distance:"340 km", time:"9h 20m", delay:"2h+ likely, landslide zone"},
  ],
  accessibility: [
    {road:"NH-27, Nagaon–Tezpur", district:"Nagaon, Assam", status:"OPEN", risk:"green", updated:"12 min ago", restore:"—"},
    {road:"NH-10, Gangtok Link", district:"East Sikkim", status:"BLOCKED", risk:"red", updated:"38 min ago", restore:"Est. 2 days"},
    {road:"NH-2, Imphal–Kohima", district:"Senapati, Manipur", status:"PARTIALLY ACCESSIBLE", risk:"amber", updated:"1h ago", restore:"Est. 6 hrs"},
    {road:"NH-40, Shillong–Silchar", district:"East Khasi Hills", status:"OPEN", risk:"green", updated:"25 min ago", restore:"—"},
    {road:"NH-702, Along–Ziro", district:"West Siang, Arunachal", status:"UNDER REPAIR", risk:"amber", updated:"3h ago", restore:"Est. 4 days"},
    {road:"NH-6, Aizawl Bypass", district:"Aizawl, Mizoram", status:"HIGH RISK", risk:"red", updated:"9 min ago", restore:"Monitoring"},
  ],
  vehicles: {
    "AS01AB1234": {type:"Refrigerated truck", cargo:"Medical Supplies", from:"Guwahati", to:"Tawang", status:"In Transit", speed:"41 km/h", eta:"4h 12m", driver:"On duty"},
    "SK02CD5678": {type:"Cargo van", cargo:"Food Supplies", from:"Gangtok", to:"Namchi", status:"In Transit", speed:"28 km/h", eta:"1h 05m", driver:"On duty"},
    "MN03EF9012": {type:"Flatbed truck", cargo:"Construction Materials", from:"Imphal", to:"Ukhrul", status:"Delayed", speed:"0 km/h", eta:"Recalculating", driver:"Halted — landslide"},
  },
  shipments: [
    {id:"SHP-2291", vehicle:"AS01AB1234", cargo:"Medical Supplies", from:"Guwahati", to:"Tawang", status:"In Transit", eta:"4h 12m", risk:"amber"},
    {id:"SHP-2292", vehicle:"SK02CD5678", cargo:"Food Supplies", from:"Gangtok", to:"Namchi", status:"In Transit", eta:"1h 05m", risk:"green"},
    {id:"SHP-2287", vehicle:"MN03EF9012", cargo:"Construction Materials", from:"Imphal", to:"Ukhrul", status:"At Risk", eta:"—", risk:"red"},
    {id:"SHP-2280", vehicle:"TR04GH3456", cargo:"Emergency Supplies", from:"Agartala", to:"Dharmanagar", status:"Delivered", eta:"Delivered", risk:"green"},
    {id:"SHP-2276", vehicle:"NL05IJ7890", cargo:"Agricultural Produce", from:"Dimapur", to:"Kohima", status:"Delayed", eta:"6h 40m", risk:"amber"},
  ],
  weather: [
    {state:"Assam", rain:"Moderate", temp:"27°C", flood:"Moderate", landslide:"Low", risk:"amber"},
    {state:"Meghalaya", rain:"Heavy", temp:"21°C", flood:"High", landslide:"High", risk:"red"},
    {state:"Arunachal Pradesh", rain:"Light", temp:"18°C", flood:"Low", landslide:"Moderate", risk:"amber"},
    {state:"Nagaland", rain:"Light", temp:"23°C", flood:"Low", landslide:"Low", risk:"green"},
    {state:"Manipur", rain:"Moderate", temp:"24°C", flood:"Moderate", landslide:"Moderate", risk:"amber"},
    {state:"Mizoram", rain:"Heavy", temp:"22°C", flood:"Moderate", landslide:"High", risk:"red"},
    {state:"Tripura", rain:"Light", temp:"29°C", flood:"Low", landslide:"Low", risk:"green"},
    {state:"Sikkim", rain:"Heavy", temp:"14°C", flood:"High", landslide:"High", risk:"red"},
  ],
  alerts: [
    {sev:"critical", title:"Landslide reported near NH-10", loc:"East Sikkim", time:"9 min ago", desc:"Route blocked near Gangtok link. Alternate via NH-10A advised.", action:"Use alternate route"},
    {sev:"critical", title:"Flash flood warning issued", loc:"East Khasi Hills, Meghalaya", time:"22 min ago", desc:"River levels rising near Shillong–Silchar corridor.", action:"Avoid low-lying stretches"},
    {sev:"warning", title:"Bridge inspection in progress", loc:"Senapati, Manipur", time:"1h ago", desc:"Single-lane movement on NH-2 near Mao.", action:"Expect delays up to 45 min"},
    {sev:"warning", title:"Heavy rainfall forecast", loc:"Aizawl, Mizoram", time:"2h ago", desc:"IMD forecasts sustained heavy rainfall over 48 hours.", action:"Reschedule non-essential trips"},
    {sev:"info", title:"Road resurfacing completed", loc:"Dimapur, Nagaland", time:"5h ago", desc:"NH-29 resurfacing near Dimapur completed ahead of schedule.", action:"No action needed"},
  ],
  aiInsights: [
    {tag:"ROUTE PREDICTION", text:"High probability of disruption on the Shillong–Silchar corridor due to sustained heavy rainfall over the next 12 hours."},
    {tag:"DISRUPTION PREDICTION", text:"Medical supply delivery to Ukhrul district may experience an approximate 3-hour delay from the current landslide closure."},
    {tag:"SUPPLY PREDICTION", text:"Medicine stock in East Sikkim projected to fall below safety threshold within 36 hours if NH-10 remains closed."},
    {tag:"RISK ANALYSIS", text:"Alternative routing through Route B reduces exposure to the flagged landslide zone by an estimated 68%."},
  ],
  notifications: [
    {type:"Critical Alert", text:"Landslide blocking NH-10 near Gangtok.", time:"9 min ago", unread:true},
    {type:"Route Update", text:"Route A re-opened between Nagaon and Tezpur.", time:"31 min ago", unread:true},
    {type:"Vehicle Update", text:"Vehicle AS01AB1234 crossed the Tezpur checkpoint.", time:"1h ago", unread:false},
    {type:"Delivery Update", text:"Shipment SHP-2280 marked as delivered.", time:"3h ago", unread:false},
    {type:"Weather Warning", text:"Heavy rainfall forecast for Mizoram over next 48 hours.", time:"4h ago", unread:false},
    {type:"System Notification", text:"Scheduled maintenance completed successfully.", time:"1d ago", unread:false},
  ],
};

/* =========================================================
   ICONS (inline, stroke-based, theme-colored)
   ========================================================= */
const ICONS = {
  overview:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>',
  route:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.2 17.5C13 12 11 6 18 7.3"/></svg>',
  accessibility:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6l8-4z"/></svg>',
  vehicles:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 13l1.5-5A2 2 0 016.4 6.5h6.2A2 2 0 0114.6 8l1.4 5"/><path d="M3 13h18v4a1 1 0 01-1 1h-1"/><path d="M5 18a1 1 0 01-1-1v-4"/><circle cx="7.5" cy="18" r="1.6"/><circle cx="16.5" cy="18" r="1.6"/></svg>',
  logistics:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>',
  weather:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19a4.5 4.5 0 000-9 6 6 0 00-11.4 1.8A4 4 0 007 19h10.5z"/></svg>',
  alerts:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.3 3.9L2.5 17a1.6 1.6 0 001.4 2.4h16.2a1.6 1.6 0 001.4-2.4L13.7 3.9a1.6 1.6 0 00-2.8 0z"/><path d="M12 9v4"/><path d="M12 16.5h.01"/></svg>',
  emergency:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6l8-4z"/><path d="M12 8v5"/><path d="M12 16.2h.01"/></svg>',
  field:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s7-6.1 7-11.5A7 7 0 005 9.5C5 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.4"/></svg>',
  supply:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 00-1-1.7l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.7l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><path d="M3.3 7l8.7 5 8.7-5"/><path d="M12 22V12"/></svg>',
  ai:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="7" width="16" height="12" rx="2.5"/><path d="M12 7V3"/><circle cx="9" cy="13" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="13" r="1.2" fill="currentColor" stroke="none"/><path d="M9 17h6"/></svg>',
  chatbot:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.4 8.4 0 01-8.9 8.4 8.9 8.9 0 01-3.6-.8L3 21l1.9-5.5a8.4 8.4 0 01-.9-3.9A8.4 8.4 0 0112.6 3a8.5 8.5 0 018.4 8.5z"/></svg>',
  notif:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 01-3.4 0"/></svg>',
  reports:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19V5"/><path d="M4 19h16"/><rect x="7" y="12" width="2.5" height="7"/><rect x="12" y="8" width="2.5" height="11"/><rect x="17" y="4" width="2.5" height="15"/></svg>',
  settings:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.9-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1-1.6 1.7 1.7 0 00-1.9.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.9 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1 1.7 1.7 0 00-.3-1.9l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.9.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.9-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.9V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z"/></svg>',
  truck:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 13l1.5-5A2 2 0 016.4 6.5h6.2A2 2 0 0114.6 8l1.4 5"/><path d="M3 13h18v4a1 1 0 01-1 1h-1"/><circle cx="7.5" cy="18" r="1.6"/><circle cx="16.5" cy="18" r="1.6"/></svg>',
  box:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 00-1-1.7l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.7l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><path d="M3.3 7l8.7 5 8.7-5"/></svg>',
  warn:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.3 3.9L2.5 17a1.6 1.6 0 001.4 2.4h16.2a1.6 1.6 0 001.4-2.4L13.7 3.9a1.6 1.6 0 00-2.8 0z"/></svg>',
  check:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.3l2.4 2.4 4.6-5"/></svg>',
};

const NAV = [
  {key:"overview", label:"Overview"},
  {key:"routes", label:"Route Intelligence"},
  {key:"accessibility", label:"Accessibility Monitor"},
  {key:"vehicles", label:"Vehicle Tracking"},
  {key:"logistics", label:"Logistics & Deliveries"},
  {key:"weather", label:"Weather Intelligence"},
  {key:"alerts", label:"Alerts & Incidents"},
  {key:"emergency", label:"Emergency Routes"},
  {key:"field-reports", label:"Field Reports"},
  {key:"supply-chain", label:"Supply Chain"},
  {key:"ai-insights", label:"AI Insights"},
  {key:"chatbot", label:"Chatbot"},
  {key:"notifications", label:"Notifications"},
  {key:"reports", label:"Reports & Analytics"},
  {key:"settings", label:"Settings"},
];
const NAV_ICON_KEY = {overview:"overview", routes:"route", accessibility:"accessibility", vehicles:"vehicles", logistics:"logistics", weather:"weather", alerts:"alerts", emergency:"emergency", "field-reports":"field", "supply-chain":"supply", "ai-insights":"ai", chatbot:"chatbot", notifications:"notif", reports:"reports", settings:"settings"};

/* =========================================================
   I18N — minimal EN/HI dictionary for key chrome strings
   ========================================================= */
const I18N = {
  en:{ overview:"Overview", routes:"Route Intelligence", accessibility:"Accessibility Monitor", vehicles:"Vehicle Tracking", logistics:"Logistics & Deliveries", weather:"Weather Intelligence", alerts:"Alerts & Incidents", emergency:"Emergency Routes", "field-reports":"Field Reports", "supply-chain":"Supply Chain", "ai-insights":"AI Insights", chatbot:"Chatbot", notifications:"Notifications", reports:"Reports & Analytics", settings:"Settings",
    dashTitle:"NER Logistics Intelligence Dashboard", searchPh:"Search routes, vehicles, districts…", getStarted:"Get Started", login:"Log in" },
  hi:{ overview:"अवलोकन", routes:"मार्ग बुद्धिमत्ता", accessibility:"सुगम्यता मॉनिटर", vehicles:"वाहन ट्रैकिंग", logistics:"लॉजिस्टिक्स और डिलीवरी", weather:"मौसम बुद्धिमत्ता", alerts:"अलर्ट और घटनाएँ", emergency:"आपातकालीन मार्ग", "field-reports":"फील्ड रिपोर्ट", "supply-chain":"आपूर्ति श्रृंखला", "ai-insights":"एआई अंतर्दृष्टि", chatbot:"चैटबॉट", notifications:"सूचनाएं", reports:"रिपोर्ट और विश्लेषण", settings:"सेटिंग्स",
    dashTitle:"पूर्वोत्तर लॉजिस्टिक्स बुद्धिमत्ता डैशबोर्ड", searchPh:"मार्ग, वाहन, जिला खोजें…", getStarted:"शुरू करें", login:"लॉग इन करें" },
};

/* =========================================================
   STATE
   ========================================================= */
const STATE = { lang:"en", sidebarCollapsed:false, user:null, settingsTab:"profile", chatHistory:[], notifs: JSON.parse(JSON.stringify(DATA.notifications)) };

/* =========================================================
   ROUTER
   ========================================================= */
function go(route){ location.hash = "#/" + route; }
window.addEventListener("hashchange", render);
window.addEventListener("DOMContentLoaded", () => { mountStaticBits(); if(!location.hash) location.hash = "#/landing"; render(); });

function render(){
  const hash = (location.hash || "#/landing").replace("#/","");
  const [top, sub] = hash.split("/");
  document.querySelectorAll(".view").forEach(v=>v.classList.remove("active"));
  if(top === "auth"){ document.getElementById("view-auth").classList.add("active"); return; }
  if(top === "app"){
    if(!STATE.user){ go("auth"); return; }
    document.getElementById("view-shell").classList.add("active");
    renderShellChrome();
    renderPage(sub || "overview");
    return;
  }
  document.getElementById("view-landing").classList.add("active");
}

/* =========================================================
   STATIC MOUNTS (logo instances, states strip, feature cards)
   ========================================================= */
function logoSVG(){ return document.getElementById("tpl-logo").innerHTML; }
function brandBlock(size){
  return `${logoSVG()}<div class="brand-text"><span class="p">PRAVAH</span><span class="n">NER CONNECT</span></div>`;
}
function mountStaticBits(){
  ["brandLanding","brandAuth","brandSidebar","brandFooter"].forEach(id=>{
    document.getElementById(id).innerHTML = brandBlock();
  });
  document.getElementById("statesStrip").innerHTML = NER_STATES.map(s=>`<div class="state-chip"><span class="dot"></span>${s}</div>`).join("");
  const features = [
    {ic:ICONS.route, t:"Route Intelligence", d:"AI-ranked routes weighted by accessibility, weather and live incidents."},
    {ic:ICONS.accessibility, t:"Accessibility Monitor", d:"Live status of every tracked road and bridge across the region."},
    {ic:ICONS.vehicles, t:"Vehicle Tracking", d:"Follow cargo movement corridor by corridor, checkpoint by checkpoint."},
    {ic:ICONS.weather, t:"Weather Intelligence", d:"Rainfall, flood and landslide risk by district, updated continuously."},
    {ic:ICONS.emergency, t:"Emergency Mode", d:"One tap to surface medical, relief and evacuation corridors."},
    {ic:ICONS.field, t:"Field Reporting", d:"Officers file ground reports that sync automatically once online."},
  ];
  document.getElementById("featureCards").innerHTML = features.map(f=>`<div class="card"><div class="ic">${f.ic}</div><h3>${f.t}</h3><p>${f.d}</p></div>`).join("");
}

/* =========================================================
   AUTH HANDLERS
   ========================================================= */
function setAuthTab(tab){
  document.getElementById("tabLogin").classList.toggle("active", tab==="login");
  document.getElementById("tabSignup").classList.toggle("active", tab==="signup");
  document.getElementById("formLogin").style.display = tab==="login" ? "block":"none";
  document.getElementById("formSignup").style.display = tab==="signup" ? "block":"none";
}
function handleLogin(e){
  e.preventDefault();
  STATE.user = { name:"A. Sharma", role:"Government Official", initials:"AS" };
  finishLogin();
  return false;
}
function handleDemoLogin(){
  STATE.user = { name:"Demo User", role:"Demo Account", initials:"DU" };
  finishLogin();
}
function finishLogin(){
  document.getElementById("userName").textContent = STATE.user.name;
  document.getElementById("userAvatar").textContent = STATE.user.initials;
  go("app/overview");
}
function handleLogout(){
  STATE.user = null;
  go("landing");
}

/* =========================================================
   SHELL CHROME (sidebar nav + labels)
   ========================================================= */
function renderShellChrome(){
  const t = I18N[STATE.lang];
  document.getElementById("navGroup").innerHTML = NAV.map(n => {
    const active = location.hash.includes("app/"+n.key) || (n.key==="overview" && location.hash.endsWith("app"));
    return `<a href="#/app/${n.key}" class="nav-item ${active?"active":""}" title="${n.label}">
      ${ICONS[NAV_ICON_KEY[n.key]]}<span class="nav-label">${t[n.key]||n.label}</span>
    </a>`;
  }).join("");
  document.getElementById("langSelect").value = STATE.lang;
}
function toggleSidebar(){
  STATE.sidebarCollapsed = !STATE.sidebarCollapsed;
  document.getElementById("shell").classList.toggle("collapsed", STATE.sidebarCollapsed);
  document.getElementById("sidebarToggleLabel").textContent = STATE.sidebarCollapsed ? "Expand" : "Collapse";
}
function toggleMobileNav(){ document.getElementById("shell").classList.toggle("mobile-open"); }
function setLang(v){ STATE.lang = v; renderShellChrome(); render(); }

/* =========================================================
   PAGE ROUTER (renders into #pageContent)
   ========================================================= */
function renderPage(key){
  const map = {
    overview: pageOverview, routes: pageRoutes, accessibility: pageAccessibility, vehicles: pageVehicles,
    logistics: pageLogistics, weather: pageWeather, alerts: pageAlerts, emergency: pageEmergency,
    "field-reports": pageFieldReports, "supply-chain": pageSupplyChain, "ai-insights": pageAIInsights,
    chatbot: pageChatbot, notifications: pageNotifications, reports: pageReports, settings: pageSettings,
  };
  const fn = map[key] || pageOverview;
  document.getElementById("pageContent").innerHTML = fn();
  afterRender(key);
}

function pageHead(title, sub){
  return `<div class="page-head"><div><h1>${title}</h1><div class="sub">${sub}</div></div><span class="demo-tag">DEMO DATA</span></div>`;
}
function gisPlaceholder(label, height){
  return `<div class="gis-map" style="min-height:${height||340}px;">
    <svg viewBox="0 0 500 320"><g opacity=".8" stroke="#5EEAD4" stroke-width="1.5" fill="none">
      <path d="M10 260 C 90 200,150 290,210 220 S 320 140,480 90"/>
      <path d="M40 40 C 120 100,200 20,280 70 S 400 160,470 260" stroke="#38BDF8" stroke-dasharray="3 7"/>
    </g>
    <circle cx="10" cy="260" r="5" fill="#38BDF8"/><circle cx="210" cy="220" r="5" fill="#5EEAD4"/>
    <circle cx="480" cy="90" r="6" fill="#F59E0B"/><circle cx="320" cy="140" r="5" fill="#DC2626"/>
    </svg>
    <div class="label"><b>GIS MAP — BACKEND INTEGRATION AREA</b><span>${label}</span></div>
    <div class="gis-legend">
      <span class="item"><span class="sw" style="background:#16A34A"></span>Safe route</span>
      <span class="item"><span class="sw" style="background:#D97706"></span>Moderate risk</span>
      <span class="item"><span class="sw" style="background:#DC2626"></span>Critical</span>
    </div>
  </div>`;
}
function riskBadge(risk){
  const map = {green:["Safe","green"], amber:["Moderate","amber"], red:["Critical","red"]};
  const [label,cls] = map[risk] || ["—","grey"];
  return `<span class="badge ${cls}">${label}</span>`;
}

/* ---------- OVERVIEW ---------- */
function pageOverview(){
  const t = I18N[STATE.lang];
  return `
  ${pageHead(t.dashTitle, "Live command-centre view across all monitored NER corridors")}
  <div class="kpi-grid">
    ${DATA.kpis.map(k=>`
      <div class="kpi">
        <div class="top"><div class="ic">${ICONS[k.icon]}</div><span class="delta ${k.tone}">${k.delta}</span></div>
        <div class="val">${k.val}</div><div class="lbl">${k.label}</div>
      </div>`).join("")}
  </div>
  <div class="two-col">
    <div class="stack">
      <div class="panel">
        <div class="panel-head"><h3>Regional accessibility map</h3><span class="badge blue">8 states</span></div>
        <div class="panel-body">${gisPlaceholder("Route lines, district markers and vehicle positions render here once GIS/GPS APIs are connected.", 360)}</div>
      </div>
      <div class="panel">
        <div class="panel-head"><h3>Incident trend — last 7 days</h3></div>
        <div class="panel-body"><canvas id="chartIncidents" height="110"></canvas></div>
      </div>
    </div>
    <div class="stack">
      <div class="panel">
        <div class="panel-head"><h3>Delivery status</h3></div>
        <div class="panel-body"><canvas id="chartDelivery" height="200"></canvas></div>
      </div>
      <div class="panel">
        <div class="panel-head"><h3>District connectivity</h3></div>
        <div class="panel-body"><canvas id="chartConnectivity" height="180"></canvas></div>
      </div>
    </div>
  </div>`;
}

/* ---------- ROUTE INTELLIGENCE ---------- */
function pageRoutes(){
  return `
  ${pageHead("Route Intelligence", "Find the safest, fastest corridor between two points")}
  <div class="two-col">
    <div class="stack">
      <div class="panel"><div class="panel-body">
        <div class="form-grid">
          <div class="field"><label>From location</label><input list="places" id="routeFrom" placeholder="e.g. Guwahati" value="Guwahati"></div>
          <div class="field"><label>To location</label><input list="places" id="routeTo" placeholder="e.g. Itanagar" value="Shillong"></div>
          <div class="field"><label>Transport type</label><select id="routeTransport"><option>Road — Truck</option><option>Road — Light vehicle</option><option>Road — Two-wheeler</option></select></div>
          <div class="field"><label>Cargo type</label><select id="routeCargo"><option>General</option><option>Medical Supplies</option><option>Food Supplies</option><option>Construction Materials</option><option>Emergency Supplies</option></select></div>
          <div class="field"><label>Vehicle type</label><select><option>Heavy truck</option><option>Mini truck</option><option>Van</option></select></div>
          <div class="field"><label>Priority</label><select id="routePriority"><option>Standard</option><option>High — time-critical</option><option>Emergency</option></select></div>
        </div>
        <button class="btn btn-primary" style="margin-top:6px;" onclick="findRoute()">Find Best Route</button>
        <datalist id="places">${DATA.places.map(p=>`<option value="${p}">`).join("")}</datalist>
      </div></div>
      <div id="routeResult"></div>
    </div>
    <div class="panel"><div class="panel-head"><h3>Corridor map</h3></div><div class="panel-body">${gisPlaceholder("Selected route and alternates will be plotted here.", 460)}</div></div>
  </div>`;
}
function findRoute(){
  const from = document.getElementById("routeFrom").value || "Guwahati";
  const to = document.getElementById("routeTo").value || "Shillong";
  const via = DATA.places[Math.floor(Math.random()*DATA.places.length)];
  document.getElementById("routeResult").innerHTML = `
  <div class="panel result-fade">
    <div class="panel-head"><h3>Recommended route</h3>${riskBadge("green")}</div>
    <div class="panel-body">
      <div style="font-weight:700;font-size:1.02rem;margin-bottom:14px;">${from} → ${via} → ${to}</div>
      <div class="kpi-grid" style="margin-bottom:16px;">
        <div class="kpi"><div class="lbl">Distance</div><div class="val" style="font-size:1.2rem;">${DATA.routeAlternates[0].distance}</div></div>
        <div class="kpi"><div class="lbl">Estimated time</div><div class="val" style="font-size:1.2rem;">${DATA.routeAlternates[0].time}</div></div>
        <div class="kpi"><div class="lbl">Current accessibility</div><div class="val" style="font-size:1.2rem;">Open</div></div>
        <div class="kpi"><div class="lbl">Expected delay</div><div class="val" style="font-size:1.2rem;">${DATA.routeAlternates[0].delay}</div></div>
      </div>
      <div class="insight-card" style="margin-bottom:18px;">
        <span class="tag">AI ROUTE RECOMMENDATION</span>
        Based on current accessibility, rainfall risk and reported incidents, <b>Route A</b> is recommended for this corridor.
      </div>
      <h4 style="margin-bottom:10px;font-size:.9rem;">Alternative routes</h4>
      <div class="table-wrap"><table><thead><tr><th>Route</th><th>Distance</th><th>Time</th><th>Delay</th><th>Risk</th></tr></thead><tbody>
        ${DATA.routeAlternates.map(r=>`<tr><td>${r.name}</td><td>${r.distance}</td><td>${r.time}</td><td>${r.delay}</td><td>${riskBadge(r.risk)}</td></tr>`).join("")}
      </tbody></table></div>
    </div>
  </div>`;
}

/* ---------- ACCESSIBILITY MONITOR ---------- */
function pageAccessibility(){
  const rows = DATA.accessibility;
  return `
  ${pageHead("Accessibility Monitor", "Live status of tracked roads and bridges")}
  <div class="filters">
    <select><option>All states</option>${NER_STATES.map(s=>`<option>${s}</option>`).join("")}</select>
    <select><option>All districts</option></select>
    <select><option>All statuses</option><option>OPEN</option><option>PARTIALLY ACCESSIBLE</option><option>BLOCKED</option><option>UNDER REPAIR</option><option>HIGH RISK</option></select>
    <select><option>All risk levels</option><option>Safe</option><option>Moderate</option><option>Critical</option></select>
    <input type="text" placeholder="Search road name…">
  </div>
  <div class="panel"><div class="table-wrap"><table>
    <thead><tr><th>Road</th><th>District</th><th>Status</th><th>Risk</th><th>Last updated</th><th>Expected restoration</th></tr></thead>
    <tbody>${rows.map(r=>`<tr><td>${r.road}</td><td>${r.district}</td><td><span class="badge ${r.risk==='green'?'green':r.risk==='amber'?'amber':'red'}">${r.status}</span></td><td>${riskBadge(r.risk)}</td><td>${r.updated}</td><td>${r.restore}</td></tr>`).join("")}</tbody>
  </table></div></div>
  <div style="margin-top:18px;">${gisPlaceholder("Road segment colour-coding renders here once GIS integration is connected.")}</div>`;
}

/* ---------- VEHICLE TRACKING ---------- */
function pageVehicles(){
  return `
  ${pageHead("Vehicle Tracking", "Enter a vehicle number to view its live movement")}
  <div class="panel"><div class="panel-body">
    <div class="field" style="max-width:320px;"><label>Vehicle number</label><input id="vehInput" placeholder="e.g. AS01AB1234" value="AS01AB1234"></div>
    <button class="btn btn-primary" onclick="trackVehicle()">Track Vehicle</button>
  </div></div>
  <div id="vehResult" style="margin-top:18px;"></div>`;
}
function trackVehicle(){
  const num = (document.getElementById("vehInput").value || "").toUpperCase().trim();
  const v = DATA.vehicles[num];
  const el = document.getElementById("vehResult");
  if(!v){
    el.innerHTML = `<div class="panel result-fade"><div class="empty-state">${ICONS.vehicles}<h3 style="margin-bottom:6px;">No vehicle found</h3><p>Try AS01AB1234, SK02CD5678 or MN03EF9012 for demo results.</p></div></div>`;
    return;
  }
  el.innerHTML = `
  <div class="two-col result-fade">
    <div class="panel"><div class="panel-head"><h3>${num}</h3><span class="badge ${v.status==='In Transit'?'blue':'amber'}">${v.status}</span></div>
      <div class="panel-body">
        <div class="kpi-grid">
          <div class="kpi"><div class="lbl">Vehicle type</div><div class="val" style="font-size:1.05rem;">${v.type}</div></div>
          <div class="kpi"><div class="lbl">Cargo</div><div class="val" style="font-size:1.05rem;">${v.cargo}</div></div>
          <div class="kpi"><div class="lbl">From</div><div class="val" style="font-size:1.05rem;">${v.from}</div></div>
          <div class="kpi"><div class="lbl">To</div><div class="val" style="font-size:1.05rem;">${v.to}</div></div>
          <div class="kpi"><div class="lbl">Speed</div><div class="val" style="font-size:1.05rem;">${v.speed}</div></div>
          <div class="kpi"><div class="lbl">ETA</div><div class="val" style="font-size:1.05rem;">${v.eta}</div></div>
        </div>
        <div style="margin-top:14px;font-size:.85rem;color:var(--ink-soft);">Driver status: <b style="color:var(--ink);">${v.driver}</b></div>
      </div>
    </div>
    <div class="panel"><div class="panel-head"><h3>GPS tracking map</h3></div><div class="panel-body">${gisPlaceholder("GPS TRACKING MAP — BACKEND INTEGRATION AREA", 300)}</div></div>
  </div>`;
}

/* ---------- LOGISTICS & DELIVERIES ---------- */
function pageLogistics(){
  const cats = ["Medical Supplies","Food Supplies","Agricultural Produce","Construction Materials","Emergency Supplies"];
  const statusCls = {"Delivered":"green","In Transit":"blue","Delayed":"amber","At Risk":"red"};
  return `
  ${pageHead("Logistics & Deliveries", "Track shipments by category and corridor")}
  <div class="grid-cards" style="margin-bottom:20px;">
    ${cats.map(c=>`<div class="card"><div class="ic">${ICONS.box}</div><h3>${c}</h3><p>${DATA.shipments.filter(s=>s.cargo===c).length} active shipment(s)</p></div>`).join("")}
  </div>
  <div class="filters">
    <select><option>All statuses</option><option>Delivered</option><option>In Transit</option><option>Delayed</option><option>At Risk</option></select>
    <select><option>All cargo types</option>${cats.map(c=>`<option>${c}</option>`).join("")}</select>
  </div>
  <div class="panel"><div class="table-wrap"><table>
    <thead><tr><th>Shipment ID</th><th>Vehicle</th><th>Cargo</th><th>Origin</th><th>Destination</th><th>Status</th><th>ETA</th><th>Risk</th></tr></thead>
    <tbody>${DATA.shipments.map(s=>`<tr><td style="font-family:var(--font-mono);font-size:.78rem;">${s.id}</td><td>${s.vehicle}</td><td>${s.cargo}</td><td>${s.from}</td><td>${s.to}</td><td><span class="badge ${statusCls[s.status]}">${s.status}</span></td><td>${s.eta}</td><td>${riskBadge(s.risk)}</td></tr>`).join("")}</tbody>
  </table></div></div>`;
}

/* ---------- WEATHER INTELLIGENCE ---------- */
function pageWeather(){
  const riskLabel = {green:"LOW", amber:"MODERATE", red:"HIGH"};
  return `
  ${pageHead("Weather Intelligence", "Rainfall, flood and landslide risk by state")}
  <div class="grid-cards" style="margin-bottom:20px;">
    ${DATA.weather.map(w=>`
      <div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
          <h3 style="margin:0;">${w.state}</h3>${riskBadge(w.risk)}
        </div>
        <div style="font-size:.83rem;color:var(--ink-soft);display:grid;gap:5px;">
          <div>Rainfall: <b style="color:var(--ink);">${w.rain}</b></div>
          <div>Temperature: <b style="color:var(--ink);">${w.temp}</b></div>
          <div>Flood risk: <b style="color:var(--ink);">${w.flood}</b></div>
          <div>Landslide risk: <b style="color:var(--ink);">${w.landslide}</b></div>
        </div>
        <div style="margin-top:10px;font-family:var(--font-mono);font-size:.68rem;color:var(--brand);">AI PREDICTION · ${riskLabel[w.risk]}</div>
      </div>`).join("")}
  </div>
  <div class="panel"><div class="panel-head"><h3>Weather API integration area</h3></div>
    <div class="panel-body" style="color:var(--ink-soft);font-size:.88rem;">
      This panel is reserved for live weather feeds (IMD / third-party weather APIs). Currently showing demo values only.
      <div style="margin-top:10px;font-family:var(--font-mono);font-size:.72rem;color:var(--brand);">// WEATHER API</div>
    </div>
  </div>`;
}

/* ---------- ALERTS & INCIDENTS ---------- */
function pageAlerts(){
  return `
  ${pageHead("Alerts & Incidents", "Real-time incident feed across the region")}
  <div class="filters">
    <button class="chip" style="background:var(--bg-deep);" onclick="filterAlerts('all')">All</button>
    <button class="chip" onclick="filterAlerts('critical')">Critical</button>
    <button class="chip" onclick="filterAlerts('warning')">Warning</button>
    <button class="chip" onclick="filterAlerts('info')">Information</button>
  </div>
  <div id="alertsList">${alertsListHTML(DATA.alerts)}</div>`;
}
function alertsListHTML(list){
  const sevBadge = {critical:"red", warning:"amber", info:"blue"};
  const sevLabel = {critical:"CRITICAL", warning:"WARNING", info:"INFO"};
  return list.map(a=>`
    <div class="alert-card ${a.sev}">
      <div class="sev"></div>
      <div style="flex:1;">
        <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;">
          <h4>${a.title}</h4><span class="badge ${sevBadge[a.sev]}">${sevLabel[a.sev]}</span>
        </div>
        <p style="font-size:.85rem;color:var(--ink-soft);">${a.desc}</p>
        <div class="meta"><span>📍 ${a.loc}</span><span>🕒 ${a.time}</span><span>➡ ${a.action}</span></div>
      </div>
    </div>`).join("") || `<div class="panel"><div class="empty-state">${ICONS.check}<h3>No incidents reported</h3></div></div>`;
}
function filterAlerts(sev){
  const list = sev==="all" ? DATA.alerts : DATA.alerts.filter(a=>a.sev===sev);
  document.getElementById("alertsList").innerHTML = alertsListHTML(list);
}

/* ---------- EMERGENCY ROUTES ---------- */
function pageEmergency(){
  return `
  ${pageHead("Emergency Accessibility Mode", "Fastest accessible corridors for critical response")}
  <div class="panel" style="margin-bottom:18px;background:linear-gradient(135deg,var(--brand-deeper),var(--brand-deep));color:#fff;border:none;">
    <div class="panel-body" style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
      <div>
        <h3 style="color:#fff;">Emergency mode is currently inactive</h3>
        <p style="color:#CFEFF3;font-size:.88rem;margin-top:4px;">Activating emergency mode prioritises medical and relief corridors across the dashboard. This is a demo simulation only.</p>
      </div>
      <button class="btn" id="emergencyBtn" style="background:#fff;color:var(--brand-deep);font-weight:700;" onclick="toggleEmergency()">Activate Emergency Mode</button>
    </div>
  </div>
  <div class="grid-cards" style="margin-bottom:18px;">
    <div class="card"><div class="ic">🚑</div><h3>Medical supply corridors</h3><p>3 active corridors reserved for medical logistics.</p></div>
    <div class="card"><div class="ic">📦</div><h3>Relief supply corridors</h3><p>5 corridors mapped to district relief centres.</p></div>
    <div class="card"><div class="ic">🧭</div><h3>Evacuation routes</h3><p>2 ranked evacuation alternates on standby.</p></div>
    <div class="card"><div class="ic">🛣</div><h3>Nearest accessible routes</h3><p>Auto-ranked by current road status.</p></div>
  </div>
  ${gisPlaceholder("Emergency route visualization renders here once GIS integration is connected.", 380)}`;
}
function toggleEmergency(){
  const btn = document.getElementById("emergencyBtn");
  const active = btn.textContent.includes("Deactivate");
  btn.textContent = active ? "Activate Emergency Mode" : "Deactivate Emergency Mode";
  btn.previousElementSibling && null;
  btn.parentElement.previousElementSibling; // no-op, keep simple
  btn.parentElement.parentElement.querySelector("h3").textContent = active ? "Emergency mode is currently inactive" : "🚨 Emergency mode is ACTIVE";
}

/* ---------- FIELD REPORTING ---------- */
function pageFieldReports(){
  return `
  ${pageHead("Field Reports", "Submit ground reports — syncs automatically once online")}
  <div class="two-col">
    <div class="panel"><div class="panel-body">
      <div class="form-grid">
        <div class="field"><label>Incident type</label><select><option>Landslide</option><option>Flood</option><option>Road blockage</option><option>Bridge damage</option><option>Vehicle breakdown</option><option>Other</option></select></div>
        <div class="field"><label>Severity</label><select><option>Low</option><option>Moderate</option><option>High</option><option>Critical</option></select></div>
        <div class="field"><label>State</label><select>${NER_STATES.map(s=>`<option>${s}</option>`).join("")}</select></div>
        <div class="field"><label>District</label><input placeholder="e.g. East Khasi Hills"></div>
        <div class="field" style="grid-column:1/-1;"><label>Location</label><input placeholder="Nearest landmark / road name"></div>
        <div class="field" style="grid-column:1/-1;"><label>Description</label><input placeholder="Describe what you're observing"></div>
        <div class="field"><label>Date</label><input type="date"></div>
        <div class="field"><label>Time</label><input type="time"></div>
      </div>
      <button class="btn btn-ghost btn-sm" style="margin:10px 0;" onclick="useLocation()">📍 Use Current Location</button>
      <div id="gpsCoords" style="font-family:var(--font-mono);font-size:.78rem;color:var(--ink-soft);margin-bottom:14px;"></div>
      <div class="upload-box">Drop a photo or document here, or click to upload<br><span style="font-size:.72rem;">(UI placeholder — no file is actually uploaded)</span></div>
      <button class="btn btn-primary" style="margin-top:16px;" onclick="submitFieldReport()">Submit Field Report</button>
      <div id="syncStatus"></div>
    </div></div>
    <div class="panel"><div class="panel-head"><h3>Recent field reports</h3></div>
      <div class="panel-body">
        <div class="notif-item"><div class="notif-dot" style="background:var(--green);"></div><div><b style="font-size:.85rem;">Road cleared near Tezpur</b><div style="font-size:.78rem;color:var(--ink-soft);">Synced · 2h ago</div></div></div>
        <div class="notif-item"><div class="notif-dot" style="background:var(--amber);"></div><div><b style="font-size:.85rem;">Minor landslide, single lane open</b><div style="font-size:.78rem;color:var(--ink-soft);">Synced · 6h ago</div></div></div>
      </div>
    </div>
  </div>`;
}
function useLocation(){
  const lat = (25 + Math.random()*3).toFixed(4);
  const lng = (91 + Math.random()*4).toFixed(4);
  document.getElementById("gpsCoords").textContent = `GPS coordinates (placeholder): ${lat}° N, ${lng}° E`;
}
function submitFieldReport(){
  const el = document.getElementById("syncStatus");
  el.innerHTML = `<div class="sync-row result-fade">✓ Saved locally</div>`;
  setTimeout(()=>{ el.innerHTML = `<div class="sync-row result-fade">⟳ Waiting for network</div>`; }, 700);
  setTimeout(()=>{ el.innerHTML = `<div class="sync-row result-fade" style="color:var(--green);">✓ Synced</div>`; }, 1600);
}

/* ---------- SUPPLY CHAIN ---------- */
function pageSupplyChain(){
  const rows = [
    {cat:"Medicine availability", demand:82, supply:61},
    {cat:"Food supply", demand:74, supply:70},
    {cat:"Construction material", demand:55, supply:38},
    {cat:"Agricultural transport", demand:66, supply:59},
  ];
  return `
  ${pageHead("Supply Chain Intelligence", "Demand vs. supply across critical categories")}
  <div class="grid-cards" style="margin-bottom:20px;">
    ${rows.map(r=>{
      const gap = r.demand - r.supply;
      const riskTone = gap>15?"red":gap>5?"amber":"green";
      return `<div class="card"><h3>${r.cat}</h3>
        <div style="display:flex;justify-content:space-between;font-size:.78rem;color:var(--ink-soft);margin:10px 0 4px;"><span>Demand</span><span>${r.demand}%</span></div>
        <div style="height:6px;border-radius:4px;background:var(--bg-deep);overflow:hidden;"><div style="height:100%;width:${r.demand}%;background:var(--brand);"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:.78rem;color:var(--ink-soft);margin:10px 0 4px;"><span>Available supply</span><span>${r.supply}%</span></div>
        <div style="height:6px;border-radius:4px;background:var(--bg-deep);overflow:hidden;"><div style="height:100%;width:${r.supply}%;background:var(--flow);"></div></div>
        <div style="margin-top:10px;">${riskBadge(riskTone)} <span style="font-size:.78rem;color:var(--ink-soft);">shortage risk</span></div>
      </div>`;
    }).join("")}
  </div>
  <div class="two-col">
    <div class="panel"><div class="panel-head"><h3>Supply vs demand</h3></div><div class="panel-body"><canvas id="chartSupply" height="200"></canvas></div></div>
    <div class="panel"><div class="panel-head"><h3>AI supply risk prediction</h3></div>
      <div class="panel-body"><div class="insight-card"><span class="tag">SUPPLY PREDICTION</span>Construction material supply is projected to fall short of demand by roughly 17 points in high-risk corridors over the next week.</div></div>
    </div>
  </div>`;
}

/* ---------- AI INSIGHTS ---------- */
function pageAIInsights(){
  return `
  ${pageHead("PRAVAH AI Intelligence", "Predictive insight generated from route, weather and incident data")}
  <div class="grid-cards">
    ${DATA.aiInsights.map(i=>`<div class="insight-card"><span class="tag">${i.tag}</span><p style="font-size:.9rem;">${i.text}</p></div>`).join("")}
  </div>`;
}

/* ---------- CHATBOT ---------- */
const CHAT_REPLIES = {
  "find safest route":"For your safest route, open Route Intelligence and enter a From/To pair — I'll rank alternatives by current risk. (Demo response)",
  "check road accessibility":"You can see live-style status for every tracked road in Accessibility Monitor, filterable by state and district. (Demo response)",
  "track vehicle":"Head to Vehicle Tracking and enter a vehicle number such as AS01AB1234 to see a demo tracking result. (Demo response)",
  "check delivery status":"Delivery status for all active shipments is listed under Logistics & Deliveries. (Demo response)",
  "show emergency routes":"Emergency Routes lists medical, relief and evacuation corridors, with an Activate Emergency Mode toggle. (Demo response)",
  "check weather risk":"Weather Intelligence shows rainfall, flood and landslide risk by state, updated per demo cycle. (Demo response)",
};
function pageChatbot(){
  if(STATE.chatHistory.length===0){
    STATE.chatHistory.push({role:"bot", text:"Hello! I am PRAVAH AI Assistant. I can help you with routes, logistics, accessibility and emergency information."});
  }
  return `
  ${pageHead("PRAVAH AI Assistant", "Frontend-only demo — responses are simulated, not live AI")}
  <div class="panel">
    <div class="chat-wrap">
      <div class="chat-log" id="chatLog">${chatLogHTML()}</div>
      <div class="chat-suggest">
        ${Object.keys(CHAT_REPLIES).map(q=>`<button class="chip" onclick="sendChat('${q}')">${q.charAt(0).toUpperCase()+q.slice(1)}</button>`).join("")}
      </div>
      <div class="chat-input">
        <input type="text" id="chatInput" placeholder="Ask about routes, weather, vehicles…" onkeydown="if(event.key==='Enter'){sendChat(this.value); this.value='';}">
        <button onclick="const i=document.getElementById('chatInput'); sendChat(i.value); i.value='';" aria-label="Send">➤</button>
      </div>
    </div>
  </div>`;
}
function chatLogHTML(){
  return STATE.chatHistory.map(m=>`<div class="msg ${m.role==='bot'?'bot':'user'}">${m.text}</div>`).join("");
}
function sendChat(text){
  if(!text || !text.trim()) return;
  STATE.chatHistory.push({role:"user", text});
  const key = text.toLowerCase().trim();
  const reply = CHAT_REPLIES[key] || "I'm a frontend demo assistant — try one of the suggested questions below, or ask about routes, vehicles, weather or emergencies. (Demo response, not live AI)";
  STATE.chatHistory.push({role:"bot", text:reply});
  const log = document.getElementById("chatLog");
  if(log){ log.innerHTML = chatLogHTML(); log.scrollTop = log.scrollHeight; }
}

/* ---------- NOTIFICATIONS ---------- */
function pageNotifications(){
  return `
  ${pageHead("Notifications", "Alerts, updates and system messages")}
  <div class="panel">
    <div class="panel-head"><h3>All notifications</h3>
      <div style="display:flex;gap:10px;">
        <button class="btn btn-ghost btn-sm" onclick="markAllRead()">Mark all as read</button>
        <button class="btn btn-ghost btn-sm" onclick="clearNotifs()">Clear all</button>
      </div>
    </div>
    <div id="notifList">${notifListHTML()}</div>
  </div>`;
}
function notifListHTML(){
  const toneDot = {"Critical Alert":"var(--red)","Route Update":"var(--brand)","Vehicle Update":"var(--sky)","Delivery Update":"var(--flow)","Weather Warning":"var(--amber)","System Notification":"var(--ink-soft)"};
  if(STATE.notifs.length===0) return `<div class="empty-state">${ICONS.check}<h3>You're all caught up</h3></div>`;
  return STATE.notifs.map((n,i)=>`
    <div class="notif-item ${n.unread?'unread':''}">
      <div class="notif-dot" style="background:${toneDot[n.type]||'var(--ink-soft)'};"></div>
      <div style="flex:1;">
        <div style="display:flex;justify-content:space-between;gap:10px;"><b style="font-size:.86rem;">${n.type}</b><span style="font-size:.74rem;color:var(--ink-soft);">${n.time}</span></div>
        <div style="font-size:.85rem;color:var(--ink-soft);">${n.text}</div>
      </div>
    </div>`).join("");
}
function markAllRead(){ STATE.notifs.forEach(n=>n.unread=false); document.getElementById("notifList").innerHTML = notifListHTML(); }
function clearNotifs(){ STATE.notifs = []; document.getElementById("notifList").innerHTML = notifListHTML(); }

/* ---------- REPORTS & ANALYTICS ---------- */
function pageReports(){
  return `
  ${pageHead("Reports & Analytics", "Performance across routes, vehicles and supply chain")}
  <div class="filters">
    <input type="date"><input type="date">
    <select><option>All states</option>${NER_STATES.map(s=>`<option>${s}</option>`).join("")}</select>
  </div>
  <div class="two-col">
    <div class="panel"><div class="panel-head"><h3>District connectivity</h3></div><div class="panel-body"><canvas id="chartReportConnectivity" height="200"></canvas></div></div>
    <div class="panel"><div class="panel-head"><h3>Route disruption trend</h3></div><div class="panel-body"><canvas id="chartReportDisruption" height="200"></canvas></div></div>
  </div>
  <div class="two-col" style="margin-top:18px;">
    <div class="panel"><div class="panel-head"><h3>Delivery efficiency</h3></div><div class="panel-body"><canvas id="chartReportDelivery" height="200"></canvas></div></div>
    <div class="panel"><div class="panel-head"><h3>Incident frequency by state</h3></div><div class="panel-body"><canvas id="chartReportIncidents" height="200"></canvas></div></div>
  </div>`;
}

/* ---------- SETTINGS ---------- */
function pageSettings(){
  const tabs = [["profile","Profile"],["language","Language"],["notifications","Notifications"],["accessibility","Accessibility"],["dashboard","Dashboard Preferences"],["security","Security"]];
  return `
  ${pageHead("Settings", "Manage your PRAVAH account and preferences")}
  <div class="two-col">
    <div class="panel"><div class="panel-body"><div class="settings-nav">
      ${tabs.map(([k,l])=>`<button class="${STATE.settingsTab===k?'active':''}" onclick="setSettingsTab('${k}')">${l}</button>`).join("")}
    </div></div></div>
    <div class="panel"><div class="panel-body" id="settingsPane">${settingsPane()}</div></div>
  </div>`;
}
function settingsPane(){
  if(STATE.settingsTab==="profile"){
    return `
    <div class="field"><label>Full name</label><input value="${STATE.user? STATE.user.name : 'Demo User'}"></div>
    <div class="field"><label>Role</label><input value="${STATE.user? STATE.user.role : 'Demo Account'}" disabled></div>
    <div class="field"><label>Organization</label><input placeholder="Department / organization"></div>
    <button class="btn btn-primary btn-sm">Save changes</button>`;
  }
  if(STATE.settingsTab==="language"){
    return `<div class="field"><label>Interface language</label><select onchange="setLang(this.value)"><option value="en" ${STATE.lang==='en'?'selected':''}>English</option><option value="hi" ${STATE.lang==='hi'?'selected':''}>हिन्दी</option></select></div>
    <p style="font-size:.8rem;color:var(--ink-soft);">Assamese, Bengali, Manipuri, Khasi, Mizo, Nagamese and Nepali are structured for translation and will be enabled as they're completed.</p>`;
  }
  if(STATE.settingsTab==="notifications"){
    return ["Critical alerts","Route updates","Vehicle updates","Weather warnings","System notifications"].map(l=>`
      <div class="setting-row"><div><div class="t">${l}</div><div class="d">Receive ${l.toLowerCase()} in the notification centre.</div></div><button class="toggle on" onclick="this.classList.toggle('on')"></button></div>`).join("");
  }
  if(STATE.settingsTab==="accessibility"){
    return `<div class="setting-row"><div><div class="t">Large text mode</div><div class="d">Increase base font size across the app.</div></div><button class="toggle" onclick="this.classList.toggle('on')"></button></div>
    <div class="setting-row"><div><div class="t">Reduce motion</div><div class="d">Minimise transitions and animated effects.</div></div><button class="toggle" onclick="this.classList.toggle('on')"></button></div>`;
  }
  if(STATE.settingsTab==="dashboard"){
    return `<div class="setting-row"><div><div class="t">Show KPI deltas</div><div class="d">Display week-over-week change on dashboard cards.</div></div><button class="toggle on" onclick="this.classList.toggle('on')"></button></div>
    <div class="setting-row"><div><div class="t">Auto-refresh data</div><div class="d">Simulate periodic refresh of dashboard figures.</div></div><button class="toggle" onclick="this.classList.toggle('on')"></button></div>`;
  }
  if(STATE.settingsTab==="security"){
    return `<div class="field"><label>Current password</label><input type="password"></div>
    <div class="field"><label>New password</label><input type="password"></div>
    <button class="btn btn-primary btn-sm">Update password</button>
    <div class="setting-row" style="margin-top:16px;"><div><div class="t">Two-factor authentication</div><div class="d">Add an extra layer of protection to your account.</div></div><button class="toggle" onclick="this.classList.toggle('on')"></button></div>`;
  }
  return "";
}
function setSettingsTab(t){ STATE.settingsTab = t; document.getElementById("pageContent").innerHTML = pageSettings(); }

/* =========================================================
   POST-RENDER HOOKS (charts, theme toggle default light)
   ========================================================= */
let CHART_REGISTRY = [];
function destroyCharts(){ CHART_REGISTRY.forEach(c=>c.destroy()); CHART_REGISTRY = []; }
function mkChart(id, config){
  const ctx = document.getElementById(id);
  if(!ctx || typeof Chart === "undefined") return;
  const c = new Chart(ctx, config);
  CHART_REGISTRY.push(c);
}
const CHART_DEFAULTS = { plugins:{legend:{labels:{font:{family:"Inter", size:11}}}}, scales:{} };

function afterRender(key){
  destroyCharts();
  if(key==="overview"){
    mkChart("chartIncidents", {type:"line", data:{labels:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], datasets:[{label:"Incidents", data:[3,5,4,7,6,9,5], borderColor:"#0E7490", backgroundColor:"rgba(14,116,144,.12)", tension:.35, fill:true}]}, options:{plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true}}}});
    mkChart("chartDelivery", {type:"doughnut", data:{labels:["Delivered","In Transit","Delayed","At Risk"], datasets:[{data:[42,31,9,4], backgroundColor:["#16A34A","#0E7490","#D97706","#DC2626"]}]}, options:{plugins:{legend:{position:"bottom"}}}});
    mkChart("chartConnectivity", {type:"bar", data:{labels:NER_STATES.map(s=>s.split(" ")[0]), datasets:[{label:"% districts accessible", data:[92,88,95,81,77,84,97,72], backgroundColor:"#14B8A6", borderRadius:5}]}, options:{plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true, max:100}}}});
  }
  if(key==="supply-chain"){
    mkChart("chartSupply", {type:"bar", data:{labels:["Medicine","Food","Construction","Agri transport"], datasets:[
      {label:"Demand", data:[82,74,55,66], backgroundColor:"#0E7490", borderRadius:5},
      {label:"Supply", data:[61,70,38,59], backgroundColor:"#14B8A6", borderRadius:5}]}, options:{plugins:{legend:{position:"bottom"}}, scales:{y:{beginAtZero:true, max:100}}}});
  }
  if(key==="reports"){
    mkChart("chartReportConnectivity", {type:"bar", data:{labels:NER_STATES.map(s=>s.split(" ")[0]), datasets:[{data:[92,88,95,81,77,84,97,72], backgroundColor:"#0E7490", borderRadius:5}]}, options:{plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true, max:100}}}});
    mkChart("chartReportDisruption", {type:"line", data:{labels:["W1","W2","W3","W4","W5","W6"], datasets:[{label:"Disruptions", data:[12,9,14,11,7,10], borderColor:"#DC2626", backgroundColor:"rgba(220,38,38,.1)", tension:.3, fill:true}]}, options:{plugins:{legend:{display:false}}}});
    mkChart("chartReportDelivery", {type:"bar", data:{labels:["On time","Delayed","Failed"], datasets:[{data:[186,34,6], backgroundColor:["#16A34A","#D97706","#DC2626"], borderRadius:5}]}, options:{plugins:{legend:{display:false}}}});
    mkChart("chartReportIncidents", {type:"bar", data:{labels:NER_STATES.map(s=>s.split(" ")[0]), datasets:[{data:[6,11,4,3,7,9,2,10], backgroundColor:"#38BDF8", borderRadius:5}]}, options:{indexAxis:"y", plugins:{legend:{display:false}}}});
  }
  if(key==="chatbot"){
    const log = document.getElementById("chatLog");
    if(log) log.scrollTop = log.scrollHeight;
  }
}

/* =========================================================
   OFFLINE / ONLINE SIMULATION
   ========================================================= */
window.addEventListener("online", updateNetStatus);
window.addEventListener("offline", updateNetStatus);
function updateNetStatus(){
  const el = document.getElementById("netStatus");
  if(!el) return;
  if(navigator.onLine){ el.textContent = "🟢 Online"; el.className = "status-chip online"; }
  else { el.textContent = "🟠 Offline Mode"; el.className = "status-chip offline"; }
}