from __future__ import annotations

import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).parent
IMAGE_PATH = APP_DIR / "assets" / "warehouse_board.jpg"

st.set_page_config(page_title="현장 인원 배치판", page_icon="📍", layout="wide")

if not IMAGE_PATH.exists():
    st.error(f"배경 이미지를 찾을 수 없습니다: {IMAGE_PATH}")
    st.stop()

image_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("ascii")

# 배경 이미지 기준 백분율 좌표. 화면 크기가 달라도 같은 위치를 유지합니다.
zones = [
    {"id": "L존", "x": 2, "y": 1, "w": 64, "h": 10},
    {"id": "M-02", "x": 25, "y": 11, "w": 19, "h": 9},
    {"id": "M-01", "x": 44, "y": 11, "w": 20, "h": 9},
    {"id": "자동화창고", "x": 19, "y": 20, "w": 39, "h": 39},
    {"id": "K-16~K-13", "x": 2, "y": 17, "w": 17, "h": 35},
    {"id": "반송기", "x": 2, "y": 52, "w": 13, "h": 10},
    {"id": "K-12", "x": 1, "y": 63, "w": 8, "h": 31},
    {"id": "F-01", "x": 15, "y": 60, "w": 42, "h": 9},
    {"id": "F-02", "x": 15, "y": 69, "w": 42, "h": 8},
    {"id": "K-22", "x": 15, "y": 77, "w": 42, "h": 7},
    {"id": "K-21/K-20", "x": 15, "y": 84, "w": 42, "h": 7},
    {"id": "K-19/K-17", "x": 15, "y": 91, "w": 42, "h": 6},
    {"id": "K-18", "x": 5, "y": 96, "w": 53, "h": 4},
    {"id": "J-01", "x": 64, "y": 13, "w": 33, "h": 18},
    {"id": "야적", "x": 65, "y": 31, "w": 31, "h": 45},
    {"id": "D-01", "x": 87, "y": 61, "w": 9, "h": 22},
    {"id": "W-01", "x": 65, "y": 76, "w": 30, "h": 17},
    {"id": "제니엘 사무실", "x": 73, "y": 91, "w": 13, "h": 9},
    {"id": "CJ 사무실", "x": 86, "y": 91, "w": 12, "h": 9},
]

default_people = [
    "김보경", "최성원", "남궁정", "양송규", "김종웅", "김병선", "김경훈",
    "성락훈", "심형식", "김재욱", "장인택", "임세호", "이건철", "이상훈",
    "임승현", "김석원", "양묘근",
]

html = r'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--green:#087f5b;--mint:#dff7ed;--line:#d8e2df;--ink:#18312b;--muted:#6a7d78;}
*{box-sizing:border-box} html,body{width:100%;height:100%;margin:0;overflow:hidden} body{background:#f4f7f6;color:var(--ink);font-family:Pretendard,"Noto Sans KR",Arial,sans-serif;user-select:none}
.app{display:grid;grid-template-columns:clamp(210px,15vw,260px) minmax(0,1fr);gap:10px;padding:8px;width:100vw;height:100vh;overflow:hidden}
.panel,.stage-wrap{background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 24px #193a3210}
.panel{padding:11px;display:flex;flex-direction:column;gap:8px;min-height:0;overflow:hidden}.title{font-size:clamp(16px,1.2vw,20px);font-weight:900}.sub{font-size:11px;color:var(--muted)}
.date{width:100%;padding:9px;border:1px solid var(--line);border-radius:9px;font-family:"Malgun Gothic","맑은 고딕",sans-serif!important;font-weight:700!important}.date::-webkit-datetime-edit,.date::-webkit-datetime-edit-text,.date::-webkit-datetime-edit-month-field,.date::-webkit-datetime-edit-day-field,.date::-webkit-datetime-edit-year-field{font-family:"Malgun Gothic","맑은 고딕",sans-serif!important;font-weight:700!important}.stats{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.stat{padding:6px 8px;border-radius:10px;background:#f2f8f6;font-size:12px}.stat b{display:inline;margin-left:5px;font-size:16px;color:var(--green)}
.dropbox{min-height:52px;border:2px dashed #b9cbc5;border-radius:11px;padding:6px;background:#fafcfb}.dropbox.hot{border-color:var(--green);background:var(--mint)}
.dropbox-title{font-weight:800;font-size:13px;margin-bottom:6px}.person-list{display:flex;flex-wrap:wrap;gap:6px;align-content:flex-start}
.person{position:relative;display:flex;align-items:center;gap:3px;padding:4px 5px 4px 8px;border-radius:8px;background:#fff;border:2px solid #2383e2;color:#123d66;font-size:12px;font-weight:800;cursor:grab;box-shadow:0 2px 7px #0002;white-space:nowrap;touch-action:none;z-index:15}.person .name{min-width:22px;outline:none}.person .name[contenteditable="true"]{background:#fff4bf;color:#111;border-radius:3px;padding:1px 3px;cursor:text}.edit-name{border:0;background:#eaf3fb;color:#216aa8;border-radius:4px;padding:1px 4px;font-size:10px;cursor:pointer}
.person.office{border-color:#12a150;color:#0b6335}.person.off{border-color:#89938f;color:#505956;background:#edf0ef}.person.shift-day{background:#dcebff;border-color:#83b8ee;color:#164b7d}.person.shift-evening{background:#ffe2c2;border-color:#efa45d;color:#7e4015}.person.shift-night{background:#d9f3df;border-color:#79bd89;color:#245f31}.person.dragging{cursor:grabbing;opacity:.92;z-index:999;transform:scale(1.04)}
.addrow{display:flex;gap:6px}.addrow input{min-width:0;flex:1;padding:8px;border:1px solid var(--line);border-radius:8px}.btn{border:0;border-radius:8px;padding:8px 10px;font-weight:800;cursor:pointer}.primary{background:var(--green);color:white}.secondary{background:#eaf1ef;color:#28443d}.danger{background:#fff0f0;color:#b42318}
.toolbar{display:grid;grid-template-columns:1fr 1fr;gap:5px}.stage-wrap{padding:8px;overflow:hidden;display:flex;flex-direction:column;min-width:0;min-height:0}.stage-head{flex:0 0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 4px 6px}.status{font-size:12px;color:var(--muted)}
.stage{position:relative;flex:0 1 auto;width:100%;max-width:calc((100vh - 48px) * 1.7779);max-height:calc(100vh - 48px);aspect-ratio:1672/941;margin:auto;background:#ddd;border-radius:8px;overflow:hidden;border:1px solid #b9c3c0}.stage>img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;pointer-events:none}
.zone{position:absolute;border:1.5px dashed transparent;border-radius:5px;pointer-events:none}.show-zones .zone{border-color:#00a56a88;background:#00a56a10}.zone-label{display:none;position:absolute;top:2px;left:3px;font-size:9px;background:#087f5bcc;color:#fff;padding:2px 4px;border-radius:4px}.show-zones .zone-label{display:block}
#stage .person.stage-person{position:absolute!important;transform:translate(-50%,-50%)!important;padding:9px 18px!important;font-size:21.6px!important;line-height:1.2!important;border-width:3px!important;border-radius:11px!important;box-shadow:0 4px 12px #0003!important}.toast{position:fixed;right:20px;bottom:20px;background:#173f35;color:#fff;padding:10px 14px;border-radius:9px;opacity:0;transition:.2s;z-index:2000}.toast.on{opacity:1}
#stage .person.stage-person.selected{outline:3px solid #e6007e!important;outline-offset:3px!important}.fine-control{display:none;position:absolute;right:8px;top:8px;z-index:120;background:#ffffffee;border:1px solid #b8c9c4;border-radius:11px;padding:7px;box-shadow:0 4px 14px #0002}.fine-control.open{display:grid;grid-template-columns:28px 28px 28px;gap:3px;align-items:center}.fine-name{grid-column:1/4;text-align:center;font-size:11px;font-weight:900;color:#34534b;max-width:90px;overflow:hidden;text-overflow:ellipsis}.nudge{width:28px;height:25px;padding:0;border:0;border-radius:5px;background:#e9f4f0;color:#176149;font-weight:900;cursor:pointer}.nudge:hover{background:#cde9df}.fine-help{grid-column:1/4;font-size:8px;text-align:center;color:#73837f}
.modal-backdrop{display:none;position:fixed;inset:0;background:#102c2466;align-items:center;justify-content:center;z-index:3000}.modal-backdrop.open{display:flex}.shift-modal{width:min(390px,90vw);background:#fff;border-radius:18px;padding:22px;box-shadow:0 18px 60px #0004;text-align:center}.shift-modal h3{margin:0 0 6px;font-size:20px}.shift-modal p{margin:0 0 18px;color:var(--muted);font-size:13px}.shift-options{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}.shift-btn{border:2px solid transparent;border-radius:12px;padding:13px 6px;font-weight:900;cursor:pointer}.shift-btn.day{background:#dcebff;border-color:#83b8ee;color:#164b7d}.shift-btn.evening{background:#ffe2c2;border-color:#efa45d;color:#7e4015}.shift-btn.night{background:#d9f3df;border-color:#79bd89;color:#245f31}.modal-cancel{margin-top:12px;border:0;background:#eef2f1;color:#455b55;border-radius:9px;padding:8px 18px;cursor:pointer;font-weight:700}
@media(max-width:900px){.app{grid-template-columns:190px minmax(0,1fr);gap:6px;padding:5px}.panel{padding:7px;gap:5px}.sub{display:none}.dropbox{min-height:42px}.person{font-size:10px;padding:3px 4px}.btn{padding:6px;font-size:11px}.stage{max-width:calc((100vh - 38px) * 1.7779);max-height:calc(100vh - 38px)}}
</style></head><body>
<div class="app">
 <aside class="panel">
  <div><div class="title">현장 인원 배치</div><div class="sub">이름표를 끌어서 원하는 위치에 놓으세요.</div></div>
  <input id="workDate" class="date" type="date">
  <div class="stats"><div class="stat"><span>현장</span><b id="fieldN">0</b></div><div class="stat"><span>사무실</span><b id="officeN">0</b></div><div class="stat"><span>휴무</span><b id="offN">0</b></div><div class="stat"><span>미배치</span><b id="poolN">0</b></div></div>
  <div id="pool" class="dropbox"><div class="dropbox-title">미배치</div><div class="person-list"></div></div>
  <div id="office" class="dropbox"><div class="dropbox-title">사무실</div><div class="person-list"></div></div>
  <div id="off" class="dropbox"><div class="dropbox-title">휴무</div><div class="person-list"></div></div>
  <div class="addrow"><input id="newName" placeholder="인원 이름"><button id="addBtn" class="btn primary">추가</button></div>
  <div class="toolbar"><button id="saveBtn" class="btn primary">저장</button><button id="yesterdayBtn" class="btn secondary">전일 불러오기</button><button id="zoneBtn" class="btn secondary">구역선 보기</button><button id="downloadBtn" class="btn secondary">JSON 백업</button></div>
  <button id="resetBtn" class="btn danger">오늘 배치 초기화</button>
  <div class="sub">이름표를 더블클릭하면 해당 인원을 삭제할 수 있습니다. 저장 데이터는 현재 브라우저에 보관됩니다.</div>
 </aside>
 <main class="stage-wrap"><div class="stage-head"><b>업무 상황판 <small style="color:#087f5b">v5.4</small></b><span id="status" class="status">변경사항 없음</span></div><div id="stage" class="stage"><img src="data:image/jpeg;base64,{{IMAGE}}"><div id="fineControl" class="fine-control"><div id="fineName" class="fine-name"></div><span></span><button class="nudge" data-dx="0" data-dy="-1">▲</button><span></span><button class="nudge" data-dx="-1" data-dy="0">◀</button><button class="nudge" data-dx="0" data-dy="1">▼</button><button class="nudge" data-dx="1" data-dy="0">▶</button><div class="fine-help">화살표 1px · Shift 5px · Esc 닫기</div></div></div></main>
</div><div id="toast" class="toast"></div>
<div id="shiftBackdrop" class="modal-backdrop"><div class="shift-modal"><h3 id="shiftTitle">근무조 선택</h3><p>이 인원의 근무시간대를 선택하세요.</p><div class="shift-options"><button class="shift-btn day" data-shift="day">주간</button><button class="shift-btn evening" data-shift="evening">석간</button><button class="shift-btn night" data-shift="night">야간</button></div><button id="shiftCancel" class="modal-cancel">배치 취소</button></div></div>
<script>
const ZONES={{ZONES}}, DEFAULT={{PEOPLE}};
const stage=document.getElementById('stage'), dateEl=document.getElementById('workDate'); let people=[], dirty=false, drag=null, pendingPlacement=null, selectedId=null;
const today=new Date(); dateEl.value=[today.getFullYear(),String(today.getMonth()+1).padStart(2,'0'),String(today.getDate()).padStart(2,'0')].join('-');
function key(d=dateEl.value){return 'warehouse-board-v1:'+d} function masterKey(){return 'warehouse-board-v1:people'}
function defaultState(){let names=JSON.parse(localStorage.getItem(masterKey())||'null')||DEFAULT; return names.map((name,i)=>({id:crypto.randomUUID?crypto.randomUUID():'p'+Date.now()+i,name,place:'pool',x:0,y:0,zone:'',shift:''}))}
function load(){let saved=JSON.parse(localStorage.getItem(key())||'null'); people=saved?.people||defaultState(); dirty=false; render(); setStatus('저장된 배치를 불러왔습니다')}
function save(){localStorage.setItem(key(),JSON.stringify({date:dateEl.value,people,updatedAt:new Date().toISOString()}));localStorage.setItem(masterKey(),JSON.stringify(people.map(p=>p.name)));dirty=false;render();toast('저장했습니다')}
function setStatus(t){document.getElementById('status').textContent=t} function changed(){dirty=true;setStatus('저장하지 않은 변경사항')}
function toast(t){let e=document.getElementById('toast');e.textContent=t;e.classList.add('on');setTimeout(()=>e.classList.remove('on'),1500)}
ZONES.forEach(z=>{let e=document.createElement('div');e.className='zone';Object.assign(e.style,{left:z.x+'%',top:z.y+'%',width:z.w+'%',height:z.h+'%'});e.innerHTML='<span class="zone-label">'+z.id+'</span>';stage.appendChild(e)})
function personEl(p){let stageClass=p.place==='stage'?' stage-person':'';let selectedClass=p.id===selectedId?' selected':'';let shiftClass=p.place==='stage'&&p.shift?' shift-'+p.shift:'';let e=document.createElement('div');e.className='person '+(p.place==='office'?'office':p.place==='off'?'off':'')+stageClass+shiftClass+selectedClass;e.dataset.id=p.id;let shiftName={day:'주간',evening:'석간',night:'야간'}[p.shift]||'';e.title=(p.zone||p.place)+(shiftName?' · '+shiftName:'')+' · 우클릭 삭제';let n=document.createElement('span');n.className='name';n.textContent=p.name;e.appendChild(n);if(p.place!=='stage'){let b=document.createElement('button');b.className='edit-name';b.textContent='수정';b.title='이름 수정';b.addEventListener('pointerdown',ev=>ev.stopPropagation());b.addEventListener('click',ev=>{ev.stopPropagation();n.contentEditable='true';n.focus();document.getSelection().selectAllChildren(n)});n.addEventListener('pointerdown',ev=>{if(n.contentEditable==='true')ev.stopPropagation()});n.addEventListener('input',()=>{let value=n.textContent.trim();if(value){p.name=value;changed()}});n.addEventListener('keydown',ev=>{if(ev.key==='Enter'){ev.preventDefault();n.blur()}if(ev.key==='Escape'){n.textContent=p.name;n.blur()}});n.addEventListener('blur',()=>{if(!n.textContent.trim())n.textContent=p.name;n.contentEditable='false';localStorage.setItem(masterKey(),JSON.stringify(people.map(x=>x.name)));render()});e.appendChild(b)}e.addEventListener('pointerdown',startDrag);e.addEventListener('contextmenu',ev=>{ev.preventDefault();if(confirm(p.name+' 인원을 삭제할까요?')){people=people.filter(x=>x.id!==p.id);if(selectedId===p.id)selectedId=null;changed();render()}});return e}
function render(){document.querySelectorAll('.person').forEach(e=>e.remove()); for(const p of people){let e=personEl(p);if(p.place==='stage'){e.style.left=p.x+'%';e.style.top=p.y+'%';stage.appendChild(e)}else document.querySelector('#'+p.place+' .person-list').appendChild(e)}let selected=people.find(p=>p.id===selectedId&&p.place==='stage'),fine=document.getElementById('fineControl');fine.classList.toggle('open',!!selected);document.getElementById('fineName').textContent=selected?.name||'';
 let counts={pool:0,office:0,off:0,stage:0};people.forEach(p=>counts[p.place]++);document.getElementById('fieldN').textContent=counts.stage;document.getElementById('officeN').textContent=counts.office;document.getElementById('offN').textContent=counts.off;document.getElementById('poolN').textContent=counts.pool}
function startDrag(ev){if(ev.target.closest('.edit-name')||ev.target.contentEditable==='true')return;ev.preventDefault();let p=people.find(x=>x.id===ev.currentTarget.dataset.id);let ghost=ev.currentTarget;let r=ghost.getBoundingClientRect();drag={p,ghost,dx:ev.clientX-r.left-r.width/2,dy:ev.clientY-r.top-r.height/2};ghost.classList.add('dragging');ghost.style.position='fixed';ghost.style.left=ev.clientX-drag.dx+'px';ghost.style.top=ev.clientY-drag.dy+'px';ghost.style.transform='translate(-50%,-50%)';document.body.appendChild(ghost);ghost.setPointerCapture(ev.pointerId);ghost.addEventListener('pointermove',moveDrag);ghost.addEventListener('pointerup',endDrag,{once:true})}
function moveDrag(ev){if(!drag)return;drag.ghost.style.left=ev.clientX-drag.dx+'px';drag.ghost.style.top=ev.clientY-drag.dy+'px';['pool','office','off'].forEach(id=>{let e=document.getElementById(id),r=e.getBoundingClientRect();e.classList.toggle('hot',ev.clientX>=r.left&&ev.clientX<=r.right&&ev.clientY>=r.top&&ev.clientY<=r.bottom)})}
function endDrag(ev){if(!drag)return;let p=drag.p,originPlace=p.place,sr=stage.getBoundingClientRect(),gr=drag.ghost.getBoundingClientRect(),centerX=gr.left+gr.width/2,centerY=gr.top+gr.height/2,placed=false;if(centerX>=sr.left&&centerX<=sr.right&&centerY>=sr.top&&centerY<=sr.bottom){let x=Math.max(1,Math.min(99,(centerX-sr.left)/sr.width*100)),y=Math.max(1,Math.min(99,(centerY-sr.top)/sr.height*100));let z=ZONES.find(z=>x>=z.x&&x<=z.x+z.w&&y>=z.y&&y<=z.y+z.h),zone=z?.id||'기타';if(originPlace!=='stage'){pendingPlacement={p,x,y,zone};placed='pending'}else{p.x=x;p.y=y;p.zone=zone;selectedId=p.id;placed=true}}
 for(const id of ['pool','office','off']){let e=document.getElementById(id),r=e.getBoundingClientRect();e.classList.remove('hot');if(ev.clientX>=r.left&&ev.clientX<=r.right&&ev.clientY>=r.top&&ev.clientY<=r.bottom){p.place=id;p.zone=id==='office'?'사무실':id==='off'?'휴무':'미배치';placed=true}}
 drag.ghost.removeEventListener('pointermove',moveDrag);drag=null;if(placed===true){changed();render()}else if(placed==='pending'){render();openShiftModal()}else render()}
function openShiftModal(){if(!pendingPlacement)return;document.getElementById('shiftTitle').textContent=pendingPlacement.p.name+' 근무조 선택';document.getElementById('shiftBackdrop').classList.add('open')}
function closeShiftModal(){document.getElementById('shiftBackdrop').classList.remove('open')}
document.querySelectorAll('.shift-btn').forEach(btn=>btn.onclick=()=>{if(!pendingPlacement)return;let {p,x,y,zone}=pendingPlacement;p.x=x;p.y=y;p.zone=zone;p.place='stage';p.shift=btn.dataset.shift;selectedId=p.id;pendingPlacement=null;closeShiftModal();changed();render()})
document.getElementById('shiftCancel').onclick=()=>{pendingPlacement=null;closeShiftModal();render()}
function nudgeSelected(dx,dy,pixels=1){let p=people.find(x=>x.id===selectedId&&x.place==='stage');if(!p)return;let r=stage.getBoundingClientRect();p.x=Math.max(0.5,Math.min(99.5,p.x+(dx*pixels/r.width*100)));p.y=Math.max(0.5,Math.min(99.5,p.y+(dy*pixels/r.height*100)));let z=ZONES.find(z=>p.x>=z.x&&p.x<=z.x+z.w&&p.y>=z.y&&p.y<=z.y+z.h);p.zone=z?.id||'기타';changed();render()}
document.querySelectorAll('.nudge').forEach(b=>{b.addEventListener('pointerdown',e=>e.stopPropagation());b.onclick=e=>nudgeSelected(Number(b.dataset.dx),Number(b.dataset.dy),e.shiftKey?5:1)})
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&selectedId){selectedId=null;e.preventDefault();render();return}if(!selectedId||e.target.matches('input,[contenteditable="true"]'))return;let moves={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]};if(moves[e.key]){e.preventDefault();nudgeSelected(...moves[e.key],e.shiftKey?5:1)}})
document.getElementById('addBtn').onclick=()=>{let i=document.getElementById('newName'),name=i.value.trim();if(!name)return;if(people.some(p=>p.name===name)){toast('이미 등록된 이름입니다');return}people.push({id:crypto.randomUUID?crypto.randomUUID():'p'+Date.now(),name,place:'pool',x:0,y:0,zone:'',shift:''});i.value='';changed();render()}
document.getElementById('newName').addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('addBtn').click()});document.getElementById('saveBtn').onclick=save;
document.getElementById('zoneBtn').onclick=()=>stage.classList.toggle('show-zones');dateEl.onchange=()=>{if(dirty&&!confirm('저장하지 않은 변경사항이 있습니다. 날짜를 이동할까요?'))return;load()}
document.getElementById('resetBtn').onclick=()=>{if(confirm(dateEl.value+' 배치를 초기화할까요?')){localStorage.removeItem(key());people=defaultState();changed();render()}}
document.getElementById('yesterdayBtn').onclick=()=>{let d=new Date(dateEl.value+'T12:00:00');d.setDate(d.getDate()-1);let yd=[d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');let prev=JSON.parse(localStorage.getItem(key(yd))||'null');if(!prev){toast('전일 저장 내역이 없습니다');return}people=prev.people.map(p=>({...p,id:crypto.randomUUID?crypto.randomUUID():p.id+Date.now()}));changed();render();toast('전일 배치를 불러왔습니다')}
document.getElementById('downloadBtn').onclick=()=>{let data=JSON.stringify({date:dateEl.value,people,zones:ZONES},null,2),a=document.createElement('a');a.href=URL.createObjectURL(new Blob([data],{type:'application/json'}));a.download='인원배치_'+dateEl.value+'.json';a.click();URL.revokeObjectURL(a.href)}
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue=''}});load();
</script></body></html>'''

html = html.replace("{{IMAGE}}", image_b64)
html = html.replace("{{ZONES}}", json.dumps(zones, ensure_ascii=False))
html = html.replace("{{PEOPLE}}", json.dumps(default_people, ensure_ascii=False))

st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"] {overflow:hidden !important;}
      .block-container {max-width:none !important; width:100% !important; padding:0 !important; margin:0 !important;}
      header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer {display:none !important;}
      iframe {width:100% !important; height:100vh !important; border:0 !important; display:block !important;}
    </style>
    """,
    unsafe_allow_html=True,
)
components.html(html, height=900, scrolling=False)
